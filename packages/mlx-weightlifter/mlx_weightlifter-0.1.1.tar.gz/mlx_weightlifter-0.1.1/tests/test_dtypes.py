#!/usr/bin/env python
"""Test dtype resolution utilities."""

import mlx.core as mx

from mlx_weightlifter import resolve_dtype


class TestResolveDtype:
    """Test dtype string to MLX dtype resolution."""

    def test_resolve_float32(self):
        """Test float32 resolution."""
        assert resolve_dtype("float32") == mx.float32

    def test_resolve_float16(self):
        """Test float16 resolution."""
        assert resolve_dtype("float16") == mx.float16
        assert resolve_dtype("fp16") == mx.float16

    def test_resolve_bfloat16(self):
        """Test bfloat16 resolution."""
        assert resolve_dtype("bfloat16") == mx.bfloat16
        assert resolve_dtype("bf16") == mx.bfloat16

    def test_resolve_none_uses_default(self):
        """Test that None uses default dtype."""
        assert resolve_dtype(None) == mx.float32
        assert resolve_dtype(None, default="bfloat16") == mx.bfloat16

    def test_resolve_unknown_uses_default(self):
        """Test that unknown dtypes fall back to default."""
        assert resolve_dtype("unknown_dtype") == mx.float32
        assert resolve_dtype("invalid", default="float16") == mx.float16

    def test_case_insensitive(self):
        """Test that dtype resolution is case-insensitive."""
        assert resolve_dtype("FLOAT32") == mx.float32
        assert resolve_dtype("BFloat16") == mx.bfloat16
