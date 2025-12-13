import json
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from typing import List, Literal, Optional, Dict, Any

from mizan_encoder.encoder import MizanTextEncoder       # Custom-trained model
from mizan_encoder.hf_model import MizanEncoderHF        # HF-compatible model


PoolingType = Literal["mean", "cls", "max", "balanced"]


# ============================================================================
#                       Utility: Safe Pooling Function
# ============================================================================
def safe_pool(last_hidden_state, attention_mask, mode="mean"):
    """
    Supports mean / max / cls / balanced pooling.
    Works even if the encoder returns only embeddings (no hidden states).
    """
    if len(last_hidden_state.shape) == 2:
        # Direct embeddings (already pooled)
        return last_hidden_state

    mask = attention_mask.unsqueeze(-1).float()
    
    if mode in ("mean", "balanced", "balanced-mean"):
        summed = (last_hidden_state * mask).sum(dim=1)
        counts = mask.sum(dim=1).clamp(min=1e-8)
        return summed / counts

    if mode == "cls":
        return last_hidden_state[:, 0, :]

    if mode == "max":
        replaced = last_hidden_state.masked_fill(mask == 0, -1e9)
        return replaced.max(dim=1).values

    raise ValueError(f"Unknown pooling method: {mode}")


# ============================================================================
#                  Fallback HF Embedding Model (generic)
# ============================================================================
class HFEmbeddingModel(nn.Module):
    """
    Generic HF model used when backbone_name = "MiniLM", "bge", "mpnet", etc.
    """
    def __init__(self, backbone_name, emb_dim=384, pooling="mean", normalize=True):
        super().__init__()
        self.backbone_name = backbone_name
        self.transformer = AutoModel.from_pretrained(backbone_name)
        
        hidden = self.transformer.config.hidden_size
        self.proj = nn.Linear(hidden, emb_dim)
        self.pooling = pooling
        self.normalize = normalize

    def forward(self, input_ids, attention_mask):
        out = self.transformer(input_ids=input_ids, attention_mask=attention_mask)

        # HF models always return last_hidden_state
        pooled = safe_pool(out.last_hidden_state, attention_mask, self.pooling)
        emb = self.proj(pooled)

        if self.normalize:
            emb = F.normalize(emb, dim=-1)

        return emb


# ============================================================================
#               UNIVERSAL Mizan Encoder Wrapper (Final Version)
# ============================================================================
class MizanTextEncoderWrapper:
    """
    ✔ Loads ALL encoder types:
        - Your custom MizanTextEncoder (50k model)
        - HF-compatible MizanEncoderHF
        - Normal HuggingFace models (BGE, MiniLM, E5, MPNet)
        - Any future Mizan encoder architecture

    ✔ Auto-detects structures
    ✔ Normalizes everything into a single "model(**enc)" interface
    ✔ Caching included
    """

    def __init__(
        self,
        backbone_name: str,
        emb_dim: int = 384,
        pooling: PoolingType = "balanced-mean",
        normalize: bool = True,
        cache: Optional[Dict[str, torch.Tensor]] = None,
        device: Optional[str] = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.cache = cache

        # ==========================================================
        # CASE 1 — LOCAL DIRECTORY (custom Mizan encoder)
        # ==========================================================
        if os.path.isdir(backbone_name):
            config_path = os.path.join(backbone_name, "config.json")

            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    cfg = json.load(f)

                # Detect model type
                if cfg.get("model_type") == "mizan-encoder":
                    print("🔵 Loading HF-style MizanEncoderHF")
                    self.tokenizer = AutoTokenizer.from_pretrained(cfg["backbone_name"])
                    self.model = MizanEncoderHF.from_pretrained(backbone_name).to(self.device)

                else:
                    # Your classic MizanTextEncoder (50k model)
                    print("🔵 Loading custom-trained MizanTextEncoder")
                    base = cfg.get("backbone", cfg.get("backbone_name"))
                    self.tokenizer = AutoTokenizer.from_pretrained(base)

                    self.model = MizanTextEncoder.from_pretrained(backbone_name).to(self.device)

                self.model.eval()
                return

        # ==========================================================
        # CASE 2 — NORMAL HF MODEL
        # ==========================================================
        print(f"🟣 Loading HF model: {backbone_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(backbone_name)

        self.model = HFEmbeddingModel(
            backbone_name=backbone_name,
            emb_dim=emb_dim,
            pooling=pooling,
            normalize=normalize,
        ).to(self.device)

        self.model.eval()

    # ============================================================================
    # Caching helpers
    # ============================================================================
    def _cache_get(self, text):
        return None if self.cache is None else self.cache.get(text)

    def _cache_put(self, text, emb):
        if self.cache is not None:
            self.cache[text] = emb

    # ============================================================================
    # Batch Encoding
    # ============================================================================
    @torch.no_grad()
    def encode(self, texts: List[str], batch_size=16) -> torch.Tensor:
        cached = {}
        to_run = []

        for t in texts:
            c = self._cache_get(t)
            if c is not None:
                cached[t] = c
            else:
                to_run.append(t)

        if to_run:
            for i in range(0, len(to_run), batch_size):
                batch = to_run[i:i+batch_size]

                enc = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=256,
                    return_token_type_ids=False,
                    return_tensors="pt"
                ).to(self.device)

                # SAFETY: remove token_type_ids if present
                if "token_type_ids" in enc:
                    enc.pop("token_type_ids")

                emb = self.model(**enc).cpu()

                for txt, e in zip(batch, emb):
                    cached[txt] = e
                    self._cache_put(txt, e)

        # return in original order
        return torch.stack([cached[t] for t in texts])

    # ============================================================================
    # Single Encoding
    # ============================================================================
    @torch.no_grad()
    def encode_one(self, text: str):
        c = self._cache_get(text)
        if c is not None:
            return c
        return self.encode([text])[0]
