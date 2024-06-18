from typing import Any
from functools import lru_cache
import torch
from transformers import AutoModel, AutoTokenizer
from core.config import settings

@lru_cache()
def load_model() -> Any:
    model = AutoModel.from_pretrained(
        settings.OCR_MODEL,
        trust_remote_code=True,
    ).to(dtype=torch.float16)

    model = model.to(device=settings.DEVICE)

    # Set model to eval mode (inference mode)
    # This turns off training-specific behaviors that can produce less reliable results
    model.eval()

    return model

@lru_cache()
def load_tokenizer() -> Any:
    tokenizer = AutoTokenizer.from_pretrained(
        settings.OCR_MODEL,
        trust_remote_code=True,
    )
    return tokenizer
