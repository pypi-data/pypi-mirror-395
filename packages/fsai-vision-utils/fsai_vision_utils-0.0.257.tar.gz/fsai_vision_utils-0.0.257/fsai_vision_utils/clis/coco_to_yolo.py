"""
COCO to YOLO Format Converter

This script converts COCO format annotations to YOLO format and creates symlinks 
for images organized in the proper YOLO directory structure. It handles the 
complexities of the ultralytics convert_coco function which may create output 
in various subdirectories.

Key Features:
- Converts COCO JSON annotations to YOLO format using ultralytics
- Automatically detects where convert_coco places the output files
- Creates proper image symlinks organized by dataset splits (train/val/test)
- Supports keypoint annotations and class mapping options
- Handles various output directory structures from different ultralytics versions

The tool will:
1. Run ultralytics convert_coco to generate YOLO format labels
2. Automatically detect the actual output location (handles 'data2', 'VOC_dataset', etc.)
3. Create symlinks from your flat image directory to the proper YOLO structure
4. Organize images into train/val/test subdirectories matching the labels

Usage:
    poetry run coco-to-yolo \\
        --input-dir ./path/to/coco/annotations \\
        --output-dir ./path/to/yolo/output \\
        --images-dir ./path/to/flat/images \\
        --use-keypoints \\
        --cls91to80

Example with typical paths:
    poetry run coco-to-yolo \\
        --input-dir /data/coco/annotations \\
        --output-dir /data/yolo/dataset \\
        --images-dir /data/coco/images \\
        --use-keypoints
"""

import argparse
from pathlib import Path

from ultralytics.data.converter import convert_coco


def create_image_symlinks(labels_root: Path, images_root: Path, target_root: Path):
    """
    Create symlinks for images based on the YOLO label structure.

    Args:
        labels_root: Path to the directory containing YOLO label subdirectories (train, val, etc.)
        images_root: Path to the flat directory containing all source images
        target_root: Path to the target directory where image symlinks will be created

    Returns:
        dict: Statistics about symlink creation
    """
    print("🔗 Creating image symlinks...")
    print(f"   Labels directory: {labels_root}")
    print(f"   Source images: {images_root}")
    print(f"   Target directory: {target_root}")

    stats = {
        "subdirs_found": 0,
        "symlinks_created": 0,
        "symlinks_existed": 0,
        "images_not_found": 0,
        "errors": 0,
    }

    found_label_subdirs = False
    for label_subdir in labels_root.glob("*"):
        if not label_subdir.is_dir():
            continue
        found_label_subdirs = True
        stats["subdirs_found"] += 1
        print(f"📁 Processing split: {label_subdir.name}")

        # Create matching subdir in target images dir (train, val, etc.)
        image_subdir = target_root / label_subdir.name
        image_subdir.mkdir(parents=True, exist_ok=True)

        label_files = list(label_subdir.glob("*.txt"))
        print(f"   Found {len(label_files)} label files")

        for label_file in label_files:
            # Try multiple image extensions
            image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
            source_image_path = None

            for ext in image_extensions:
                potential_path = images_root / (label_file.stem + ext)
                if potential_path.exists():
                    source_image_path = potential_path
                    break

            if source_image_path is None:
                stats["images_not_found"] += 1
                continue

            symlink_path = image_subdir / source_image_path.name

            if source_image_path.exists():
                if not symlink_path.exists():
                    try:
                        symlink_path.symlink_to(source_image_path)
                        stats["symlinks_created"] += 1
                    except Exception as e:
                        print(
                            f"❌ Error creating symlink {symlink_path} -> {source_image_path}: {e}"
                        )
                        stats["errors"] += 1
                else:
                    stats["symlinks_existed"] += 1

    if not found_label_subdirs:
        print(f"⚠️  No label subdirectories found in {labels_root}")
        print("   Expected subdirectories like 'train', 'val', 'test'")

    return stats


def find_actual_output_directory(base_output_dir: Path) -> Path:
    """
    Find the actual directory where convert_coco placed the labels.

    ultralytics convert_coco can create output in various locations depending on version:
    - Directly in the specified directory
    - In a 'VOC_dataset' subdirectory
    - In a parallel 'data2' directory

    Args:
        base_output_dir: The directory passed to convert_coco

    Returns:
        Path to the actual output directory containing 'labels' subdirectory

    Raises:
        FileNotFoundError: If no labels directory can be found
    """
    print("🔍 Searching for actual output directory...")

    # List of potential locations to check
    candidates = [
        base_output_dir,  # Direct output
        base_output_dir / "VOC_dataset",  # Common ultralytics pattern
        base_output_dir.parent / "data2",  # Alternative pattern
        base_output_dir.parent / (base_output_dir.name + "2"),  # Generic pattern
    ]

    for candidate in candidates:
        labels_dir = candidate / "labels"
        if labels_dir.exists() and labels_dir.is_dir():
            print(f"✅ Found labels directory at: {candidate}")
            return candidate

    # If not found, list what's actually in the base directory for debugging
    print("❌ Could not find 'labels' directory in any expected location.")
    print(f"Contents of {base_output_dir}:")
    if base_output_dir.exists():
        for item in base_output_dir.iterdir():
            print(f"   {item.name} ({'dir' if item.is_dir() else 'file'})")
    else:
        print("   Directory does not exist!")

    raise FileNotFoundError(
        f"Could not find 'labels' directory. Checked: {[str(c) for c in candidates]}"
    )


def convert_coco_to_yolo(
    input_dir: str,
    output_dir: str,
    images_dir: str,
    use_keypoints: bool = False,
    cls91to80: bool = False,
) -> dict:
    """
    Convert COCO format annotations to YOLO format and create image symlinks.

    Args:
        input_dir: Directory containing COCO format annotations (JSON files)
        output_dir: Directory to save YOLO format annotations
        images_dir: Flat directory containing all source images
        use_keypoints: Whether to process keypoint annotations
        cls91to80: Whether to convert 91 classes to 80 classes (COCO format)

    Returns:
        dict: Statistics about the conversion process
    """
    print("🚀 Starting COCO to YOLO conversion...")
    print(f"   Input annotations: {input_dir}")
    print(f"   Output directory: {output_dir}")
    print(f"   Source images: {images_dir}")
    print(f"   Use keypoints: {use_keypoints}")
    print(f"   Convert 91->80 classes: {cls91to80}")

    # Validate input paths
    input_path = Path(input_dir)
    images_path = Path(images_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not images_path.exists():
        raise FileNotFoundError(f"Images directory does not exist: {images_dir}")

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Run ultralytics conversion
    print("⚙️  Running ultralytics convert_coco...")
    try:
        convert_coco(
            labels_dir=str(input_path),
            save_dir=str(output_path),
            use_keypoints=use_keypoints,
            cls91to80=cls91to80,
        )
        print("✅ convert_coco completed successfully")
    except Exception as e:
        raise RuntimeError(f"convert_coco failed: {e}")

    # Find the actual output directory
    try:
        actual_output_root = find_actual_output_directory(output_path)
    except FileNotFoundError as e:
        raise RuntimeError(f"Could not locate converted labels: {e}")

    # Set up paths for symlink creation
    labels_root = actual_output_root / "labels"
    target_images_root = actual_output_root / "images"

    # Ensure target images directory exists
    target_images_root.mkdir(parents=True, exist_ok=True)

    # Create image symlinks
    symlink_stats = create_image_symlinks(labels_root, images_path, target_images_root)

    # Collect overall statistics
    stats = {
        "conversion_successful": True,
        "actual_output_directory": str(actual_output_root),
        "labels_directory": str(labels_root),
        "images_directory": str(target_images_root),
        "symlink_stats": symlink_stats,
    }

    return stats


def parse_args():
    """Parse command line arguments for the COCO to YOLO converter."""
    parser = argparse.ArgumentParser(
        description="Convert COCO format annotations to YOLO format and create image symlinks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  %(prog)s --input-dir ./coco/annotations --output-dir ./yolo/data --images-dir ./coco/images
  
  # With keypoints and class conversion
  %(prog)s --input-dir ./coco/annotations --output-dir ./yolo/data --images-dir ./coco/images --use-keypoints --cls91to80
        """,
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Directory containing COCO format annotations (JSON files)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save YOLO format annotations and images",
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        required=True,
        help="Flat directory containing all source images (supports .jpg, .jpeg, .png, .bmp, .tiff)",
    )
    parser.add_argument(
        "--use-keypoints",
        action="store_true",
        help="Process keypoint annotations (default: False)",
    )
    parser.add_argument(
        "--cls91to80",
        action="store_true",
        help="Convert COCO 91 classes to 80 classes (default: False)",
    )
    return parser.parse_args()


def main():
    """Main entry point for the COCO to YOLO converter."""
    try:
        args = parse_args()

        stats = convert_coco_to_yolo(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            images_dir=args.images_dir,
            use_keypoints=args.use_keypoints,
            cls91to80=args.cls91to80,
        )

        # Print summary statistics
        print("\n✅ Conversion completed successfully!")
        print("📊 Summary:")
        print(f"   Output directory: {stats['actual_output_directory']}")
        print(f"   Labels: {stats['labels_directory']}")
        print(f"   Images: {stats['images_directory']}")

        symlink_stats = stats["symlink_stats"]
        print(f"   Dataset splits found: {symlink_stats['subdirs_found']}")
        print(f"   Symlinks created: {symlink_stats['symlinks_created']}")
        print(f"   Symlinks already existed: {symlink_stats['symlinks_existed']}")

        if symlink_stats["images_not_found"] > 0:
            print(f"   ⚠️  Images not found: {symlink_stats['images_not_found']}")
        if symlink_stats["errors"] > 0:
            print(f"   ❌ Symlink errors: {symlink_stats['errors']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
