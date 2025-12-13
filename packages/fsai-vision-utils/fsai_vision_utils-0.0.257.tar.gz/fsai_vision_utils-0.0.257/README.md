# fsai-vision-utils

A comprehensive collection of computer vision utilities and CLI tools for COCO dataset processing, image manipulation, and machine learning workflows.

## 🚀 Installation

```shell
poetry add fsai-vision-utils
```

## 📋 Overview

This package provides a suite of command-line tools designed to streamline computer vision workflows, particularly for COCO format datasets. Whether you're preparing data for training, augmenting datasets, or analyzing annotations, these tools offer efficient, parallelized solutions for common computer vision tasks.

## 🛠️ Available CLI Tools

### Data Processing & Manipulation
- **[aws-batch-download](docs/cli/aws-batch-download.md)** - Download multiple files from S3 with multi-threading and retry logic
- **[coco-resize](docs/cli/coco-resize.md)** - Resize COCO dataset images while maintaining aspect ratio and filtering annotations
- **[coco-slice-dataset](docs/cli/coco-slice-dataset.md)** - Slice large images into smaller tiles for training or inference
- **[coco-background-crop](docs/cli/coco-background-crop.md)** - Generate random background crops from COCO images for negative samples

### Data Augmentation & Enhancement
- **[coco-augment](docs/cli/coco-augment.md)** - Apply data augmentation to COCO datasets with bounding boxes and keypoints

### Dataset Management
- **[coco-merge](docs/cli/coco-merge.md)** - Merge multiple COCO datasets into a single unified dataset
- **[coco-split](docs/cli/coco-split.md)** - Split COCO datasets into train/validation/test sets with stratification
- **[coco-remap](docs/cli/coco-remap.md)** - Remap COCO category IDs to be contiguous starting from 0 or 1

### Analysis & Visualization
- **[coco-analyze-dimensions](docs/cli/coco-analyze-dimensions.md)** - Analyze object dimensions and size distributions with comprehensive statistics and visualizations
- **[coco-count-annotations-by-category](docs/cli/coco-count-annotations-by-category.md)** - Count and analyze annotations by category across multiple COCO files
- **[coco-visualize](docs/cli/coco-visualize.md)** - Visualize COCO datasets using FiftyOne for interactive exploration

### Model Configuration & Deployment
- **[detectron-config](docs/cli/detectron-config.md)** - Generate Detectron2 configuration files from model zoo templates
- **[detectron-strip](docs/cli/detectron-strip.md)** - Extract model weights from Detectron2 checkpoints for deployment

## 🎯 Quick Start Examples

### Basic Dataset Processing Pipeline

```bash
# 1. Download images from S3
aws-batch-download --ids_txt_file image_ids.txt --aws_path s3://bucket/images --output_path ./images

# 2. Resize images and filter annotations
coco-resize --input-coco-json annotations.json --input-image-dir ./images --output-images-dir ./resized --output-coco-json ./resized/annotations.json --max-size 1024

# 3. Augment the dataset
coco-augment --input-json ./resized/annotations.json --input-images ./resized --output-json ./augmented/annotations.json --output-images ./augmented --num-augmentations 5

# 4. Split into train/val/test sets
coco-split --input-coco-json ./augmented/annotations.json --output-coco-dir ./splits --train-ratio 0.7 --val-ratio 0.15 --test-ratio 0.15
```

### Large Image Processing

```bash
# Slice large images into manageable tiles
coco-slice-dataset --input-coco-json large_images.json --image-dir ./large_images --output-dir ./sliced --slice-height 1024 --slice-width 1024 --overlap-height-ratio 0.2 --overlap-width-ratio 0.2
```

### Dataset Analysis

```bash
# Analyze object dimensions and size distributions
coco-analyze-dimensions --input-coco-json annotations.json --output-stats ./dimension_report.txt

# Count annotations by category
coco-count-annotations-by-category train.json val.json test.json --individual

# Visualize dataset interactively
coco-visualize --image-dir ./images --input-coco-json annotations.json --dataset-name "my_dataset"
```

## 🔧 Key Features

### Performance & Scalability
- **Multi-threading/Multi-processing**: All tools support parallel processing for optimal performance
- **Memory Efficient**: Designed to handle large datasets without excessive memory usage
- **Progress Tracking**: Real-time progress bars and statistics for long-running operations

### Robustness & Reliability
- **Error Handling**: Graceful handling of corrupted files and invalid annotations
- **Retry Logic**: Automatic retry mechanisms for network operations
- **Validation**: Built-in validation for COCO format compliance

### Flexibility & Customization
- **Configurable Parameters**: Extensive command-line options for fine-tuning behavior
- **Format Support**: Support for various image formats (JPG, PNG, etc.)
- **Extensible**: Modular design allows for easy extension and customization

## 📚 Documentation

Each CLI tool has detailed documentation with usage examples, parameter descriptions, and best practices:

- [AWS Batch Download](docs/cli/aws-batch-download.md)
- [COCO Analyze Dimensions](docs/cli/coco-analyze-dimensions.md)
- [COCO Augment](docs/cli/coco-augment.md)
- [COCO Background Crop](docs/cli/coco-background-crop.md)
- [COCO Count Annotations by Category](docs/cli/coco-count-annotations-by-category.md)
- [COCO Merge](docs/cli/coco-merge.md)
- [COCO Remap](docs/cli/coco-remap.md)
- [COCO Resize](docs/cli/coco-resize.md)
- [COCO Slice Dataset](docs/cli/coco-slice-dataset.md)
- [COCO Split](docs/cli/coco-split.md)
- [COCO Visualize](docs/cli/coco-visualize.md)
- [Detectron Config](docs/cli/detectron-config.md)
- [Detectron Strip](docs/cli/detectron-strip.md)

## 🏗️ Architecture

The package is organized into several key components:

```
fsai_vision_utils/
├── clis/           # Command-line interface implementations
├── libs/           # Core library functions
│   ├── sahi/       # SAHI (Slicing Aided Hyper Inference) utilities
│   └── ensemble_model/  # Model ensemble utilities
└── __init__.py
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on how to submit pull requests, report issues, and suggest improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Homepage**: https://github.com/fsai-dev/fsai-vision-utils
- **Repository**: https://github.com/fsai-dev/fsai-vision-utils
- **Issues**: https://github.com/fsai-dev/fsai-vision-utils/issues

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/) for detailed usage instructions
2. Search existing [issues](https://github.com/fsai-dev/fsai-vision-utils/issues) for similar problems
3. Create a new issue with a detailed description of your problem
