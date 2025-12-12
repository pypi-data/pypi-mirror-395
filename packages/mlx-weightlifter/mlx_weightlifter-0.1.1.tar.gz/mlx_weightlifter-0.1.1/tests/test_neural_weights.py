#!/usr/bin/env python
"""Test neural_weights module for nn.Module weight loading."""

import pytest
import mlx.core as mx
import mlx.nn as nn

from mlx_weightlifter import get_parameter_dict, set_parameter, load_weights_from_dict


class SimpleModel(nn.Module):
    """Simple test model with nested structure."""

    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(10, 5)
        self.linear2 = nn.Linear(5, 2)

    def __call__(self, x):
        x = nn.relu(self.linear1(x))
        return self.linear2(x)


class NestedModel(nn.Module):
    """Model with deeper nesting for testing traversal."""

    def __init__(self):
        super().__init__()
        self.encoder = SimpleModel()
        self.decoder = nn.Linear(2, 10)

    def __call__(self, x):
        return self.decoder(self.encoder(x))


class TestGetParameterDict:
    """Test parameter extraction from modules."""

    def test_simple_model(self):
        """Test parameter extraction from simple model."""
        model = SimpleModel()
        params = get_parameter_dict(model)

        expected_keys = {"linear1.weight", "linear1.bias", "linear2.weight", "linear2.bias"}
        assert set(params.keys()) == expected_keys

    def test_nested_model(self):
        """Test parameter extraction from nested model."""
        model = NestedModel()
        params = get_parameter_dict(model)

        expected_keys = {
            "encoder.linear1.weight",
            "encoder.linear1.bias",
            "encoder.linear2.weight",
            "encoder.linear2.bias",
            "decoder.weight",
            "decoder.bias",
        }
        assert set(params.keys()) == expected_keys

    def test_sequential_model(self):
        """Test parameter extraction from nn.Sequential."""
        model = nn.Sequential(nn.Linear(10, 5), nn.Linear(5, 2))
        params = get_parameter_dict(model)

        expected_keys = {"layers.0.weight", "layers.0.bias", "layers.1.weight", "layers.1.bias"}
        assert set(params.keys()) == expected_keys


class TestSetParameter:
    """Test parameter setting in modules."""

    def test_set_simple_param(self):
        """Test setting a simple parameter."""
        model = nn.Linear(10, 5)
        new_weight = mx.zeros((5, 10))

        success = set_parameter(model, "weight", new_weight)
        assert success is True
        assert mx.array_equal(model.weight, new_weight)

    def test_set_nested_param(self):
        """Test setting a nested parameter."""
        model = NestedModel()
        new_weight = mx.ones((5, 10))

        success = set_parameter(model, "encoder.linear1.weight", new_weight)
        assert success is True
        assert mx.array_equal(model.encoder.linear1.weight, new_weight)

    def test_set_nonexistent_param(self):
        """Test setting a nonexistent parameter returns False."""
        model = nn.Linear(10, 5)

        success = set_parameter(model, "nonexistent", mx.zeros((1,)))
        assert success is False


class TestLoadWeightsFromDict:
    """Test loading weights from dictionary."""

    def test_basic_loading(self):
        """Test basic weight loading."""
        model = SimpleModel()
        weights = {
            "linear1.weight": mx.ones((5, 10)),
            "linear1.bias": mx.zeros((5,)),
            "linear2.weight": mx.ones((2, 5)),
            "linear2.bias": mx.zeros((2,)),
        }

        load_weights_from_dict(model, weights, strict=True)

        assert mx.array_equal(model.linear1.weight, mx.ones((5, 10)))
        assert mx.array_equal(model.linear1.bias, mx.zeros((5,)))

    def test_dtype_conversion(self):
        """Test dtype conversion during loading."""
        model = nn.Linear(10, 5)
        weights = {
            "weight": mx.ones((5, 10), dtype=mx.float32),
            "bias": mx.zeros((5,), dtype=mx.float32),
        }

        load_weights_from_dict(model, weights, target_dtype=mx.bfloat16)

        assert model.weight.dtype == mx.bfloat16
        assert model.bias.dtype == mx.bfloat16

    def test_strip_prefix(self):
        """Test prefix stripping during loading."""
        model = nn.Linear(10, 5)
        weights = {
            "model.weight": mx.ones((5, 10)),
            "model.bias": mx.zeros((5,)),
        }

        load_weights_from_dict(model, weights, strip_prefix="model.", strict=True)

        assert mx.array_equal(model.weight, mx.ones((5, 10)))

    def test_key_mapper(self):
        """Test custom key mapping."""
        model = nn.Linear(10, 5)
        weights = {
            "old_weight": mx.ones((5, 10)),
            "old_bias": mx.zeros((5,)),
        }

        def mapper(key):
            return key.replace("old_", "")

        load_weights_from_dict(model, weights, key_mapper=mapper, strict=True)

        assert mx.array_equal(model.weight, mx.ones((5, 10)))

    def test_strict_mode_missing_keys(self):
        """Test strict mode raises on missing keys."""
        model = SimpleModel()
        weights = {
            "linear1.weight": mx.ones((5, 10)),
            # Missing other parameters
        }

        with pytest.raises(ValueError, match="Missing.*required parameters"):
            load_weights_from_dict(model, weights, strict=True)

    def test_permissive_mode(self):
        """Test permissive mode loads partial weights."""
        model = SimpleModel()
        weights = {
            "linear1.weight": mx.ones((5, 10)),
            "linear1.bias": mx.zeros((5,)),
        }

        load_weights_from_dict(model, weights, strict=False)

        assert mx.array_equal(model.linear1.weight, mx.ones((5, 10)))

    def test_return_diagnostics(self):
        """Test diagnostic return values."""
        model = SimpleModel()
        weights = {
            "linear1.weight": mx.ones((5, 10)),
            "extra_key": mx.zeros((1,)),
        }

        missing, unexpected = load_weights_from_dict(
            model, weights, strict=False, return_diagnostics=True
        )

        assert "linear1.bias" in missing
        assert "linear2.weight" in missing
        assert "extra_key" in unexpected
