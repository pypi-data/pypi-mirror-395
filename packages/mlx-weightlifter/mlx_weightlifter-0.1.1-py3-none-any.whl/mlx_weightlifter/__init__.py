#!/usr/bin/env python
"""
Weightlifter - Lift any checkpoint into MLX.

Supports:
- PyTorch (.pt, .bin, .jit)
- Safetensors (.safetensors)
- GGUF (.gguf) with auto architecture detection

Modules
-------
- pytorch: Load PyTorch .pt/.bin/.jit files
- safetensors: Load HuggingFace safetensors files
- gguf: Load GGUF quantized models
- config: Configuration loading and dimension computation
- weights: Weight loading utilities with key mapping
- neural_weights: Universal nn.Module parameter loading
- dtypes: Dtype string to MLX dtype mapping
"""

# Format-specific loaders
from .gguf import load_gguf_with_mlx, is_gguf_file, install_gguf_support
from .pytorch import load_pytorch_bin, load_jit
from .safetensors import load_safetensors_weights

# Configuration utilities
from .config import (
    load_config,
    load_safetensor_shards,
    compute_derived_dims,
    round_up_to_multiple,
)

# Generic weight loading
from .weights import (
    load_weights_with_mapping,
    load_weights_with_prefix,
    load_npz_weights,
    get_parameter_count,
    verify_weights_loaded,
)

# nn.Module weight loading
from .neural_weights import (
    get_parameter_dict,
    set_parameter,
    load_weights_from_dict,
    load_weights_from_safetensors,
)

# Dtype utilities
from .dtypes import resolve_dtype

# Config inference
from .infer_checkpoint import infer_config_from_checkpoint
from .infer_safetensors import infer_config_from_safetensors

__version__ = "0.1.0"

__all__ = [
    # Format loaders
    "load_pytorch_bin",
    "load_jit",
    "load_safetensors_weights",
    "load_gguf_with_mlx",
    "is_gguf_file",
    "install_gguf_support",
    # Config utilities
    "load_config",
    "load_safetensor_shards",
    "compute_derived_dims",
    "round_up_to_multiple",
    # Weight loading with mapping
    "load_weights_with_mapping",
    "load_weights_with_prefix",
    "load_npz_weights",
    "get_parameter_count",
    "verify_weights_loaded",
    # Generic nn.Module loading
    "get_parameter_dict",
    "set_parameter",
    "load_weights_from_dict",
    "load_weights_from_safetensors",
    # Dtype utilities
    "resolve_dtype",
    # Config inference
    "infer_config_from_checkpoint",
    "infer_config_from_safetensors",
]
