import json
from pathlib import Path
import argparse


def remap_coco_category_ids(input_json_path, output_json_path, start_id=0):
    # Load the original COCO JSON
    with open(input_json_path, "r") as f:
        coco = json.load(f)

    # Create a mapping from old category IDs to new ones
    original_categories = coco["categories"]
    id_mapping = {
        cat["id"]: new_id + start_id for new_id, cat in enumerate(original_categories)
    }

    # Update the categories with new contiguous IDs
    new_categories = []
    for new_id, cat in enumerate(original_categories):
        new_cat = cat.copy()
        new_cat["id"] = new_id + start_id
        new_categories.append(new_cat)
    coco["categories"] = new_categories

    # Update all annotations with the new category IDs
    for ann in coco["annotations"]:
        old_id = ann["category_id"]
        ann["category_id"] = id_mapping[old_id]

    # Save the updated COCO JSON
    with open(output_json_path, "w") as f:
        json.dump(coco, f, indent=2)

    print(f"✅ Category IDs remapped and saved to: {output_json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remap COCO category IDs to be contiguous."
    )
    parser.add_argument(
        "--input-coco-json",
        "-i",
        default="coco.json",
        help="Path to input COCO JSON file",
    )
    parser.add_argument(
        "--output-coco-json",
        "-o",
        default="coco_remapped.json",
        help="Path to output COCO JSON file",
    )
    parser.add_argument(
        "--start-id",
        "-s",
        type=int,
        choices=[0, 1],
        default=1,
        help="Starting ID for category mapping (0 or 1)",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    Path(args.output_coco_json).parent.mkdir(parents=True, exist_ok=True)

    remap_coco_category_ids(args.input_coco_json, args.output_coco_json, args.start_id)
