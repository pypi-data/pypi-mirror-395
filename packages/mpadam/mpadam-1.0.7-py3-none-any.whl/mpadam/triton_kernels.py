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
import triton
import triton.language as tl

MAX_FLOAT16 = tl.constexpr(torch.finfo(torch.float16).max)
MIN_FLOAT16 = tl.constexpr(torch.finfo(torch.float16).min)

TWO_POWER_112 = 1.0
for i in range(112):
    TWO_POWER_112 = TWO_POWER_112 * 2
TWO_POWER_112 = tl.constexpr(TWO_POWER_112)

TWO_POWER_60 = 1.0
for i in range(60):
    TWO_POWER_60 = TWO_POWER_60 * 2
TWO_POWER_60 = tl.constexpr(TWO_POWER_60)


@triton.jit
def contains_nan_or_inf_float16(x_f16):
    x = x_f16.cast(tl.uint16, bitcast=True)
    x = x & 0b0111110000000000
    x = tl.max(x)
    return x == 0b0111110000000000


@triton.jit
def contains_nan_or_inf_bfloat16(x_f16):
    x = x_f16.cast(tl.uint16, bitcast=True)
    x = x & 0b0111111110000000
    x = tl.max(x)
    return x == 0b0111111110000000


@triton.jit
def create_bitmask(num_1_bits):
    zero_bits = num_1_bits == 0
    num_1_bits = tl.where(zero_bits, 1, num_1_bits)
    x = 1 << (num_1_bits - 1)
    x = (x - 1) | x
    return tl.where(zero_bits, 0, x)


@triton.jit
def signed_shiftleft(x, shift):
    shift_exceeds_31 = tl.abs(shift) > 31
    shift = tl.where(shift_exceeds_31, 0, shift)
    result = tl.where(shift >= 0, x << shift, x >> (-shift))
    result = tl.where(shift_exceeds_31, 0, result)
    return result


@triton.jit
def load_state(state_ui8_ptr,
               offsets,
               BLOCK_SIZE: tl.constexpr,
               NBYTES: tl.constexpr,
               W_HIDDEN_BITS: tl.constexpr,
               M_EXP_BITS: tl.constexpr,
               M_FRAC_BITS: tl.constexpr,
               V_EXP_BITS: tl.constexpr,
               V_FRAC_BITS: tl.constexpr):
    m_bits: tl.constexpr = M_EXP_BITS + M_FRAC_BITS + 1
    v_bits: tl.constexpr = V_EXP_BITS + V_FRAC_BITS
    m_offset: tl.constexpr = W_HIDDEN_BITS + v_bits
    v_offset: tl.constexpr = W_HIDDEN_BITS

    w_hidden_ui32 = tl.zeros((BLOCK_SIZE, ), tl.uint32)
    m_ui32 = tl.zeros((BLOCK_SIZE, ), tl.uint32)
    v_ui32 = tl.zeros((BLOCK_SIZE, ), tl.uint32)

    for i in tl.static_range(NBYTES):
        state = tl.load((state_ui8_ptr + BLOCK_SIZE * i) + offsets)
        state = state.to(tl.uint32)
        w_hidden_ui32 |= signed_shiftleft(state, 8 * i)
        m_ui32 |= signed_shiftleft(state, 8 * i - m_offset)
        v_ui32 |= signed_shiftleft(state, 8 * i - v_offset)

    w_hidden_ui32 &= create_bitmask(W_HIDDEN_BITS)
    m_ui32 &= create_bitmask(m_bits)
    v_ui32 &= create_bitmask(v_bits)

    return w_hidden_ui32, m_ui32, v_ui32


@triton.jit
def save_state(state_ui8_ptr,
               offsets,
               mask,
               w_hidden_ui32,
               m_ui32,
               v_ui32,
               BLOCK_SIZE: tl.constexpr,
               NBYTES: tl.constexpr,
               W_HIDDEN_BITS: tl.constexpr,
               V_EXP_BITS: tl.constexpr,
               V_FRAC_BITS: tl.constexpr):
    v_bits: tl.constexpr = V_EXP_BITS + V_FRAC_BITS
    m_offset: tl.constexpr = W_HIDDEN_BITS + v_bits
    v_offset: tl.constexpr = W_HIDDEN_BITS

    for i in tl.static_range(NBYTES):
        state = signed_shiftleft(w_hidden_ui32, -8 * i)
        state |= signed_shiftleft(m_ui32, m_offset - 8 * i)
        state |= signed_shiftleft(v_ui32, v_offset - 8 * i)

        state = (state & 0xff).to(tl.uint8)
        tl.store((state_ui8_ptr + BLOCK_SIZE * i) + offsets, state, mask=mask)


@triton.jit
def quantize_weight_float16(tensor32, randint_values, W_HIDDEN_BITS: tl.constexpr):
    tensor32 = tl.clamp(tensor32, MIN_FLOAT16, MAX_FLOAT16)
    tensor32 /= TWO_POWER_112
    tensor32 = tensor32.cast(tl.uint32, bitcast=True)
    missing_bits = tl.cast(13 - W_HIDDEN_BITS, tl.uint32)
    tensor32 += randint_values % (1 << missing_bits)
    w_hidden_ui32 = (tensor32 >> missing_bits) & create_bitmask(W_HIDDEN_BITS)
    round_up = w_hidden_ui32 >= (1 << (tl.maximum(W_HIDDEN_BITS, 1) - 1))
    tensor32 = tl.where(round_up, tensor32 + 0x00002000, tensor32)
    tensor32 &= 0xffffe000
    tensor16 = (tensor32.cast(tl.float32, bitcast=True) * TWO_POWER_112).cast(tl.float16, fp_downcast_rounding="rtne")
    return tensor16, w_hidden_ui32


@triton.jit
def dequantize_weight_float16(tensor16, w_hidden_ui32, W_HIDDEN_BITS: tl.constexpr):
    tensor32 = tensor16.cast(tl.float32)
    tensor32 /= TWO_POWER_112
    tensor32 = tensor32.cast(tl.uint32, bitcast=True)
    round_up = w_hidden_ui32 >= (1 << (tl.maximum(W_HIDDEN_BITS, 1) - 1))
    tensor32 = tl.where(round_up, tensor32 - 0x00002000, tensor32)
    missing_bits = tl.cast(13 - W_HIDDEN_BITS, tl.uint32)
    tensor32 |= w_hidden_ui32 << missing_bits

    return tensor32.cast(tl.float32, bitcast=True) * TWO_POWER_112


@triton.jit
def quantize_weight_bfloat16(tensor32, randint_values, W_HIDDEN_BITS: tl.constexpr):
    tensor32 = tensor32.cast(tl.uint32, bitcast=True)
    missing_bits = tl.cast(16 - W_HIDDEN_BITS, tl.uint32)
    tensor32 += randint_values % (1 << missing_bits)
    w_hidden_ui32 = (tensor32 >> missing_bits) & create_bitmask(W_HIDDEN_BITS)
    round_up = w_hidden_ui32 >= (1 << (tl.maximum(W_HIDDEN_BITS, 1) - 1))
    tensor32 = tl.where(round_up, tensor32 + 0x00010000, tensor32)
    tensor32 &= 0xffff0000
    tensor16 = tensor32.cast(tl.float32, bitcast=True).cast(tl.bfloat16)
    return tensor16, w_hidden_ui32


@triton.jit
def dequantize_weight_bfloat16(tensor16, w_hidden_ui32, W_HIDDEN_BITS: tl.constexpr):
    tensor32 = tensor16.cast(tl.float32)
    tensor32 = tensor32.cast(tl.uint32, bitcast=True)
    round_up = w_hidden_ui32 >= (1 << (tl.maximum(W_HIDDEN_BITS, 1) - 1))
    tensor32 = tl.where(round_up, tensor32 - 0x00010000, tensor32)
    missing_bits = tl.cast(16 - W_HIDDEN_BITS, tl.uint32)
    tensor32 |= w_hidden_ui32 << missing_bits
    return tensor32.cast(tl.float32, bitcast=True)


@triton.jit
def quantize_v(tensor32, randint_values, V_EXP_BITS: tl.constexpr, V_FRAC_BITS: tl.constexpr):
    max_quantized_value = create_bitmask(24 + V_EXP_BITS) - create_bitmask(23 - V_FRAC_BITS)
    max_quantized_value = tl.cast(max_quantized_value, tl.float32, bitcast=True)

    min_quantized_value = 1 << (23 + V_EXP_BITS)
    min_quantized_value = tl.cast(min_quantized_value, tl.float32, bitcast=True)

    tensor32 = tl.sqrt_rn(tensor32)
    tensor32 = tensor32 / TWO_POWER_60

    v_scale_f32 = tl.max(tensor32, axis=0, keep_dims=True) / max_quantized_value
    v_scale_f32 = tl.maximum(v_scale_f32, 2e-38)
    v_scale_f32 = tl.cast(v_scale_f32, tl.uint32, bitcast=True)
    v_scale_f32 += 65535
    v_scale_f32 &= 0xffff0000
    v_scale_f32 = tl.cast(v_scale_f32, tl.float32, bitcast=True)
    tensor32 = tensor32 / v_scale_f32

    tensor32 = tl.clamp(tensor32, min_quantized_value, max_quantized_value)
    tensor32 = tensor32.cast(tl.uint32, bitcast=True)
    missing_bits = tl.cast(23 - V_FRAC_BITS, tl.uint32)
    tensor32 += randint_values % (1 << missing_bits)
    tensor32 = (tensor32 >> missing_bits) & create_bitmask(V_EXP_BITS + V_FRAC_BITS)

    return tensor32, v_scale_f32.cast(tl.bfloat16)


@triton.jit
def dequantize_v(tensor32, v_scale_f32, V_EXP_BITS: tl.constexpr, V_FRAC_BITS: tl.constexpr):
    missing_bits = tl.cast(23 - V_FRAC_BITS, tl.uint32)
    tensor32 = (tensor32 << missing_bits) | (1 << (23 + V_EXP_BITS))
    tensor32 = tensor32.cast(tl.float32, bitcast=True)
    tensor32 = tensor32 * v_scale_f32.cast(tl.float32)
    tensor32 = tensor32 * TWO_POWER_60
    return tensor32 * tensor32


@triton.jit
def quantize_m(tensor32, randint_values, M_EXP_BITS: tl.constexpr, M_FRAC_BITS: tl.constexpr):
    max_quantized_value = create_bitmask(23 + M_EXP_BITS) - create_bitmask(23 - M_FRAC_BITS)
    max_quantized_value = tl.cast(max_quantized_value, tl.float32, bitcast=True)

    tensor32 = tensor32 / TWO_POWER_60

    m_scale_f32 = tl.max(tl.abs(tensor32), axis=0, keep_dims=True) / max_quantized_value
    m_scale_f32 = tl.maximum(m_scale_f32, 2e-38)
    m_scale_f32 = tl.cast(m_scale_f32, tl.uint32, bitcast=True)
    m_scale_f32 += 65535
    m_scale_f32 &= 0xffff0000
    m_scale_f32 = tl.cast(m_scale_f32, tl.float32, bitcast=True)
    tensor32 = tensor32 / m_scale_f32

    tensor32 = tl.clamp(tensor32, -max_quantized_value, max_quantized_value)
    tensor32 = tensor32.cast(tl.uint32, bitcast=True)
    missing_bits = tl.cast(23 - M_FRAC_BITS, tl.uint32)
    tensor32 = tensor32 + randint_values % (1 << missing_bits)
    sign = tensor32 & 0x80000000
    value = tensor32 & 0x7fffffff

    tensor32 = (value >> missing_bits) | (sign >> (31 - M_EXP_BITS - M_FRAC_BITS))
    return tensor32, m_scale_f32.cast(tl.bfloat16)


@triton.jit
def dequantize_m(tensor32, m_scale_f32, M_EXP_BITS: tl.constexpr, M_FRAC_BITS: tl.constexpr):
    sign = (tensor32 << (31 - M_EXP_BITS - M_FRAC_BITS)) & 0x80000000
    missing_bits = tl.cast(23 - M_FRAC_BITS, tl.uint32)
    value = (tensor32 & create_bitmask(M_EXP_BITS + M_FRAC_BITS)) << missing_bits
    tensor32 = sign | value
    tensor32 = tensor32.cast(tl.float32, bitcast=True)
    tensor32 = tensor32 * m_scale_f32.cast(tl.float32)
    return tensor32 * TWO_POWER_60


@triton.jit
def adam_kernel(block_layer_index_ptr,
                layer_first_block_index_ptr,
                layer_n_elements_ptr,
                layer_group_ptr,
                w_f16_ptrs,
                state_ui8_ptrs,
                g_f16_ptrs,
                g_scale_f32_ptr,
                m_scale_f32_ptr,
                v_scale_f32_ptr,
                step_ui32_ptr,
                max_grad_f16_ptr,
                beta1_f32_ptr,
                beta2_f32_ptr,
                weight_decay_f32_ptr,
                lr_f32_ptr,
                eps_f32_ptr,
                NBYTES: tl.constexpr,
                W_HIDDEN_BITS: tl.constexpr,
                M_EXP_BITS: tl.constexpr,
                M_FRAC_BITS: tl.constexpr,
                V_EXP_BITS: tl.constexpr,
                V_FRAC_BITS: tl.constexpr,
                ADAMW: tl.constexpr,
                CLIP_OUTLIERS: tl.constexpr,
                BFLOAT16: tl.constexpr,
                QUANTIZATION_BLOCK_SIZE: tl.constexpr,
                TRITON_BLOCK_SIZE: tl.constexpr,
                ):

    pid = tl.program_id(axis=0)
    block_id = pid
    layer_index = tl.load(block_layer_index_ptr + block_id)
    group_index = tl.load(layer_group_ptr + layer_index)

    w_f16_ptr = tl.load(w_f16_ptrs + layer_index)
    g_f16_ptr = tl.load(g_f16_ptrs + layer_index)
    if BFLOAT16:
        w_f16_ptr = w_f16_ptr.to(tl.pointer_type(tl.bfloat16))
        g_f16_ptr = g_f16_ptr.to(tl.pointer_type(tl.bfloat16))
    else:
        w_f16_ptr = w_f16_ptr.to(tl.pointer_type(tl.float16))
        g_f16_ptr = g_f16_ptr.to(tl.pointer_type(tl.float16))

    state_ui8_ptr = tl.load(state_ui8_ptrs + layer_index).to(tl.pointer_type(tl.uint8))

    layer_first_block_index = tl.load(layer_first_block_index_ptr + layer_index)
    n_elements = tl.load(layer_n_elements_ptr + layer_index)

    block_start = (block_id - layer_first_block_index) * TRITON_BLOCK_SIZE
    offsets = block_start + tl.arange(0, TRITON_BLOCK_SIZE)
    scale_offsets = tl.arange(0, TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE)
    state_offsets = block_start * NBYTES + tl.arange(0, TRITON_BLOCK_SIZE)
    mask = offsets < n_elements

    g_f16 = tl.load(g_f16_ptr + offsets, mask=mask, other=0.0)
    if BFLOAT16:
        save_step = not contains_nan_or_inf_bfloat16(g_f16)
    else:
        save_step = not contains_nan_or_inf_float16(g_f16)
        max_grad_f16 = tl.max(tl.abs(g_f16))
        max_grad_f16 = tl.where(save_step, max_grad_f16, MAX_FLOAT16)
        tl.store(max_grad_f16_ptr + block_id, max_grad_f16)
    mask = mask & save_step

    g_f32 = g_f16.cast(tl.float32)
    g_f16 = None
    if not BFLOAT16:
        g_scale_f32 = tl.load(g_scale_f32_ptr)
        g_f32 /= g_scale_f32
        g_scale_f32 = None
    g_f32 = g_f32.reshape(QUANTIZATION_BLOCK_SIZE, TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE, can_reorder=True)

    w_hidden_ui32, m_ui32, v_ui32 = load_state(state_ui8_ptr,
                                               state_offsets,
                                               TRITON_BLOCK_SIZE,
                                               NBYTES,
                                               W_HIDDEN_BITS,
                                               M_EXP_BITS,
                                               M_FRAC_BITS,
                                               V_EXP_BITS,
                                               V_FRAC_BITS)
    w_hidden_ui32 = w_hidden_ui32.reshape(QUANTIZATION_BLOCK_SIZE,
                                          TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE,
                                          can_reorder=True)
    m_ui32 = m_ui32.reshape(QUANTIZATION_BLOCK_SIZE,
                            TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE,
                            can_reorder=True)
    v_ui32 = v_ui32.reshape(QUANTIZATION_BLOCK_SIZE,
                            TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE,
                            can_reorder=True)

    w_f16 = tl.load(w_f16_ptr + offsets, mask=mask, other=0.0)
    w_f16 = w_f16.reshape(QUANTIZATION_BLOCK_SIZE,
                          TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE,
                          can_reorder=True)
    if BFLOAT16:
        w_f32 = dequantize_weight_bfloat16(w_f16, w_hidden_ui32, W_HIDDEN_BITS)
    else:
        w_f32 = dequantize_weight_float16(w_f16, w_hidden_ui32, W_HIDDEN_BITS)
    w_f16 = None

    weight_decay_f32 = tl.load(weight_decay_f32_ptr + group_index)
    beta1_f32 = tl.load(beta1_f32_ptr + group_index)
    beta2_f32 = tl.load(beta2_f32_ptr + group_index)
    eps_f32 = tl.load(eps_f32_ptr + group_index)
    lr_f32 = tl.load(lr_f32_ptr + group_index)

    step_ui32 = tl.load(step_ui32_ptr + block_id)

    if ADAMW:
        w_f32 *= (1 - lr_f32 * weight_decay_f32)
    else:
        g_f32 += weight_decay_f32 * w_f32

    v_scale_f32 = tl.load(v_scale_f32_ptr + block_id * (TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE) + scale_offsets)
    v_scale_f32 = v_scale_f32.reshape(1, TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE, can_reorder=True)
    v_f32 = dequantize_v(v_ui32, v_scale_f32, V_EXP_BITS, V_FRAC_BITS)

    m_scale_f32 = tl.load(m_scale_f32_ptr + block_id * (TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE) + scale_offsets)
    m_scale_f32 = m_scale_f32.reshape(1, TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE, can_reorder=True)
    m_f32 = dequantize_m(m_ui32, m_scale_f32, M_EXP_BITS, M_FRAC_BITS)

    v_f32 = beta2_f32 * v_f32 + (1.0 - beta2_f32) * (g_f32 * g_f32)
    m_f32 = beta1_f32 * m_f32 + (1.0 - beta1_f32) * g_f32
    g_f32 = None

    randint_values = tl.randint(step_ui32, (offsets % 1073741824).cast(tl.uint32)).cast(tl.uint32, bitcast=True)
    randint_values = randint_values.reshape(QUANTIZATION_BLOCK_SIZE, TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE, can_reorder=True)

    v_ui32, v_scale_f32 = quantize_v(v_f32, randint_values, V_EXP_BITS, V_FRAC_BITS)
    v_scale_f32 = v_scale_f32.reshape(TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE, can_reorder=True)
    tl.store(v_scale_f32_ptr + block_id * (TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE) + scale_offsets, v_scale_f32, mask=save_step)
    v_scale_f32 = None

    beta1_correction_f32 = 1 - tl.exp(step_ui32.cast(tl.float32) * tl.log(beta1_f32))
    beta2_correction_f32 = 1 - tl.exp(step_ui32.cast(tl.float32) * tl.log(beta2_f32))

    v_f32 /= beta2_correction_f32
    v_sqrt_f32 = tl.sqrt_rn(v_f32)
    v_f32 = None
    if CLIP_OUTLIERS:
        max_m = v_sqrt_f32 * (4 * tl.sqrt_rn(beta1_f32))
        max_m *= beta1_correction_f32
        m_f32 = tl.clamp(m_f32, -max_m, max_m)

    m_ui32, m_scale_f32 = quantize_m(m_f32, randint_values, M_EXP_BITS, M_FRAC_BITS)
    m_scale_f32 = m_scale_f32.reshape(TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE, can_reorder=True)
    tl.store(m_scale_f32_ptr + block_id * (TRITON_BLOCK_SIZE // QUANTIZATION_BLOCK_SIZE) + scale_offsets,
             m_scale_f32,
             mask=save_step)
    m_scale_f32 = None

    m_f32 /= beta1_correction_f32

    step_ui32 = tl.where(step_ui32 == 4000000000, 2000000000, step_ui32 + 1)
    tl.store(step_ui32_ptr + block_id, step_ui32, mask=save_step)

    w_f32 -= lr_f32 * m_f32 / (v_sqrt_f32 + eps_f32)

    if BFLOAT16:
        w_f16, w_hidden_ui32 = quantize_weight_bfloat16(w_f32, randint_values, W_HIDDEN_BITS)
    else:
        w_f16, w_hidden_ui32 = quantize_weight_float16(w_f32, randint_values, W_HIDDEN_BITS)
    w_f16 = w_f16.reshape(TRITON_BLOCK_SIZE, can_reorder=True)
    tl.store(w_f16_ptr + offsets, w_f16, mask=mask)
    w_hidden_ui32 = w_hidden_ui32.reshape(TRITON_BLOCK_SIZE, can_reorder=True)
    m_ui32 = m_ui32.reshape(TRITON_BLOCK_SIZE, can_reorder=True)
    v_ui32 = v_ui32.reshape(TRITON_BLOCK_SIZE, can_reorder=True)
    save_state(state_ui8_ptr,
               state_offsets,
               save_step,
               w_hidden_ui32,
               m_ui32,
               v_ui32,
               TRITON_BLOCK_SIZE,
               NBYTES,
               W_HIDDEN_BITS,
               V_EXP_BITS,
               V_FRAC_BITS)


def adam_triton(block_layer_index: torch.Tensor,
                layer_first_block_index: torch.Tensor,
                layer_n_elements: torch.Tensor,
                layer_group: torch.Tensor,
                w_f16_ptrs: torch.Tensor,
                state_ui8_ptrs: torch.Tensor,
                g_f16_ptrs: torch.Tensor,
                g_scale_f32: torch.Tensor,
                m_scale_f32: torch.Tensor,
                v_scale_f32: torch.Tensor,
                step_ui32: torch.Tensor,
                beta1_f32: torch.Tensor,
                beta2_f32: torch.Tensor,
                weight_decay_f32: torch.Tensor,
                lr_f32: torch.Tensor,
                eps_f32: torch.Tensor,
                nbytes: int,
                w_hidden_bits: int,
                m_exp_bits: int,
                m_frac_bits: int,
                v_exp_bits: int,
                v_frac_bits: int,
                adamw: bool,
                clip_outliers: bool,
                bfloat16: bool,
                quantization_block_size: int,
                triton_block_size: int,
                ):

    num_blocks = step_ui32.numel()
    if bfloat16:
        max_grad_f16 = g_scale_f32 # these tensors are not used in bf16 mode
    else:
        max_grad_f16 = torch.empty([num_blocks,], dtype=torch.float16, device=v_scale_f32.device)
    grid = lambda meta: (num_blocks, )

    adam_kernel[grid](
        block_layer_index,
        layer_first_block_index,
        layer_n_elements,
        layer_group,
        w_f16_ptrs,
        state_ui8_ptrs,
        g_f16_ptrs,
        g_scale_f32,
        m_scale_f32,
        v_scale_f32,
        step_ui32,
        max_grad_f16,
        beta1_f32,
        beta2_f32,
        weight_decay_f32,
        lr_f32,
        eps_f32,
        nbytes,
        w_hidden_bits,
        m_exp_bits,
        m_frac_bits,
        v_exp_bits,
        v_frac_bits,
        adamw,
        clip_outliers,
        bfloat16,
        quantization_block_size,
        triton_block_size)

    return max_grad_f16
