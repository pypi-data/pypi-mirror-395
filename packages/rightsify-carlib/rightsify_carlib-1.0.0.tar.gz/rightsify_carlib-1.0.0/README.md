# CarLib - Efficient ML Training with CAR Format

CarLib is a comprehensive Python library and CLI tool for neural network training with compressed datasets. It provides dataset conversion to CAR (Compressed ARchive) format, efficient data loaders, and decode utilities for ML workflows.

## Quick Start

### Installation
```bash
cd carlib
pip install -e .[all]  # Install with all format support
# or
./install.sh          # Automated installation
```

### Basic Usage

**Converting datasets:**
```bash
# Convert audio files
carlib convert /path/to/audio --modality vanilla --target-modality audio -o /output

# Convert WebDataset with auto-detected GPUs in parallel
carlib convert /path/to/data.tar --modality webdataset --target-modality image -o /output

# Convert with specific number of GPUs
carlib convert /path/to/data.tar --modality webdataset --target-modality image --gpus 4 -o /output

# Use custom configuration
carlib convert /path/to/data --modality vanilla --target-modality video --config my_config.yaml -o /output
```

**Loading CAR files for ML training:**
```python
import carlib

# PyTorch Dataset for training
dataset = carlib.CARDataset("/path/to/car/files", modality="audio")
loader = carlib.CARLoader(dataset, batch_size=32, shuffle=True)

for batch in loader:
    # Access encoded tokens/features for training
    audio_codes = batch['data']['codes']      # Shape: [batch, seq_len]
    metadata = batch['metadata']              # List of metadata dicts
    
    # Train your model on encoded representations
    loss = model(audio_codes)

# JAX loader for JAX-based training
jax_loader = carlib.load_car_jax("/path/to/car/files", modality="audio")
for item in jax_loader:
    tokens = item['data']['tokens']  # JAX arrays for training

# Load single CAR file
single_data = carlib.load_single_car("/path/to/file.car")
```

## Supported Formats

### Input Formats
- **vanilla**: Regular media files on filesystem
- **webdataset**: WebDataset tar archives (.tar, .tar.gz, etc.)
- **hdf5**: HDF5 data files (.hdf5, .h5, .hdf)
- **tfrecord**: TensorFlow record files (.tfrecord, .tfrecords)

### Target Modalities
- **audio**: Audio files (.wav, .mp3, .flac, .m4a, .ogg, .aac)
- **image**: Image files (.jpg, .png, .webp, .bmp, .tiff, .gif)
- **video**: Video files (.mp4, .avi, .mov, .mkv, .webm, .wmv)

## CLI Commands

### Convert Datasets
```bash
carlib convert INPUT_PATH --modality {vanilla,webdataset,hdf5,tfrecord} --target-modality {audio,image,video} -o OUTPUT_PATH
```

**Required Arguments:**
- `INPUT_PATH`: Path to input dataset directory or file
- `--modality, -m`: Input format type
- `--target-modality, -t`: Target media type  
- `--output, -o`: Output directory for CAR files

**Optional Arguments:**
- `--config, -c`: Custom YAML configuration file
- `--parallel`: Enable parallel processing (default: True)
- `--sequential`: Force sequential processing
- `--gpus, -g`: Number of GPUs to use (auto-detected if not specified)
- `--max-files`: Maximum files to process
- `--model-name`: Override model name
- `--model-type`: Override model type (encodec, dac, snac for audio)
- `--recursive/-r`: Search recursively (default: True)
- `--verbose, -v`: Verbose output

### Configuration Management
```bash
carlib config list                    # List available configurations
carlib config show audio             # Show audio configuration
carlib config create audio -o my.yaml # Create custom config template
carlib config validate config.yaml   # Validate configuration file
```

### System Information
```bash
carlib info                          # Show system info and dependencies
carlib validate file1.car file2.car # Validate CAR files
```

## Configuration

CarLib uses YAML files to configure processing parameters. Each target modality has default settings that can be customized.

### Default Configurations

**Audio** (`configs/audio_config.yaml`):
```yaml
model_name: "facebook/encodec_32khz"
model_type: "encodec"
device: "cuda"
target_sample_rate: 32000
max_duration: null
quality_threshold: 0.0
output_format: "car"
```

**Image** (`configs/image_config.yaml`):
```yaml
model_name: "CI8x8"
image_size: [224, 224]
maintain_aspect_ratio: false
normalize_images: true
checkpoint_dir: "pretrained_ckpts"
device: "cuda"
dtype: "bfloat16"
quality_threshold: 0.0
output_format: "car"
```

**Video** (`configs/video_config.yaml`):
```yaml
model_name: "DV4x8x8"
max_frames: null
frame_size: [224, 224]
frame_skip: 1
target_fps: null
normalize_frames: true
checkpoint_dir: "pretrained_ckpts"
device: "cuda"
dtype: "bfloat16"
quality_threshold: 0.0
output_format: "car"
```

### Creating Custom Configurations

1. **Create a template:**
```bash
carlib config create audio -o my_audio_config.yaml
```

2. **Edit the configuration:**
```yaml
# High-quality audio processing
model_name: "facebook/encodec_48khz"
model_type: "encodec"
device: "cuda"
target_sample_rate: 48000
max_duration: 60.0  # Process max 60 seconds
quality_threshold: 0.7
output_format: "car"
```

3. **Use the custom config:**
```bash
carlib convert /audio/data --modality vanilla --target-modality audio --config my_audio_config.yaml -o /output
```

### Configuration Priority
Settings are applied in this order (highest to lowest priority):
1. Command-line arguments 
2. Custom config file (--config)
3. Default config files
4. Built-in fallbacks

## Python API

### Dataset Conversion
```python
from carlib import convert_dataset_to_car, load_config_from_yaml

# Basic conversion
convert_dataset_to_car(
    input_path="/path/to/dataset",
    output_path="/path/to/output",
    modality="vanilla",
    target_modality="audio",
    parallel=True,  # Enable parallel processing (default)
    num_gpus=None   # Auto-detect GPUs (or specify: num_gpus=2)
)

# With custom configuration
config = load_config_from_yaml("my_config.yaml", "audio")
convert_dataset_to_car(
    input_path="/path/to/dataset", 
    output_path="/path/to/output",
    modality="vanilla",
    target_modality="audio",
    parallel=True,
    config_file="my_config.yaml"
)
```

### ML Training with CAR Data
```python
import carlib
import torch
from torch.utils.data import DataLoader

# Create PyTorch dataset
dataset = carlib.CARDataset(
    car_dir="/path/to/car/files",
    modality="audio",           # Filter by modality
    cache_in_memory=False       # Set True for small datasets
)

# Create DataLoader for training
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    collate_fn=dataset._collate_fn  # Custom batching
)

# Training loop
model = YourModel()
optimizer = torch.optim.Adam(model.parameters())

for epoch in range(num_epochs):
    for batch in dataloader:
        # Access encoded data (compressed tokens/features)
        encoded_data = batch['data']
        
        # Different modalities have different keys:
        if 'codes' in encoded_data:          # Audio (EnCodec/DAC/SNAC)
            tokens = encoded_data['codes']    # Shape: [batch, seq_len] or [batch, n_q, seq_len]
        elif 'tokens' in encoded_data:       # Image/Video (Cosmos)
            tokens = encoded_data['tokens']   # Shape: [batch, h, w] or [batch, frames, h, w]
        
        # Train on compressed representations
        logits = model(tokens)
        loss = criterion(logits, targets)
        
        optimizer.zero_grad()
        loss.backward() 
        optimizer.step()
```

### Advanced Dataset Usage
```python
# Streaming dataset for large datasets
streaming_dataset = carlib.CARIterableDataset(
    car_dir="/path/to/large/dataset", 
    shuffle=True,
    modality="image"
)

# Custom collate function for variable-length sequences
def custom_collate(batch):
    # Handle variable sequence lengths
    sequences = [item['data']['codes'] for item in batch]
    padded = torch.nn.utils.rnn.pad_sequence(sequences, batch_first=True)
    
    return {
        'data': {'codes': padded},
        'metadata': [item['metadata'] for item in batch],
        'lengths': [len(seq) for seq in sequences]
    }

dataloader = DataLoader(dataset, collate_fn=custom_collate)
```

### JAX Training Support
```python
import carlib
import jax
import jax.numpy as jnp

# JAX loader for JAX-based models
jax_loader = carlib.JAXCARLoader("/path/to/car/files", modality="audio")

# Training with JAX
for batch_paths in batched_car_files:
    batch_data = jax_loader.load_batch(batch_paths)
    tokens = batch_data['data']['tokens']  # JAX arrays
    
    # JAX training step
    params, loss = train_step(params, tokens, targets)
```

### Validation/Decoding (Separate from Training)
```python
import carlib

# Only decode for validation/visualization - NOT during training
decoder = carlib.CARDecoder(device="cuda")

# Decode validation samples to evaluate quality
val_sample = "/path/to/validation_sample.car"
decoded_result = decoder.decode_car(val_sample, save_decoded=True)
original_audio = decoded_result['decoded_data']  # Waveform tensor

# Or decode model generations for evaluation
model_output = model.generate(input_tokens)
decoded_output = decoder.decode_data(
    encoded_data=model_output,
    target_modality="audio", 
    output_path="generated_sample.wav"
)
```

## Examples

### Audio Processing
```bash
# Convert MP3 collection to CAR
carlib convert /music/collection --modality vanilla --target-modality audio -o /output/cars

# High-quality audio with custom settings and specific GPU count
carlib convert /audio/dataset --modality vanilla --target-modality audio \
  --model-name "facebook/encodec_48khz" --gpus 4 -o /output

# Sequential processing (single GPU/CPU)
carlib convert /audio/dataset --modality vanilla --target-modality audio \
  --model-name "facebook/encodec_48khz" --sequential -o /output

# Process WebDataset audio archives
carlib convert /datasets/audio.tar --modality webdataset --target-modality audio \
  --max-files 10000 -o /output
```

### Image Processing
```bash
# Convert image directory
carlib convert /images/dataset --modality vanilla --target-modality image -o /output/cars

# High-resolution image processing with auto-detected GPUs
carlib convert /images --modality vanilla --target-modality image \
  --config high_res_config.yaml -o /output

# High-resolution with specific GPU count
carlib convert /images --modality vanilla --target-modality image \
  --config high_res_config.yaml --gpus 8 -o /output

# Process HDF5 image dataset
carlib convert /data/images.hdf5 --modality hdf5 --target-modality image -o /output
```

### Video Processing  
```bash
# Convert video files
carlib convert /videos/dataset --modality vanilla --target-modality video -o /output

# Process with frame sampling
carlib convert /videos --modality vanilla --target-modality video \
  --config frame_sampling_config.yaml --max-files 500 -o /output

# Process TFRecord video dataset with auto-detected GPUs
carlib convert /data/videos.tfrecord --modality tfrecord --target-modality video -o /output

# Process with specific GPU count
carlib convert /data/videos.tfrecord --modality tfrecord --target-modality video \
  --gpus 4 -o /output
```

### Batch Processing
```python
# Process multiple datasets
import os
from carlib import convert_dataset_to_car

datasets = [
    ("/data/audio1", "audio"),
    ("/data/images1", "image"), 
    ("/data/videos1", "video")
]

for i, (dataset_path, target_modality) in enumerate(datasets):
    output_path = f"/output/batch_{i}"
    os.makedirs(output_path, exist_ok=True)
    
    convert_dataset_to_car(
        input_path=dataset_path,
        output_path=output_path,
        modality="vanilla", 
        target_modality=target_modality,
        parallel=True,
        num_gpus=2,  # Or None for auto-detect
        max_files=1000
    )
```

## Model Options

### Audio Models
- **EnCodec**: `facebook/encodec_32khz`, `facebook/encodec_24khz`, `facebook/encodec_48khz`
- **DAC**: Set `model_type: "dac"` and `model_name: "dac_44khz"`, `"dac_24khz"`, etc.  
- **SNAC**: Set `model_type: "snac"` and appropriate model name

### Image Models
- **Cosmos Image**: `CI8x8`, `DI16x16`, etc.
- Custom checkpoint directory via `checkpoint_dir` setting

### Video Models  
- **Cosmos Video**: `CV8x8x8`, `DV8x16x16`, `DV4x8x8`, etc.
- Custom checkpoint directory via `checkpoint_dir` setting

## Performance Tips

### Multi-GPU Usage
```bash
# Auto-detect and use all available GPUs (default)
carlib convert /large/dataset --modality vanilla --target-modality audio -o /output

# Specify exact number of GPUs
carlib convert /large/dataset --modality vanilla --target-modality audio --gpus 8 -o /output

# Force sequential processing (single GPU/CPU)
carlib convert /large/dataset --modality vanilla --target-modality audio --sequential -o /output
```

### Memory Management
- Use `max_files` to limit memory usage for large datasets
- Adjust `batch_size` in config files for memory constraints
- Use `dtype: "float16"` for lower memory usage

### Processing Optimization
- Set `max_duration` for audio to skip very long files
- Use `frame_skip` for video to reduce processing time
- Enable `quality_threshold` to filter low-quality inputs

## Dependencies

### Required
- torch >= 1.9.0
- torchaudio >= 0.9.0
- transformers >= 4.20.0
- PyYAML >= 5.4.0
- tqdm >= 4.60.0

### Optional (install with `pip install -e .[all]`)
- webdataset >= 0.2.0 (for WebDataset support)
- h5py >= 3.0.0 (for HDF5 support)  
- tensorflow >= 2.8.0 (for TFRecord support)

## Troubleshooting

### Common Issues

**"carlib command not found"**
```bash
# Ensure installation completed
pip install -e .[all]
# Add to PATH if needed
export PATH=$PATH:$(python -m site --user-base)/bin
```

**"CUDA out of memory"**
- Reduce `--gpus` parameter
- Set `max_files` to process in smaller batches
- Use `dtype: "float16"` in config

**"Config file not found"**
```bash
# Check available configs
carlib config list
# Create custom config
carlib config create audio -o my_config.yaml
```

**"No files found"**
- Check input path exists
- Verify file extensions match target modality
- Use `--verbose` for detailed scanning info

### Getting Help
```bash
carlib --help                    # General help
carlib convert --help           # Conversion options
carlib config --help            # Configuration help
carlib info                     # System information
```

## License

MIT License - see LICENSE file for details.