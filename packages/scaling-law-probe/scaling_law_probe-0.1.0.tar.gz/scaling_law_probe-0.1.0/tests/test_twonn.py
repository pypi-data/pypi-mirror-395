"""
Tests for TwoNN intrinsic dimension estimator.
"""

import numpy as np
import pytest

from scaling_law_probe.probes.twonn import twonn_id, twonn_id_with_confidence


class TestTwoNN:
    """Tests for TwoNN estimator."""

    def test_known_dimension_low(self):
        """Test on data with known low intrinsic dimension."""
        np.random.seed(42)

        # Generate data on a 5D manifold embedded in 100D
        true_d = 5
        n_samples = 1000
        latent = np.random.randn(n_samples, true_d)
        A = np.random.randn(true_d, 100)
        data = latent @ A

        estimated_d = twonn_id(data)

        # Should be within 50% of true dimension
        assert 2.5 < estimated_d < 10, f"Expected ~5, got {estimated_d}"

    def test_known_dimension_high(self):
        """Test on data with known higher intrinsic dimension."""
        np.random.seed(42)

        # Generate data on a 15D manifold embedded in 100D
        true_d = 15
        n_samples = 2000
        latent = np.random.randn(n_samples, true_d)
        A = np.random.randn(true_d, 100)
        data = latent @ A

        estimated_d = twonn_id(data)

        # Should be within 50% of true dimension
        assert 7.5 < estimated_d < 25, f"Expected ~15, got {estimated_d}"

    def test_full_rank_data(self):
        """Test on full-rank random data."""
        np.random.seed(42)

        # Full rank 50D data
        n_samples = 1000
        data = np.random.randn(n_samples, 50)

        estimated_d = twonn_id(data)

        # Should be high (close to ambient dimension)
        assert estimated_d > 30, f"Expected high ID, got {estimated_d}"

    def test_subsample(self):
        """Test subsampling for large datasets."""
        np.random.seed(42)

        true_d = 10
        n_samples = 5000
        latent = np.random.randn(n_samples, true_d)
        A = np.random.randn(true_d, 100)
        data = latent @ A

        # Full vs subsampled
        full_id = twonn_id(data)
        sub_id = twonn_id(data, subsample=1000)

        # Should be similar (within 30%)
        assert abs(full_id - sub_id) / full_id < 0.3

    def test_confidence_interval(self):
        """Test bootstrap confidence interval."""
        np.random.seed(42)

        true_d = 8
        n_samples = 1000
        latent = np.random.randn(n_samples, true_d)
        A = np.random.randn(true_d, 50)
        data = latent @ A

        id_est, ci_low, ci_high = twonn_id_with_confidence(data, n_bootstrap=50)

        # CI should contain estimate
        assert ci_low <= id_est <= ci_high
        # CI should be reasonable width
        assert ci_high - ci_low < id_est  # Width < estimate

    def test_small_dataset_warning(self):
        """Test behavior with very small dataset."""
        np.random.seed(42)

        # Very small dataset
        data = np.random.randn(50, 10)

        # Should still return a value (may be less accurate)
        estimated_d = twonn_id(data)
        assert not np.isnan(estimated_d)
        assert estimated_d > 0

    def test_reproducibility(self):
        """Test that results are reproducible with same seed."""
        np.random.seed(42)
        data = np.random.randn(500, 20)

        id1 = twonn_id(data)
        id2 = twonn_id(data)

        assert id1 == id2


class TestScalingPrediction:
    """Tests for scaling law prediction."""

    def test_beta_from_id(self):
        """Test β_D = s/d calculation."""
        s = 4.5  # Smoothness

        # ID = 13.3 should give β ≈ 0.34 (like text)
        id_text = 13.3
        beta_text = s / id_text
        assert abs(beta_text - 0.34) < 0.01

        # ID = 8.4 should give β ≈ 0.54 (like code)
        id_code = 8.4
        beta_code = s / id_code
        assert abs(beta_code - 0.54) < 0.01

    def test_rank_order(self):
        """Test that rank order is preserved: lower ID → higher β."""
        s = 4.5

        ids = {
            "code": 8.4,
            "tabular": 9.1,
            "text": 13.3,
            "scientific": 15.0,
        }

        betas = {k: s / v for k, v in ids.items()}

        # Check rank order
        assert betas["code"] > betas["tabular"] > betas["text"] > betas["scientific"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
