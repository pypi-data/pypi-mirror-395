#!/usr/bin/env python3
"""
Dataset to CAR Converter

This script converts datasets to CAR format with support for multiple modalities.
Based on the benchmark.py reference implementation.

Modalities:
- vanilla: Regular media files (audio, image, video)
- webdataset: WebDataset tar files
- hdf5: HDF5 files
- tfrecord: TFRecord files

Target modalities (independent of format):
- audio: Audio files
- image: Image files
- video: Video files

Usage:
    python dataset_to_car.py /path/to/dataset --modality vanilla --target-modality audio --output /path/to/output
    python dataset_to_car.py /path/to/webdataset --modality webdataset --target-modality image --output /path/to/output
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback
from datetime import datetime
from tqdm import tqdm
import yaml

# Add processors to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .processors.audio_codecs import AudioProcessor, AudioConfig
from .processors.image_codecs import CosmosImageProcessor, ImageConfig  
from .processors.video_codecs import CosmosVideoProcessor, VideoConfig

# File extension mappings
EXTENSIONS = {
    'vanilla': ['.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac', '.wma',  # audio
                '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif',  # image
                '.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v', '.wmv', '.flv'],  # video
    'webdataset': ['.tar', '.tar.gz', '.tar.bz2', '.tar.xz', '.tgz', '.tbz2'],
    'hdf5': ['.hdf5', '.h5', '.hdf'],
    'tfrecord': ['.tfrecord', '.tfrecords', '.tfrec']
}

# Target modality file extensions
TARGET_EXTENSIONS = {
    'audio': ['.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac', '.wma'],
    'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v', '.wmv', '.flv']
}

# Temp file suffix mapping for compound formats
TEMP_FILE_SUFFIXES = {
    'audio': '.wav',
    'image': '.png', 
    'video': '.mp4'
}

# Default config file paths
DEFAULT_CONFIG_FILES = {
    'audio': 'configs/audio_config.yaml',
    'image': 'configs/image_config.yaml', 
    'video': 'configs/video_config.yaml'
}

# Fallback configurations if YAML files are not found
def get_gpu_memory_gb() -> float:
    """Get GPU memory in GB for the current device"""
    try:
        import torch
        if torch.cuda.is_available():
            # Get memory of the current device (device 0 by default)
            memory_bytes = torch.cuda.get_device_properties(0).total_memory
            return memory_bytes / (1024**3)  # Convert to GB
    except:
        pass
    return 0.0  # CPU or unknown

def get_modality_workers_per_gpu(modality: str) -> int:
    """
    Get the recommended number of workers per GPU for different modalities,
    adaptive to GPU memory capacity
    
    Args:
        modality: Target modality ('audio', 'image', 'video')
        
    Returns:
        Number of workers that can efficiently run per GPU
    """
    gpu_memory_gb = get_gpu_memory_gb()
    
    # Base workers for different memory tiers
    if gpu_memory_gb >= 70:  # High-end GPUs (A100 80GB, H100 80GB)
        base_workers = {
            'audio': 16,  # Audio is very memory efficient
            'image': 12,  # Can handle more image processing
            'video': 8    # Even video can scale more
        }
    elif gpu_memory_gb >= 40:  # Mid-high GPUs (A100 40GB, A6000 48GB)
        base_workers = {
            'audio': 12,
            'image': 10,
            'video': 6
        }
    elif gpu_memory_gb >= 20:  # Standard GPUs (RTX 4090 24GB, V100 32GB)
        base_workers = {
            'audio': 10,
            'image': 8,
            'video': 5
        }
    elif gpu_memory_gb >= 10:  # Consumer GPUs (RTX 4080 16GB, 3080 12GB)
        base_workers = {
            'audio': 8,
            'image': 6,
            'video': 4
        }
    else:  # Lower-end or unknown GPUs
        base_workers = {
            'audio': 6,
            'image': 4,
            'video': 2
        }
    
    workers = base_workers.get(modality, 1)
    
    # Print GPU info for transparency
    if gpu_memory_gb > 0:
        print(f"🎯 Detected GPU memory: {gpu_memory_gb:.1f}GB -> {workers} workers/GPU for {modality}")
    
    return workers

def get_optimal_worker_config(target_modality: str, requested_workers: int, available_gpus: int) -> Tuple[int, List[int]]:
    """
    Calculate optimal number of workers and their GPU assignments based on modality
    
    Args:
        target_modality: Target modality ('audio', 'image', 'video')
        requested_workers: Number of workers requested by user
        available_gpus: Number of available GPUs
        
    Returns:
        Tuple of (actual_workers, gpu_assignments)
    """
    if available_gpus == 0:
        # CPU only processing
        return requested_workers, [None] * requested_workers
    
    workers_per_gpu = get_modality_workers_per_gpu(target_modality)
    max_workers = available_gpus * workers_per_gpu
    
    # Use the minimum of requested workers and what we can efficiently support
    actual_workers = min(requested_workers, max_workers)
    
    # If user requested more workers than optimal, warn them
    if requested_workers > max_workers:
        print(f"⚠️  Requested {requested_workers} workers, but {target_modality} modality supports max {max_workers} workers")
        print(f"   ({available_gpus} GPUs × {workers_per_gpu} workers/GPU = {max_workers} max workers)")
        print(f"   Using {actual_workers} workers for optimal performance")
    
    # Assign workers to GPUs
    gpu_assignments = []
    for i in range(actual_workers):
        gpu_id = i % available_gpus
        gpu_assignments.append(gpu_id)
    
    return actual_workers, gpu_assignments

# Fallback configurations if YAML files are not found
FALLBACK_CONFIGS = {
    'audio': {
        'model_name': 'facebook/encodec_32khz',
        'model_type': 'encodec',
        'output_format': 'car',
        'device': 'cuda',
        'target_sample_rate': 32000,
        'quality_threshold': 0.0
    },
    'image': {
        'model_name': 'CI8x8',
        'image_size': [224, 224],
        'maintain_aspect_ratio': False,
        'normalize_images': True,
        'checkpoint_dir': 'pretrained_ckpts',
        'device': 'cuda',
        'dtype': 'bfloat16',
        'quality_threshold': 0.0,
        'output_format': 'car'
    },
    'video': {
        'model_name': 'DV4x8x8',
        'max_frames': None,
        'frame_size': [224, 224],
        'frame_skip': 1,
        'target_fps': None,
        'normalize_frames': True,
        'checkpoint_dir': 'pretrained_ckpts',
        'device': 'cuda',
        'dtype': 'bfloat16',
        'quality_threshold': 0.0,
        'output_format': 'car'
    }
}

def find_files(folder_path: str, extensions: List[str], recursive: bool = True) -> List[str]:
    """Find all files with specified extensions in a folder"""
    files = []
    path = Path(folder_path)
    
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"
    
    for ext in extensions:
        files.extend(path.glob(f"{pattern}{ext}"))
        files.extend(path.glob(f"{pattern}{ext.upper()}"))
    
    return [str(f) for f in sorted(files)]

def load_config_from_yaml(config_path: str, target_modality: str) -> Dict[str, Any]:
    """Load configuration from YAML file with fallback to default"""
    config = FALLBACK_CONFIGS[target_modality].copy()
    
    try:
        # Try to load from provided path or default path
        if config_path:
            yaml_path = Path(config_path)
        else:
            # Use default config file relative to script location
            script_dir = Path(__file__).parent
            yaml_path = script_dir / DEFAULT_CONFIG_FILES[target_modality]
        
        if yaml_path.exists():
            with open(yaml_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    config.update(yaml_config)
                    print(f"✅ Loaded {target_modality} config from: {yaml_path}")
                else:
                    print(f"⚠️  Empty config file: {yaml_path}, using defaults")
        else:
            print(f"⚠️  Config file not found: {yaml_path}, using defaults")
            
    except Exception as e:
        print(f"❌ Error loading config from {config_path}: {e}")
        print(f"ℹ️  Using fallback configuration for {target_modality}")
    
    return config

def get_target_modality_from_file(file_path: str) -> Optional[str]:
    """Determine target modality from file extension for vanilla files"""
    ext = Path(file_path).suffix.lower()
    
    for modality, extensions in TARGET_EXTENSIONS.items():
        if ext in extensions:
            return modality
    
    return None

def find_webdataset_samples(tar_path: str, target_modality: str, max_files: Optional[int] = None) -> List[tuple]:
    """Extract samples from webdataset tar files"""
    try:
        import webdataset as wds
    except ImportError:
        print("❌ webdataset library not found. Install with: pip install webdataset")
        return []
    
    samples = []
    try:
        dataset = wds.WebDataset(tar_path)
        
        # Configure decoder based on target modality
        if target_modality == 'audio':
            dataset = dataset.to_tuple('wav;flac;mp3', 'json', handler=wds.ignore_and_continue)
        elif target_modality == 'image':
            dataset = dataset.decode('pil').to_tuple('jpg;jpeg;png', 'json', handler=wds.ignore_and_continue)
        elif target_modality == 'video':
            dataset = dataset.to_tuple('mp4;avi;mov', 'json', handler=wds.ignore_and_continue)
        else:
            print(f"❌ Unsupported target modality for webdataset: {target_modality}")
            return []
        
        # Process samples with optional early termination
        if max_files:
            # Use itertools.islice for early termination without full materialization
            import itertools
            limited_dataset = itertools.islice(dataset, max_files)
            for i, sample in enumerate(limited_dataset):
                sample_key = f"{Path(tar_path).stem}_{i:06d}"
                samples.append((sample_key, sample))
        else:
            # Process all samples
            for i, sample in enumerate(dataset):
                sample_key = f"{Path(tar_path).stem}_{i:06d}"
                samples.append((sample_key, sample))
            
    except Exception as e:
        print(f"❌ Failed to load webdataset {tar_path}: {e}")
    
    return samples

def find_hdf5_samples(hdf5_path: str, target_modality: str, max_files: Optional[int] = None) -> List[tuple]:
    """Extract samples from HDF5 files"""
    try:
        import h5py
    except ImportError:
        print("❌ h5py library not found. Install with: pip install h5py")
        return []
    
    samples = []
    try:
        with h5py.File(hdf5_path, 'r') as hdf5_file:
            # Find appropriate dataset
            dataset_names = {
                'audio': ['audio', 'waveforms', 'data', 'samples'],
                'image': ['images', 'data', 'pixels', 'frames'], 
                'video': ['videos', 'frames', 'data', 'sequences']
            }
            
            main_dataset = None
            if 'file_data' in hdf5_file:
                main_dataset = hdf5_file['file_data']
            else:
                for name in dataset_names.get(target_modality, []):
                    if name in hdf5_file:
                        main_dataset = hdf5_file[name]
                        break
            
            if main_dataset is None:
                available_keys = list(hdf5_file.keys())
                metadata_keys = ['extensions', 'metadata', 'info', 'labels', 'keys', '__key__']
                data_keys = [k for k in available_keys if k not in metadata_keys]
                if data_keys:
                    main_dataset = hdf5_file[data_keys[0]]
            
            if main_dataset is not None:
                total_samples = main_dataset.shape[0] if hasattr(main_dataset, 'shape') else len(list(main_dataset.keys()))
                
                # Sample indices if needed
                if max_files and total_samples > max_files:
                    import random
                    indices = sorted(random.sample(range(total_samples), max_files))
                else:
                    indices = list(range(total_samples))
                
                for idx in indices:
                    sample_key = f"{Path(hdf5_path).stem}_{idx:06d}"
                    samples.append((sample_key, hdf5_path, idx))
                    
    except Exception as e:
        print(f"❌ Failed to load HDF5 {hdf5_path}: {e}")
    
    return samples

def find_tfrecord_samples(tfrecord_path: str, target_modality: str, max_files: Optional[int] = None) -> List[tuple]:
    """Extract samples from TFRecord files"""
    try:
        import tensorflow as tf
    except ImportError:
        print("❌ tensorflow library not found. Install with: pip install tensorflow")
        return []
    
    samples = []
    try:
        dataset = tf.data.TFRecordDataset(tfrecord_path)
        
        if max_files:
            # Use take() for early termination without counting all records
            limited_dataset = dataset.take(max_files)
            for idx, _ in enumerate(limited_dataset):
                sample_key = f"{Path(tfrecord_path).stem}_{idx:06d}"
                samples.append((sample_key, tfrecord_path, idx))
        else:
            # Process all records
            for idx, _ in enumerate(dataset):
                sample_key = f"{Path(tfrecord_path).stem}_{idx:06d}"
                samples.append((sample_key, tfrecord_path, idx))
                
    except Exception as e:
        print(f"❌ Failed to load TFRecord {tfrecord_path}: {e}")
    
    return samples

def process_vanilla_file_worker(args):
    """Worker function for processing a single vanilla file"""
    file_path, output_dir, target_modality, config, gpu_id = args
    
    try:
        # Set GPU device if available
        if gpu_id is not None:
            import torch
            if torch.cuda.is_available():
                torch.cuda.set_device(gpu_id)
                config['device'] = f'cuda:{gpu_id}'
            else:
                config['device'] = 'cpu'
        
        # Create output path
        file_path_obj = Path(file_path)
        output_path = Path(output_dir) / f"{file_path_obj.stem}.car"
        
        # Skip if output already exists
        if output_path.exists():
            return {
                'file_path': file_path,
                'output_path': str(output_path),
                'status': 'skipped',
                'message': 'Output file already exists'
            }
        
        # Create processor based on target modality
        if target_modality == 'audio':
            audio_config = AudioConfig(**config)
            processor = AudioProcessor(audio_config)
        elif target_modality == 'image':
            image_config = ImageConfig(**config)
            processor = CosmosImageProcessor(image_config)
        elif target_modality == 'video':
            video_config = VideoConfig(**config)
            processor = CosmosVideoProcessor(video_config)
        else:
            raise ValueError(f"Unsupported target modality: {target_modality}")
        
        # Process file to CAR format
        result = processor.process_single_file(file_path, str(output_path), {})
        
        return {
            'file_path': file_path,
            'output_path': str(output_path),
            'status': 'success',
            'result': result
        }
        
    except Exception as e:
        return {
            'file_path': file_path,
            'output_path': str(output_path) if 'output_path' in locals() else 'unknown',
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def process_compound_file_worker(args):
    """Worker function for processing compound format files (webdataset, hdf5, tfrecord)"""
    sample_data, output_dir, modality, target_modality, config, gpu_id = args
    
    try:
        # Set GPU device if available
        if gpu_id is not None:
            import torch
            if torch.cuda.is_available():
                torch.cuda.set_device(gpu_id)
                config['device'] = f'cuda:{gpu_id}'
            else:
                config['device'] = 'cpu'
        
        # Extract sample information
        if modality == 'webdataset':
            sample_key, sample = sample_data
            output_path = Path(output_dir) / f"{sample_key}.car"
        elif modality in ['hdf5', 'tfrecord']:
            sample_key, file_path, index = sample_data
            output_path = Path(output_dir) / f"{sample_key}.car"
        else:
            raise ValueError(f"Unsupported compound modality: {modality}")
        
        # Skip if output already exists
        if output_path.exists():
            return {
                'sample_key': sample_key,
                'output_path': str(output_path),
                'status': 'skipped',
                'message': 'Output file already exists'
            }
        
        # Create processor based on target modality
        if target_modality == 'audio':
            audio_config = AudioConfig(**config)
            processor = AudioProcessor(audio_config)
        elif target_modality == 'image':
            image_config = ImageConfig(**config)
            processor = CosmosImageProcessor(image_config)
        elif target_modality == 'video':
            video_config = VideoConfig(**config)
            processor = CosmosVideoProcessor(video_config)
        else:
            raise ValueError(f"Unsupported target modality: {target_modality}")
        
        # Process sample to temporary file then to CAR
        import tempfile
        suffix = TEMP_FILE_SUFFIXES[target_modality]
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_path = temp_file.name
            
            # Extract data from compound format to temp file
            if modality == 'webdataset':
                # Write sample data to temp file
                if target_modality == 'audio':
                    temp_file.write(sample[0])  # Audio data is first element
                elif target_modality == 'image':
                    sample[0].save(temp_file, format='PNG')  # PIL image
                elif target_modality == 'video':
                    temp_file.write(sample[0])  # Video data
            elif modality == 'hdf5':
                import h5py
                with h5py.File(file_path, 'r') as hf:
                    # Find the main dataset and extract sample
                    main_dataset = None
                    if 'file_data' in hf:
                        main_dataset = hf['file_data']
                    else:
                        # Use first available dataset
                        keys = list(hf.keys())
                        if keys:
                            main_dataset = hf[keys[0]]
                    
                    if main_dataset is not None:
                        data = main_dataset[index]
                        temp_file.write(data.tobytes() if hasattr(data, 'tobytes') else bytes(data))
            elif modality == 'tfrecord':
                import tensorflow as tf
                dataset = tf.data.TFRecordDataset(file_path)
                for i, record in enumerate(dataset):
                    if i == index:
                        # Parse the record and extract data
                        example = tf.train.Example()
                        example.ParseFromString(record.numpy())
                        
                        # Try to find the media data in the example
                        for key, feature in example.features.feature.items():
                            if 'data' in key.lower() or target_modality in key.lower():
                                temp_file.write(feature.bytes_list.value[0])
                                break
                        break
        
        try:
            # Process temp file to CAR format
            result = processor.process_single_file(temp_path, str(output_path), {})
            
            return {
                'sample_key': sample_key,
                'output_path': str(output_path),
                'status': 'success',
                'result': result
            }
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
        
    except Exception as e:
        return {
            'sample_key': sample_data[0] if isinstance(sample_data, tuple) else 'unknown',
            'output_path': str(output_path) if 'output_path' in locals() else 'unknown',
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }

def convert_dataset_to_car(
    input_path: str,
    output_path: str, 
    modality: str,
    target_modality: str = 'audio',
    parallel: bool = True,
    num_gpus: Optional[int] = None,
    recursive: bool = True,
    max_files: Optional[int] = None,
    config_file: Optional[str] = None,
    model_config: Optional[Dict[str, Any]] = None
):
    """Convert dataset files to CAR format"""
    
    # Check CUDA availability and determine GPU count
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        available_gpus = torch.cuda.device_count() if cuda_available else 0
        
        if not parallel:
            # Sequential processing - use 1 GPU or CPU
            num_gpus = 1 if cuda_available else 0
            print("🔄 Sequential processing mode enabled")
        else:
            # Parallel processing - auto-detect or use specified GPU count
            if num_gpus is None:
                num_gpus = available_gpus if cuda_available else 1
                if cuda_available:
                    print(f"🚀 Auto-detected {num_gpus} GPUs for parallel processing")
                else:
                    print("⚠️  CUDA not available, using CPU for parallel processing")
            else:
                if not cuda_available:
                    print("⚠️  CUDA not available, falling back to CPU")
                    num_gpus = 1
                elif num_gpus > available_gpus:
                    print(f"⚠️  Requested {num_gpus} GPUs but only {available_gpus} available")
                    num_gpus = available_gpus
                else:
                    print(f"🚀 Using {num_gpus} GPUs for parallel processing")
    except ImportError:
        print("⚠️  PyTorch not available, using CPU")
        cuda_available = False
        num_gpus = 1
    
    # Validate inputs
    if not os.path.exists(input_path):
        raise ValueError(f"Input path does not exist: {input_path}")
    
    if modality not in EXTENSIONS:
        raise ValueError(f"Unsupported modality: {modality}. Supported: {list(EXTENSIONS.keys())}")
    
    if target_modality not in TARGET_EXTENSIONS:
        raise ValueError(f"Unsupported target modality: {target_modality}. Supported: {list(TARGET_EXTENSIONS.keys())}")
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    # Ensure num_gpus is at least 1
    num_gpus = max(num_gpus, 1)
    
    # Find files or samples to process
    print(f"Scanning for {modality} files in {input_path}...")
    print(f"Target modality: {target_modality}")
    
    if modality == 'vanilla':
        # Handle vanilla files - filter by target modality
        files = find_files(input_path, EXTENSIONS[modality], recursive)
        
        # Filter files by target modality
        filtered_files = []
        for file_path in files:
            file_target_modality = get_target_modality_from_file(file_path)
            if file_target_modality == target_modality:
                filtered_files.append(file_path)
        
        if max_files:
            filtered_files = filtered_files[:max_files]
        
        print(f"Found {len(filtered_files)} {target_modality} files to process")
        
        if not filtered_files:
            print("No files found to process")
            return
            
        processing_items = filtered_files
        use_compound_worker = False
        
    elif modality in ['webdataset', 'hdf5', 'tfrecord']:
        # Handle compound formats
        files = find_files(input_path, EXTENSIONS[modality], recursive)
        all_samples = []
        
        for file_path in files:
            if modality == 'webdataset':
                samples = find_webdataset_samples(file_path, target_modality, max_files)
            elif modality == 'hdf5':
                samples = find_hdf5_samples(file_path, target_modality, max_files)
            elif modality == 'tfrecord':
                samples = find_tfrecord_samples(file_path, target_modality, max_files)
            else:
                samples = []
            
            all_samples.extend(samples)
            
        if max_files and len(all_samples) > max_files:
            all_samples = all_samples[:max_files]
            
        print(f"Found {len(all_samples)} {target_modality} samples from {len(files)} {modality} files")
        
        if not all_samples:
            print("No samples found to process")
            return
            
        processing_items = all_samples
        use_compound_worker = True
    else:
        raise ValueError(f"Unknown modality: {modality}")
    
    # Load configuration from YAML file
    config = load_config_from_yaml(config_file, target_modality)
    
    # Override device setting based on CUDA availability
    if not cuda_available:
        config['device'] = 'cpu'
    
    # Override with any command-line model config
    if model_config:
        config.update(model_config)
        print(f"ℹ️  Applied {len(model_config)} command-line config overrides")
    
    # Prepare worker arguments
    worker_args = []
    gpu_assignments = []
    
    # Distribute items across GPUs
    for i, item in enumerate(processing_items):
        gpu_id = i % num_gpus if num_gpus > 0 else None
        gpu_assignments.append(gpu_id)
        if use_compound_worker:
            worker_args.append((item, output_path, modality, target_modality, config, gpu_id))
        else:
            worker_args.append((item, output_path, target_modality, config, gpu_id))
    
    # Process files
    results = []
    successful = 0
    failed = 0
    skipped = 0
    
    # Choose appropriate worker function
    worker_func = process_compound_file_worker if use_compound_worker else process_vanilla_file_worker
    
    if parallel:
        # Calculate optimal worker configuration based on target modality
        # Use number of processing items as initial requested workers, or default
        requested_workers = min(len(processing_items), num_gpus * get_modality_workers_per_gpu(target_modality))
        actual_workers, gpu_assignments = get_optimal_worker_config(target_modality, requested_workers, num_gpus if cuda_available else 0)
        
        # Only use parallel processing if we have multiple workers or multiple items
        use_parallel = actual_workers > 1 and len(processing_items) > 1
        
        if use_parallel:
            print(f"🚀 Processing {len(processing_items)} items in parallel")
            print(f"🎯 Target modality: {target_modality} ({get_modality_workers_per_gpu(target_modality)} workers/GPU)")
            print(f"🎯 Using {actual_workers} workers across {num_gpus if cuda_available else 0} GPU(s)")
            print(f"🎯 GPU assignments: {gpu_assignments}")
        else:
            print(f"🔄 Processing {len(processing_items)} items sequentially (optimal for this workload)")
        
        if use_parallel:
            # Update worker args with optimal GPU assignments
            updated_worker_args = []
            for i, args in enumerate(worker_args):
                if i < len(gpu_assignments):
                    # Replace the original gpu_id with the optimal assignment
                    if use_compound_worker:
                        item, output_path, modality, target_modality, config, _ = args
                        updated_worker_args.append((item, output_path, modality, target_modality, config, gpu_assignments[i % len(gpu_assignments)]))
                    else:
                        item, output_path, target_modality, config, _ = args
                        updated_worker_args.append((item, output_path, target_modality, config, gpu_assignments[i % len(gpu_assignments)]))
                else:
                    # For remaining items beyond optimal workers, cycle through GPU assignments
                    updated_worker_args.append(args)
            
            with ProcessPoolExecutor(max_workers=actual_workers) as executor:
                # Submit all jobs with updated worker args
                futures = [executor.submit(worker_func, args) for args in updated_worker_args]
                
                # Process results as they complete
                for future in tqdm(as_completed(futures), total=len(futures), desc="Converting files"):
                    try:
                        result = future.result()
                        results.append(result)
                        
                        if result['status'] == 'success':
                            successful += 1
                        elif result['status'] == 'error':
                            failed += 1
                            print(f"❌ Failed: {result.get('file_path', result.get('sample_key', 'unknown'))} - {result['error']}")
                        elif result['status'] == 'skipped':
                            skipped += 1
                            
                    except Exception as e:
                        failed += 1
                        print(f"❌ Unexpected error: {e}")
        else:
            # Sequential processing (but still with optimal GPU assignment for single items)
            updated_worker_args = []
            for i, args in enumerate(worker_args):
                # Even in sequential mode, assign the optimal GPU
                optimal_gpu = gpu_assignments[0] if gpu_assignments and gpu_assignments[0] is not None else None
                if use_compound_worker:
                    item, output_path, modality, target_modality, config, _ = args
                    updated_worker_args.append((item, output_path, modality, target_modality, config, optimal_gpu))
                else:
                    item, output_path, target_modality, config, _ = args
                    updated_worker_args.append((item, output_path, target_modality, config, optimal_gpu))
            
            for args in tqdm(updated_worker_args, desc="Converting files"):
                try:
                    result = worker_func(args)
                    results.append(result)
                    
                    if result['status'] == 'success':
                        successful += 1
                    elif result['status'] == 'error':
                        failed += 1
                        print(f"❌ Failed: {result.get('file_path', result.get('sample_key', 'unknown'))} - {result['error']}")
                    elif result['status'] == 'skipped':
                        skipped += 1
                        
                except Exception as e:
                    failed += 1
                    print(f"❌ Unexpected error: {e}")
    else:
        # Force sequential processing (--sequential flag used)
        print(f"🔄 Processing {len(processing_items)} items sequentially...")
        
        # Sequential processing with basic GPU assignment
        for args in tqdm(worker_args, desc="Converting files"):
            try:
                result = worker_func(args)
                results.append(result)
                
                if result['status'] == 'success':
                    successful += 1
                elif result['status'] == 'error':
                    failed += 1
                    print(f"❌ Failed: {result.get('file_path', result.get('sample_key', 'unknown'))} - {result['error']}")
                elif result['status'] == 'skipped':
                    skipped += 1
                    
            except Exception as e:
                failed += 1
                print(f"❌ Unexpected error: {e}")
    
    # Save results log
    log_file = Path(output_path) / f"conversion_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w') as f:
        json.dump({
            'input_path': input_path,
            'output_path': output_path,
            'modality': modality,
            'target_modality': target_modality,
            'config': config,
            'total_items': len(processing_items),
            'successful': successful,
            'failed': failed,
            'skipped': skipped,
            'results': results
        }, f, indent=2)
    
    # Print summary
    print(f"\n📊 Conversion Summary:")
    print(f"  Total items: {len(processing_items)}")
    print(f"  ✅ Successful: {successful}")
    print(f"  ⏭️  Skipped: {skipped}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📋 Log saved to: {log_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert dataset files to CAR format")
    parser.add_argument("input_path", help="Path to input dataset directory")
    parser.add_argument("--output", "-o", required=True, help="Output directory for CAR files")
    parser.add_argument("--modality", "-m", required=True, 
                       choices=['vanilla', 'webdataset', 'hdf5', 'tfrecord'], 
                       help="Format type to process")
    parser.add_argument("--target-modality", "-t", required=True, choices=['audio', 'image', 'video'],
                       help="Target media type (required for all modalities)")
    parser.add_argument("--parallel", action="store_true", default=True,
                       help="Enable parallel processing (default: True)")
    parser.add_argument("--sequential", action="store_true", default=False,
                       help="Force sequential processing")
    parser.add_argument("--gpus", "-g", type=int, help="Number of GPUs to use (auto-detected if not specified)")
    parser.add_argument("--recursive", "-r", action="store_true", default=False,
                       help="Search recursively in subdirectories")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to process")
    parser.add_argument("--config", "-c", help="Path to YAML configuration file")
    parser.add_argument("--model-name", help="Override model name")
    parser.add_argument("--model-type", help="Override model type (for audio: encodec, dac, snac)")
    
    args = parser.parse_args()
    
    # Determine parallelization mode
    parallel = not args.sequential and args.parallel
    
    # Build model config from arguments
    model_config = {}
    if args.model_name:
        model_config['model_name'] = args.model_name
    if args.model_type:
        model_config['model_type'] = args.model_type
    
    try:
        convert_dataset_to_car(
            input_path=args.input_path,
            output_path=args.output,
            modality=args.modality,
            target_modality=args.target_modality,
            parallel=parallel,
            num_gpus=args.gpus,
            recursive=args.recursive,
            max_files=args.max_files,
            config_file=args.config,
            model_config=model_config if model_config else None
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()