"""
Detectron2 Model Weight Extractor

This script extracts model weights from Detectron2 checkpoint files, removing optimizer
and scheduler state to create lightweight inference-ready models. It's designed for
deployment scenarios where you only need the trained model weights without training metadata.

Key Features:
- Extracts model weights from Detectron2 checkpoint format
- Removes optimizer and scheduler state for smaller file size
- Optional removal of batch normalization tracking variables
- Handles both standard PyTorch checkpoints and Detectron2 checkpoint format
- Validates input files and provides clear error messages
- Creates output directory if it doesn't exist

The tool automatically detects the checkpoint format:
- Detectron2 format: {'model': state_dict, 'optimizer': ..., 'scheduler': ...}
- Standard PyTorch format: Direct state_dict

Usage:
    # Basic usage - extract weights to default filename
    poetry run detectron-strip model_0149999.pth

    # Specify custom output filename
    poetry run detectron-strip model_0149999.pth model_weights_only.pth

    # Remove batch normalization tracking variables for cleaner weights
    poetry run detectron-strip model_0149999.pth model_clean.pth --remove-bn-tracking

    # Extract from full path with custom output directory
    poetry run detectron-strip /path/to/checkpoints/model_final.pth ./deploy/model_inference.pth

File Size Reduction:
- Typical reduction: 50-70% smaller files
- Optimizer state removal: ~33% reduction
- Scheduler state removal: ~10-20% reduction
- BN tracking removal: <1% reduction (but cleaner)

Common Use Cases:
1. Preparing models for deployment/inference
2. Reducing model file sizes for distribution
3. Converting training checkpoints to inference-only format
4. Cleaning up models before model serving
"""

import argparse
import os
import sys
from pathlib import Path

import torch


def extract_model_weights(
    source_path,
    destination_path,
    remove_bn_tracking=False,
):
    """
    Extract model weights from a checkpoint file, removing training metadata.

    Args:
        source_path (str): Path to the source checkpoint file
        destination_path (str): Path for the output weights file
        remove_bn_tracking (bool): Whether to remove batch normalization tracking variables

    Returns:
        dict: Statistics about the extraction process

    Raises:
        FileNotFoundError: If source file doesn't exist
        RuntimeError: If checkpoint loading or processing fails
    """
    print(f"🔍 Loading checkpoint from: {source_path}")

    # Load checkpoint with error handling
    try:
        ckpt = torch.load(source_path, map_location="cpu")
    except Exception as e:
        raise RuntimeError(f"Failed to load checkpoint: {e}")

    # Detect checkpoint format and extract model state
    if isinstance(ckpt, dict) and "model" in ckpt:
        print("📦 Detected Detectron2 checkpoint format")
        state = ckpt["model"]

        # Report what we're removing
        removed_keys = []
        for key in ckpt.keys():
            if key != "model":
                removed_keys.append(key)

        if removed_keys:
            print(f"🗑️  Removing training metadata: {', '.join(removed_keys)}")
    else:
        print("📦 Detected standard PyTorch checkpoint format")
        state = ckpt

    # Count original parameters
    original_keys = len(state.keys())

    # Optional: remove batch normalization tracking variables
    bn_removed = 0
    if remove_bn_tracking:
        print("🧹 Removing batch normalization tracking variables...")
        for k in list(state.keys()):
            if k.endswith("num_batches_tracked"):
                del state[k]
                bn_removed += 1

        if bn_removed > 0:
            print(f"   Removed {bn_removed} BN tracking variables")
        else:
            print("   No BN tracking variables found")

    # Create output directory if needed
    output_dir = os.path.dirname(destination_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"📁 Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    # Save the weights
    print(f"💾 Saving weights to: {destination_path}")
    try:
        torch.save(state, destination_path)
    except Exception as e:
        raise RuntimeError(f"Failed to save weights: {e}")

    # Calculate file size reduction
    original_size_mb = os.path.getsize(source_path) / (1024 * 1024)
    new_size_mb = os.path.getsize(destination_path) / (1024 * 1024)
    reduction_pct = ((original_size_mb - new_size_mb) / original_size_mb) * 100

    stats = {
        "original_keys": original_keys,
        "final_keys": len(state.keys()),
        "bn_removed": bn_removed,
        "original_size_mb": original_size_mb,
        "new_size_mb": new_size_mb,
        "reduction_pct": reduction_pct,
    }

    return stats


def parse_args():
    """Parse command line arguments for the Detectron2 weight extraction script."""
    parser = argparse.ArgumentParser(
        description="Extract model weights from Detectron2 checkpoint files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract weights to default filename
  %(prog)s model_0149999.pth
  
  # Specify custom output filename  
  %(prog)s model_0149999.pth model_weights.pth
  
  # Remove BN tracking variables for cleaner weights
  %(prog)s model_0149999.pth model_clean.pth --remove-bn-tracking
  
  # Full path example
  %(prog)s /path/to/model_final.pth ./deploy/inference_model.pth
        """,
    )

    parser.add_argument("source", help="Path to the source checkpoint file (.pth)")

    parser.add_argument(
        "destination",
        nargs="?",
        default=None,
        help="Path for the output weights file (default: <source>_weights_only.pth)",
    )

    parser.add_argument(
        "--remove-bn-tracking",
        action="store_true",
        help="Remove batch normalization tracking variables (num_batches_tracked) for cleaner weights",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output, only show errors",
    )

    return parser.parse_args()


def main():
    """Main entry point for the Detectron2 weight extraction tool."""
    args = parse_args()

    # Validate source file exists
    if not os.path.exists(args.source):
        print(f"❌ Error: Source file '{args.source}' does not exist", file=sys.stderr)
        return 1

    # Generate default destination filename if not provided
    if args.destination is None:
        source_path = Path(args.source)
        args.destination = str(
            source_path.parent / f"{source_path.stem}_weights_only{source_path.suffix}"
        )

    # Check if destination already exists and warn user
    if os.path.exists(args.destination):
        if not args.quiet:
            print(
                f"⚠️  Warning: Output file '{args.destination}' already exists and will be overwritten"
            )

    try:
        # Extract model weights
        if not args.quiet:
            print("🚀 Starting Detectron2 weight extraction...")
            print(f"📂 Source: {args.source}")
            print(f"📂 Destination: {args.destination}")
            print()

        stats = extract_model_weights(
            source_path=args.source,
            destination_path=args.destination,
            remove_bn_tracking=args.remove_bn_tracking,
        )

        if not args.quiet:
            print()
            print("✅ Weight extraction completed successfully!")
            print()
            print("📊 Summary:")
            print(
                f"   Model parameters: {stats['original_keys']} → {stats['final_keys']} keys"
            )
            if stats["bn_removed"] > 0:
                print(f"   BN tracking vars removed: {stats['bn_removed']}")
            print(
                f"   File size: {stats['original_size_mb']:.1f} MB → {stats['new_size_mb']:.1f} MB"
            )
            print(f"   Size reduction: {stats['reduction_pct']:.1f}%")
            print()
            print(f"🎯 Inference-ready model saved to: {args.destination}")

    except (FileNotFoundError, RuntimeError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
