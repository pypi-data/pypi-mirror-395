"""
CAR format loaders for PyTorch and JAX
"""
import os
import torch
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Iterator, Tuple
from torch.utils.data import Dataset, DataLoader, IterableDataset
import glob

try:
    import jax.numpy as jnp
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False
    jnp = None


class CARHandler:
    """Handler for Content Addressable aRchive (CAR) format loading"""
    
    @staticmethod
    def car_to_np(car_data: bytes) -> Tuple[Dict[str, Any], dict]:
        """
        Extract data from CAR format bytes and convert to torch tensors.
        
        Args:
            car_data: CAR format bytes
            
        Returns:
            (torch_data_dict, metadata)
        """
        import io
        import json
        import gzip
        
        try:
            # Try to decompress if gzipped
            try:
                car_data = gzip.decompress(car_data)
            except:
                pass  # Not compressed
            
            # Find the separator between metadata and data
            separator = b'\n---DATA---\n'
            if separator not in car_data:
                raise ValueError("Invalid CAR format: missing data separator")
            
            metadata_bytes, bin_data = car_data.split(separator, 1)
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            
            # Handle different format types
            if metadata.get('format') == 'direct_bytes':
                tensor_info = metadata['tensor_info']
                tensor_key = tensor_info['key']
                dtype_str = tensor_info['dtype']
                shape = tuple(tensor_info['shape'])
                
                # Reconstruct numpy array from raw bytes
                np_array = np.frombuffer(bin_data, dtype=dtype_str).reshape(shape)
                
                # Convert to contiguous torch tensor
                contiguous_array = np.ascontiguousarray(np_array)
                torch_tensor = torch.from_numpy(contiguous_array)
                
                # Create result dictionary
                torch_data = {tensor_key: torch_tensor}
                
                return torch_data, metadata
            
            else:
                # Handle torch.save format (fallback)
                data_buffer = io.BytesIO(bin_data)
                torch_data = torch.load(data_buffer, map_location='cpu')
                return torch_data, metadata
                
        except Exception as e:
            raise ValueError(f"Failed to parse CAR data: {e}")


class CARDataset(Dataset):
    """PyTorch Dataset for loading CAR files"""
    
    def __init__(
        self, 
        car_dir: str, 
        pattern: str = "*.car",
        transform: Optional[callable] = None,
        cache_in_memory: bool = False,
        modality: Optional[str] = None
    ):
        """
        Initialize CAR dataset
        
        Args:
            car_dir: Directory containing CAR files
            pattern: Glob pattern for CAR files
            transform: Optional transform function to apply to data
            cache_in_memory: Whether to cache loaded data in memory
            modality: Filter by modality (audio, image, video)
        """
        self.car_dir = Path(car_dir)
        self.transform = transform
        self.cache_in_memory = cache_in_memory
        self.modality = modality
        self._cache = {} if cache_in_memory else None
        
        # Find all CAR files
        self.car_files = list(glob.glob(str(self.car_dir / pattern)))
        
        # Filter by modality if specified
        if modality:
            filtered_files = []
            for car_file in self.car_files:
                try:
                    _, metadata = self._load_car_file(car_file)
                    if metadata.get('target_modality') == modality:
                        filtered_files.append(car_file)
                except:
                    continue  # Skip files that can't be loaded
            self.car_files = filtered_files
        
        if not self.car_files:
            raise ValueError(f"No CAR files found in {car_dir} with pattern {pattern}")
    
    def _load_car_file(self, car_path: str) -> Tuple[Dict[str, Any], dict]:
        """Load a single CAR file"""
        if self.cache_in_memory and car_path in self._cache:
            return self._cache[car_path]
        
        with open(car_path, 'rb') as f:
            car_data = f.read()
        
        data, metadata = CARHandler.car_to_np(car_data)
        
        if self.cache_in_memory:
            self._cache[car_path] = (data, metadata)
        
        return data, metadata
    
    def __len__(self) -> int:
        return len(self.car_files)
    
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        car_path = self.car_files[idx]
        data, metadata = self._load_car_file(car_path)
        
        result = {
            'data': data,
            'metadata': metadata,
            'file_path': car_path
        }
        
        if self.transform:
            result = self.transform(result)
        
        return result


class CARIterableDataset(IterableDataset):
    """PyTorch IterableDataset for streaming CAR files"""
    
    def __init__(
        self,
        car_dir: str,
        pattern: str = "*.car",
        transform: Optional[callable] = None,
        shuffle: bool = False,
        modality: Optional[str] = None
    ):
        """
        Initialize streaming CAR dataset
        
        Args:
            car_dir: Directory containing CAR files
            pattern: Glob pattern for CAR files
            transform: Optional transform function
            shuffle: Whether to shuffle files
            modality: Filter by modality (audio, image, video)
        """
        self.car_dir = Path(car_dir)
        self.pattern = pattern
        self.transform = transform
        self.shuffle = shuffle
        self.modality = modality
    
    def __iter__(self) -> Iterator[Dict[str, Any]]:
        car_files = list(glob.glob(str(self.car_dir / self.pattern)))
        
        if self.shuffle:
            import random
            random.shuffle(car_files)
        
        for car_path in car_files:
            try:
                with open(car_path, 'rb') as f:
                    car_data = f.read()
                
                data, metadata = CARHandler.car_to_np(car_data)
                
                # Filter by modality if specified
                if self.modality and metadata.get('target_modality') != self.modality:
                    continue
                
                result = {
                    'data': data,
                    'metadata': metadata,
                    'file_path': car_path
                }
                
                if self.transform:
                    result = self.transform(result)
                
                yield result
                
            except Exception as e:
                print(f"Warning: Failed to load {car_path}: {e}")
                continue


class CARLoader:
    """High-level CAR file loader with PyTorch DataLoader integration"""
    
    def __init__(
        self,
        car_dir: str,
        batch_size: int = 32,
        shuffle: bool = True,
        num_workers: int = 0,
        pattern: str = "*.car",
        transform: Optional[callable] = None,
        cache_in_memory: bool = False,
        modality: Optional[str] = None,
        streaming: bool = False
    ):
        """
        Initialize CAR loader
        
        Args:
            car_dir: Directory containing CAR files
            batch_size: Batch size for DataLoader
            shuffle: Whether to shuffle data
            num_workers: Number of worker processes
            pattern: Glob pattern for CAR files
            transform: Optional transform function
            cache_in_memory: Whether to cache data in memory
            modality: Filter by modality (audio, image, video)
            streaming: Use streaming dataset (IterableDataset)
        """
        if streaming:
            self.dataset = CARIterableDataset(
                car_dir=car_dir,
                pattern=pattern,
                transform=transform,
                shuffle=shuffle,
                modality=modality
            )
        else:
            self.dataset = CARDataset(
                car_dir=car_dir,
                pattern=pattern,
                transform=transform,
                cache_in_memory=cache_in_memory,
                modality=modality
            )
        
        self.dataloader = DataLoader(
            self.dataset,
            batch_size=batch_size,
            shuffle=shuffle if not streaming else False,
            num_workers=num_workers,
            collate_fn=self._collate_fn
        )
    
    def _collate_fn(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Custom collate function for batching CAR data"""
        # Group data by keys
        data_keys = set()
        for item in batch:
            if 'data' in item:
                data_keys.update(item['data'].keys())
        
        batched_data = {}
        for key in data_keys:
            tensors = []
            for item in batch:
                if 'data' in item and key in item['data']:
                    tensors.append(item['data'][key])
            
            if tensors:
                try:
                    # Try to stack tensors
                    batched_data[key] = torch.stack(tensors)
                except:
                    # If stacking fails, return list
                    batched_data[key] = tensors
        
        return {
            'data': batched_data,
            'metadata': [item['metadata'] for item in batch],
            'file_paths': [item['file_path'] for item in batch]
        }
    
    def __iter__(self):
        return iter(self.dataloader)
    
    def __len__(self):
        return len(self.dataloader)


if JAX_AVAILABLE:
    class JAXCARLoader:
        """JAX-compatible CAR file loader"""
        
        def __init__(
            self,
            car_dir: str,
            pattern: str = "*.car",
            modality: Optional[str] = None
        ):
            """
            Initialize JAX CAR loader
            
            Args:
                car_dir: Directory containing CAR files
                pattern: Glob pattern for CAR files
                modality: Filter by modality (audio, image, video)
            """
            self.car_dir = Path(car_dir)
            self.pattern = pattern
            self.modality = modality
            
            # Find all CAR files
            self.car_files = list(glob.glob(str(self.car_dir / pattern)))
            
            if not self.car_files:
                raise ValueError(f"No CAR files found in {car_dir} with pattern {pattern}")
        
        def load_single(self, car_path: str) -> Dict[str, Any]:
            """Load a single CAR file and convert to JAX arrays"""
            with open(car_path, 'rb') as f:
                car_data = f.read()
            
            data, metadata = CARHandler.car_to_np(car_data)
            
            # Convert PyTorch tensors to JAX arrays
            jax_data = {}
            for key, tensor in data.items():
                if isinstance(tensor, torch.Tensor):
                    numpy_array = tensor.cpu().numpy()
                    jax_data[key] = jnp.array(numpy_array)
                else:
                    jax_data[key] = jnp.array(tensor)
            
            return {
                'data': jax_data,
                'metadata': metadata,
                'file_path': car_path
            }
        
        def load_batch(self, car_paths: List[str]) -> Dict[str, Any]:
            """Load multiple CAR files as a batch"""
            batch_data = []
            batch_metadata = []
            batch_paths = []
            
            for car_path in car_paths:
                try:
                    result = self.load_single(car_path)
                    
                    # Filter by modality if specified
                    if self.modality and result['metadata'].get('target_modality') != self.modality:
                        continue
                    
                    batch_data.append(result['data'])
                    batch_metadata.append(result['metadata'])
                    batch_paths.append(result['file_path'])
                    
                except Exception as e:
                    print(f"Warning: Failed to load {car_path}: {e}")
                    continue
            
            if not batch_data:
                return {'data': {}, 'metadata': [], 'file_paths': []}
            
            # Stack data by keys
            stacked_data = {}
            data_keys = set()
            for data in batch_data:
                data_keys.update(data.keys())
            
            for key in data_keys:
                arrays = []
                for data in batch_data:
                    if key in data:
                        arrays.append(data[key])
                
                if arrays:
                    try:
                        # Try to stack arrays
                        stacked_data[key] = jnp.stack(arrays)
                    except:
                        # If stacking fails, return list
                        stacked_data[key] = arrays
            
            return {
                'data': stacked_data,
                'metadata': batch_metadata,
                'file_paths': batch_paths
            }
        
        def __iter__(self):
            """Iterate over all CAR files"""
            for car_path in self.car_files:
                try:
                    yield self.load_single(car_path)
                except Exception as e:
                    print(f"Warning: Failed to load {car_path}: {e}")
                    continue
        
        def __len__(self):
            return len(self.car_files)

else:
    class JAXCARLoader:
        """Placeholder when JAX is not available"""
        def __init__(self, car_dir, **_kwargs):
            del car_dir, _kwargs  # Suppress unused variable warnings
            raise ImportError("JAX is not available. Please install JAX to use JAXCARLoader.")


# Convenience functions
def load_car_pytorch(
    car_dir: str,
    batch_size: int = 32,
    shuffle: bool = True,
    num_workers: int = 0,
    modality: Optional[str] = None,
    **kwargs
) -> CARLoader:
    """Convenience function to create a PyTorch CAR loader"""
    return CARLoader(
        car_dir=car_dir,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        modality=modality,
        **kwargs
    )


def load_car_jax(
    car_dir: str,
    modality: Optional[str] = None,
    **kwargs
) -> 'JAXCARLoader':
    """Convenience function to create a JAX CAR loader"""
    return JAXCARLoader(
        car_dir=car_dir,
        modality=modality,
        **kwargs
    )


def load_single_car(car_path: str, framework: str = 'pytorch') -> Dict[str, Any]:
    """
    Load a single CAR file
    
    Args:
        car_path: Path to CAR file
        framework: 'pytorch' or 'jax'
    
    Returns:
        Dictionary with data, metadata, and file_path
    """
    if framework == 'pytorch':
        with open(car_path, 'rb') as f:
            car_data = f.read()
        
        data, metadata = CARHandler.car_to_np(car_data)
        
        return {
            'data': data,
            'metadata': metadata,
            'file_path': car_path
        }
    
    elif framework == 'jax':
        if not JAX_AVAILABLE:
            raise ImportError("JAX is not available")
        
        loader = JAXCARLoader(os.path.dirname(car_path))
        return loader.load_single(car_path)
    
    else:
        raise ValueError(f"Unknown framework: {framework}. Use 'pytorch' or 'jax'")