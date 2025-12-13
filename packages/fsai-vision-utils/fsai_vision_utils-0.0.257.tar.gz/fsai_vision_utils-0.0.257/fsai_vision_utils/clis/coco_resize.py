"""
COCO Dataset Resizer and Filter

This script resizes images in a COCO dataset while maintaining aspect ratio and filtering
annotations based on size thresholds. It's designed for computer vision datasets where
you want to:

1. Resize images to a maximum dimension while preserving aspect ratio
2. Filter images based on whether they contain annotations meeting minimum size criteria
3. Filter annotations after resizing based on visibility metrics
4. Handle keypoint annotations by scaling coordinates
5. Generate a new COCO JSON with updated annotations

Key Features:
- Filters images based on annotations with minimum width/height in ORIGINAL resolution
- Maintains aspect ratio during resizing
- Filters annotations after resizing based on minimum size thresholds
- Supports visibility metrics (min_width, min_height, min_area)
- Handles keypoint annotations (scales x,y coordinates)
- Preserves original image metadata with updated dimensions

Usage:
    poetry run coco-resize \
        --input-coco-json ./tests/data/annotations/coco.json \
        --input-image-dir ./tests/data/images/ \
        --output-images-dir ./tmp/output/resized/images \
        --output-coco-json ./tmp/output/resized/annotations/coco.json \
        --max-size 1024 \
        --min-width-for-image-selection 1024 \
        --min-height-for-image-selection 0 \
        --min-width-after-resize 10 \
        --min-height-after-resize 10 \
        --min-area-after-resize 50 \
        --num-workers 8
"""

import argparse
import concurrent.futures
import json
import os
import time
from copy import deepcopy

import cv2
from tqdm import tqdm


def process_single_image(
    img_data,
    images_dir,
    output_images_dir,
    max_size,
    min_width_for_image_selection,
    min_height_for_image_selection,
    min_width_after_resize,
    min_height_after_resize,
    min_area_after_resize,
    include_empty_images,
    annotations_by_image,
):
    """
    Process a single image: load, check if it qualifies, resize, filter annotations, and save.

    Args:
        img_data: Image metadata from COCO JSON
        images_dir: Directory containing original images
        output_images_dir: Directory to save resized images
        max_size: Maximum dimension for resized images
        min_width_for_image_selection: Minimum width in ORIGINAL resolution to include image
        min_height_for_image_selection: Minimum height in ORIGINAL resolution to include image
        min_width_after_resize: Minimum width AFTER resizing to keep annotation
        min_height_after_resize: Minimum height AFTER resizing to keep annotation
        min_area_after_resize: Minimum area AFTER resizing to keep annotation
        include_empty_images: Whether to include images with no annotations
        annotations_by_image: Dictionary mapping image ID to annotations

    Returns:
        tuple: (new_img_meta, new_annotations) or None if image should be skipped
    """
    img = img_data

    # Get annotations for this image
    anns = annotations_by_image.get(img["id"], [])

    # Pre-check: does this image contain at least one annotation meeting the selection criteria?
    qualifies_for_selection = False
    if anns:
        for ann in anns:
            x, y, w, h = ann["bbox"]
            # Check if annotation meets ORIGINAL resolution thresholds
            if (
                w >= min_width_for_image_selection
                and h >= min_height_for_image_selection
            ):
                qualifies_for_selection = True
                break

    # Skip image if it doesn't have qualifying annotations (unless including empty images)
    if not qualifies_for_selection and not include_empty_images:
        return None

    # Load the image
    img_path = os.path.join(images_dir, img["file_name"])
    image = cv2.imread(img_path)
    if image is None:
        print(f"Warning: Failed to load {img_path}")
        return None

    # Calculate resize scale to maintain aspect ratio
    height, width = image.shape[:2]
    scale = min(max_size / max(height, width), 1.0)  # Never upscale, only downscale
    new_w, new_h = round(width * scale), round(height * scale)

    # Resize the image
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Save the resized image
    output_path = os.path.join(output_images_dir, img["file_name"])
    cv2.imwrite(output_path, resized_image)

    # Create new image metadata with updated dimensions
    new_img_meta = deepcopy(img)
    new_img_meta["width"] = new_w
    new_img_meta["height"] = new_h

    # Process annotations for this image
    new_anns = []
    for ann in anns:
        x, y, w, h = ann["bbox"]

        # Scale bounding box coordinates
        w_scaled = w * scale
        h_scaled = h * scale
        area_scaled = w_scaled * h_scaled

        # Filter based on POST-RESIZE visibility metrics
        if w_scaled < min_width_after_resize:
            continue
        if h_scaled < min_height_after_resize:
            continue
        if area_scaled < min_area_after_resize:
            continue

        # Create new annotation with scaled coordinates
        new_ann = deepcopy(ann)
        new_ann["bbox"] = [x * scale, y * scale, w_scaled, h_scaled]
        new_ann["area"] = area_scaled

        # Handle keypoint annotations if present
        if "keypoints" in new_ann:
            kps = new_ann["keypoints"]
            new_kps = []
            for i in range(0, len(kps), 3):
                kp_x = kps[i] * scale  # Scale x coordinate
                kp_y = kps[i + 1] * scale  # Scale y coordinate
                v = kps[i + 2]  # Keep visibility unchanged
                new_kps += [kp_x, kp_y, v]
            new_ann["keypoints"] = new_kps

        # Update annotation metadata
        new_ann["image_id"] = new_img_meta["id"]

        new_anns.append(new_ann)

    # Return results if we have annotations or should include empty images
    if new_anns or include_empty_images:
        return (new_img_meta, new_anns)
    else:
        return None


def resize_coco_dataset(
    coco_json_path,
    images_dir,
    output_images_dir,
    output_json_path,
    max_size=1024,
    min_width_for_image_selection=1024,
    min_height_for_image_selection=0,
    min_width_after_resize=10,
    min_height_after_resize=10,
    min_area_after_resize=50,
    include_empty_images=False,
    num_workers=8,
):
    """
    Resize COCO dataset images and filter based on annotation criteria.

    Args:
        coco_json_path (str): Path to input COCO JSON annotation file
        images_dir (str): Directory containing original images
        output_images_dir (str): Directory to save resized images
        output_json_path (str): Path to save new COCO JSON with updated annotations
        max_size (int): Maximum dimension (width or height) for resized images
        min_width_for_image_selection (float): Minimum annotation width in ORIGINAL resolution
                                               to include the entire image
        min_height_for_image_selection (float): Minimum annotation height in ORIGINAL resolution
                                                to include the entire image
        min_width_after_resize (float): Minimum annotation width AFTER resizing to keep it
        min_height_after_resize (float): Minimum annotation height AFTER resizing to keep it
        min_area_after_resize (float): Minimum annotation area AFTER resizing to keep it
        include_empty_images (bool): Whether to include images with no annotations
        num_workers (int): Number of parallel workers for processing images

    Returns:
        None: Saves resized images and updated COCO JSON to specified paths
    """
    # Load the COCO annotation file
    with open(coco_json_path, "r") as f:
        coco = json.load(f)

    # Create output directory for resized images
    os.makedirs(output_images_dir, exist_ok=True)

    # Create output directory for JSON file
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Group annotations by image_id for efficient lookup
    annotations_by_image = {}
    for ann in coco["annotations"]:
        annotations_by_image.setdefault(ann["image_id"], []).append(ann)

    # Create mappings for category lookups
    category_id_to_name = {cat["id"]: cat["name"] for cat in coco["categories"]}
    category_counts = {}
    images_per_category = {}

    # Initialize lists for new dataset
    new_images = []
    new_annotations = []
    new_ann_id = 1

    # Process images in parallel using ThreadPoolExecutor
    print(f"🚀 Processing {len(coco['images'])} images using {num_workers} workers...")
    print(f"📋 Image selection criteria:")
    print(f"   - Min width (original): {min_width_for_image_selection}px")
    print(f"   - Min height (original): {min_height_for_image_selection}px")
    print(f"📋 Annotation retention criteria (after resize):")
    print(f"   - Min width: {min_width_after_resize}px")
    print(f"   - Min height: {min_height_after_resize}px")
    print(f"   - Min area: {min_area_after_resize}px²")

    start_time = time.time()
    processed_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit all image processing tasks
        futures = {
            executor.submit(
                process_single_image,
                img,
                images_dir,
                output_images_dir,
                max_size,
                min_width_for_image_selection,
                min_height_for_image_selection,
                min_width_after_resize,
                min_height_after_resize,
                min_area_after_resize,
                include_empty_images,
                annotations_by_image,
            ): img
            for img in coco["images"]
        }

        # Collect results as they complete
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Processing images",
        ):
            result = future.result()
            processed_count += 1

            if result is not None:
                new_img_meta, new_anns = result

                # Update annotation IDs and collect category counts
                image_categories = set()
                for new_ann in new_anns:
                    new_ann["id"] = new_ann_id
                    new_ann_id += 1
                    category_counts[new_ann["category_id"]] = (
                        category_counts.get(new_ann["category_id"], 0) + 1
                    )
                    image_categories.add(new_ann["category_id"])

                # Track images per category (count each image only once per category)
                for cat_id in image_categories:
                    images_per_category[cat_id] = images_per_category.get(cat_id, 0) + 1

                # Add to final dataset
                new_images.append(new_img_meta)
                new_annotations.extend(new_anns)

            # Log progress every 50 images
            if processed_count % 50 == 0:
                elapsed = time.time() - start_time
                rate = processed_count / elapsed if elapsed > 0 else 0
                print(
                    f"⚡ Processed {processed_count}/{len(coco['images'])} images at {rate:.1f} imgs/sec"
                )

    # Final timing info
    total_time = time.time() - start_time
    final_rate = len(coco["images"]) / total_time if total_time > 0 else 0
    print(f"⏱️  Total processing time: {total_time:.2f}s ({final_rate:.1f} imgs/sec)")

    # Create new COCO dataset structure
    new_coco = {
        "images": new_images,
        "annotations": new_annotations,
        "categories": coco["categories"],
    }

    # Save the new COCO JSON file
    with open(output_json_path, "w") as f:
        json.dump(new_coco, f, indent=2)

    print(f"\n✅ Done! Saved resized dataset to: {output_json_path}")
    print(f"📊 Summary:")
    print(f"   Original images: {len(coco['images'])}")
    print(f"   Kept images: {len(new_images)}")
    print(f"   Original annotations: {len(coco['annotations'])}")
    print(f"   Kept annotations: {len(new_annotations)}")

    # Print category statistics
    if category_counts:
        print("\n📊 Category counts after filtering:")
        for cat_id, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            cat_name = category_id_to_name.get(cat_id, f"ID {cat_id}")
            print(f"   {cat_name:<25} → {count} annotations")
    else:
        print("\n⚠️ No annotations passed the filter criteria.")

    # Print images per category statistics
    if images_per_category:
        print("\n📷 Images per category after filtering:")
        for cat_id, count in sorted(images_per_category.items(), key=lambda x: -x[1]):
            cat_name = category_id_to_name.get(cat_id, f"ID {cat_id}")
            print(f"   {cat_name:<25} → {count} images")
    else:
        print("\n⚠️ No images contain annotations that passed the filter criteria.")


def parse_args():
    """Parse command line arguments for the COCO resizing script."""
    parser = argparse.ArgumentParser(
        description="Resize COCO images and filter annotations"
    )
    parser.add_argument(
        "--input-coco-json", required=True, help="Path to COCO JSON file"
    )
    parser.add_argument(
        "--input-image-dir", required=True, help="Directory with original images"
    )
    parser.add_argument(
        "--output-images-dir", required=True, help="Directory to save resized images"
    )
    parser.add_argument(
        "--output-coco-json", required=True, help="Path to save new COCO JSON"
    )
    parser.add_argument(
        "--max-size", type=int, default=1024, help="Max dimension (width/height)"
    )
    parser.add_argument(
        "--min-width-for-image-selection",
        type=float,
        default=1024,
        help="Minimum annotation width (ORIGINAL resolution) to include image",
    )
    parser.add_argument(
        "--min-height-for-image-selection",
        type=float,
        default=0,
        help="Minimum annotation height (ORIGINAL resolution) to include image",
    )
    parser.add_argument(
        "--min-width-after-resize",
        type=float,
        default=10,
        help="Minimum annotation width AFTER resizing to keep annotation",
    )
    parser.add_argument(
        "--min-height-after-resize",
        type=float,
        default=10,
        help="Minimum annotation height AFTER resizing to keep annotation",
    )
    parser.add_argument(
        "--min-area-after-resize",
        type=float,
        default=50,
        help="Minimum annotation area AFTER resizing to keep annotation",
    )
    parser.add_argument(
        "--include-empty-images",
        action="store_true",
        help="Include images with no annotations",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=8,
        help="Number of parallel workers for processing images",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    resize_coco_dataset(
        coco_json_path=args.input_coco_json,
        images_dir=args.input_image_dir,
        output_images_dir=args.output_images_dir,
        output_json_path=args.output_coco_json,
        max_size=args.max_size,
        min_width_for_image_selection=args.min_width_for_image_selection,
        min_height_for_image_selection=args.min_height_for_image_selection,
        min_width_after_resize=args.min_width_after_resize,
        min_height_after_resize=args.min_height_after_resize,
        min_area_after_resize=args.min_area_after_resize,
        include_empty_images=args.include_empty_images,
        num_workers=args.num_workers,
    )


if __name__ == "__main__":
    main()
