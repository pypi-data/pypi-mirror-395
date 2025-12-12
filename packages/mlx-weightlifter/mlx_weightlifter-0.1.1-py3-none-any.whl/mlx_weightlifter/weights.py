#!/usr/bin/env python
"""
Weight Loading Utilities – MLX Implementation

Generic utilities for loading pretrained weights into MLX models.
Supports various weight mapping strategies and checkpoint formats.

Features
--------
1. Flexible key mapping (prefix stripping, renaming)
2. Automatic dtype conversion
3. Nested module traversal
4. Partial loading with validation

Usage
-----
Basic weight loading::

    import mlx.core as mx
    from csm_mlx.loaders import load_weights_with_mapping

    weights = mx.load("model.npz")
    key_map = {"old.key": "new.key"}
    load_weights_with_mapping(my_model, weights, key_map)

With prefix stripping::

    from csm_mlx.loaders import load_weights_with_prefix

    load_weights_with_prefix(my_model, weights, prefix="backbone.")
"""

from typing import Dict, Callable, Optional, List, Tuple

import mlx.core as mx
import mlx.nn as nn


def load_weights_with_mapping(
    model: nn.Module,
    weights: Dict[str, mx.array],
    key_mapping: Dict[str, str],
    strict: bool = False
) -> Tuple[List[str], List[str]]:
    """Load weights into model using explicit key mapping.

    Parameters
    ----------
    model : nn.Module
        Target MLX model.
    weights : dict
        Source weight dictionary.
    key_mapping : dict
        Mapping from source keys to model parameter paths.
        Example: {"layer.0.weight": "layers.0.linear.weight"}
    strict : bool
        If True, raise error on missing weights.

    Returns
    -------
    loaded : list
        Keys that were successfully loaded.
    missing : list
        Keys in mapping that were not found in weights.

    Examples
    --------
    >>> key_map = {
    ...     "embed.weight": "embedding.weight",
    ...     "out.weight": "lm_head.weight"
    ... }
    >>> loaded, missing = load_weights_with_mapping(model, weights, key_map)
    """
    loaded = []
    missing = []

    for src_key, dst_path in key_mapping.items():
        if src_key not in weights:
            missing.append(src_key)
            if strict:
                raise KeyError(f"Weight not found: {src_key}")
            continue

        # Navigate to target parameter
        parts = dst_path.split(".")
        target = model
        for part in parts[:-1]:
            if hasattr(target, part):
                target = getattr(target, part)
            elif hasattr(target, "blocks") and part in target.blocks:
                target = target.blocks[part]
            else:
                missing.append(src_key)
                continue

        # Set the weight
        param_name = parts[-1]
        if hasattr(target, param_name):
            setattr(target, param_name, weights[src_key])
            loaded.append(src_key)
        else:
            missing.append(src_key)

    return loaded, missing


def load_weights_with_prefix(
    model: nn.Module,
    weights: Dict[str, mx.array],
    prefix: str = "",
    strip_prefix: bool = True
) -> Tuple[List[str], List[str]]:
    """Load weights by matching parameter names with optional prefix handling.

    Parameters
    ----------
    model : nn.Module
        Target MLX model.
    weights : dict
        Source weight dictionary.
    prefix : str
        Prefix to strip from or add to weight keys.
    strip_prefix : bool
        If True, strip prefix from weight keys. If False, add prefix.

    Returns
    -------
    loaded : list
        Keys that were successfully loaded.
    missing : list
        Model parameters that had no matching weight.

    Examples
    --------
    >>> # Weights have "backbone.layers.0.weight", model expects "layers.0.weight"
    >>> load_weights_with_prefix(model, weights, prefix="backbone.", strip_prefix=True)
    """
    # Get model parameters
    model_params = dict(model.parameters())

    loaded = []
    missing = []

    for param_path in model_params.keys():
        # Construct expected weight key
        if strip_prefix:
            weight_key = prefix + param_path
        else:
            weight_key = param_path[len(prefix):] if param_path.startswith(prefix) else None

        if weight_key and weight_key in weights:
            # Navigate and set
            parts = param_path.split(".")
            target = model
            for part in parts[:-1]:
                target = getattr(target, part)
            setattr(target, parts[-1], weights[weight_key])
            loaded.append(weight_key)
        else:
            missing.append(param_path)

    return loaded, missing


def load_npz_weights(
    npz_path: str,
    model: nn.Module,
    key_transform: Optional[Callable[[str], str]] = None,
    strict: bool = False
) -> Dict[str, mx.array]:
    """Load weights from NPZ file into model.

    Parameters
    ----------
    npz_path : str
        Path to .npz file.
    model : nn.Module
        Target model.
    key_transform : callable, optional
        Function to transform weight keys before matching.
    strict : bool
        If True, raise error on unmatched weights.

    Returns
    -------
    weights : dict
        The loaded weight dictionary (for inspection).

    Examples
    --------
    >>> def transform(key):
    ...     return key.replace("backbone.", "")
    >>> load_npz_weights("model.npz", model, key_transform=transform)
    """
    weights = mx.load(npz_path)

    if key_transform:
        weights = {key_transform(k): v for k, v in weights.items()}

    model_params = dict(model.parameters())

    loaded = 0
    for param_path, param in model_params.items():
        if param_path in weights:
            # Navigate and set
            parts = param_path.split(".")
            target = model
            for part in parts[:-1]:
                target = getattr(target, part)
            setattr(target, parts[-1], weights[param_path])
            loaded += 1
        elif strict:
            raise KeyError(f"Weight not found for: {param_path}")

    print(f"Loaded {loaded}/{len(model_params)} parameters from {npz_path}")

    return weights


def get_parameter_count(model: nn.Module) -> Dict[str, int]:
    """Count parameters in model by component.

    Parameters
    ----------
    model : nn.Module
        Model to analyze.

    Returns
    -------
    counts : dict
        Parameter counts by top-level module.

    Examples
    --------
    >>> counts = get_parameter_count(model)
    >>> print(f"Total: {sum(counts.values()):,}")
    """
    counts = {}
    for name, param in model.parameters().items():
        top_level = name.split(".")[0]
        size = param.size
        counts[top_level] = counts.get(top_level, 0) + size

    return counts


def verify_weights_loaded(
    model: nn.Module,
    expected_shapes: Dict[str, Tuple[int, ...]]
) -> List[str]:
    """Verify model parameters have expected shapes.

    Parameters
    ----------
    model : nn.Module
        Model to verify.
    expected_shapes : dict
        Mapping of parameter paths to expected shapes.

    Returns
    -------
    mismatches : list
        List of parameters with unexpected shapes.

    Examples
    --------
    >>> expected = {"embedding.weight": (50000, 4096)}
    >>> mismatches = verify_weights_loaded(model, expected)
    >>> assert not mismatches, f"Shape mismatches: {mismatches}"
    """
    mismatches = []

    for param_path, expected_shape in expected_shapes.items():
        parts = param_path.split(".")
        target = model
        try:
            for part in parts:
                target = getattr(target, part)
            if target.shape != expected_shape:
                mismatches.append(
                    f"{param_path}: expected {expected_shape}, got {target.shape}"
                )
        except AttributeError:
            mismatches.append(f"{param_path}: not found")

    return mismatches
