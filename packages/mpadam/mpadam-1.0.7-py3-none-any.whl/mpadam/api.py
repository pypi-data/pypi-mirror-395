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

from .adam import AdamBase
from .config import MPConfig


class MPAdam(AdamBase):
    def __init__(self,
                 params,
                 lr=0.001,
                 betas=(0.9, 0.999),
                 eps=1e-8,
                 weight_decay=0,
                 config: str | MPConfig = "medium"):
        """Mixed Precision Adam optimizer.

        Arguments:
            params:
                The parameters to optimize. The format is the same as in
                torch.optim.Adam.
            lr (`float`, defaults to 0.001):
                The learning rate.
            betas (`tuple(float, float)`, defaults to (0.9, 0.999)):
                The beta values of the first and second-order moments.
            eps (`float`, defaults to 1e-8):
                The epsilon value prevents division by zero.
            weight_decay (`float`, defaults to 0):
                The weight decay value.
            config (`MPConfig` or `str`, defaults to 'medium'):
                The quantization config or config preset name.
                Supports the following presets (the size includes the weights,
                the gradients and the optimizer state):
                    'small': (6 bytes) the smallest preset that achieves the
                        same accuracy and the same loss curve as the regular
                        Adam on ResNet-50, ViT-b, and NanoGPT models.
                    'medium': (8 bytes) all the precision settings are equally
                        increased compared to the 'small' preset
                    'large': (11 bytes) in this mode the theoretical error from
                        the optimizer quantization is smaller than the error
                        from the 16 bit gradients when beta1 <= 0.9 and
                        beta2 <= 0.999.
        """
        super().__init__(params=params,
                         lr=lr,
                         betas=betas,
                         eps=eps,
                         weight_decay=weight_decay,
                         config=config,
                         adamw=False)


class MPAdamW(AdamBase):
    def __init__(self,
                 params,
                 lr=0.001,
                 betas=(0.9, 0.999),
                 eps=1e-8,
                 weight_decay=0.01,
                 config: str | MPConfig = "small"):
        """Mixed Precision AdamW optimizer.

        Arguments:
            params:
                The parameters to optimize. The format is the same as in
                torch.optim.AdamW.
            lr (`float`, defaults to 0.001):
                The learning rate.
            betas (`tuple(float, float)`, defaults to (0.9, 0.999)):
                The beta values of the first and second-order moments.
            eps (`float`, defaults to 1e-8):
                The epsilon value prevents division by zero.
            weight_decay (`float`, defaults to 0.01):
                The weight decay value.
            config (`MPConfig` or `str`, defaults to 'small'):
                The quantization config or config preset name.
                Supports the following presets (the size includes the weights,
                the gradients and the optimizer state):
                    'small': (6 bytes) the smallest preset that achieves the
                        same accuracy and same loss curve as the regular AdamW
                        on ResNet-50, ViT-b, and NanoGPT models.
                    'medium': (8 bytes) all the precision settings are equally
                        increased compared to the 'small' preset
                    'large': (11 bytes) in this mode the theoretical error from
                        the optimizer quantization is smaller than the error
                        from the 16 bit gradients when beta1 <= 0.9 and
                        beta2 <= 0.999.
        """
        super().__init__(params=params,
                         lr=lr,
                         betas=betas,
                         eps=eps,
                         weight_decay=weight_decay,
                         config=config,
                         adamw=True)
