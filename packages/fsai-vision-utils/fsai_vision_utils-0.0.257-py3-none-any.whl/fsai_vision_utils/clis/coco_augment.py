# poetry run coco-augment \
#     --input-json tmp/output/resized/annotations/coco.json \
#     --input-images tmp/output/resized/images \
#     --output-json tmp/output/augmented/coco.json \
#     --output-images tmp/output/augmented/images \
#     --num-augmentations 20 \
#     --num-keypoints 2 \
#     --min-visible-keypoints 1 \
#     --visualize

import argparse
import json
import os
import uuid
from pathlib import Path

import albumentations as A
import cv2
import matplotlib.pyplot as plt
from albumentations import BboxParams, KeypointParams
from pycocotools.coco import COCO
from tqdm import tqdm


def parse_category_names(category_names_str, coco):
    if not category_names_str:
        return None
    names = []
    for part in category_names_str.split(","):
        names.extend(part.strip().split())
    names = [name.strip() for name in names if name.strip()]
    categories = coco.loadCats(coco.getCatIds())
    category_name_to_id = {cat["name"]: cat["id"] for cat in categories}
    category_ids = []
    invalid_names = []
    for name in names:
        if name in category_name_to_id:
            category_ids.append(category_name_to_id[name])
        else:
            invalid_names.append(name)
    if invalid_names:
        available_names = list(category_name_to_id.keys())
        raise ValueError(
            f"Invalid category names: {invalid_names}. Available categories: {available_names}"
        )
    return category_ids


def normalize_keypoints(keypoints, expected_num_keypoints):
    """
    Normalize keypoints by padding them to the expected number.

    Args:
        keypoints: List of keypoints in [x1, y1, v1, x2, y2, v2, ...] format
        expected_num_keypoints: Expected number of keypoints per annotation

    Returns:
        Normalized keypoints list padded with (0.0, 0.0, 0) entries
    """
    if len(keypoints) % 3 != 0:
        raise ValueError(
            f"Keypoints must be in groups of 3 (x, y, v), got {len(keypoints)} values"
        )

    current_num_keypoints = len(keypoints) // 3

    if current_num_keypoints >= expected_num_keypoints:
        # If we have enough or more keypoints, truncate to expected number
        return keypoints[: expected_num_keypoints * 3]
    else:
        # Pad with dummy keypoints (0.0, 0.0, 0)
        padding_needed = expected_num_keypoints - current_num_keypoints
        padding = [0.0, 0.0, 0] * padding_needed
        return keypoints + padding


def track_keypoints_through_transformation(
    original_keypoints,
    transformed_keypoints,
    transformed_visibilities,
    expected_num_keypoints,
):
    """
    Track keypoints through albumentations transformation and ensure proper ordering.

    Args:
        original_keypoints: Original keypoints in [x1, y1, v1, x2, y2, v2, ...] format
        transformed_keypoints: Transformed keypoints from albumentations
        transformed_visibilities: Transformed visibilities from albumentations
        expected_num_keypoints: Expected number of keypoints

    Returns:
        Properly ordered keypoints array with correct length
    """
    # Convert to list of (x, y, v) tuples for easier manipulation
    original_kps = []
    for i in range(0, len(original_keypoints), 3):
        original_kps.append(
            (
                original_keypoints[i],
                original_keypoints[i + 1],
                original_keypoints[i + 2],
            )
        )

    # Convert transformed keypoints to list of (x, y, v) tuples
    transformed_kps = []
    for i, (x, y) in enumerate(transformed_keypoints):
        v = transformed_visibilities[i] if i < len(transformed_visibilities) else 0
        transformed_kps.append((x, y, v))

    # Create result array with expected length
    result = []

    # First pass: try to match keypoints in order with strict distance threshold
    used_transformed_indices = set()
    matched_positions = {}  # Track which original position each transformed keypoint matched to

    for i in range(expected_num_keypoints):
        if i < len(original_kps):
            orig_x, orig_y, orig_v = original_kps[i]

            # Find the transformed keypoint that best matches this original position
            best_match = None
            best_distance = float("inf")
            best_index = -1

            for j, (trans_x, trans_y, trans_v) in enumerate(transformed_kps):
                if j in used_transformed_indices:
                    continue

                # Calculate distance between original and transformed
                distance = ((orig_x - trans_x) ** 2 + (orig_y - trans_y) ** 2) ** 0.5

                # Use stricter threshold for initial matching
                if distance < best_distance and distance < 500:  # Stricter threshold
                    best_distance = distance
                    best_match = (trans_x, trans_y, trans_v)
                    best_index = j

            if best_match:
                result.extend(best_match)
                used_transformed_indices.add(best_index)
                matched_positions[best_index] = i
            else:
                result.extend([0.0, 0.0, 0])
        else:
            result.extend([0.0, 0.0, 0])

    # Second pass: handle remaining transformed keypoints that weren't matched
    # These might be keypoints that got shifted significantly but are still valid
    remaining_transformed = []
    for j, (trans_x, trans_y, trans_v) in enumerate(transformed_kps):
        if j not in used_transformed_indices:
            remaining_transformed.append((j, trans_x, trans_y, trans_v))

    # Find positions that still have dummy keypoints and try to fill them
    for j, trans_x, trans_y, trans_v in remaining_transformed:
        # Find the closest dummy position
        best_position = -1
        best_distance = float("inf")

        for i in range(expected_num_keypoints):
            if i < len(result) // 3:
                # Check if this position has a dummy keypoint
                idx = i * 3
                if (
                    result[idx] == 0.0
                    and result[idx + 1] == 0.0
                    and result[idx + 2] == 0
                ):
                    # This is a dummy position, calculate distance to original
                    if i < len(original_kps):
                        orig_x, orig_y, _ = original_kps[i]
                        distance = (
                            (orig_x - trans_x) ** 2 + (orig_y - trans_y) ** 2
                        ) ** 0.5
                        if (
                            distance < best_distance and distance < 1000
                        ):  # More lenient threshold
                            best_distance = distance
                            best_position = i

        # If we found a good position, replace the dummy keypoint
        if best_position >= 0:
            idx = best_position * 3
            result[idx : idx + 3] = [trans_x, trans_y, trans_v]

    return result


def get_expected_keypoints_per_category(categories, default_num_keypoints):
    """
    Get the expected number of keypoints for each category.
    If category has keypoints info, use that; otherwise use default.

    Args:
        categories: List of category dictionaries from COCO
        default_num_keypoints: Default number of keypoints to use

    Returns:
        Dictionary mapping category_id to expected number of keypoints
    """
    category_keypoints = {}
    for cat in categories:
        cat_id = cat["id"]
        # Check if category has keypoints configuration
        if "keypoints" in cat and isinstance(cat["keypoints"], list):
            category_keypoints[cat_id] = len(cat["keypoints"])
        else:
            category_keypoints[cat_id] = default_num_keypoints
    return category_keypoints


def validate_keypoint_consistency(annotations, category_keypoints):
    """
    Validate that all annotations have consistent keypoint counts.

    Args:
        annotations: List of annotation dictionaries
        category_keypoints: Dictionary mapping category_id to expected keypoint count

    Returns:
        Dictionary with validation results
    """
    validation_results = {}
    inconsistencies = []

    for ann in annotations:
        cat_id = ann["category_id"]
        expected_kps = category_keypoints.get(cat_id, 2)  # Default to 2
        actual_kps = len(ann["keypoints"]) // 3

        if actual_kps != expected_kps:
            inconsistencies.append(
                {
                    "annotation_id": ann["id"],
                    "category_id": cat_id,
                    "expected": expected_kps,
                    "actual": actual_kps,
                }
            )

    validation_results["total_annotations"] = len(annotations)
    validation_results["inconsistent_annotations"] = len(inconsistencies)
    validation_results["inconsistencies"] = inconsistencies

    return validation_results


def parse_args():
    parser = argparse.ArgumentParser(
        description="Augment COCO dataset (bboxes + keypoints) and output new COCO JSON."
    )
    parser.add_argument(
        "--input-json", required=True, help="Path to input COCO annotations JSON"
    )
    parser.add_argument(
        "--input-images", required=True, help="Path to folder with input images"
    )
    parser.add_argument("--output-json", required=True, help="Path to output COCO JSON")
    parser.add_argument(
        "--output-images",
        required=True,
        help="Path to folder where augmented images will be saved",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Show debug visualization for each augmented image",
    )
    parser.add_argument(
        "--max-visualize",
        type=int,
        default=5,
        help="Maximum number of images to visualize (default: 5, set to -1 for unlimited)",
    )
    parser.add_argument(
        "--min-visible-keypoints",
        type=int,
        default=1,
        help="Minimum number of visible keypoints required to keep annotation",
    )
    parser.add_argument(
        "--category-names",
        type=str,
        help="Only process images that have at least one annotation from these category names.",
    )
    parser.add_argument(
        "--num-augmentations",
        type=int,
        default=1,
        help="Number of augmented copies to generate per image",
    )
    parser.add_argument(
        "--num-keypoints",
        type=int,
        default=2,
        help="Expected number of keypoints per annotation (used as fallback if not specified in categories)",
    )
    return parser.parse_args()


def create_transform():
    return A.Compose(
        [
            A.HorizontalFlip(p=0.8),
            A.VerticalFlip(p=0.8),
            A.RandomRotate90(p=0.8),
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.8),
            A.HueSaturationValue(
                hue_shift_limit=2, sat_shift_limit=5, val_shift_limit=5, p=0.5
            ),
            A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), p=0.4),
            A.GaussNoise(
                std_range=(0.01, 0.03), mean_range=(0.0, 0.0), per_channel=False, p=0.5
            ),
            A.GaussianBlur(blur_limit=(3, 5), p=0.4),
            A.ElasticTransform(alpha=1.0, sigma=50.0, alpha_affine=5.0, p=0.7),
        ],
        bbox_params=BboxParams(
            format="coco", label_fields=["category_ids"], min_visibility=0.0
        ),
        keypoint_params=KeypointParams(
            format="xy", label_fields=["keypoint_visibilities"], remove_invisible=False
        ),
    )


def clip_bbox(bbox, img_width, img_height):
    x, y, w, h = bbox
    x = max(0, min(x, img_width - 1))
    y = max(0, min(y, img_height - 1))
    w = max(1, min(w, img_width - x))
    h = max(1, min(h, img_height - y))
    return [x, y, w, h]


def clip_keypoints(kps, img_width, img_height, visibility):
    clipped = []
    for (x, y), v in zip(kps, visibility):
        if 0 <= x < img_width and 0 <= y < img_height:
            clipped.append((round(x, 2), round(y, 2), int(v)))
        else:
            clipped.append(
                (
                    round(max(0, min(x, img_width - 1)), 2),
                    round(max(0, min(y, img_height - 1)), 2),
                    0,
                )
            )
    return clipped


def visualize_debug(image, annotations_data, title="Augmented Sample"):
    """
    Visualize all annotations on a single image.

    Args:
        image: The image to visualize
        annotations_data: List of tuples (bbox, keypoints, annotation_info)
        title: Title for the plot
    """
    img = image.copy()
    colors = [
        (0, 255, 0),
        (255, 0, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
    ]

    for i, (bbox, keypoints, ann_info) in enumerate(annotations_data):
        color = colors[i % len(colors)]

        # Draw bounding box
        x, y, w, h = map(int, bbox)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

        # Draw annotation label
        label = (
            f"Ann {i + 1} (vis: {ann_info['visible_kps']}/{ann_info['expected_kps']})"
        )
        cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Draw keypoints
        for j in range(0, len(keypoints), 3):
            xk, yk, v = int(keypoints[j]), int(keypoints[j + 1]), keypoints[j + 2]
            if v > 0:
                cv2.circle(img, (xk, yk), 4, color, -1)
            else:
                cv2.circle(img, (xk, yk), 2, (128, 128, 128), -1)

    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"{title} - {len(annotations_data)} annotations")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    args = parse_args()
    os.makedirs(args.output_images, exist_ok=True)

    coco = COCO(args.input_json)
    target_category_ids = parse_category_names(args.category_names, coco)
    transform = create_transform()

    new_images = []
    new_annotations = []
    categories = coco.loadCats(coco.getCatIds())

    # Get expected keypoints per category
    category_keypoints = get_expected_keypoints_per_category(
        categories, args.num_keypoints
    )

    image_id_counter = 1
    annotation_id_counter = 1

    total_original_annotations = 0
    total_augmented_annotations = 0
    included_images = 0
    skipped_images = 0
    skipped_annotations = 0
    keypoint_padding_stats = {}  # Track keypoint padding statistics
    visualized_images = 0  # Track how many images have been visualized

    for img_id in tqdm(coco.getImgIds()):
        img_info = coco.loadImgs([img_id])[0]
        img_path = os.path.join(args.input_images, img_info["file_name"])
        image = cv2.imread(img_path)

        if image is None:
            print(f"Warning: failed to load image {img_path}")
            skipped_images += 1
            continue

        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)

        if not anns:
            continue

        if target_category_ids is not None:
            has_target_category = any(
                ann.get("category_id") in target_category_ids for ann in anns
            )
            if not has_target_category:
                continue

        valid_anns = []
        for ann in anns:
            if "bbox" not in ann or "keypoints" not in ann:
                skipped_annotations += 1
                continue
            bbox = ann["bbox"]
            if None in bbox or any(v is None for v in bbox) or len(bbox) != 4:
                skipped_annotations += 1
                continue
            kp = ann["keypoints"]
            if len(kp) % 3 != 0:
                skipped_annotations += 1
                continue
            kp_xy = [(kp[i], kp[i + 1]) for i in range(0, len(kp), 3)]
            if any(
                None in kp_coord or any(v is None for v in kp_coord)
                for kp_coord in kp_xy
            ):
                skipped_annotations += 1
                continue

            # Normalize keypoints for this annotation
            cat_id = ann["category_id"]
            expected_kps = category_keypoints.get(cat_id, args.num_keypoints)
            try:
                normalized_kp = normalize_keypoints(kp, expected_kps)
                ann["normalized_keypoints"] = normalized_kp

                # Debug info for keypoint padding
                original_kps = len(kp) // 3
                if original_kps < expected_kps:
                    print(
                        f"Padded keypoints for category {cat_id}: {original_kps} -> {expected_kps}"
                    )
                    # Track padding statistics
                    if cat_id not in keypoint_padding_stats:
                        keypoint_padding_stats[cat_id] = {"padded": 0, "total": 0}
                    keypoint_padding_stats[cat_id]["padded"] += 1

                if cat_id not in keypoint_padding_stats:
                    keypoint_padding_stats[cat_id] = {"padded": 0, "total": 0}
                keypoint_padding_stats[cat_id]["total"] += 1

                valid_anns.append(ann)
            except ValueError as e:
                print(
                    f"Warning: Skipping annotation due to keypoint normalization error: {e}"
                )
                skipped_annotations += 1
                continue

        if not valid_anns:
            continue

        for _ in range(args.num_augmentations):
            # Collect all annotations for this image
            bboxes = []
            category_ids = []
            all_keypoints = []
            all_keypoint_vis = []
            keypoint_counts = []

            for ann in valid_anns:
                bboxes.append(ann["bbox"])
                category_ids.append(ann["category_id"])
                kp = ann["normalized_keypoints"]  # Use normalized keypoints
                kp_xy = [(kp[i], kp[i + 1]) for i in range(0, len(kp), 3)]
                kp_v = [kp[i + 2] for i in range(0, len(kp), 3)]
                all_keypoints.extend(kp_xy)
                all_keypoint_vis.extend(kp_v)
                keypoint_counts.append(len(kp_xy))

            total_original_annotations += len(bboxes)

            # Apply transformation to the entire image with all annotations
            try:
                transformed = transform(
                    image=image,
                    bboxes=bboxes,
                    keypoints=all_keypoints,
                    category_ids=category_ids,
                    keypoint_visibilities=all_keypoint_vis,
                )
            except Exception as e:
                print(
                    f"Skipping image {img_info['file_name']} due to transform error: {e}"
                )
                skipped_images += 1
                continue

            if not transformed["bboxes"] or not transformed["keypoints"]:
                skipped_images += 1
                continue

            original_stem = Path(img_info["file_name"]).stem.replace(" ", "_")
            extension = Path(img_info["file_name"]).suffix
            short_uid = uuid.uuid4().hex[:8]
            new_filename = f"{original_stem}_augmented_{short_uid}{extension}"
            new_img_path = os.path.join(args.output_images, new_filename)
            cv2.imwrite(new_img_path, transformed["image"])

            height, width = transformed["image"].shape[:2]
            annotations_created = 0
            visualization_data = []  # Collect data for visualization

            # Reconstruct annotations from transformed data
            kp_idx = 0
            for i, (bbox, cat_id, n_kps) in enumerate(
                zip(transformed["bboxes"], category_ids, keypoint_counts)
            ):
                # Get the expected number of keypoints for this category
                expected_kps = category_keypoints.get(cat_id, args.num_keypoints)

                # Get the original normalized keypoints for this annotation
                original_kp = valid_anns[i]["normalized_keypoints"]

                # Get available transformed keypoints
                available_kps = min(n_kps, len(transformed["keypoints"]) - kp_idx)
                kp_xy = transformed["keypoints"][kp_idx : kp_idx + available_kps]
                kp_v = transformed["keypoint_visibilities"][
                    kp_idx : kp_idx + available_kps
                ]
                kp_idx += n_kps

                bbox = clip_bbox(bbox, width, height)

                # Use keypoint tracking to ensure proper ordering and length
                flat_kps = track_keypoints_through_transformation(
                    original_kp, kp_xy, kp_v, expected_kps
                )

                # Count visible keypoints
                visible_kps = 0
                for j in range(0, len(flat_kps), 3):
                    if flat_kps[j + 2] > 0:  # visibility > 0
                        visible_kps += 1

                # Debug output for keypoint tracking
                original_visible = sum(
                    1 for j in range(0, len(original_kp), 3) if original_kp[j + 2] > 0
                )
                if visible_kps != original_visible:
                    print(
                        f"Keypoint tracking: annotation {annotation_id_counter}, category {cat_id}: visible {original_visible} -> {visible_kps}"
                    )

                # Additional debug: show keypoint matching details
                if len(kp_xy) > 0:
                    original_kps_count = len(original_kp) // 3
                    transformed_kps_count = len(kp_xy)
                    if original_kps_count != transformed_kps_count:
                        print(
                            f"Keypoint count mismatch: annotation {annotation_id_counter}, original: {original_kps_count}, transformed: {transformed_kps_count}"
                        )

                # Final validation: ensure keypoints array has correct length
                if len(flat_kps) != expected_kps * 3:
                    print(
                        f"ERROR: Annotation {annotation_id_counter} has incorrect keypoint length: {len(flat_kps)} != {expected_kps * 3}"
                    )
                    skipped_annotations += 1
                    continue

                if visible_kps < args.min_visible_keypoints:
                    skipped_annotations += 1
                    continue

                # Collect data for visualization
                if args.visualize:
                    visualization_data.append(
                        (
                            bbox,
                            flat_kps,
                            {
                                "visible_kps": visible_kps,
                                "expected_kps": expected_kps,
                                "category_id": cat_id,
                            },
                        )
                    )

                new_annotations.append(
                    {
                        "id": annotation_id_counter,
                        "image_id": image_id_counter,
                        "category_id": cat_id,
                        "bbox": [round(c, 2) for c in bbox],
                        "area": round(bbox[2] * bbox[3], 2),
                        "iscrowd": 0,
                        "keypoints": flat_kps,
                        "num_keypoints": expected_kps,  # Use expected number of keypoints for consistency
                    }
                )
                annotation_id_counter += 1
                total_augmented_annotations += 1
                annotations_created += 1

            # Show visualization for this image (all annotations together)
            if args.visualize and visualization_data:
                # Check if we should visualize this image
                should_visualize = (
                    args.max_visualize == -1 or visualized_images < args.max_visualize
                )

                if should_visualize:
                    visualize_debug(
                        transformed["image"],
                        visualization_data,
                        title=f"{img_info['file_name']} augmented",
                    )
                    visualized_images += 1
                elif visualized_images == args.max_visualize:
                    print(
                        f"Reached visualization limit of {args.max_visualize} images. Use --max-visualize -1 to see all."
                    )

            if annotations_created > 0:
                new_images.append(
                    {
                        "id": image_id_counter,
                        "file_name": new_filename,
                        "height": height,
                        "width": width,
                    }
                )
                image_id_counter += 1
                included_images += 1
            else:
                skipped_images += 1

    new_coco = {
        "images": new_images,
        "annotations": new_annotations,
        "categories": categories,
    }

    with open(args.output_json, "w") as f:
        json.dump(new_coco, f)

    print("\n✅ Done. Augmented dataset saved to:")
    print(f"- JSON: {args.output_json}")
    print(f"- Images: {args.output_images}")
    print("\n📊 Statistics:")
    print(f"- Original annotations: {total_original_annotations}")
    print(f"- Augmented annotations: {total_augmented_annotations}")
    print(
        f"- Retention rate: {total_augmented_annotations / total_original_annotations * 100:.1f}%"
    )
    print(f"- Included images: {included_images}")
    print(f"- Skipped images: {skipped_images}")
    print(f"- Skipped annotations: {skipped_annotations}")

    # Print keypoint padding statistics
    if keypoint_padding_stats:
        print("\n🔑 Keypoint Normalization Statistics:")
        for cat_id, stats in keypoint_padding_stats.items():
            cat_name = next(
                (cat["name"] for cat in categories if cat["id"] == cat_id),
                f"Category {cat_id}",
            )
            padding_rate = (
                (stats["padded"] / stats["total"] * 100) if stats["total"] > 0 else 0
            )
            print(
                f"- {cat_name} (ID: {cat_id}): {stats['padded']}/{stats['total']} annotations padded ({padding_rate:.1f}%)"
            )

    # Validate keypoint consistency
    validation_results = validate_keypoint_consistency(
        new_annotations, category_keypoints
    )
    print("\n✅ Keypoint Consistency Validation:")
    print(f"- Total annotations: {validation_results['total_annotations']}")
    print(
        f"- Inconsistent annotations: {validation_results['inconsistent_annotations']}"
    )
    if validation_results["inconsistent_annotations"] > 0:
        print(
            f"⚠️  Warning: Found {validation_results['inconsistent_annotations']} annotations with inconsistent keypoint counts!"
        )
        for inc in validation_results["inconsistencies"][
            :5
        ]:  # Show first 5 inconsistencies
            print(
                f"  - Annotation {inc['annotation_id']} (Category {inc['category_id']}): expected {inc['expected']}, got {inc['actual']}"
            )
        if len(validation_results["inconsistencies"]) > 5:
            print(f"  ... and {len(validation_results['inconsistencies']) - 5} more")
    else:
        print("✅ All annotations have consistent keypoint counts!")


if __name__ == "__main__":
    main()
