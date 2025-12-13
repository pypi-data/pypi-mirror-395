import argparse
import os

from detectron2 import model_zoo
from detectron2.config import get_cfg


def main():
    parser = argparse.ArgumentParser(description="Generate Detectron2 config file")
    parser.add_argument(
        "--config-file",
        type=str,
        default="COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml",
        help="Config file name from model zoo (e.g., 'COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml')",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default="./tmp/output_configs",
        help="Output directory path for the generated config file",
    )

    args = parser.parse_args()

    config_file = args.config_file
    output_dir = args.output_path

    config_file_base_name = config_file.split("/")[-1].split(".")[0]

    # Load and modify config
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(config_file))

    # Write to YAML file
    output_yaml_path = os.path.join(output_dir, f"{config_file_base_name}.yaml")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_yaml_path, "w") as f:
        f.write(cfg.dump())  # `dump()` returns a string in YAML format

    print(f"Config file generated: {output_yaml_path}")


if __name__ == "__main__":
    main()
