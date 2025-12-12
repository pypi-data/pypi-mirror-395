#!/usr/bin/env python
"""
GGUF loader for MLX with mlx-lm model support.

Supports multiple architectures by detecting from GGUF metadata and
dispatching to the appropriate mlx-lm model class.
"""

import os
import re
from typing import Any, Dict, Optional, Tuple

import mlx.core as mx
import mlx.nn as nn


def is_gguf_file(path: str) -> bool:
    """Check if a file is GGUF by reading magic bytes."""
    if not os.path.isfile(path):
        return False
    try:
        with open(path, 'rb') as f:
            magic = f.read(4)
            return magic == b'GGUF'
    except:
        return False


def _meta_int(meta: Dict, name: str) -> int:
    """Extract integer from GGUF metadata."""
    v = meta[name]
    return int(v.item()) if hasattr(v, 'item') else int(v)


def _meta_float(meta: Dict, name: str) -> float:
    """Extract float from GGUF metadata."""
    v = meta[name]
    return float(v.item()) if hasattr(v, 'item') else float(v)


def _meta_str(meta: Dict, name: str) -> str:
    """Extract string from GGUF metadata."""
    v = meta.get(name, "")
    if hasattr(v, 'item'):
        return str(v.item())
    return str(v)


def get_architecture(meta: Dict) -> str:
    """Detect model architecture from GGUF metadata."""
    arch = meta.get("general.architecture", "")
    if hasattr(arch, 'item'):
        arch = arch.item()
    return str(arch).lower()


# =============================================================================
# Architecture-specific loaders
# =============================================================================

def load_qwen3moe(weights: Dict, meta: Dict) -> Tuple[nn.Module, Dict]:
    """Load Qwen3-MoE model from GGUF weights."""
    from mlx_lm.models.qwen3_moe import Model, ModelArgs

    # Extract config from metadata
    config = ModelArgs(
        model_type="qwen3_moe",
        hidden_size=_meta_int(meta, "qwen3moe.embedding_length"),
        num_hidden_layers=_meta_int(meta, "qwen3moe.block_count"),
        intermediate_size=_meta_int(meta, "qwen3moe.feed_forward_length"),
        num_attention_heads=_meta_int(meta, "qwen3moe.attention.head_count"),
        num_key_value_heads=_meta_int(meta, "qwen3moe.attention.head_count_kv"),
        head_dim=_meta_int(meta, "qwen3moe.attention.key_length"),
        rms_norm_eps=_meta_float(meta, "qwen3moe.attention.layer_norm_rms_epsilon"),
        vocab_size=len(meta.get("tokenizer.ggml.tokens", [])),
        rope_theta=_meta_float(meta, "qwen3moe.rope.freq_base"),
        num_experts=_meta_int(meta, "qwen3moe.expert_count"),
        num_experts_per_tok=_meta_int(meta, "qwen3moe.expert_used_count"),
        moe_intermediate_size=_meta_int(meta, "qwen3moe.expert_feed_forward_length"),
        # Required fields with sensible defaults
        decoder_sparse_step=1,  # Every layer is MoE
        mlp_only_layers=[],  # No dense-only layers
        tie_word_embeddings=False,
        max_position_embeddings=_meta_int(meta, "qwen3moe.context_length"),
        norm_topk_prob=True,
    )

    print(f"    Qwen3-MoE: {config.num_hidden_layers} layers, {config.hidden_size}D, "
          f"{config.num_experts} experts ({config.num_experts_per_tok} active)")

    model = Model(config)

    # Map weights
    mapped = map_qwen3moe_weights(weights, config)

    return model, mapped


def map_qwen3moe_weights(weights: Dict, config) -> Dict[str, mx.array]:
    """Map GGUF weight names to mlx-lm Qwen3-MoE parameter names."""
    mapped = {}

    for gguf_key, tensor in weights.items():
        mlx_key = None

        # Global weights
        if gguf_key == "token_embd.weight":
            mlx_key = "model.embed_tokens.weight"
        elif gguf_key == "output_norm.weight":
            mlx_key = "model.norm.weight"
        elif gguf_key == "output.weight":
            mlx_key = "lm_head.weight"

        # Layer weights
        m = re.match(r"blk\.(\d+)\.(.+)", gguf_key)
        if m:
            layer_idx, rest = m.groups()
            prefix = f"model.layers.{layer_idx}"

            # Attention
            if rest == "attn_q.weight":
                mlx_key = f"{prefix}.self_attn.q_proj.weight"
            elif rest == "attn_k.weight":
                mlx_key = f"{prefix}.self_attn.k_proj.weight"
            elif rest == "attn_v.weight":
                mlx_key = f"{prefix}.self_attn.v_proj.weight"
            elif rest == "attn_output.weight":
                mlx_key = f"{prefix}.self_attn.o_proj.weight"
            elif rest == "attn_q_norm.weight":
                mlx_key = f"{prefix}.self_attn.q_norm.weight"
            elif rest == "attn_k_norm.weight":
                mlx_key = f"{prefix}.self_attn.k_norm.weight"
            elif rest == "attn_norm.weight":
                mlx_key = f"{prefix}.input_layernorm.weight"
            elif rest == "ffn_norm.weight":
                mlx_key = f"{prefix}.post_attention_layernorm.weight"

            # MoE gate
            elif rest == "ffn_gate_inp.weight":
                mlx_key = f"{prefix}.mlp.gate.weight"

            # MoE experts - consolidated tensors need expansion
            elif rest == "ffn_gate_exps.weight":
                # Shape: [num_experts, intermediate, hidden]
                # Need to expand to per-expert weights
                for e in range(tensor.shape[0]):
                    mapped[f"{prefix}.mlp.experts.{e}.gate_proj.weight"] = tensor[e]
                continue
            elif rest == "ffn_up_exps.weight":
                for e in range(tensor.shape[0]):
                    mapped[f"{prefix}.mlp.experts.{e}.up_proj.weight"] = tensor[e]
                continue
            elif rest == "ffn_down_exps.weight":
                for e in range(tensor.shape[0]):
                    mapped[f"{prefix}.mlp.experts.{e}.down_proj.weight"] = tensor[e]
                continue

            # Non-MoE FFN (some layers might be dense)
            elif rest == "ffn_gate.weight":
                mlx_key = f"{prefix}.mlp.gate_proj.weight"
            elif rest == "ffn_up.weight":
                mlx_key = f"{prefix}.mlp.up_proj.weight"
            elif rest == "ffn_down.weight":
                mlx_key = f"{prefix}.mlp.down_proj.weight"

        if mlx_key:
            mapped[mlx_key] = tensor

    return mapped


def load_qwen3(weights: Dict, meta: Dict) -> Tuple[nn.Module, Dict]:
    """Load Qwen3 (dense) model from GGUF weights."""
    from mlx_lm.models.qwen3 import Model, ModelArgs

    config = ModelArgs(
        model_type="qwen3",
        hidden_size=_meta_int(meta, "qwen3.embedding_length"),
        num_hidden_layers=_meta_int(meta, "qwen3.block_count"),
        intermediate_size=_meta_int(meta, "qwen3.feed_forward_length"),
        num_attention_heads=_meta_int(meta, "qwen3.attention.head_count"),
        num_key_value_heads=_meta_int(meta, "qwen3.attention.head_count_kv"),
        head_dim=_meta_int(meta, "qwen3.attention.key_length"),
        rms_norm_eps=_meta_float(meta, "qwen3.attention.layer_norm_rms_epsilon"),
        vocab_size=len(meta.get("tokenizer.ggml.tokens", [])),
        rope_theta=_meta_float(meta, "qwen3.rope.freq_base"),
    )

    print(f"    Qwen3: {config.num_hidden_layers} layers, {config.hidden_size}D")

    model = Model(config)
    mapped = map_qwen3_weights(weights)

    return model, mapped


def map_qwen3_weights(weights: Dict) -> Dict[str, mx.array]:
    """Map GGUF weight names to mlx-lm Qwen3 parameter names."""
    mapped = {}

    for gguf_key, tensor in weights.items():
        mlx_key = None

        if gguf_key == "token_embd.weight":
            mlx_key = "model.embed_tokens.weight"
        elif gguf_key == "output_norm.weight":
            mlx_key = "model.norm.weight"
        elif gguf_key == "output.weight":
            mlx_key = "lm_head.weight"

        m = re.match(r"blk\.(\d+)\.(.+)", gguf_key)
        if m:
            layer_idx, rest = m.groups()
            prefix = f"model.layers.{layer_idx}"

            if rest == "attn_q.weight":
                mlx_key = f"{prefix}.self_attn.q_proj.weight"
            elif rest == "attn_k.weight":
                mlx_key = f"{prefix}.self_attn.k_proj.weight"
            elif rest == "attn_v.weight":
                mlx_key = f"{prefix}.self_attn.v_proj.weight"
            elif rest == "attn_output.weight":
                mlx_key = f"{prefix}.self_attn.o_proj.weight"
            elif rest == "attn_q_norm.weight":
                mlx_key = f"{prefix}.self_attn.q_norm.weight"
            elif rest == "attn_k_norm.weight":
                mlx_key = f"{prefix}.self_attn.k_norm.weight"
            elif rest == "attn_norm.weight":
                mlx_key = f"{prefix}.input_layernorm.weight"
            elif rest == "ffn_norm.weight":
                mlx_key = f"{prefix}.post_attention_layernorm.weight"
            elif rest == "ffn_gate.weight":
                mlx_key = f"{prefix}.mlp.gate_proj.weight"
            elif rest == "ffn_up.weight":
                mlx_key = f"{prefix}.mlp.up_proj.weight"
            elif rest == "ffn_down.weight":
                mlx_key = f"{prefix}.mlp.down_proj.weight"

        if mlx_key:
            mapped[mlx_key] = tensor

    return mapped


def load_gemma3(weights: Dict, meta: Dict) -> Tuple[nn.Module, Dict]:
    """Load Gemma3 model from GGUF weights."""
    from mlx_lm.models.gemma3_text import Model, ModelArgs

    head_dim = _meta_int(meta, "gemma3.attention.key_length")
    config = ModelArgs(
        model_type="gemma3_text",
        hidden_size=_meta_int(meta, "gemma3.embedding_length"),
        intermediate_size=_meta_int(meta, "gemma3.feed_forward_length"),
        num_hidden_layers=_meta_int(meta, "gemma3.block_count"),
        num_attention_heads=_meta_int(meta, "gemma3.attention.head_count"),
        num_key_value_heads=_meta_int(meta, "gemma3.attention.head_count_kv"),
        head_dim=head_dim,
        query_pre_attn_scalar=head_dim,
        vocab_size=262208,
        rms_norm_eps=1e-6,
        sliding_window=_meta_int(meta, "gemma3.attention.sliding_window"),
        rope_global_base_freq=_meta_float(meta, "gemma3.rope.freq_base"),
    )

    print(f"    Gemma3: {config.num_hidden_layers} layers, {config.hidden_size}D")

    model = Model(config)
    mapped = map_gemma3_weights(weights)

    return model, mapped


def map_gemma3_weights(weights: Dict) -> Dict[str, mx.array]:
    """Map GGUF weight names to mlx-lm Gemma3 parameter names."""
    mapped = {}

    for gguf_key, tensor in weights.items():
        mlx_key = None

        if gguf_key == "token_embd.weight":
            mlx_key = "model.embed_tokens.weight"
        elif gguf_key == "output_norm.weight":
            mlx_key = "model.norm.weight"
        elif gguf_key == "output.weight":
            mlx_key = "lm_head.weight"

        m = re.match(r"blk\.(\d+)\.(.+)", gguf_key)
        if m:
            layer_idx, rest = m.groups()
            prefix = f"model.layers.{layer_idx}"

            if rest == "attn_q.weight":
                mlx_key = f"{prefix}.self_attn.q_proj.weight"
            elif rest == "attn_k.weight":
                mlx_key = f"{prefix}.self_attn.k_proj.weight"
            elif rest == "attn_v.weight":
                mlx_key = f"{prefix}.self_attn.v_proj.weight"
            elif rest == "attn_output.weight":
                mlx_key = f"{prefix}.self_attn.o_proj.weight"
            elif rest == "attn_q_norm.weight":
                mlx_key = f"{prefix}.self_attn.q_norm.weight"
            elif rest == "attn_k_norm.weight":
                mlx_key = f"{prefix}.self_attn.k_norm.weight"
            elif rest == "attn_norm.weight":
                mlx_key = f"{prefix}.input_layernorm.weight"
            elif rest == "post_attention_norm.weight":
                mlx_key = f"{prefix}.post_attention_layernorm.weight"
            elif rest == "ffn_norm.weight":
                mlx_key = f"{prefix}.pre_feedforward_layernorm.weight"
            elif rest == "post_ffw_norm.weight":
                mlx_key = f"{prefix}.post_feedforward_layernorm.weight"
            elif rest == "ffn_gate.weight":
                mlx_key = f"{prefix}.mlp.gate_proj.weight"
            elif rest == "ffn_up.weight":
                mlx_key = f"{prefix}.mlp.up_proj.weight"
            elif rest == "ffn_down.weight":
                mlx_key = f"{prefix}.mlp.down_proj.weight"

        if mlx_key:
            mapped[mlx_key] = tensor

    return mapped


def load_llama(weights: Dict, meta: Dict) -> Tuple[nn.Module, Dict]:
    """Load Llama model from GGUF weights."""
    from mlx_lm.models.llama import Model, ModelArgs

    config = ModelArgs(
        model_type="llama",
        hidden_size=_meta_int(meta, "llama.embedding_length"),
        num_hidden_layers=_meta_int(meta, "llama.block_count"),
        intermediate_size=_meta_int(meta, "llama.feed_forward_length"),
        num_attention_heads=_meta_int(meta, "llama.attention.head_count"),
        num_key_value_heads=_meta_int(meta, "llama.attention.head_count_kv"),
        rms_norm_eps=_meta_float(meta, "llama.attention.layer_norm_rms_epsilon"),
        vocab_size=len(meta.get("tokenizer.ggml.tokens", [])),
        rope_theta=_meta_float(meta, "llama.rope.freq_base"),
    )

    print(f"    Llama: {config.num_hidden_layers} layers, {config.hidden_size}D")

    model = Model(config)
    mapped = map_llama_weights(weights)

    return model, mapped


def map_llama_weights(weights: Dict) -> Dict[str, mx.array]:
    """Map GGUF weight names to mlx-lm Llama parameter names."""
    mapped = {}

    for gguf_key, tensor in weights.items():
        mlx_key = None

        if gguf_key == "token_embd.weight":
            mlx_key = "model.embed_tokens.weight"
        elif gguf_key == "output_norm.weight":
            mlx_key = "model.norm.weight"
        elif gguf_key == "output.weight":
            mlx_key = "lm_head.weight"

        m = re.match(r"blk\.(\d+)\.(.+)", gguf_key)
        if m:
            layer_idx, rest = m.groups()
            prefix = f"model.layers.{layer_idx}"

            if rest == "attn_q.weight":
                mlx_key = f"{prefix}.self_attn.q_proj.weight"
            elif rest == "attn_k.weight":
                mlx_key = f"{prefix}.self_attn.k_proj.weight"
            elif rest == "attn_v.weight":
                mlx_key = f"{prefix}.self_attn.v_proj.weight"
            elif rest == "attn_output.weight":
                mlx_key = f"{prefix}.self_attn.o_proj.weight"
            elif rest == "attn_norm.weight":
                mlx_key = f"{prefix}.input_layernorm.weight"
            elif rest == "ffn_norm.weight":
                mlx_key = f"{prefix}.post_attention_layernorm.weight"
            elif rest == "ffn_gate.weight":
                mlx_key = f"{prefix}.mlp.gate_proj.weight"
            elif rest == "ffn_up.weight":
                mlx_key = f"{prefix}.mlp.up_proj.weight"
            elif rest == "ffn_down.weight":
                mlx_key = f"{prefix}.mlp.down_proj.weight"

        if mlx_key:
            mapped[mlx_key] = tensor

    return mapped


# =============================================================================
# Main loader
# =============================================================================

# Architecture dispatch table
ARCH_LOADERS = {
    "qwen3moe": load_qwen3moe,
    "qwen3": load_qwen3,
    "gemma3": load_gemma3,
    "llama": load_llama,
}


class GGUFTokenizer:
    """
    Tokenizer built from GGUF metadata.

    Implements the minimal interface needed for mlx-lm.generate().
    """

    def __init__(self, meta: Dict):
        """Build tokenizer from GGUF metadata."""
        # Extract vocab
        tokens = meta.get("tokenizer.ggml.tokens", [])
        if not tokens:
            raise ValueError("No tokenizer.ggml.tokens in GGUF metadata")

        # Convert to strings
        self._vocab = []
        for tok in tokens:
            if hasattr(tok, 'tolist'):
                self._vocab.append(bytes(tok.tolist()).decode('utf-8', errors='replace'))
            elif isinstance(tok, bytes):
                self._vocab.append(tok.decode('utf-8', errors='replace'))
            else:
                self._vocab.append(str(tok))

        self._token_to_id = {tok: i for i, tok in enumerate(self._vocab)}

        # Extract merges for BPE
        merges = meta.get("tokenizer.ggml.merges", [])
        self._merges = []
        for merge in merges:
            if hasattr(merge, 'tolist'):
                merge_str = bytes(merge.tolist()).decode('utf-8', errors='replace')
            elif isinstance(merge, bytes):
                merge_str = merge.decode('utf-8', errors='replace')
            else:
                merge_str = str(merge)
            parts = merge_str.split()
            if len(parts) == 2:
                self._merges.append(tuple(parts))

        self._bpe_ranks = {merge: i for i, merge in enumerate(self._merges)}

        # Special tokens
        self._eos_id = meta.get("tokenizer.ggml.eos_token_id", 0)
        if hasattr(self._eos_id, 'item'):
            self._eos_id = self._eos_id.item()

        self._bos_id = meta.get("tokenizer.ggml.bos_token_id", None)
        if self._bos_id is not None and hasattr(self._bos_id, 'item'):
            self._bos_id = self._bos_id.item()

        self._pad_id = meta.get("tokenizer.ggml.padding_token_id", None)
        if self._pad_id is not None and hasattr(self._pad_id, 'item'):
            self._pad_id = self._pad_id.item()

        print(f"    Tokenizer: {len(self._vocab)} tokens, {len(self._merges)} merges")

    def _get_pairs(self, word: tuple) -> set:
        """Get adjacent pairs in word."""
        pairs = set()
        prev = word[0]
        for char in word[1:]:
            pairs.add((prev, char))
            prev = char
        return pairs

    def _bpe(self, token: str) -> list:
        """Apply BPE to token."""
        if not self._merges:
            return list(token)

        word = tuple(token)
        pairs = self._get_pairs(word)

        if not pairs:
            return [token]

        while True:
            bigram = min(pairs, key=lambda p: self._bpe_ranks.get(p, float('inf')))
            if bigram not in self._bpe_ranks:
                break

            first, second = bigram
            new_word = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except ValueError:
                    new_word.extend(word[i:])
                    break

                if i < len(word) - 1 and word[i] == first and word[i + 1] == second:
                    new_word.append(first + second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1

            word = tuple(new_word)
            if len(word) == 1:
                break
            pairs = self._get_pairs(word)

        return list(word)

    def encode(self, text: str) -> list:
        """Encode text to token IDs."""
        tokens = []
        # Pre-tokenize on whitespace, preserving spaces as part of tokens
        import re
        # Split keeping spaces attached to following word (like GPT-2)
        words = re.findall(r'\s*\S+', text)
        if not words and text:
            words = [text]

        for word in words:
            bpe_tokens = self._bpe(word)
            for tok in bpe_tokens:
                if tok in self._token_to_id:
                    tokens.append(self._token_to_id[tok])
                else:
                    # Byte fallback
                    for byte in tok.encode('utf-8'):
                        byte_tok = f'<0x{byte:02X}>'
                        if byte_tok in self._token_to_id:
                            tokens.append(self._token_to_id[byte_tok])

        return tokens

    def decode(self, ids: list) -> str:
        """Decode token IDs to text."""
        tokens = []
        for id in ids:
            if 0 <= id < len(self._vocab):
                tokens.append(self._vocab[id])
        return ''.join(tokens)

    @property
    def eos_token_id(self) -> int:
        return self._eos_id

    @property
    def bos_token_id(self):
        return self._bos_id

    @property
    def pad_token_id(self):
        return self._pad_id

    @property
    def vocab_size(self) -> int:
        return len(self._vocab)


def load_gguf_with_mlx(gguf_path: str) -> Tuple[nn.Module, Any]:
    """
    Load a GGUF file and wrap it for mlx-lm compatibility.

    Args:
        gguf_path: Path to GGUF file (with or without .gguf extension)

    Returns:
        (model, tokenizer) compatible with mlx-lm.generate()
    """
    # Load weights and metadata
    print(f"Loading GGUF: {gguf_path}")
    weights, meta = mx.load(gguf_path, return_metadata=True)
    print(f"    Loaded {len(weights)} tensors")

    # Detect architecture
    arch = get_architecture(meta)
    print(f"    Architecture: {arch}")

    if arch not in ARCH_LOADERS:
        raise ValueError(
            f"Unsupported architecture: {arch}\n"
            f"Supported: {list(ARCH_LOADERS.keys())}"
        )

    # Load model using architecture-specific loader
    model, mapped_weights = ARCH_LOADERS[arch](weights, meta)

    # Handle weight tying
    if "lm_head.weight" not in mapped_weights and "model.embed_tokens.weight" in mapped_weights:
        print(f"    Using weight tying: lm_head.weight = embed_tokens.weight")
        mapped_weights["lm_head.weight"] = mapped_weights["model.embed_tokens.weight"]

    print(f"    Mapped {len(mapped_weights)}/{len(weights)} tensors")

    # Load weights into model
    weight_list = list(mapped_weights.items())
    model.load_weights(weight_list, strict=False)
    print(f"    Model weights loaded")

    # Build tokenizer from GGUF metadata
    tokenizer = GGUFTokenizer(meta)

    return model, tokenizer


def patched_load(path_or_hf_repo: str, **kwargs) -> Tuple[nn.Module, Any]:
    """
    Patched version of mlx_lm.load() that handles GGUF files.

    GGUF ONLY - no fallback. Fail hard if not GGUF.
    """
    if not is_gguf_file(path_or_hf_repo):
        raise ValueError(
            f"Expected GGUF file, got: {path_or_hf_repo}\n"
            f"This loader only supports raw GGUF files. "
            f"Check that the file exists and has GGUF magic bytes."
        )

    return load_gguf_with_mlx(path_or_hf_repo)


def install_gguf_support():
    """
    Monkeypatch mlx_lm.utils.load() and mlx_lm.load() to add GGUF support.

    Call this before using mlx-lm.load() or mlx-lm.generate().
    """
    import mlx_lm.utils

    mlx_lm.utils.load = patched_load
    mlx_lm.load = patched_load

    print("Installed GGUF loader for mlx-lm")
