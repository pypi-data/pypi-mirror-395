
from gguf_connector.quant5c import dequantize_functions
from gguf_connector.reader import GGML_QUANT_SIZES, GGMLQuantizationType
# call gguf-connector engine striaght for easier maintenance

import inspect
import os
from contextlib import nullcontext
import torch
import torch.nn as nn

# credits should be given to huggingface, city96, etc., for this part still
from ...utils import is_accelerate_available, is_kernels_available

if is_accelerate_available():
    import accelerate
    from accelerate import init_empty_weights
    from accelerate.hooks import add_hook_to_module, remove_hook_from_module

can_use_cuda_kernels = (
    os.getenv("DIFFUSERS_GGUF_CUDA_KERNELS", "false").lower() in ["1", "true", "yes"]
    and torch.cuda.is_available()
    and torch.cuda.get_device_capability()[0] >= 7
)
if can_use_cuda_kernels and is_kernels_available():
    from kernels import get_kernel
    ops = get_kernel("Isotr0py/ggml")
else:
    ops = None

UNQUANTIZED_TYPES = {GGMLQuantizationType.F32, GGMLQuantizationType.F16, GGMLQuantizationType.BF16}
STANDARD_QUANT_TYPES = {
    GGMLQuantizationType.Q4_0,
    GGMLQuantizationType.Q4_1,
    GGMLQuantizationType.Q5_0,
    GGMLQuantizationType.Q5_1,
    GGMLQuantizationType.Q8_0,
    GGMLQuantizationType.Q8_1,
}
KQUANT_TYPES = {
    GGMLQuantizationType.Q2_K,
    GGMLQuantizationType.Q3_K,
    GGMLQuantizationType.Q4_K,
    GGMLQuantizationType.Q5_K,
    GGMLQuantizationType.Q6_K,
}
IMATRIX_QUANT_TYPES = {
    GGMLQuantizationType.IQ1_M,
    GGMLQuantizationType.IQ1_S,
    GGMLQuantizationType.IQ2_XXS,
    GGMLQuantizationType.IQ2_XS,
    GGMLQuantizationType.IQ2_S,
    GGMLQuantizationType.IQ3_XXS,
    GGMLQuantizationType.IQ3_S,
    GGMLQuantizationType.IQ4_XS,
    GGMLQuantizationType.IQ4_NL,
}
# TODO(Isotr0py): Currently, we don't have MMQ kernel for I-Matrix quantization.
# Consolidate DEQUANT_TYPES, MMVQ_QUANT_TYPES and MMQ_QUANT_TYPES after we add
# MMQ kernel for I-Matrix quantization.
DEQUANT_TYPES = STANDARD_QUANT_TYPES | KQUANT_TYPES | IMATRIX_QUANT_TYPES
MMVQ_QUANT_TYPES = STANDARD_QUANT_TYPES | KQUANT_TYPES | IMATRIX_QUANT_TYPES
MMQ_QUANT_TYPES = STANDARD_QUANT_TYPES | KQUANT_TYPES

def _fused_mul_mat_gguf(x: torch.Tensor, qweight: torch.Tensor, qweight_type: int) -> torch.Tensor:
    # there is no need to call any kernel for fp16/bf16
    if qweight_type in UNQUANTIZED_TYPES:
        return x @ qweight.T
    # TODO(Isotr0py): GGUF's MMQ and MMVQ implementation are designed for
    # contiguous batching and inefficient with diffusers' batching,
    # so we disabled it now.

    # elif qweight_type in MMVQ_QUANT_TYPES:
    #     y = ops.ggml_mul_mat_vec_a8(qweight, x, qweight_type, qweight.shape[0])
    # elif qweight_type in MMQ_QUANT_TYPES:
    #     y = ops.ggml_mul_mat_a8(qweight, x, qweight_type, qweight.shape[0])

    # If there is no available MMQ kernel, fallback to dequantize
    if qweight_type in DEQUANT_TYPES:
        block_size, type_size = GGML_QUANT_SIZES[qweight_type]
        shape = (qweight.shape[0], qweight.shape[1] // type_size * block_size)
        weight = ops.ggml_dequantize(qweight, qweight_type, *shape)
        y = x @ weight.to(x.dtype).T
    else:
        # Raise an error if the quantization type is not supported.
        # Might be useful if llama.cpp adds a new quantization type.
        # Wrap to GGMLQuantizationType IntEnum to make sure it's a valid type.
        qweight_type = GGMLQuantizationType(qweight_type)
        raise NotImplementedError(f"Unsupported GGUF quantization type: {qweight_type}")
    return y.as_tensor()

# Copied from diffusers.quantizers.bitsandbytes.utils._create_accelerate_new_hook
def _create_accelerate_new_hook(old_hook):
    r"""
    Creates a new hook based on the old hook. Use it only if you know what you are doing ! This method is a copy of:
    https://github.com/huggingface/peft/blob/748f7968f3a31ec06a1c2b0328993319ad9a150a/src/peft/utils/other.py#L245 with
    some changes
    """
    old_hook_cls = getattr(accelerate.hooks, old_hook.__class__.__name__)
    old_hook_attr = old_hook.__dict__
    filtered_old_hook_attr = {}
    old_hook_init_signature = inspect.signature(old_hook_cls.__init__)
    for k in old_hook_attr.keys():
        if k in old_hook_init_signature.parameters:
            filtered_old_hook_attr[k] = old_hook_attr[k]
    new_hook = old_hook_cls(**filtered_old_hook_attr)
    return new_hook

def _replace_with_gguf_linear(model, compute_dtype, state_dict, prefix="", modules_to_not_convert=[]):
    def _should_convert_to_gguf(state_dict, prefix):
        weight_key = prefix + "weight"
        return weight_key in state_dict and isinstance(state_dict[weight_key], GGUFParameter)

    has_children = list(model.children())
    if not has_children:
        return

    for name, module in model.named_children():
        module_prefix = prefix + name + "."
        _replace_with_gguf_linear(module, compute_dtype, state_dict, module_prefix, modules_to_not_convert)
        if (
            isinstance(module, nn.Linear)
            and _should_convert_to_gguf(state_dict, module_prefix)
            and name not in modules_to_not_convert
        ):
            ctx = init_empty_weights if is_accelerate_available() else nullcontext
            with ctx():
                model._modules[name] = GGUFLinear(
                    module.in_features,
                    module.out_features,
                    module.bias is not None,
                    compute_dtype=compute_dtype,
                )
            model._modules[name].source_cls = type(module)
            # Force requires_grad to False to avoid unexpected errors
            model._modules[name].requires_grad_(False)
    return model

def _dequantize_gguf_and_restore_linear(model, modules_to_not_convert=[]):
    for name, module in model.named_children():
        if isinstance(module, GGUFLinear) and name not in modules_to_not_convert:
            device = module.weight.device
            bias = getattr(module, "bias", None)
            ctx = init_empty_weights if is_accelerate_available() else nullcontext
            with ctx():
                new_module = nn.Linear(
                    module.in_features,
                    module.out_features,
                    module.bias is not None,
                    device=device,
                )
            new_module.weight = nn.Parameter(dequantize_gguf_tensor(module.weight))
            if bias is not None:
                new_module.bias = bias
            # Create a new hook and attach it in case we use accelerate
            if hasattr(module, "_hf_hook"):
                old_hook = module._hf_hook
                new_hook = _create_accelerate_new_hook(old_hook)
                remove_hook_from_module(module)
                add_hook_to_module(new_module, new_hook)
            new_module.to(device)
            model._modules[name] = new_module
        has_children = list(module.children())
        if has_children:
            _dequantize_gguf_and_restore_linear(module, modules_to_not_convert)
    return model

SUPPORTED_GGUF_QUANT_TYPES = list(dequantize_functions.keys())

def _quant_shape_from_byte_shape(shape, type_size, block_size):
    return (*shape[:-1], shape[-1] // type_size * block_size)

def dequantize_gguf_tensor(tensor):
    if not hasattr(tensor, "quant_type"):
        return tensor
    quant_type = tensor.quant_type
    dequant_fn = dequantize_functions[quant_type]
    block_size, type_size = GGML_QUANT_SIZES[quant_type]
    tensor = tensor.view(torch.uint8)
    shape = _quant_shape_from_byte_shape(tensor.shape, type_size, block_size)
    n_blocks = tensor.numel() // type_size
    blocks = tensor.reshape((n_blocks, type_size))
    dequant = dequant_fn(blocks, block_size, type_size)
    dequant = dequant.reshape(shape)
    return dequant.as_tensor()

class GGUFParameter(torch.nn.Parameter):
    def __new__(cls, data, requires_grad=False, quant_type=None):
        data = data if data is not None else torch.empty(0)
        self = torch.Tensor._make_subclass(cls, data, requires_grad)
        self.quant_type = quant_type
        block_size, type_size = GGML_QUANT_SIZES[quant_type]
        self.quant_shape = _quant_shape_from_byte_shape(self.shape, type_size, block_size)
        return self

    def as_tensor(self):
        return torch.Tensor._make_subclass(torch.Tensor, self, self.requires_grad)

    @staticmethod
    def _extract_quant_type(args):
        # When converting from original format checkpoints we often use splits, cats etc on tensors
        # this method ensures that the returned tensor type from those operations remains GGUFParameter
        # so that we preserve quant_type information
        for arg in args:
            if isinstance(arg, list) and isinstance(arg[0], GGUFParameter):
                return arg[0].quant_type
            if isinstance(arg, GGUFParameter):
                return arg.quant_type
        return None

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        result = super().__torch_function__(func, types, args, kwargs)
        if isinstance(result, torch.Tensor):
            quant_type = cls._extract_quant_type(args)
            return cls(result, quant_type=quant_type)
        # Handle tuples and lists
        elif type(result) in (list, tuple):
            # Preserve the original type (tuple or list)
            quant_type = cls._extract_quant_type(args)
            wrapped = [cls(x, quant_type=quant_type) if isinstance(x, torch.Tensor) else x for x in result]
            return type(result)(wrapped)
        else:
            return result

class GGUFLinear(nn.Linear):
    def __init__(
        self,
        in_features,
        out_features,
        bias=False,
        compute_dtype=None,
        device=None,
    ) -> None:
        super().__init__(in_features, out_features, bias, device)
        self.compute_dtype = compute_dtype
        self.device = device

    def forward(self, inputs: torch.Tensor):
        if ops is not None and self.weight.is_cuda and inputs.is_cuda:
            return self.forward_cuda(inputs)
        return self.forward_native(inputs)

    def forward_native(self, inputs: torch.Tensor):
        weight = dequantize_gguf_tensor(self.weight)
        weight = weight.to(self.compute_dtype)
        bias = self.bias.to(self.compute_dtype) if self.bias is not None else None
        output = torch.nn.functional.linear(inputs, weight, bias)
        return output

    def forward_cuda(self, inputs: torch.Tensor):
        quant_type = self.weight.quant_type
        output = _fused_mul_mat_gguf(inputs.to(self.compute_dtype), self.weight, quant_type)
        if self.bias is not None:
            output += self.bias.to(self.compute_dtype)
        return output