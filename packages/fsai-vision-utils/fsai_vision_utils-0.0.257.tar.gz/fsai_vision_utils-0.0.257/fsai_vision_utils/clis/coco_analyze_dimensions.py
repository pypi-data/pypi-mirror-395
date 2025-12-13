"""
Analyze distribution of object dimensions (width, height, area) per class
from a COCO-format annotation JSON file.

This tool provides comprehensive statistical analysis of annotation dimensions
including histograms, scatter plots, and per-class breakdowns.
"""

import argparse
import json
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


def compute_mask_area(segmentation):
    """
    Compute mask area for polygon segmentations (COCO style).
    segmentation: list of polygon lists (each polygon = [x1,y1,x2,y2,...])
    """
    if not isinstance(segmentation, list):
        return 0  # RLE case not implemented here
    area = 0
    for poly in segmentation:
        if len(poly) < 6:
            continue
        xs = np.array(poly[0::2])
        ys = np.array(poly[1::2])
        # Shoelace formula
        area += 0.5 * np.abs(xs[:-1] * ys[1:] - xs[1:] * ys[:-1]).sum()
    return area


def analyze_coco_json(
    ann_file,
    use_mask_area=False,
    plot_histograms=True,
    max_classes_to_plot=16,
    output_stats=None,
):
    """
    Analyze COCO annotation dimensions and generate statistics.

    Args:
        ann_file: Path to COCO annotations JSON file
        use_mask_area: Whether to use mask area instead of bbox area
        plot_histograms: Whether to generate histogram plots
        max_classes_to_plot: Maximum number of classes to plot individually
        output_stats: Optional path to save statistics as text file
    """
    with open(ann_file, "r") as f:
        coco = json.load(f)

    # category_id -> name
    category_map = {cat["id"]: cat["name"] for cat in coco["categories"]}

    # category_id -> list of areas, widths, heights
    areas = defaultdict(list)
    widths = defaultdict(list)
    heights = defaultdict(list)

    # image id → (w, h)
    image_sizes = {img["id"]: (img["width"], img["height"]) for img in coco["images"]}

    for ann in coco["annotations"]:
        cid = ann["category_id"]
        img_w, img_h = image_sizes[ann["image_id"]]

        # bbox = [x, y, w, h]
        x, y, w, h = ann["bbox"]
        area = w * h

        if use_mask_area and "segmentation" in ann:
            area = compute_mask_area(ann["segmentation"])

        if area > 0:
            areas[cid].append(area)
            widths[cid].append(w)
            heights[cid].append(h)

    # === Generate Statistics ===
    stats_output = []
    stats_output.append("\n=== Dimension Analysis Statistics ===\n")
    stats_output.append(
        f"{'CID':>5} | {'Class Name':<30} | {'Count':>6} | "
        f"{'Mean W':>10} | {'Mean H':>10} | {'Median W':>10} | {'Median H':>10} | "
        f"{'Max W':>10} | {'Max H':>10} | {'P90 W':>10} | {'P90 H':>10}"
    )
    stats_output.append("-" * 150)

    all_class_ids = sorted(areas.keys())
    global_widths = []
    global_heights = []
    global_areas = []

    for cid in all_class_ids:
        w_arr = np.array(widths[cid], dtype=np.float32)
        h_arr = np.array(heights[cid], dtype=np.float32)
        a_arr = np.array(areas[cid], dtype=np.float32)

        global_widths.extend(w_arr.tolist())
        global_heights.extend(h_arr.tolist())
        global_areas.extend(a_arr.tolist())

        cname = category_map.get(cid, f"class_{cid}")
        stats_line = (
            f"{cid:5d} | {cname:<30} | {len(w_arr):6d} | "
            f"{w_arr.mean():10.1f} | {h_arr.mean():10.1f} | "
            f"{np.median(w_arr):10.1f} | {np.median(h_arr):10.1f} | "
            f"{w_arr.max():10.1f} | {h_arr.max():10.1f} | "
            f"{np.percentile(w_arr, 90):10.1f} | {np.percentile(h_arr, 90):10.1f}"
        )
        stats_output.append(stats_line)

    global_widths = np.array(global_widths, dtype=np.float32)
    global_heights = np.array(global_heights, dtype=np.float32)
    global_areas = np.array(global_areas, dtype=np.float32)

    stats_output.append("\n" + "=" * 150)
    global_stats = (
        f"{'GLOBAL':<36} | {len(global_widths):6d} | "
        f"{global_widths.mean():10.1f} | {global_heights.mean():10.1f} | "
        f"{np.median(global_widths):10.1f} | {np.median(global_heights):10.1f} | "
        f"{global_widths.max():10.1f} | {global_heights.max():10.1f} | "
        f"{np.percentile(global_widths, 90):10.1f} | {np.percentile(global_heights, 90):10.1f}"
    )
    stats_output.append(global_stats)

    # Add area statistics
    stats_output.append(f"\n=== Area Statistics ===")
    stats_output.append(f"Mean area: {global_areas.mean():,.1f} px²")
    stats_output.append(f"Median area: {np.median(global_areas):,.1f} px²")
    stats_output.append(f"Max area: {global_areas.max():,.1f} px²")
    stats_output.append(
        f"90th percentile area: {np.percentile(global_areas, 90):,.1f} px²"
    )
    stats_output.append(
        f"95th percentile area: {np.percentile(global_areas, 95):,.1f} px²"
    )
    stats_output.append(
        f"99th percentile area: {np.percentile(global_areas, 99):,.1f} px²"
    )

    # Print to console
    for line in stats_output:
        print(line)

    # Save to file if requested
    if output_stats:
        with open(output_stats, "w") as f:
            f.write("\n".join(stats_output))
        print(f"\n✅ Statistics saved to: {output_stats}")

    # === Plot Histograms ===
    if plot_histograms and len(global_widths) > 0:
        plt.figure(figsize=(16, 6))

        # Global distribution plot
        plt.subplot(1, 4, 1)
        plt.hist(global_widths, bins=50, alpha=0.7, label="Width", color="blue")
        plt.hist(global_heights, bins=50, alpha=0.7, label="Height", color="orange")
        plt.axvline(512, color="purple", linestyle="--", alpha=0.7, label="512px")
        plt.axvline(1024, color="r", linestyle="--", alpha=0.7, label="1024px")
        plt.axvline(2048, color="g", linestyle="--", alpha=0.7, label="2048px")
        plt.title("Global Width/Height Distribution")
        plt.xlabel("Dimension (px)")
        plt.ylabel("Count")
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Width vs Height scatter
        plt.subplot(1, 4, 2)
        plt.scatter(global_widths, global_heights, alpha=0.3, s=1)
        plt.axvline(512, color="purple", linestyle="--", alpha=0.5)
        plt.axhline(512, color="purple", linestyle="--", alpha=0.5)
        plt.axvline(1024, color="r", linestyle="--", alpha=0.5)
        plt.axhline(1024, color="r", linestyle="--", alpha=0.5)
        plt.axvline(2048, color="g", linestyle="--", alpha=0.5)
        plt.axhline(2048, color="g", linestyle="--", alpha=0.5)
        plt.title("Width vs Height")
        plt.xlabel("Width (px)")
        plt.ylabel("Height (px)")
        plt.grid(True, alpha=0.3)

        # Log scale distribution
        plt.subplot(1, 4, 3)
        log_w = np.log10(global_widths[global_widths > 0])
        log_h = np.log10(global_heights[global_heights > 0])
        plt.hist(log_w, bins=50, alpha=0.7, label="Width", color="blue")
        plt.hist(log_h, bins=50, alpha=0.7, label="Height", color="orange")
        plt.title("Distribution (log10 scale)")
        plt.xlabel("log10(dimension)")
        plt.ylabel("Count")
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Area distribution
        plt.subplot(1, 4, 4)
        plt.hist(
            np.log10(global_areas[global_areas > 0]), bins=50, alpha=0.7, color="green"
        )
        plt.title("Area Distribution (log10)")
        plt.xlabel("log10(area px²)")
        plt.ylabel("Count")
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        # Per-class plots
        if len(all_class_ids) > 1:
            n = min(max_classes_to_plot, len(all_class_ids))
            cols = 4
            rows = int(np.ceil(n / cols))
            fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))

            if rows == 1:
                axes = axes.reshape(1, -1)
            axes = axes.flatten()

            for i, cid in enumerate(all_class_ids[:n]):
                w_arr = np.array(widths[cid])
                h_arr = np.array(heights[cid])

                axes[i].scatter(w_arr, h_arr, alpha=0.6, s=15)
                axes[i].axvline(512, color="purple", linestyle="--", alpha=0.5)
                axes[i].axhline(512, color="purple", linestyle="--", alpha=0.5)
                axes[i].axvline(1024, color="r", linestyle="--", alpha=0.5)
                axes[i].axhline(1024, color="r", linestyle="--", alpha=0.5)
                axes[i].axvline(2048, color="g", linestyle="--", alpha=0.5)
                axes[i].axhline(2048, color="g", linestyle="--", alpha=0.5)
                axes[i].set_title(f"{category_map.get(cid, cid)} (n={len(w_arr)})")
                axes[i].set_xlabel("Width (px)")
                axes[i].set_ylabel("Height (px)")
                axes[i].grid(True, alpha=0.3)

            # Hide unused subplots
            for j in range(i + 1, len(axes)):
                axes[j].axis("off")

            plt.tight_layout()
            plt.show()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze COCO annotation dimensions and generate statistics with visualizations"
    )
    parser.add_argument(
        "--input-coco-json",
        "--ann",
        required=True,
        help="Path to COCO annotations JSON file",
    )
    parser.add_argument(
        "--no-plots", action="store_true", help="Disable histogram and scatter plots"
    )
    parser.add_argument(
        "--max-classes-to-plot",
        type=int,
        default=16,
        help="Maximum number of classes to plot individually (default: 16)",
    )
    parser.add_argument(
        "--use-mask-area",
        action="store_true",
        help="Use segmentation mask area instead of bounding box area",
    )
    parser.add_argument(
        "--output-stats", type=str, help="Optional path to save statistics as text file"
    )
    return parser.parse_args()


def main():
    """Main entry point for the CLI tool."""
    args = parse_args()

    try:
        analyze_coco_json(
            ann_file=args.input_coco_json,
            use_mask_area=args.use_mask_area,
            plot_histograms=not args.no_plots,
            max_classes_to_plot=args.max_classes_to_plot,
            output_stats=args.output_stats,
        )
    except FileNotFoundError:
        print(f"❌ Error: COCO JSON file '{args.input_coco_json}' not found.")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format in '{args.input_coco_json}': {e}")
        return 1
    except Exception as e:
        print(f"❌ Error analyzing dimensions: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
