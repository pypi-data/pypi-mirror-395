#!/usr/bin/env python
"""
Direct safetensors weight loader for HuggingFace models.

Loads HuggingFace safetensors directly into MLX arrays without conversion.
Provides generic loading utilities for any model architecture.
"""

import json
from pathlib import Path
from typing import Dict

import mlx.core as mx


def load_safetensors_weights(model_dir: Path) -> Dict[str, mx.array]:
    """
    Load weights from HuggingFace safetensors (generic loader).

    Supports both single-file and sharded formats. Returns a flat dictionary
    of weight tensors that can be used with generic weight loading utilities.

    Parameters
    ----------
    model_dir : Path or str
        Path to HuggingFace model directory containing safetensors files.

    Returns
    -------
    weights : Dict[str, mx.array]
        Dictionary mapping parameter names to MLX arrays.

    Raises
    ------
    FileNotFoundError
        If no safetensors files found in model_dir.

    Examples
    --------
    >>> weights = load_safetensors_weights("path/to/model")
    >>> weights['model.layers.0.weight'].shape
    (4096, 4096)

    Notes
    -----
    - Automatically detects single-file vs sharded format
    - Uses index.json for sharded checkpoints to load all shards
    - All tensors loaded directly as MLX arrays (no NumPy conversion)
    """
    model_dir = Path(model_dir)
    print(f"Loading weights from: {model_dir}")

    # Check for single file or sharded format
    single_file = model_dir / "model.safetensors"
    index_file = model_dir / "model.safetensors.index.json"

    weights = {}

    if single_file.exists():
        # Single file format
        weights = mx.load(str(single_file))
        print(f"Loaded {len(weights)} tensors from single safetensors file")
    elif index_file.exists():
        # Sharded format
        with open(index_file) as f:
            index = json.load(f)

        shard_files = sorted(set(index["weight_map"].values()))
        print(f"Loading {len(shard_files)} shards...")

        for shard_file in shard_files:
            shard_path = model_dir / shard_file
            shard_weights = mx.load(str(shard_path))
            weights.update(shard_weights)

        print(f"Loaded {len(weights)} tensors from sharded safetensors")
    else:
        raise FileNotFoundError(f"No safetensors found in {model_dir}")

    return weights
