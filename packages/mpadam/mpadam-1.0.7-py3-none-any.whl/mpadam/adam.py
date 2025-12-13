# Copyright 2025 Alexander Lyulkov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch

from .config import MPConfig, check_config, get_preset, get_num_bytes
from .triton_kernels import adam_triton


def get_device_context(tensor):
    if tensor.is_cuda:
        return torch.cuda.device_of(tensor)
    elif hasattr(tensor, "is_xpu") and tensor.is_xpu:
        return torch.xpu.device_of(tensor)
    else:
        raise Exception("Unknown device type")


class AdamBase(torch.optim.Optimizer):
    def __init__(self,
                 params,
                 lr: float,
                 betas: list[float],
                 eps: float,
                 weight_decay: float,
                 adamw: bool,
                 config: str | MPConfig = "small",
                 ):
        super(AdamBase, self).__init__(params,
                                       defaults={"lr": lr,
                                                 "betas": betas,
                                                 "eps": eps,
                                                 "weight_decay": weight_decay})

        self.adamw = adamw
        self.weight_dtype = self.param_groups[0]['params'][0].dtype
        self.device = self.param_groups[0]['params'][0].device
        self.on_gpu = False

        if self.weight_dtype != torch.float16 and self.weight_dtype != torch.bfloat16:
            raise Exception("Weight type should be either float16 or bfloat16")

        if isinstance(config, str):
            self.config = get_preset(config, self.weight_dtype)
        else:
            self.config = config
        assert isinstance(self.config, MPConfig)
        check_config(self.config, self.weight_dtype)
        self.state_bytes = get_num_bytes(self.config)

        self.state = {}
        num_elements = []
        layer_group_id = []
        kernel_block_size = self.config.kernel_block_size
        quantization_block_size = self.config.quantization_block_size
        p_index = 0

        for i in range(len(self.param_groups)):
            for p in self.param_groups[i]['params']:
                assert p.dtype == self.weight_dtype
                num_elements.append(p.numel())
                layer_group_id.append(i)
                cur_num_blocks = ((p.numel() + kernel_block_size - 1) // kernel_block_size)
                self.state[p_index] = torch.zeros([cur_num_blocks, self.state_bytes, kernel_block_size],
                                                  dtype=torch.uint8,
                                                  device=self.device)
                p_index += 1

        block_layer_id = []
        layer_first_block = []
        num_layers = len(num_elements)
        for i in range(num_layers):
            layer_first_block.append(len(block_layer_id))
            cur_num_blocks = (num_elements[i] + kernel_block_size - 1) // kernel_block_size
            block_layer_id += [i,] * cur_num_blocks

        num_blocks = len(block_layer_id)
        if num_layers > 65535:
            block_layer_id_dtype = torch.uint32
        elif num_layers > 255:
            block_layer_id_dtype = torch.uint16
        else:
            block_layer_id_dtype = torch.uint8

        self.block_layer_id = torch.tensor(block_layer_id, dtype=block_layer_id_dtype, device=self.device)
        self.layer_first_block = torch.tensor(layer_first_block, dtype=torch.int64, device=self.device)
        self.layer_group_id = torch.tensor(layer_group_id, dtype=torch.int32, device=self.device)
        self.layer_num_elements = torch.tensor(num_elements, dtype=torch.int64, device=self.device)

        self.state["opt_m_scale"] = torch.zeros([num_blocks * (kernel_block_size // quantization_block_size),],
                                                dtype=torch.bfloat16,
                                                device=self.device)
        self.state["opt_v_scale"] = torch.zeros([num_blocks * (kernel_block_size // quantization_block_size),],
                                                dtype=torch.bfloat16,
                                                device=self.device)
        self.state["opt_step"] = torch.ones([num_blocks,],
                                            dtype=torch.uint32,
                                            device=self.device)

        self.hparams_values = self.get_hparams()
        self.hparams_tensors = {}
        for key, value in self.hparams_values.items():
            self.hparams_tensors[key] = torch.tensor(value, dtype=torch.float32, device=self.device)

        self.data_ptrs_values = self.get_data_ptrs(skip_grad=True)
        self.data_ptrs_tensors = {}
        for key, value in self.data_ptrs_values.items():
            self.data_ptrs_tensors[key] = torch.tensor(value, dtype=torch.int64, device=self.device)

        self.g_scale = 1.0
        self.g_scale_tensor = torch.tensor(self.g_scale, dtype=torch.float32, device=self.device)

    def get_hparams(self):
        hparams = {"lr": [], "beta1": [], "beta2": [], "eps": [], "weight_decay": []}

        for group in self.param_groups:
            hparams["lr"].append(group["lr"])
            hparams["beta1"].append(group["betas"][0])
            hparams["beta2"].append(group["betas"][1])
            hparams["eps"].append(group["eps"])
            hparams["weight_decay"].append(group["weight_decay"])

        return hparams

    def set_hparams(self, hparams):
        for i in range(len(self.param_groups)):
            self.param_groups[i]["lr"] = hparams["lr"][i]
            self.param_groups[i]["betas"] = (hparams["beta1"][i], hparams["beta2"][i])
            self.param_groups[i]["eps"] = hparams["eps"][i]
            self.param_groups[i]["weight_decay"] = hparams["weight_decay"][i]

    def update_hparams_tensors(self):
        hparams = self.get_hparams()

        for key, value in hparams.items():
            if self.hparams_values[key] != value:
                self.hparams_values[key] = value
                self.hparams_tensors[key].copy_(torch.tensor(value, dtype=torch.float32))

    def get_data_ptrs(self, skip_grad: bool):
        w = []
        state = []
        g = []
        p_index = 0
        for group in self.param_groups:
            for p in group['params']:

                w.append(p.data.data_ptr())
                if skip_grad:
                    g.append(0)
                else:
                    assert p.grad is not None
                    g.append(p.grad.data_ptr())
                state.append(self.state[p_index].data_ptr())
                p_index += 1

        return {"w": w, "g": g, "state": state}

    def update_data_ptrs(self):
        data_ptrs = self.get_data_ptrs(skip_grad=False)

        for key, value in data_ptrs.items():
            if self.data_ptrs_values[key] != value:
                self.data_ptrs_values[key] = value
                self.data_ptrs_tensors[key].copy_(torch.tensor(value, dtype=torch.int64))

    def move_to_gpu(self):
        if self.device != self.param_groups[0]['params'][0].device:
            self.device = self.param_groups[0]['params'][0].device

            for i in range(len(self.param_groups)):
                for p in self.param_groups[i]['params']:
                    assert p.device == self.device
                    assert p.dtype == self.weight_dtype

            for key in self.state.keys():
                self.state[key] = self.state[key].to(self.device)
            for key in self.hparams_tensors.keys():
                self.hparams_tensors[key] = self.hparams_tensors[key].to(self.device)
            for key in self.data_ptrs_tensors.keys():
                self.data_ptrs_tensors[key] = self.data_ptrs_tensors[key].to(self.device)

            self.block_layer_id = self.block_layer_id.to(self.device)
            self.layer_first_block = self.layer_first_block.to(self.device)
            self.layer_group_id = self.layer_group_id.to(self.device)
            self.layer_num_elements = self.layer_num_elements.to(self.device)
            self.g_scale_tensor = self.g_scale_tensor.to(self.device)

        if "cpu" in str(self.device):
            raise Exception("Weights should be on gpu")
        self.on_gpu = True

    def step(self, grad_scale: float | None = None):
        if not self.on_gpu:
            self.move_to_gpu()
        self.update_hparams_tensors()
        self.update_data_ptrs()
        if self.weight_dtype == torch.bfloat16:
            assert grad_scale is None
            self.do_step()
        else:
            if grad_scale is None:
                raise Exception("Step should be called using grad_scaler.step(optimizer) when model type is float16. grad_scaler should be an object of minioptim.GradScaler class")
            if self.g_scale != grad_scale:
                self.g_scale = grad_scale
                self.g_scale_tensor.copy_(torch.tensor(grad_scale, dtype=torch.float32))
            max_grad_value = self.do_step()
            return max_grad_value.item()

    def do_step(self):
        with get_device_context(self.data_ptrs_tensors["w"]):
            with torch.no_grad():
                max_grad = adam_triton(
                    block_layer_index=self.block_layer_id,
                    layer_first_block_index=self.layer_first_block,
                    layer_n_elements=self.layer_num_elements,
                    layer_group=self.layer_group_id,
                    w_f16_ptrs=self.data_ptrs_tensors["w"],
                    state_ui8_ptrs=self.data_ptrs_tensors["state"],
                    g_f16_ptrs=self.data_ptrs_tensors["g"],
                    g_scale_f32=self.g_scale_tensor,
                    m_scale_f32=self.state["opt_m_scale"],
                    v_scale_f32=self.state["opt_v_scale"],
                    step_ui32=self.state["opt_step"],
                    beta1_f32=self.hparams_tensors["beta1"],
                    beta2_f32=self.hparams_tensors["beta2"],
                    weight_decay_f32=self.hparams_tensors["weight_decay"],
                    lr_f32=self.hparams_tensors["lr"],
                    eps_f32=self.hparams_tensors["eps"],
                    nbytes=self.state_bytes,
                    w_hidden_bits=self.config.w_hidden_bits,
                    m_exp_bits=self.config.m_exp_bits,
                    m_frac_bits=self.config.m_frac_bits,
                    v_exp_bits=self.config.v_exp_bits,
                    v_frac_bits=self.config.v_frac_bits,
                    adamw=self.adamw,
                    clip_outliers=self.config.clip_outliers,
                    bfloat16=self.weight_dtype == torch.bfloat16,
                    quantization_block_size=self.config.quantization_block_size,
                    triton_block_size=self.config.kernel_block_size,
                )

                if self.weight_dtype == torch.float16:
                    return torch.max(max_grad)

    def state_dict(self):
        state_dict = {}
        for key, value in self.state.items():
            state_dict[key] = value.cpu()
        state_dict["hparams"] = self.get_hparams()
        return state_dict

    def load_state_dict(self, state_dict):
        assert len(list(state_dict.keys())) == len(list(self.state.keys())) + 1
        for key in self.state.keys():
            assert key in state_dict
            assert self.state[key].dtype == state_dict[key].dtype
            assert self.state[key].shape == state_dict[key].shape
            self.state[key].copy_(state_dict[key])
        self.set_hparams(state_dict["hparams"])
