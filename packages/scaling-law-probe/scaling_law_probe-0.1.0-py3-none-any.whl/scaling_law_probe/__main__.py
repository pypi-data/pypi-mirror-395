"""
Command-line interface for Neural Scaling Probe.

Usage:
    python -m scaling_law_probe --file data.txt
    python -m scaling_law_probe --dataset wikitext --n-samples 5000
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Neural Scaling Probe: Predict scaling laws from data geometry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From a text file (one text per line)
  python -m scaling_law_probe --file data.txt

  # With specific encoder
  python -m scaling_law_probe --file data.txt --encoder mpnet

  # From HuggingFace dataset
  python -m scaling_law_probe --dataset wikitext --n-samples 5000

Reference scaling exponents (β_D):
  Code:       ~0.45 (Kaplan et al., 2020)
  Text:       ~0.34 (Hoffmann et al., 2022)
  Scientific: ~0.32 (estimated from Galactica)

Theory: β_D = s/d where s ≈ 4.5 (calibrated on text), d = intrinsic dimension
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--file", "-f",
        type=str,
        help="Path to text file (one text per line)"
    )
    input_group.add_argument(
        "--dataset", "-d",
        type=str,
        help="HuggingFace dataset name (e.g., 'wikitext', 'ccdv/pubmed-summarization')"
    )

    # Options
    parser.add_argument(
        "--encoder", "-e",
        type=str,
        default="minilm",
        choices=["minilm", "mpnet"],
        help="Encoder to use (default: minilm)"
    )
    parser.add_argument(
        "--n-samples", "-n",
        type=int,
        default=10000,
        help="Number of samples to use (default: 10000)"
    )
    parser.add_argument(
        "--smoothness", "-s",
        type=float,
        default=4.5,
        help="Smoothness parameter (default: 4.5, calibrated on text)"
    )
    parser.add_argument(
        "--batch-size", "-b",
        type=int,
        default=32,
        help="Batch size for embedding (default: 32)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device for embedding (default: cpu)"
    )
    parser.add_argument(
        "--confidence",
        action="store_true",
        help="Compute bootstrap confidence interval"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show progress"
    )

    args = parser.parse_args()

    # Import here to avoid slow startup for --help
    from .probe import ScalingProbe
    from .probes.twonn import twonn_id_with_confidence
    import numpy as np

    print("=" * 60)
    print("Neural Scaling Probe")
    print("=" * 60)

    # Load data
    texts = []

    if args.file:
        print(f"\nLoading from file: {args.file}")
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if len(line) > 50:  # Filter very short texts
                    texts.append(line)
        print(f"  Loaded {len(texts)} texts")

    elif args.dataset:
        print(f"\nLoading dataset: {args.dataset}")
        try:
            from datasets import load_dataset

            if args.dataset.lower() == "wikitext":
                ds = load_dataset("wikitext", "wikitext-103-raw-v1", split="train", streaming=True)
                field = "text"
            elif "pubmed" in args.dataset.lower():
                ds = load_dataset("ccdv/pubmed-summarization", "document", split="train", streaming=True)
                field = "article"
            else:
                ds = load_dataset(args.dataset, split="train", streaming=True)
                field = "text"

            for ex in ds:
                text = ex.get(field, ex.get("content", ""))
                if isinstance(text, str) and len(text) > 50:
                    texts.append(text[:512])
                if len(texts) >= args.n_samples * 2:  # Get extra for filtering
                    break

            print(f"  Loaded {len(texts)} texts")

        except ImportError:
            print("ERROR: Please install datasets: pip install datasets")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Failed to load dataset: {e}")
            sys.exit(1)

    # Sample if needed
    if len(texts) > args.n_samples:
        np.random.seed(42)
        indices = np.random.choice(len(texts), args.n_samples, replace=False)
        texts = [texts[i] for i in indices]

    print(f"  Using {len(texts)} samples")

    # Create probe
    print(f"\nEncoder: {args.encoder}")
    print(f"Smoothness: {args.smoothness}")
    print(f"Device: {args.device}")

    probe = ScalingProbe(
        encoder=args.encoder,
        smoothness=args.smoothness,
        device=args.device
    )

    # Embed
    print("\nEmbedding texts...")
    embeddings = probe.embed(texts, batch_size=args.batch_size)
    print(f"  Shape: {embeddings.shape}")

    # Measure ID
    print("\nMeasuring intrinsic dimension...")
    if args.confidence:
        id_est, ci_low, ci_high = twonn_id_with_confidence(embeddings)
        print(f"  ID: {id_est:.2f} (95% CI: [{ci_low:.2f}, {ci_high:.2f}])")
    else:
        id_est = probe.measure_id(embeddings)
        print(f"  ID: {id_est:.2f}")

    # Predict beta
    beta = args.smoothness / id_est

    # Output
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\n  Intrinsic Dimension:  {id_est:.2f}")
    print(f"  Smoothness (s):       {args.smoothness}")
    print(f"  Predicted β_D:        {beta:.3f}")

    # Interpretation
    print("\n--- Interpretation ---")
    if beta > 0.45:
        print("  → Highly structured data (like code)")
        print("  → Expect FAST scaling with more data")
    elif beta > 0.35:
        print("  → Moderately structured (like general text)")
        print("  → Expect MODERATE scaling with more data")
    elif beta > 0.25:
        print("  → Less structured (like specialized text)")
        print("  → Expect SLOWER scaling with more data")
    else:
        print("  → High-dimensional / unstructured data")
        print("  → Scaling may be slow; consider data curation")

    # Reference table
    print("\n--- Reference Values (from literature) ---")
    print("  Code:       β_D ≈ 0.45")
    print("  Text:       β_D ≈ 0.34 (Chinchilla)")
    print("  Scientific: β_D ≈ 0.32")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
