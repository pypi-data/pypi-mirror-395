# Configuration Files

This directory contains YAML configuration files for the dataset to CAR converter.

## Configuration Files

### `audio_config.yaml`
Configuration for audio processing using AudioProcessor:
- **model_name**: Audio model to use (e.g., "facebook/encodec_32khz")  
- **model_type**: Type of audio codec ("encodec", "dac", "snac")
- **device**: Processing device ("cuda", "cpu", "auto")
- **target_sample_rate**: Target sample rate in Hz
- **max_duration**: Maximum audio duration in seconds (null for no limit)
- **quality_threshold**: Quality threshold for processing

### `image_config.yaml`
Configuration for image processing using CosmosImageProcessor:
- **model_name**: Image model to use (e.g., "CI8x8", "DI16x16")
- **image_size**: Target image dimensions [width, height]
- **maintain_aspect_ratio**: Whether to preserve aspect ratio
- **normalize_images**: Whether to normalize image values
- **checkpoint_dir**: Directory containing model checkpoints
- **device**: Processing device ("cuda", "cpu", "auto")
- **dtype**: Data type ("float32", "float16", "bfloat16")

### `video_config.yaml` 
Configuration for video processing using CosmosVideoProcessor:
- **model_name**: Video model to use (e.g., "DV4x8x8", "CV8x8x8")
- **max_frames**: Maximum frames to process (null for no limit)
- **frame_size**: Target frame dimensions [width, height]
- **frame_skip**: Process every Nth frame (1 = all frames)
- **target_fps**: Target FPS (null to maintain original)
- **normalize_frames**: Whether to normalize frame values
- **checkpoint_dir**: Directory containing model checkpoints

## Usage

### Using Default Configs
```bash
# Uses default configs from carlib/configs/ directory
python dataset_to_car.py /path/to/data --modality vanilla --target-modality audio --output /path/to/output
```

### Using Custom Config File
```bash
# Specify custom config file
python dataset_to_car.py /path/to/data --modality vanilla --target-modality audio --config /path/to/my_audio_config.yaml --output /path/to/output
```

### Command-line Overrides
```bash
# Override specific config values via command line
python dataset_to_car.py /path/to/data --modality vanilla --target-modality audio --model-name "facebook/encodec_24khz" --output /path/to/output
```

## Configuration Priority
1. Command-line arguments (highest priority)
2. Custom YAML config file (via --config)  
3. Default YAML config files
4. Built-in fallback configs (lowest priority)

## Example Custom Config

Create a custom audio config file `my_audio.yaml`:

```yaml
# High quality audio processing
model_name: "facebook/encodec_48khz"
model_type: "encodec"
device: "cuda"
target_sample_rate: 48000
max_duration: 30.0  # Process max 30 seconds
quality_threshold: 0.8
output_format: "car"

# Optional advanced settings
batch_size: 4
num_workers: 8
```

Then use it:
```bash
python dataset_to_car.py /path/to/audio --modality vanilla --target-modality audio --config my_audio.yaml --output /path/to/output
```