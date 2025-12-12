#!/usr/bin/env python
"""Test GGUF loading with mlx-weightlifter."""

import pytest
import mlx.core as mx

from mlx_weightlifter import load_gguf_with_mlx, is_gguf_file


class TestGGUFDetection:
    """Test GGUF file detection."""

    def test_is_gguf_file_valid(self, qwen3_moe_path):
        """Test that valid GGUF files are detected."""
        assert is_gguf_file(str(qwen3_moe_path)) is True

    def test_is_gguf_file_invalid(self, tmp_path):
        """Test that non-GGUF files are rejected."""
        fake_file = tmp_path / "fake.gguf"
        fake_file.write_bytes(b"not a gguf file")
        assert is_gguf_file(str(fake_file)) is False


class TestGGUFMetadata:
    """Test GGUF metadata loading."""

    def test_load_qwen3_metadata(self, qwen3_moe_path):
        """Load Qwen3-MoE GGUF and verify metadata."""
        weights, meta = mx.load(str(qwen3_moe_path), return_metadata=True)

        # Check architecture
        arch = meta.get("general.architecture")
        if hasattr(arch, "item"):
            arch = arch.item()
        assert arch == "qwen3moe"

        # Check we have weights
        assert len(weights) > 0

    def test_load_gemma3_metadata(self, gemma3_csm_path):
        """Load Gemma3-CSM GGUF and verify metadata."""
        weights, meta = mx.load(str(gemma3_csm_path), return_metadata=True)

        # Check architecture
        arch = meta.get("general.architecture")
        if hasattr(arch, "item"):
            arch = arch.item()
        assert arch == "gemma3"

        # Check we have weights
        assert len(weights) > 0


class TestGGUFModelLoading:
    """Test full GGUF model loading."""

    def test_load_qwen3moe_model(self, qwen3_moe_path):
        """Load Qwen3-MoE model and tokenizer."""
        model, tokenizer = load_gguf_with_mlx(str(qwen3_moe_path))

        # Verify model has parameters
        params = model.parameters()
        assert len(params) > 0

        # Verify tokenizer works
        tokens = tokenizer.encode("Hello, world!")
        assert len(tokens) > 0

    def test_load_gemma3_model(self, gemma3_csm_path):
        """Load Gemma3-CSM model and tokenizer."""
        model, tokenizer = load_gguf_with_mlx(str(gemma3_csm_path))

        # Verify model has parameters
        params = model.parameters()
        assert len(params) > 0

        # Verify tokenizer works
        tokens = tokenizer.encode("Hello, world!")
        assert len(tokens) > 0


class TestParameterCounting:
    """Test parameter counting utilities."""

    def _count_params(self, params):
        """Recursively count parameters in nested dict."""
        total = 0
        for v in params.values():
            if isinstance(v, dict):
                total += self._count_params(v)
            elif hasattr(v, "size"):
                total += v.size
        return total

    def test_qwen3moe_param_count(self, qwen3_moe_path):
        """Verify Qwen3-MoE has expected parameter count."""
        model, _ = load_gguf_with_mlx(str(qwen3_moe_path))
        total_params = self._count_params(model.parameters())

        # Qwen3-Coder-30B-A3B should have ~30B params
        assert total_params > 20_000_000_000
        assert total_params < 40_000_000_000

    def test_gemma3_param_count(self, gemma3_csm_path):
        """Verify Gemma3-CSM has expected parameter count."""
        model, _ = load_gguf_with_mlx(str(gemma3_csm_path))
        total_params = self._count_params(model.parameters())

        # Gemma3-12B-CSM should have ~12B params
        assert total_params > 5_000_000_000
        assert total_params < 20_000_000_000
