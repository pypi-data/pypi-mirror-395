#!/usr/bin/env python
"""
Configuration Loader – MLX Implementation (HuggingFace Config Parsing)

Overview
--------
Loads model configuration from HuggingFace-style `config.json` files
and provides utilities for dimension computation and config manipulation.

This module bridges the gap between:
  - HuggingFace checkpoint format (config.json with base hyperparameters)
  - Runtime model instantiation (needs computed dimensions)

Features
--------
1. Load config.json from model directories
2. Compute derived dimensions with proper rounding
3. Fill missing defaults for inference mode
4. Load sharded safetensors checkpoints

Dimension Computation
---------------------
Many models store dimension factors rather than raw dimensions. This loader
computes derived dimensions with proper alignment:

  raw_dim = int(base_dim * factor)
  aligned_dim = round_up(raw_dim, alignment)  # e.g., 64 for SIMD

Usage
-----
Basic loading::

    from csm_mlx.loaders import load_config

    config = load_config("path/to/model")
    print(config['hidden_size'])

Load safetensor shards::

    from csm_mlx.loaders import load_safetensor_shards

    weights = load_safetensor_shards("path/to/model")
    # Use with generic weight loader
"""

import json
from pathlib import Path
from typing import Any, Dict, Tuple

import mlx.core as mx


def round_up_to_multiple(value: int, multiple_of: int) -> int:
    """Round value up to nearest multiple.

    Useful for aligning dimensions to hardware SIMD widths or
    ensuring compatibility with quantized weight shapes.

    Parameters
    ----------
    value : int
        Raw dimension value.
    multiple_of : int
        Alignment boundary (typically 64 for SIMD/safetensors).

    Returns
    -------
    rounded : int
        Value rounded up to nearest multiple.

    Examples
    --------
    >>> round_up_to_multiple(2048, 64)
    2048
    >>> round_up_to_multiple(2050, 64)
    2112
    """
    if multiple_of <= 0:
        return value
    return ((value + multiple_of - 1) // multiple_of) * multiple_of


def load_config(model_path: str) -> Dict[str, Any]:
    """Load model configuration from HuggingFace model directory.

    Reads config.json and returns it as a dictionary. Does not modify
    the config - use compute_derived_dims() for dimension computation.

    Parameters
    ----------
    model_path : str
        Path to model directory containing config.json, or direct path
        to a config.json file.

    Returns
    -------
    config : dict
        Raw configuration dictionary from config.json.

    Raises
    ------
    FileNotFoundError
        If config.json not found in model_path.

    Examples
    --------
    >>> config = load_config("path/to/model")
    >>> config['hidden_size']
    4096
    """
    config_path = Path(model_path)
    if config_path.is_dir():
        config_path /= "config.json"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config = json.load(f)

    return config


def compute_derived_dims(
    config: Dict[str, Any],
    dim_factors: Dict[str, Tuple[str, str]] = None,
    round_multiple: int = 64
) -> Dict[str, Any]:
    """Compute derived dimensions from base config.

    Many model configs specify dimension factors (e.g., qk_dim_factor=0.5)
    rather than absolute dimensions. This function computes the actual
    dimensions with proper alignment.

    Parameters
    ----------
    config : dict
        Base configuration with dimension factors.
    dim_factors : dict, optional
        Mapping of {output_key: (base_key, factor_key)}.
        Example: {'qk_dim': ('embedding_dim', 'qk_dim_factor')}
    round_multiple : int
        Alignment boundary for computed dimensions.

    Returns
    -------
    config : dict
        Config with computed dimensions added.

    Examples
    --------
    >>> config = {'embedding_dim': 4096, 'qk_dim_factor': 0.5}
    >>> config = compute_derived_dims(
    ...     config,
    ...     dim_factors={'qk_dim': ('embedding_dim', 'qk_dim_factor')}
    ... )
    >>> config['qk_dim']
    2048
    """
    if dim_factors is None:
        return config

    result = config.copy()

    for output_key, (base_key, factor_key) in dim_factors.items():
        if base_key in config and factor_key in config:
            base_dim = config[base_key]
            factor = config[factor_key]
            raw_dim = int(base_dim * factor)
            result[output_key] = round_up_to_multiple(raw_dim, round_multiple)

    return result


def load_safetensor_shards(
    model_path: str,
    index_filename: str = "model.safetensors.index.json"
) -> Dict[str, mx.array]:
    """Load sharded safetensors checkpoint into a flat dictionary.

    HuggingFace large models are often split across multiple .safetensors
    files with an index.json that maps tensor names to shard files.

    Parameters
    ----------
    model_path : str
        Directory containing model.safetensors.* files.
    index_filename : str
        Name of the shard index file.

    Returns
    -------
    tensors : dict
        Mapping of tensor names to MLX arrays.

    Raises
    ------
    FileNotFoundError
        If index file or any shard file is missing.

    Examples
    --------
    >>> weights = load_safetensor_shards("path/to/model")
    >>> weights['model.layers.0.self_attn.q_proj.weight'].shape
    (4096, 4096)
    """
    model_dir = Path(model_path)
    index_path = model_dir / index_filename

    if not index_path.exists():
        # Try single-file checkpoint
        single_file = model_dir / "model.safetensors"
        if single_file.exists():
            return mx.load(str(single_file), return_metadata=False)
        raise FileNotFoundError(f"Safetensors index not found: {index_path}")

    with open(index_path) as f:
        index = json.load(f)

    weight_map = index.get("weight_map", {})
    shard_files = sorted(set(weight_map.values()))

    if not shard_files:
        raise FileNotFoundError(f"No shard entries listed in {index_path}")

    tensors: Dict[str, mx.array] = {}
    for shard in shard_files:
        shard_path = model_dir / shard
        if not shard_path.exists():
            raise FileNotFoundError(f"Shard file missing: {shard_path}")
        shard_data = mx.load(str(shard_path), return_metadata=False)
        tensors.update(shard_data)

    return tensors


# Backward compatibility alias
_round_up = round_up_to_multiple
