"""
Transform functions for CarLib datasets

This module provides transform functions that can be used with CAR datasets,
including decode transforms for automatic decoding during data loading.
"""
from typing import Dict, Any, Optional, Callable


class DecodeTransform:
    """
    Transform that decodes CAR data during loading
    
    This is the recommended way to add decoding to datasets - as a transform
    rather than built into the loader itself.
    """
    
    def __init__(self, device: str = "cuda", save_decoded: bool = False):
        """
        Initialize decode transform
        
        Args:
            device: Device to use for decoding ("cuda" or "cpu")
            save_decoded: Whether to save decoded files (not recommended for datasets)
        """
        self.device = device
        self.save_decoded = save_decoded
        self._decoder = None
    
    def _get_decoder(self):
        """Lazy initialization of decoder"""
        if self._decoder is None:
            from .decode import CARDecoder
            self._decoder = CARDecoder(device=self.device)
        return self._decoder
    
    def __call__(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply decode transform to a dataset item
        
        Args:
            item: Dataset item with 'data', 'metadata', 'file_path'
            
        Returns:
            Item with added 'decoded_data' field
        """
        try:
            decoder = self._get_decoder()
            target_modality = item['metadata'].get('target_modality')
            
            if target_modality:
                decoded_result = decoder.decode_data(
                    encoded_data=item['data'],
                    target_modality=target_modality,
                    save_decoded=self.save_decoded
                )
                item['decoded_data'] = decoded_result['decoded_data']
            else:
                item['decoded_data'] = None
                
        except Exception as e:
            print(f"Warning: Failed to decode {item.get('file_path', 'unknown')}: {e}")
            item['decoded_data'] = None
        
        return item


class ModalityFilter:
    """Filter transform to only return items of specific modality"""
    
    def __init__(self, target_modality: str):
        """
        Initialize modality filter
        
        Args:
            target_modality: Only return items of this modality
        """
        self.target_modality = target_modality
    
    def __call__(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Filter item by modality
        
        Returns:
            Item if modality matches, None otherwise
        """
        item_modality = item['metadata'].get('target_modality')
        if item_modality == self.target_modality:
            return item
        return None


def create_decode_transform(device: str = "cuda") -> DecodeTransform:
    """
    Convenience function to create a decode transform
    
    Args:
        device: Device to use for decoding
        
    Returns:
        DecodeTransform instance
    """
    return DecodeTransform(device=device)


def create_modality_filter(target_modality: str) -> ModalityFilter:
    """
    Convenience function to create a modality filter
    
    Args:
        target_modality: Target modality to filter for
        
    Returns:
        ModalityFilter instance
    """
    return ModalityFilter(target_modality)


def compose_transforms(*transforms: Callable) -> Callable:
    """
    Compose multiple transforms into a single transform function
    
    Args:
        *transforms: Transform functions to compose
        
    Returns:
        Composed transform function
    """
    def composed_transform(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for transform in transforms:
            item = transform(item)
            if item is None:  # Transform filtered out the item
                return None
        return item
    
    return composed_transform