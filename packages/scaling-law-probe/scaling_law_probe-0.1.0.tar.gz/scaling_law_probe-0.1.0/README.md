# Neural Scaling Probe

**Predict scaling laws before training—save $10M.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/scaling-law-probe.svg)](https://badge.fury.io/py/scaling-law-probe)

Neural Scaling Probe predicts how well your dataset will scale with more data—*before* you spend millions on training. Using intrinsic dimension measurement, it estimates the data scaling exponent β_D in ~10 minutes on a laptop.

## The 10-Second Pitch

| What you do today | What this tool does |
|-------------------|---------------------|
| Train 10+ models across scales ($100K–$10M) | Run a 10-minute probe ($0) |
| Discover β_D after the fact | **Predict β_D before training** |

## Quick Start

```bash
pip install scaling-law-probe
```

```python
from scaling_law_probe import predict_beta

# Load your text data
texts = ["Your text samples...", "More text...", ...]

# Predict scaling in 3 lines
beta, intrinsic_dim = predict_beta(texts, encoder="minilm")
print(f"Predicted β_D: {beta:.3f}, ID: {intrinsic_dim:.1f}")
```

**CLI:**
```bash
python -m scaling_law_probe --file your_data.txt
# Output: Predicted β_D = 0.34, ID = 13.3
```

## Validation Results

We validated on 4 modalities using fixed smoothness s = 4.5 (calibrated on text):

| Modality | Measured ID | Predicted β_D | Published β_D | Error |
|----------|-------------|---------------|---------------|-------|
| Code | 8.4 | 0.53 | ~0.45 | +18% |
| Tabular-as-text | 9.1 | 0.50 | ~0.40 | +24% |
| Text (WikiText) | 13.3 | 0.34 | 0.34 (Chinchilla) | <1% |
| Scientific (PubMed) | 15.0 | 0.30 | ~0.32 | -6% |

**Key findings:**
- ✅ All predictions within 25%—consistent with empirical variance in scaling law estimates
- ✅ Rank order (code > tabular > text > scientific) preserved across encoders
- ✅ Structured data shows lower smoothness (s ≈ 3.6–3.8), a useful diagnostic

## How It Works

The theory: **β_D = s/d** where:
- **β_D** is the data scaling exponent (Loss ∝ Data^{-β_D})
- **d** is the intrinsic dimension of your data manifold
- **s** is the smoothness of the target function (≈4.5 for text)

Lower intrinsic dimension → faster learning → higher β_D.

```
┌─────────────────────────────────────────────────────────┐
│  Your Data  →  Embed (MiniLM)  →  Measure ID (TwoNN)   │
│                                           ↓             │
│                              Predict β_D = 4.5 / ID     │
└─────────────────────────────────────────────────────────┘
```

## Installation

**From PyPI:**
```bash
pip install scaling-law-probe
```

**From source:**
```bash
git clone https://github.com/sandroandric/neural-scaling-probe.git
cd neural-scaling-probe
pip install -e .
```

**With HuggingFace datasets support:**
```bash
pip install scaling-law-probe[datasets]
```

## Usage

### Python API

```python
from scaling_law_probe import predict_beta, measure_id, ScalingProbe

# Quick prediction
beta, id_est = predict_beta(texts, encoder="minilm", n_samples=10000)

# Just measure intrinsic dimension
id_est = measure_id(texts)

# Full control with ScalingProbe class
probe = ScalingProbe(encoder="mpnet", smoothness=4.5, device="cuda")
embeddings = probe.embed(texts)
beta, id_est = probe.predict_from_embeddings(embeddings)
```

### Command Line

```bash
# From a text file
python -m scaling_law_probe --file data.txt

# From HuggingFace dataset
python -m scaling_law_probe --dataset wikitext --n-samples 5000

# With different encoder
python -m scaling_law_probe --file data.txt --encoder mpnet

# With confidence interval
python -m scaling_law_probe --file data.txt --confidence
```

### Interpreting Results

| Predicted β_D | Interpretation |
|---------------|----------------|
| > 0.45 | Highly structured (like code). Expect **fast** scaling. |
| 0.35–0.45 | Moderately structured (like general text). **Moderate** scaling. |
| 0.25–0.35 | Less structured (specialized text). **Slower** scaling. |
| < 0.25 | High-dimensional. Scaling may be slow; consider data curation. |

## Limitations

- **Embedding-space ID**: Measurements depend on the encoder (MiniLM/MPNet). Rank order is preserved but absolute values vary.
- **Text serialization**: Tabular data must be converted to text, which may inflate ID.
- **Smoothness varies**: s ≈ 4.5 works for unstructured text; structured data (code, tabular) has lower smoothness (~3.6–3.8).

## Citation

If you use this tool in your research, please cite:

```bibtex
@article{neural_scaling_probe_2024,
  title={Predicting Neural Scaling Laws from Data Geometry},
  author={Anonymous},
  journal={arXiv preprint},
  year={2024}
}
```

## References

- Hoffmann et al. (2022). Training compute-optimal large language models. [Chinchilla paper]
- Kaplan et al. (2020). Scaling laws for neural language models.
- Facco et al. (2017). Estimating the intrinsic dimension of datasets by a minimal neighborhood information.

## License

MIT License - see [LICENSE](LICENSE) for details.
