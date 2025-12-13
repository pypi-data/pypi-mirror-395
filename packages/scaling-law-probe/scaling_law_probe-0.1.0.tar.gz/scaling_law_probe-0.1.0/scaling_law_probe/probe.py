"""
Main probe interface for scaling law prediction.
"""

import numpy as np
from typing import List, Tuple, Optional, Union
from pathlib import Path

from .probes.twonn import twonn_id
from .encoders.text import get_encoder, embed_texts


# Calibrated smoothness from text (WikiText)
# See paper: β_D = s/d, where s ≈ 4.5 for text-like data
DEFAULT_SMOOTHNESS = 4.5


class ScalingProbe:
    """
    Probe for predicting neural scaling laws from data geometry.

    The theory: β_D ≈ s/d where:
    - β_D is the data scaling exponent (L ∝ D^{-β_D})
    - d is the intrinsic dimension of the data manifold
    - s is the smoothness of the target function (≈4.5 for text)

    Example:
        >>> probe = ScalingProbe(encoder="minilm")
        >>> beta, id_est = probe.predict(texts)
        >>> print(f"Predicted β_D: {beta:.3f}")
    """

    def __init__(
        self,
        encoder: str = "minilm",
        smoothness: float = DEFAULT_SMOOTHNESS,
        device: str = "cpu"
    ):
        """
        Initialize the scaling probe.

        Args:
            encoder: Encoder name ("minilm", "mpnet", or path to model)
            smoothness: Calibrated smoothness parameter (default 4.5 from text)
            device: Device for embedding ("cpu" or "cuda")
        """
        self.encoder_name = encoder
        self.smoothness = smoothness
        self.device = device
        self._encoder = None
        self._tokenizer = None

    def _load_encoder(self):
        """Lazy load the encoder."""
        if self._encoder is None:
            self._encoder, self._tokenizer = get_encoder(self.encoder_name, self.device)

    def embed(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Embed texts using the encoder.

        Args:
            texts: List of text strings
            batch_size: Batch size for embedding

        Returns:
            numpy array of embeddings (n_samples, embedding_dim)
        """
        self._load_encoder()
        return embed_texts(texts, self._encoder, self._tokenizer, batch_size)

    def measure_id(self, embeddings: np.ndarray) -> float:
        """
        Measure intrinsic dimension using TwoNN estimator.

        Args:
            embeddings: numpy array (n_samples, embedding_dim)

        Returns:
            Estimated intrinsic dimension
        """
        return twonn_id(embeddings)

    def predict(
        self,
        texts: List[str],
        n_samples: Optional[int] = None,
        batch_size: int = 32
    ) -> Tuple[float, float]:
        """
        Predict scaling exponent from text data.

        Args:
            texts: List of text strings
            n_samples: Number of samples to use (default: all)
            batch_size: Batch size for embedding

        Returns:
            Tuple of (predicted_beta, intrinsic_dimension)
        """
        # Sample if needed
        if n_samples and len(texts) > n_samples:
            indices = np.random.choice(len(texts), n_samples, replace=False)
            texts = [texts[i] for i in indices]

        # Embed
        embeddings = self.embed(texts, batch_size)

        # Measure ID
        id_estimate = self.measure_id(embeddings)

        # Predict beta
        beta = self.smoothness / id_estimate

        return beta, id_estimate

    def predict_from_embeddings(self, embeddings: np.ndarray) -> Tuple[float, float]:
        """
        Predict scaling exponent from pre-computed embeddings.

        Args:
            embeddings: numpy array (n_samples, embedding_dim)

        Returns:
            Tuple of (predicted_beta, intrinsic_dimension)
        """
        id_estimate = self.measure_id(embeddings)
        beta = self.smoothness / id_estimate
        return beta, id_estimate


def predict_beta(
    texts: Optional[List[str]] = None,
    embeddings: Optional[np.ndarray] = None,
    encoder: str = "minilm",
    smoothness: float = DEFAULT_SMOOTHNESS,
    n_samples: Optional[int] = 10000,
    batch_size: int = 32,
    device: str = "cpu"
) -> Tuple[float, float]:
    """
    Predict scaling exponent β_D from text data or embeddings.

    This is the main entry point for quick predictions.

    Args:
        texts: List of text strings (provide this OR embeddings)
        embeddings: Pre-computed embeddings (provide this OR texts)
        encoder: Encoder name ("minilm", "mpnet")
        smoothness: Smoothness parameter (default 4.5, calibrated on text)
        n_samples: Number of samples to use (default 10000)
        batch_size: Batch size for embedding
        device: Device for embedding ("cpu" or "cuda")

    Returns:
        Tuple of (predicted_beta, intrinsic_dimension)

    Example:
        >>> texts = ["Example text 1", "Example text 2", ...]
        >>> beta, id_est = predict_beta(texts)
        >>> print(f"Predicted β_D: {beta:.3f}, ID: {id_est:.1f}")

    Reference scaling exponents (from literature):
        - Code: β_D ≈ 0.45 (Kaplan et al., 2020)
        - Text: β_D ≈ 0.34 (Hoffmann et al., 2022, Chinchilla)
        - Scientific: β_D ≈ 0.32 (estimated from Galactica)
    """
    if texts is None and embeddings is None:
        raise ValueError("Must provide either texts or embeddings")

    probe = ScalingProbe(encoder=encoder, smoothness=smoothness, device=device)

    if embeddings is not None:
        return probe.predict_from_embeddings(embeddings)
    else:
        return probe.predict(texts, n_samples=n_samples, batch_size=batch_size)


def measure_id(
    texts: Optional[List[str]] = None,
    embeddings: Optional[np.ndarray] = None,
    encoder: str = "minilm",
    n_samples: Optional[int] = 10000,
    batch_size: int = 32,
    device: str = "cpu"
) -> float:
    """
    Measure intrinsic dimension of text data.

    Args:
        texts: List of text strings (provide this OR embeddings)
        embeddings: Pre-computed embeddings (provide this OR texts)
        encoder: Encoder name
        n_samples: Number of samples
        batch_size: Batch size
        device: Device

    Returns:
        Estimated intrinsic dimension
    """
    _, id_estimate = predict_beta(
        texts=texts,
        embeddings=embeddings,
        encoder=encoder,
        n_samples=n_samples,
        batch_size=batch_size,
        device=device
    )
    return id_estimate
