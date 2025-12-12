"""
CarLib Checkpoint Manager

Automatic checkpoint downloading and management for CarLib models.
This module handles downloading model checkpoints from a public S3 bucket,
making CarLib installation completely permissionless and friction-free.

The checkpoints are downloaded to ~/.carlib/checkpoints/ by default,
but this can be configured via environment variables.
"""

import os
import requests
import zipfile
from pathlib import Path
from typing import Dict, Optional, Union
import urllib.parse
from tqdm import tqdm

# S3 Configuration
S3_BUCKET_URL = "https://carlib-checkpoints.s3.amazonaws.com"  # Replace with your bucket URL
S3_REGION = "us-east-1"  # Replace with your bucket region

# Model registry - maps model names to their S3 keys
MODEL_REGISTRY = {
    # Continuous Video Tokenizers
    "CV4x8x8": "Cosmos-0.1-Tokenizer-CV4x8x8.zip",
    "CV8x8x8": "Cosmos-0.1-Tokenizer-CV8x8x8.zip", 
    "CV8x16x16": "Cosmos-0.1-Tokenizer-CV8x16x16.zip",
    "CV8x8x8_v1": "Cosmos-1.0-Tokenizer-CV8x8x8.zip",
    
    # Discrete Video Tokenizers
    "DV4x8x8": "Cosmos-0.1-Tokenizer-DV4x8x8.zip",
    "DV8x8x8": "Cosmos-0.1-Tokenizer-DV8x8x8.zip",
    "DV8x16x16": "Cosmos-0.1-Tokenizer-DV8x16x16.zip",
    "DV8x16x16_v1": "Cosmos-1.0-Tokenizer-DV8x16x16.zip",
    
    # Continuous Image Tokenizers  
    "CI8x8": "Cosmos-0.1-Tokenizer-CI8x8.zip",
    "CI16x16": "Cosmos-0.1-Tokenizer-CI16x16.zip",
    
    # Discrete Image Tokenizers
    "DI8x8": "Cosmos-0.1-Tokenizer-DI8x8.zip", 
    "DI16x16": "Cosmos-0.1-Tokenizer-DI16x16.zip",
}

# Model type mapping for easy lookup
MODEL_TYPES = {
    # Video models
    "CV4x8x8": "video", "CV8x8x8": "video", "CV8x16x16": "video", "CV8x8x8_v1": "video",
    "DV4x8x8": "video", "DV8x8x8": "video", "DV8x16x16": "video", "DV8x16x16_v1": "video",
    # Image models  
    "CI8x8": "image", "CI16x16": "image",
    "DI8x8": "image", "DI16x16": "image",
}

def download_with_progress(url: str, destination: Path) -> bool:
    """Download a file from URL with progress bar"""
    try:
        response = requests.head(url, timeout=30)
        if response.status_code != 200:
            return False
            
        file_size = int(response.headers.get('content-length', 0))
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            if file_size > 0:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=destination.name) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
        return True
        
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def extract_checkpoint_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract checkpoint zip file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False

class CheckpointManager:
    """Manages automatic checkpoint downloads and caching from S3"""
    
    def __init__(self, cache_dir: Optional[Union[str, Path]] = None, s3_bucket_url: Optional[str] = None):
        """
        Initialize checkpoint manager
        
        Args:
            cache_dir: Directory to store checkpoints. Defaults to ~/.carlib/checkpoints
            s3_bucket_url: Custom S3 bucket URL. Defaults to public CarLib bucket
        """
        # Cache directory with environment variable support
        if cache_dir is None:
            cache_dir = os.environ.get("CARLIB_CACHE_DIR")
            if cache_dir is None:
                # Use user's home directory by default
                self.cache_dir = Path.home() / ".carlib" / "checkpoints"
            else:
                self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(cache_dir)
            
        # Also check for legacy pretrained_ckpts directory
        self.legacy_dir = Path("pretrained_ckpts")
        
        # S3 bucket URL with environment variable support
        if s3_bucket_url is None:
            s3_bucket_url = os.environ.get("CARLIB_S3_BUCKET_URL", S3_BUCKET_URL)
        self.s3_bucket_url = s3_bucket_url
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Track downloaded models to avoid re-downloading
        self._downloaded = set()
    def _get_s3_url(self, model_name: str) -> str:
        """Get S3 download URL for a model"""
        if model_name not in MODEL_REGISTRY:
            raise ValueError(f"Unknown model: {model_name}")
            
        s3_key = MODEL_REGISTRY[model_name]
        return f"{self.s3_bucket_url}/{s3_key}"
            
    def get_checkpoint_path(self, model_name: str) -> Path:
        """
        Get the local path where a model checkpoint should be stored
        
        Args:
            model_name: Model name (e.g., 'CV8x8x8', 'CI8x8')
            
        Returns:
            Path to model checkpoint directory
        """
        # Check legacy location first (for backward compatibility)
        legacy_path = self.legacy_dir / f"Cosmos-0.1-Tokenizer-{model_name}"
        if legacy_path.exists():
            return legacy_path
            
        # Use new cache location
        return self.cache_dir / model_name
        
    def is_checkpoint_available(self, model_name: str) -> bool:
        """
        Check if a checkpoint is available locally
        
        Args:
            model_name: Model name to check
            
        Returns:
            True if checkpoint exists locally
        """
        checkpoint_path = self.get_checkpoint_path(model_name)
        return checkpoint_path.exists() and any(checkpoint_path.iterdir())
        
    def download_checkpoint(self, model_name: str, force: bool = False) -> bool:
        """
        Download a specific checkpoint from S3
        
        Args:
            model_name: Model name to download
            force: Force re-download even if already exists
            
        Returns:
            True if download successful, False otherwise
        """
        if model_name not in MODEL_REGISTRY:
            print(f"❌ Unknown model: {model_name}")
            print(f"   Available models: {list(MODEL_REGISTRY.keys())}")
            return False
            
        checkpoint_path = self.get_checkpoint_path(model_name)
        
        # Skip if already downloaded (unless forced)
        if not force and self.is_checkpoint_available(model_name):
            print(f"✅ Checkpoint {model_name} already available at {checkpoint_path}")
            return True
            
        try:
            s3_url = self._get_s3_url(model_name)
            zip_filename = MODEL_REGISTRY[model_name]
            
            print(f"📥 Downloading {model_name} from S3...")
            print(f"   URL: {s3_url}")
            print(f"   Destination: {checkpoint_path}")
            
            # Create directory
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download zip file to temporary location
            temp_zip = checkpoint_path.parent / f"{model_name}_temp.zip"
            
            if not download_with_progress(s3_url, temp_zip):
                print(f"❌ Failed to download {model_name}")
                return False
            
            # Extract zip file
            print(f"📦 Extracting {model_name}...")
            checkpoint_path.mkdir(exist_ok=True)
            
            if not extract_checkpoint_zip(temp_zip, checkpoint_path):
                print(f"❌ Failed to extract {model_name}")
                # Clean up
                temp_zip.unlink(missing_ok=True)
                if checkpoint_path.exists():
                    import shutil
                    shutil.rmtree(checkpoint_path, ignore_errors=True)
                return False
            
            # Clean up zip file
            temp_zip.unlink(missing_ok=True)
            
            # Verify extraction worked
            if not self.is_checkpoint_available(model_name):
                print(f"❌ Checkpoint extraction verification failed for {model_name}")
                return False
            
            self._downloaded.add(model_name)
            print(f"✅ Successfully downloaded and extracted {model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download {model_name}: {e}")
            # Clean up partial download
            temp_zip = checkpoint_path.parent / f"{model_name}_temp.zip"
            temp_zip.unlink(missing_ok=True)
            if checkpoint_path.exists():
                import shutil
                shutil.rmtree(checkpoint_path, ignore_errors=True)
            return False
            
    def download_all_checkpoints(self, model_type: Optional[str] = None) -> Dict[str, bool]:
        """
        Download all available checkpoints
        
        Args:
            model_type: Filter by model type ('image', 'video', or None for all)
            
        Returns:
            Dictionary mapping model names to download success status
        """
        models_to_download = []
        
        if model_type:
            models_to_download = [name for name, mtype in MODEL_TYPES.items() if mtype == model_type]
        else:
            models_to_download = list(MODEL_REGISTRY.keys())
            
        results = {}
        print(f"📦 Downloading {len(models_to_download)} checkpoints...")
        
        for model_name in models_to_download:
            results[model_name] = self.download_checkpoint(model_name)
            
        successful = sum(results.values())
        print(f"\n📊 Download Summary: {successful}/{len(models_to_download)} successful")
        
        return results
        
    def ensure_checkpoint(self, model_name: str) -> str:
        """
        Ensure a checkpoint is available, downloading if necessary
        
        Args:
            model_name: Model name to ensure is available
            
        Returns:
            Path to checkpoint directory
            
        Raises:
            RuntimeError: If checkpoint cannot be made available
        """
        if self.is_checkpoint_available(model_name):
            return str(self.get_checkpoint_path(model_name))
            
        print(f"🔄 Checkpoint {model_name} not found locally, downloading...")
        
        if not self.download_checkpoint(model_name):
            raise RuntimeError(f"Failed to download checkpoint: {model_name}")
            
        return str(self.get_checkpoint_path(model_name))
        
    def list_available_models(self) -> Dict[str, Dict[str, Union[str, bool]]]:
        """
        List all available models and their status
        
        Returns:
            Dictionary with model info and availability status
        """
        models = {}
        for model_name in MODEL_REGISTRY:
            models[model_name] = {
                "type": MODEL_TYPES.get(model_name, "unknown"),
                "s3_key": MODEL_REGISTRY[model_name],
                "s3_url": self._get_s3_url(model_name),
                "available": self.is_checkpoint_available(model_name),
                "path": str(self.get_checkpoint_path(model_name))
            }
        return models
        
    def cleanup_cache(self, keep_recent: int = 5) -> int:
        """
        Clean up old cached checkpoints
        
        Args:
            keep_recent: Number of most recently used checkpoints to keep
            
        Returns:
            Number of checkpoints removed
        """
        # This is a placeholder - could implement LRU-based cleanup
        print("ℹ️  Cache cleanup not yet implemented")
        return 0

# Global instance
_checkpoint_manager = None

def get_checkpoint_manager() -> CheckpointManager:
    """Get the global checkpoint manager instance"""
    global _checkpoint_manager
    if _checkpoint_manager is None:
        _checkpoint_manager = CheckpointManager()
    return _checkpoint_manager

def ensure_checkpoint(model_name: str) -> str:
    """
    Convenience function to ensure a checkpoint is available
    
    Args:
        model_name: Model name to ensure is available
        
    Returns:
        Path to checkpoint directory
    """
    return get_checkpoint_manager().ensure_checkpoint(model_name)

def list_models() -> Dict[str, Dict[str, Union[str, bool]]]:
    """List all available models and their status"""
    return get_checkpoint_manager().list_available_models()

def download_model(model_name: str, force: bool = False) -> bool:
    """Download a specific model"""
    return get_checkpoint_manager().download_checkpoint(model_name, force=force)

def download_all(model_type: Optional[str] = None) -> Dict[str, bool]:
    """Download all models of a specific type"""
    return get_checkpoint_manager().download_all_checkpoints(model_type=model_type)