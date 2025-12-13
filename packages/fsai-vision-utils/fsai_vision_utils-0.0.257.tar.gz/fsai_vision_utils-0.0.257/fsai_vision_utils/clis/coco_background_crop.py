import argparse
import concurrent.futures
import json
import os
import random
import time

from PIL import Image

MAX_WORKERS = 20


def format_progress_bar(completed, total, width=50):
    """
    Create a text-based progress bar.

    Args:
        completed (int): Number of completed items
        total (int): Total number of items
        width (int): Width of the progress bar in characters

    Returns:
        str: Formatted progress bar string
    """
    if total == 0:
        return "[" + "=" * width + "] 100.0%"

    progress = completed / total
    filled_width = int(width * progress)
    bar = "=" * filled_width + "-" * (width - filled_width)
    percentage = progress * 100

    return f"[{bar}] {percentage:5.1f}%"


def format_time_elapsed(seconds):
    """Format elapsed time in a human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def estimate_time_remaining(completed, total, elapsed_time):
    """Estimate time remaining based on current progress."""
    if completed == 0 or completed >= total:
        return "N/A"

    rate = completed / elapsed_time
    remaining_items = total - completed
    remaining_time = remaining_items / rate

    return format_time_elapsed(remaining_time)


def is_valid_image(image_path, min_file_size=100):
    """
    Check if an image file is valid and not corrupted/zero'd out.

    Args:
        image_path (str): Path to the image file
        min_file_size (int): Minimum file size in bytes (default: 100 bytes)

    Returns:
        bool: True if image is valid, False otherwise
    """
    try:
        # Check if file exists and has reasonable size
        if not os.path.exists(image_path):
            return False

        file_size = os.path.getsize(image_path)
        if file_size < min_file_size:
            return False

        # Open and check the image
        with Image.open(image_path) as img:
            # Check if image has valid dimensions
            width, height = img.size
            if width <= 0 or height <= 0:
                return False

            # Convert to RGB to check if image has actual content
            rgb_img = img.convert("RGB")

            # Sample pixels to check for completely black images (zero'd out)
            sample_pixels = []
            step_x = max(1, width // 10)
            step_y = max(1, height // 10)

            for x in range(0, width, step_x):
                for y in range(0, height, step_y):
                    if x < width and y < height:
                        sample_pixels.append(rgb_img.getpixel((x, y)))

            # Only reject if image is completely black (zero'd out)
            if len(sample_pixels) > 0:
                black_count = sum(1 for p in sample_pixels if p == (0, 0, 0))
                # Reject if more than 95% of pixels are black
                if black_count / len(sample_pixels) > 0.95:
                    return False

        return True

    except Exception as e:
        print(f"Image validation failed for {image_path}: {e}")
        return False


def process_single_image(args):
    """
    Process a single image for parallel execution.
    Args is a tuple containing all the necessary parameters.
    """
    (
        img_info,
        input_dir,
        output_dir,
        crops_per_image,
        crop_width,
        crop_height,
        starting_image_id,
    ) = args

    file_name = img_info["file_name"]
    # Try full relative path first
    candidate_path = os.path.join(input_dir, file_name)
    if not os.path.isfile(candidate_path):
        # Fallback: just use basename
        base_name = os.path.basename(file_name)
        candidate_path = os.path.join(input_dir, base_name)

    if not os.path.isfile(candidate_path):
        print(f"WARNING: could not find image file for {file_name}, skipping.")
        return [], 0

    base_name = os.path.basename(candidate_path)
    base_no_ext, ext = os.path.splitext(base_name)

    crops, _ = random_crops_for_image(
        candidate_path,
        base_no_ext,
        ext,
        crops_per_image,
        crop_width,
        crop_height,
        output_dir,
        starting_image_id,
    )

    return crops, len(crops)


def random_crops_for_image(
    img_path,
    base_name_no_ext,
    ext,
    crops_per_image,
    crop_width,
    crop_height,
    output_dir,
    starting_image_id,
):
    """
    Generate random crops for a single image and return:
      - list of new COCO image dicts
      - next available image id
    """
    # Check if all crops for this image already exist
    existing_crops = []
    all_exist = True

    for i in range(crops_per_image):
        new_filename = (
            f"{base_name_no_ext}_background_{i + 1:03d}_{crop_width}x{crop_height}{ext}"
        )
        out_path = os.path.join(output_dir, new_filename)

        if os.path.exists(out_path):
            # Validate existing image before adding to list
            if is_valid_image(out_path):
                existing_crops.append(
                    {
                        "id": starting_image_id + i,
                        "file_name": new_filename,
                        "width": crop_width,
                        "height": crop_height,
                    }
                )
            else:
                # Remove invalid existing image
                print(f"Removing invalid existing crop: {new_filename}")
                try:
                    os.remove(out_path)
                except OSError as e:
                    print(f"Failed to remove invalid image {out_path}: {e}")
                all_exist = False
                break
        else:
            all_exist = False
            break

    # If all crops already exist, return them without processing
    if all_exist:
        print(f"Skipping {img_path}: all {crops_per_image} crops already exist")
        return existing_crops, starting_image_id + crops_per_image

    image = Image.open(img_path)
    width, height = image.size

    if width < crop_width or height < crop_height:
        print(f"Skipping {img_path}: smaller than crop size ({width}x{height})")
        return [], starting_image_id

    new_images = []
    image_id = starting_image_id

    for i in range(crops_per_image):
        new_filename = (
            f"{base_name_no_ext}_background_{i + 1:03d}_{crop_width}x{crop_height}{ext}"
        )
        out_path = os.path.join(output_dir, new_filename)

        # Skip if this specific crop already exists and is valid
        if os.path.exists(out_path):
            if is_valid_image(out_path):
                print(f"Skipping existing valid crop: {new_filename}")
                new_images.append(
                    {
                        "id": image_id,
                        "file_name": new_filename,
                        "width": crop_width,
                        "height": crop_height,
                    }
                )
                image_id += 1
                continue
            else:
                # Remove invalid existing image and recreate it
                print(f"Removing and recreating invalid crop: {new_filename}")
                try:
                    os.remove(out_path)
                except OSError as e:
                    print(f"Failed to remove invalid image {out_path}: {e}")

        max_x = width - crop_width
        max_y = height - crop_height

        left = 0 if max_x == 0 else random.randint(0, max_x)
        top = 0 if max_y == 0 else random.randint(0, max_y)

        right = left + crop_width
        bottom = top + crop_height

        crop = image.crop((left, top, right, bottom))
        crop.save(out_path)

        # Validate the saved image before adding to COCO JSON
        if is_valid_image(out_path):
            new_images.append(
                {
                    "id": image_id,
                    "file_name": new_filename,
                    "width": crop_width,
                    "height": crop_height,
                }
            )
        else:
            # Remove invalid saved image
            print(f"Generated invalid crop, removing: {new_filename}")
            try:
                os.remove(out_path)
            except OSError as e:
                print(f"Failed to remove invalid generated image {out_path}: {e}")

        image_id += 1

    return new_images, image_id


def build_background_coco(
    coco_input_path,
    input_dir,
    output_dir,
    coco_output_path,
    crops_per_image,
    crop_size,
    seed=None,
    num_workers=MAX_WORKERS,
):
    if seed is not None:
        random.seed(seed)

    os.makedirs(output_dir, exist_ok=True)

    with open(coco_input_path, "r") as f:
        coco = json.load(f)

    input_images = coco.get("images", [])

    new_images = []
    next_image_id = 1

    # Optional: carry over some metadata if present
    new_coco = {
        "info": coco.get("info", {}),
        "licenses": coco.get("licenses", []),
        "images": new_images,
        "annotations": [],
        "categories": [],
    }

    crop_width, crop_height = crop_size

    total_images = len(input_images)
    print(f"Processing {total_images} images in parallel with {num_workers} workers...")
    print(
        f"Target: {crops_per_image} crops per image ({total_images * crops_per_image} total crops)"
    )
    print()

    # Prepare arguments for parallel processing
    # We'll assign image IDs sequentially after processing to avoid conflicts
    args_list = []
    current_image_id = next_image_id
    for img in input_images:
        args_list.append(
            (
                img,
                input_dir,
                output_dir,
                crops_per_image,
                crop_width,
                crop_height,
                current_image_id,
            )
        )
        current_image_id += crops_per_image  # Reserve IDs for this image's crops

    # Process images in parallel
    start_time = time.time()
    total_crops_generated = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        future_to_img = {
            executor.submit(process_single_image, args): args[0] for args in args_list
        }

        completed = 0
        for future in concurrent.futures.as_completed(future_to_img):
            img_info = future_to_img[future]
            try:
                crops, num_crops = future.result()
                new_images.extend(crops)
                completed += 1
                total_crops_generated += num_crops

                # Calculate timing
                elapsed_time = time.time() - start_time
                eta = estimate_time_remaining(completed, total_images, elapsed_time)

                # Enhanced progress update
                progress_bar = format_progress_bar(completed, total_images)
                elapsed_str = format_time_elapsed(elapsed_time)

                print(
                    f"{progress_bar} {completed:4d}/{total_images} images | "
                    f"Crops: {total_crops_generated:5d} | "
                    f"Time: {elapsed_str} | ETA: {eta} | "
                    f"Current: {os.path.basename(img_info['file_name'])} ({num_crops} crops)"
                )

            except Exception as exc:
                print(f"ERROR processing {img_info['file_name']}: {exc}")
                completed += 1

    # Update next_image_id for consistency (though not used after this point)
    next_image_id = current_image_id

    # Final completion summary
    total_elapsed = time.time() - start_time
    print()
    print("=" * 80)
    print("PROCESSING COMPLETE!")
    print("=" * 80)
    print(f"📊 Images processed:     {completed:,} / {total_images:,}")
    print(f"🖼️  Crops generated:     {len(new_images):,}")
    print(f"⏱️  Total time:          {format_time_elapsed(total_elapsed)}")
    print(f"🚀 Processing rate:     {completed / total_elapsed:.1f} images/sec")
    if len(new_images) > 0:
        print(
            f"📈 Crop generation rate: {len(new_images) / total_elapsed:.1f} crops/sec"
        )
    print(f"📁 Output directory:     {output_dir}")
    print(f"📄 COCO JSON file:       {coco_output_path}")
    print("=" * 80)

    with open(coco_output_path, "w") as f:
        json.dump(new_coco, f, indent=2)

    print("✅ New COCO file successfully written!")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate random background crops from COCO images "
        "and create a new COCO JSON with only image entries."
    )
    parser.add_argument(
        "--input-coco-json",
        type=str,
        required=True,
        help="Path to input COCO JSON file.",
    )
    parser.add_argument(
        "--input-image-dir",
        type=str,
        required=True,
        help="Directory containing the original images.",
    )
    parser.add_argument(
        "--output-images-dir",
        type=str,
        required=True,
        help="Directory to save cropped images.",
    )
    parser.add_argument(
        "--output-coco-json",
        type=str,
        required=True,
        help="Path to save the new COCO JSON file.",
    )
    parser.add_argument(
        "--crops-per-image",
        type=int,
        default=1,
        help="Number of random crops to generate per input image.",
    )
    parser.add_argument(
        "--crop-size",
        type=int,
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        default=[2048, 2048],
        help="Crop size as WIDTH HEIGHT (default: 2048 2048).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (optional).",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Number of parallel workers for processing (default: {MAX_WORKERS}).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    build_background_coco(
        coco_input_path=args.input_coco_json,
        input_dir=args.input_image_dir,
        output_dir=args.output_images_dir,
        coco_output_path=args.output_coco_json,
        crops_per_image=args.crops_per_image,
        crop_size=tuple(args.crop_size),
        seed=args.seed,
        num_workers=args.num_workers,
    )


if __name__ == "__main__":
    main()
