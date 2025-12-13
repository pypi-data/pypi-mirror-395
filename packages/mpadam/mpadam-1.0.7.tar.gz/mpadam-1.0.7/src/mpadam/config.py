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


class MPConfig:
    def __init__(self,
                 w_hidden_bits=8,
                 m_exp_bits=4,
                 m_frac_bits=7,
                 v_exp_bits=4,
                 v_frac_bits=8,
                 clip_outliers=True,
                 quantization_block_size=64,
                 kernel_block_size=1024):
        """Config for Mixed Precision Adam optimizer.

        Arguments:
            w_hidden_bits (`int`, defaults to 8):
                The number of bits in the hidden part of weight fraction part
                (0-16 for bfloat16, 0-13 for float16).
            m_exp_bits (`int`, defaults to 4):
                The number of bits in the exponent part of the first order
                Adam state (0-7).
            m_frac_bits (`int`, defaults to 7):
                The number of bits in the fraction part of the first order
                Adam state (0-23).
            v_exp_bits (`int`, defaults to 4):
                The number of bits in the exponent part of the second order
                Adam state (0-7).
            v_frac_bits (`int`, defaults to 8):
                The number of bits in the fraction part of the second order
                Adam state (0-23).
            clip_outliers (`bool`, defaults to True):
                Enables clipping large out of distribution weight updates.
            quantization_block_size (`int`, defaults to 64):
                The size of the blockwise quantization block.
                Should be a power of 2.
            kernel_block_size (`int`, defaults to 1024):
                The size of the triton kernel block size.
                Should be a power of 2.
                Shouldn't be smaller the quantization_blocks_size.
        """
        self.w_hidden_bits = w_hidden_bits
        self.m_exp_bits = m_exp_bits
        self.m_frac_bits = m_frac_bits
        self.v_exp_bits = v_exp_bits
        self.v_frac_bits = v_frac_bits
        self.clip_outliers = clip_outliers
        self.quantization_block_size = quantization_block_size
        self.kernel_block_size = kernel_block_size


def get_preset(preset_name, weight_dtype):
    if weight_dtype != torch.float16 and weight_dtype != torch.bfloat16:
        raise Exception("Weight type should be either float16 or bfloat16")

    if preset_name == "small":
        if weight_dtype == torch.bfloat16:
            return MPConfig(w_hidden_bits=4,
                            m_exp_bits=3,
                            m_frac_bits=2,
                            v_exp_bits=3,
                            v_frac_bits=3,
                            clip_outliers=True)
        else:
            return MPConfig(w_hidden_bits=2,
                            m_exp_bits=3,
                            m_frac_bits=3,
                            v_exp_bits=3,
                            v_frac_bits=4,
                            clip_outliers=True)

    elif preset_name == "medium":
        if weight_dtype == torch.bfloat16:
            return MPConfig(w_hidden_bits=8,
                            m_exp_bits=4,
                            m_frac_bits=7,
                            v_exp_bits=4,
                            v_frac_bits=8,
                            clip_outliers=True)
        else:
            return MPConfig(w_hidden_bits=6,
                            m_exp_bits=4,
                            m_frac_bits=8,
                            v_exp_bits=4,
                            v_frac_bits=9,
                            clip_outliers=True)

    elif preset_name == "large":
        if weight_dtype == torch.bfloat16:
            return MPConfig(w_hidden_bits=16,
                            m_exp_bits=4,
                            m_frac_bits=13,
                            v_exp_bits=4,
                            v_frac_bits=18,
                            clip_outliers=False)
        else:
            return MPConfig(w_hidden_bits=13,
                            m_exp_bits=4,
                            m_frac_bits=14,
                            v_exp_bits=4,
                            v_frac_bits=20,
                            clip_outliers=False)

    else:
        raise Exception(f'Unknown preset name {preset_name}. Supported presets: "small", "medium", "large"')


def check_config(config, weight_dtype):
    assert config.w_hidden_bits >= 0 and config.w_hidden_bits <= 16
    if weight_dtype == torch.float16:
        assert config.w_hidden_bits <= 13
    assert config.m_exp_bits >= 0 and config.m_exp_bits <= 7
    assert config.m_frac_bits >= 0 and config.m_frac_bits <= 23
    assert config.v_exp_bits >= 0 and config.v_exp_bits <= 7
    assert config.v_frac_bits >= 0 and config.v_frac_bits <= 23


def get_num_bytes(config):
    m_sign_bits = 1
    state_bits = (config.w_hidden_bits +
                  m_sign_bits + config.m_exp_bits + config.m_frac_bits +
                  config.v_exp_bits + config.v_frac_bits)
    if state_bits % 8 != 0:
        raise Exception("Total state bits is not divisible by 8. (w_hidden_bits + m_exp_bits + m_frac_bits + v_exp_bits + v_frac_bits + 1) should be divisible by 8.")
    return state_bits // 8
    