"""
Text encoders for embedding.

Supported encoders:
- MiniLM (384-dim): Fast, good quality
- MPNet (768-dim): Higher quality, slower
"""

import numpy as np
from typing import List, Tuple, Any

# Encoder configurations
ENCODERS = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "mpnet": "sentence-transformers/all-mpnet-base-v2",
}


def get_encoder(name: str, device: str = "cpu") -> Tuple[Any, Any]:
    """
    Load a text encoder.

    Args:
        name: Encoder name ("minilm", "mpnet") or HuggingFace model path
        device: Device ("cpu" or "cuda")

    Returns:
        Tuple of (model, tokenizer)
    """
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
    except ImportError:
        raise ImportError(
            "Please install transformers and torch:\n"
            "  pip install transformers torch"
        )

    # Resolve encoder name
    model_name = ENCODERS.get(name.lower(), name)

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.to(device)
    model.eval()

    return model, tokenizer


def embed_texts(
    texts: List[str],
    model: Any,
    tokenizer: Any,
    batch_size: int = 32,
    max_length: int = 128,
    show_progress: bool = False
) -> np.ndarray:
    """
    Embed texts using a transformer model.

    Args:
        texts: List of text strings
        model: Loaded model
        tokenizer: Loaded tokenizer
        batch_size: Batch size
        max_length: Maximum token length
        show_progress: Show progress bar

    Returns:
        numpy array of embeddings (n_samples, embedding_dim)
    """
    try:
        import torch
    except ImportError:
        raise ImportError("Please install torch: pip install torch")

    embeddings = []
    device = next(model.parameters()).device

    # Optional progress bar
    if show_progress:
        try:
            from tqdm import tqdm
            iterator = tqdm(range(0, len(texts), batch_size), desc="Embedding")
        except ImportError:
            iterator = range(0, len(texts), batch_size)
    else:
        iterator = range(0, len(texts), batch_size)

    with torch.no_grad():
        for i in iterator:
            batch = texts[i:i + batch_size]

            # Tokenize
            inputs = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt"
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}

            # Forward pass
            outputs = model(**inputs)

            # Mean pooling
            emb = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            embeddings.append(emb)

    return np.vstack(embeddings)
