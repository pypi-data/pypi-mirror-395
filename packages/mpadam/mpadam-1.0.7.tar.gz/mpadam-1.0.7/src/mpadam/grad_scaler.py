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

MAX_FLOAT16 = torch.finfo(torch.float16).max


class GradScaler:
    def __init__(
            self,
            range_min = MAX_FLOAT16 / 4,
            range_max = MAX_FLOAT16 / 2,
            calibration_range_min = MAX_FLOAT16 / 32,
            decay = 0.999,
            max_calibration_attempts = 100,
            ):
        self.range_min = range_min
        self.range_max = range_max
        self.calibration_range_min = calibration_range_min
        self.max_calibration_attempts = max_calibration_attempts
        self.decay = decay

        self.max_grad = 0
        self.scale_value = 1.0
        self.calibrated = False
        self.calibration_attempts = 0

    def meets_calibration_requirements(self, max_grad):
        return max_grad > self.calibration_range_min and max_grad < self.range_max

    def scale(self, loss):
        return loss * self.scale_value

    def step(self, optimizer):
        cur_max_grad = None
        if not self.calibrated:
            cur_max_grad = []
            for group in optimizer.param_groups:
                for p in group['params']:
                    if p.grad is not None:
                        grad = p.grad.nan_to_num(nan=MAX_FLOAT16, posinf=MAX_FLOAT16, neginf=MAX_FLOAT16)
                        cur_max_grad.append(grad.abs().max())
            if len(cur_max_grad) == 0:
                raise Exception("All gradients are None")
            cur_max_grad = torch.stack(cur_max_grad, 0).max().item()

        if self.calibrated or self.meets_calibration_requirements(cur_max_grad):
            cur_max_grad = optimizer.step(self.scale_value)

        self.max_grad = max(self.max_grad, cur_max_grad)

    def update(self):
        if not self.calibrated:
            if self.meets_calibration_requirements(self.max_grad):
                self.calibrated = True
            else:
                self.calibration_attempts += 1
                if self.calibration_attempts > self.max_calibration_attempts:
                    raise Exception("Can't calibrate gradient scaler")

        if self.max_grad < 1:
            self.scale_value *= 32
            self.max_grad *= 32
        elif self.max_grad < self.range_min or self.max_grad > self.range_max:
            factor = (self.range_max + self.range_min) / 2 / self.max_grad
            self.scale_value *= factor
            self.max_grad *= factor

        self.max_grad *= self.decay

        if not self.calibrated:
            self.max_grad = 0

    def state_dict(self):
        return {
            "max_grad": self.max_grad,
            "scale_value": self.scale_value,
            "calibrated": self.calibrated,
            "calibration_attempts": self.calibration_attempts,
        }

    def load_state_dict(self, state_dict):
        self.max_grad = state_dict["max_grad"]
        self.scale_value = state_dict["scale_value"]
        self.calibrated = state_dict["calibrated"]
        self.calibration_attempts = state_dict["calibration_attempts"]
