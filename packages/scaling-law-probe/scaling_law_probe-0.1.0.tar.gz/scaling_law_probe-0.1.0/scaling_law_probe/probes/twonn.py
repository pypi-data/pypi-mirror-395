"""
TwoNN intrinsic dimension estimator.

Reference:
    Facco, E., et al. (2017). Estimating the intrinsic dimension of datasets
    by a minimal neighborhood information. Scientific Reports, 7, 12140.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from typing import Optional


def twonn_id(
    embeddings: np.ndarray,
    k1: int = 1,
    k2: int = 2,
    subsample: Optional[int] = None,
    seed: int = 42
) -> float:
    """
    Estimate intrinsic dimension using the TwoNN method.

    The TwoNN estimator uses the ratio of distances to the first and second
    nearest neighbors. Under the assumption that data lies on a d-dimensional
    manifold, this ratio follows a known distribution parameterized by d.

    Args:
        embeddings: numpy array of shape (n_samples, n_features)
        k1: Index of first neighbor (default: 1, i.e., nearest neighbor)
        k2: Index of second neighbor (default: 2)
        subsample: If set, subsample to this many points (for large datasets)
        seed: Random seed for subsampling

    Returns:
        Estimated intrinsic dimension

    Example:
        >>> embeddings = np.random.randn(1000, 384)  # 1000 samples, 384 dims
        >>> id_estimate = twonn_id(embeddings)
        >>> print(f"Intrinsic dimension: {id_estimate:.2f}")

    Notes:
        - Robust to noise and works well in high dimensions
        - Requires no hyperparameters beyond k1, k2
        - Recommended: n_samples >= 1000 for reliable estimates
        - Duplicate embeddings are automatically deduplicated
    """
    # Deduplicate embeddings (duplicates cause zero distances)
    embeddings = np.unique(embeddings, axis=0)
    N = embeddings.shape[0]

    # Need at least 3 unique points for TwoNN
    if N < 3:
        return np.nan

    # Subsample if needed (for large datasets)
    if subsample and N > subsample:
        np.random.seed(seed)
        indices = np.random.choice(N, subsample, replace=False)
        embeddings = embeddings[indices]
        N = subsample

    # Compute pairwise distances
    distances = squareform(pdist(embeddings, metric='euclidean'))

    # Compute ratios r2/r1 for each point
    # Note: sorted_dists[0] is self-distance (0), so we use k1+1 and k2+1
    ratios = []
    for i in range(N):
        sorted_dists = np.sort(distances[i])
        # Skip zero distances (self and duplicates)
        nonzero_dists = sorted_dists[sorted_dists > 1e-10]
        if len(nonzero_dists) >= 2:
            r1 = nonzero_dists[0]  # Distance to nearest neighbor
            r2 = nonzero_dists[1]  # Distance to 2nd nearest neighbor
            ratios.append(r2 / r1)

    ratios = np.array(ratios)

    if len(ratios) == 0:
        return np.nan

    # Filter out ratios <= 1 (edge cases)
    log_ratios = np.log(ratios[ratios > 1])

    if len(log_ratios) == 0:
        return np.nan

    # MLE estimator: d = N / sum(log(r2/r1))
    id_estimate = len(log_ratios) / np.sum(log_ratios)

    return id_estimate


def twonn_id_with_confidence(
    embeddings: np.ndarray,
    n_bootstrap: int = 100,
    k1: int = 1,
    k2: int = 2,
    seed: int = 42
) -> tuple:
    """
    Estimate intrinsic dimension with bootstrap confidence interval.

    Args:
        embeddings: numpy array of shape (n_samples, n_features)
        n_bootstrap: Number of bootstrap samples
        k1: Index of first neighbor
        k2: Index of second neighbor
        seed: Random seed

    Returns:
        Tuple of (id_estimate, ci_low, ci_high)
    """
    np.random.seed(seed)
    N = embeddings.shape[0]

    bootstrap_ids = []
    for _ in range(n_bootstrap):
        indices = np.random.choice(N, N, replace=True)
        boot_embeddings = embeddings[indices]
        boot_id = twonn_id(boot_embeddings, k1=k1, k2=k2)
        if not np.isnan(boot_id):
            bootstrap_ids.append(boot_id)

    if len(bootstrap_ids) == 0:
        return np.nan, np.nan, np.nan

    id_estimate = np.mean(bootstrap_ids)
    ci_low = np.percentile(bootstrap_ids, 2.5)
    ci_high = np.percentile(bootstrap_ids, 97.5)

    return id_estimate, ci_low, ci_high
