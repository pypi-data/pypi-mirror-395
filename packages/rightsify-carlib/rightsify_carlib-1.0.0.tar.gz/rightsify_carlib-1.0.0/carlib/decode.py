"""
High-level decode functions for CarLib

This module provides easy-to-use functions for decoding CAR files and encoded data
back to their original media formats.
"""
import os
from typing import Dict, Any, Optional, List
import glob

from .processors.audio_codecs import AudioProcessor, AudioConfig
from .processors.image_codecs import CosmosImageProcessor, ImageConfig
from .processors.video_codecs import CosmosVideoProcessor, VideoConfig
from .loaders import load_single_car


def decode_car_file(
    car_path: str,
    output_path: Optional[str] = None,
    device: str = "cuda",
    save_decoded: bool = True
) -> Dict[str, Any]:
    """
    Decode a CAR file back to its original media format
    
    Args:
        car_path: Path to CAR file
        output_path: Optional output path (inferred from metadata if not provided)
        device: Device to use for decoding ("cuda" or "cpu")
        save_decoded: Whether to save decoded media to file
    
    Returns:
        Dictionary with decoded data, metadata, and output path
    """
    # Load CAR file
    result = load_single_car(car_path, framework="pytorch")
    data = result['data']
    metadata = result['metadata']
    
    # Determine modality from metadata
    target_modality = metadata.get('target_modality')
    if not target_modality:
        raise ValueError("CAR file metadata missing 'target_modality'")
    
    # Initialize appropriate processor
    if target_modality == 'audio':
        config = AudioConfig(device=device)
        if 'model_name' in metadata:
            config.model_name = metadata['model_name']
            config.model_type = metadata.get('model_type', 'encodec')
        processor = AudioProcessor(config)
        
        # Decode audio
        decoded_data = processor.decode_audio(data)
        
        if save_decoded:
            if output_path is None:
                base_name = os.path.splitext(car_path)[0]
                output_path = f"{base_name}_decoded.wav"
            
            processor.save_decoded_audio(decoded_data, output_path, metadata)
    
    elif target_modality == 'image':
        config = ImageConfig(device=device)
        if 'model_name' in metadata:
            config.model_name = metadata['model_name']
        processor = CosmosImageProcessor(config)
        
        # Decode image
        decoded_data = processor.decode_image(data)
        
        if save_decoded:
            if output_path is None:
                base_name = os.path.splitext(car_path)[0]
                output_path = f"{base_name}_decoded.png"
            
            processor.save_decoded_image(decoded_data, output_path)
    
    elif target_modality == 'video':
        config = VideoConfig(device=device)
        if 'model_name' in metadata:
            config.model_name = metadata['model_name']
        processor = CosmosVideoProcessor(config)
        
        # Decode video
        decoded_data = processor.decode_video(data)
        
        if save_decoded:
            if output_path is None:
                base_name = os.path.splitext(car_path)[0]
                output_path = f"{base_name}_decoded.mp4"
            
            processor.save_decoded_video(decoded_data, output_path, metadata)
    
    else:
        raise ValueError(f"Unsupported target modality: {target_modality}")
    
    return {
        'decoded_data': decoded_data,
        'metadata': metadata,
        'output_path': output_path if save_decoded else None,
        'target_modality': target_modality
    }


def decode_encoded_data(
    encoded_data: Dict[str, Any],
    target_modality: str,
    output_path: Optional[str] = None,
    device: str = "cuda",
    save_decoded: bool = True,
    **config_kwargs
) -> Dict[str, Any]:
    """
    Decode encoded data dictionary back to original media format
    
    Args:
        encoded_data: Dictionary with encoded data (from processor.encode_*)
        target_modality: Target modality ("audio", "image", "video")
        output_path: Optional output path for saving
        device: Device to use for decoding
        save_decoded: Whether to save decoded media to file
        **config_kwargs: Additional configuration arguments
    
    Returns:
        Dictionary with decoded data, metadata, and output path
    """
    if target_modality == 'audio':
        config = AudioConfig(device=device, **config_kwargs)
        if 'model_name' in encoded_data:
            config.model_name = encoded_data['model_name']
            config.model_type = encoded_data.get('model_type', 'encodec')
        processor = AudioProcessor(config)
        
        # Decode audio
        decoded_data = processor.decode_audio(encoded_data)
        
        if save_decoded and output_path:
            processor.save_decoded_audio(decoded_data, output_path, encoded_data)
    
    elif target_modality == 'image':
        config = ImageConfig(device=device, **config_kwargs)
        if 'model_name' in encoded_data:
            config.model_name = encoded_data['model_name']
        processor = CosmosImageProcessor(config)
        
        # Decode image
        decoded_data = processor.decode_image(encoded_data)
        
        if save_decoded and output_path:
            processor.save_decoded_image(decoded_data, output_path)
    
    elif target_modality == 'video':
        config = VideoConfig(device=device, **config_kwargs)
        if 'model_name' in encoded_data:
            config.model_name = encoded_data['model_name']
        processor = CosmosVideoProcessor(config)
        
        # Decode video
        decoded_data = processor.decode_video(encoded_data)
        
        if save_decoded and output_path:
            processor.save_decoded_video(decoded_data, output_path, encoded_data)
    
    else:
        raise ValueError(f"Unsupported target modality: {target_modality}")
    
    return {
        'decoded_data': decoded_data,
        'metadata': encoded_data,
        'output_path': output_path if save_decoded else None,
        'target_modality': target_modality
    }


def decode_car_directory(
    car_dir: str,
    output_dir: str,
    pattern: str = "*.car",
    device: str = "cuda",
    max_files: Optional[int] = None,
    modality: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Decode all CAR files in a directory
    
    Args:
        car_dir: Directory containing CAR files
        output_dir: Output directory for decoded files
        pattern: Glob pattern for CAR files
        device: Device to use for decoding
        max_files: Maximum number of files to decode
        modality: Filter by specific modality
    
    Returns:
        List of decode results
    """
    os.makedirs(output_dir, exist_ok=True)
    
    car_files = list(glob.glob(os.path.join(car_dir, pattern)))
    if max_files:
        car_files = car_files[:max_files]
    
    results = []
    for car_path in car_files:
        try:
            # Check modality filter
            if modality:
                temp_result = load_single_car(car_path, framework="pytorch")
                if temp_result['metadata'].get('target_modality') != modality:
                    continue
            
            # Generate output path
            car_filename = os.path.basename(car_path)
            base_name = os.path.splitext(car_filename)[0]
            
            # Decode based on modality (we'll determine this from metadata)
            temp_result = load_single_car(car_path, framework="pytorch") 
            target_modality = temp_result['metadata'].get('target_modality')
            
            if target_modality == 'audio':
                output_path = os.path.join(output_dir, f"{base_name}_decoded.wav")
            elif target_modality == 'image':
                output_path = os.path.join(output_dir, f"{base_name}_decoded.png")
            elif target_modality == 'video':
                output_path = os.path.join(output_dir, f"{base_name}_decoded.mp4")
            else:
                print(f"Warning: Unknown modality {target_modality} for {car_path}")
                continue
            
            result = decode_car_file(
                car_path=car_path,
                output_path=output_path,
                device=device,
                save_decoded=True
            )
            
            results.append({
                'input_path': car_path,
                'output_path': result['output_path'],
                'target_modality': result['target_modality'],
                'status': 'success'
            })
            
            print(f"✅ Decoded: {car_path} -> {result['output_path']}")
            
        except Exception as e:
            print(f"❌ Failed to decode {car_path}: {e}")
            results.append({
                'input_path': car_path,
                'output_path': None,
                'target_modality': None,
                'status': 'failed',
                'error': str(e)
            })
    
    return results


class CARDecoder:
    """
    High-level CAR decoder class for convenient decoding operations
    """
    
    def __init__(self, device: str = "cuda"):
        """
        Initialize CAR decoder
        
        Args:
            device: Device to use for decoding ("cuda" or "cpu")
        """
        self.device = device
        self._processors = {}
    
    def _get_processor(self, target_modality: str, model_config: Optional[Dict[str, Any]] = None):
        """Get or create processor for given modality"""
        cache_key = (target_modality, str(model_config))
        
        if cache_key not in self._processors:
            if target_modality == 'audio':
                config = AudioConfig(device=self.device)
                if model_config:
                    for key, value in model_config.items():
                        setattr(config, key, value)
                self._processors[cache_key] = AudioProcessor(config)
                
            elif target_modality == 'image':
                config = ImageConfig(device=self.device)
                if model_config:
                    for key, value in model_config.items():
                        setattr(config, key, value)
                self._processors[cache_key] = CosmosImageProcessor(config)
                
            elif target_modality == 'video':
                config = VideoConfig(device=self.device)
                if model_config:
                    for key, value in model_config.items():
                        setattr(config, key, value)
                self._processors[cache_key] = CosmosVideoProcessor(config)
                
            else:
                raise ValueError(f"Unsupported target modality: {target_modality}")
        
        return self._processors[cache_key]
    
    def decode_car(
        self, 
        car_path: str, 
        output_path: Optional[str] = None,
        save_decoded: bool = True
    ) -> Dict[str, Any]:
        """Decode a single CAR file"""
        return decode_car_file(
            car_path=car_path,
            output_path=output_path,
            device=self.device,
            save_decoded=save_decoded
        )
    
    def decode_data(
        self,
        encoded_data: Dict[str, Any],
        target_modality: str,
        output_path: Optional[str] = None,
        save_decoded: bool = True
    ) -> Dict[str, Any]:
        """Decode encoded data dictionary"""
        return decode_encoded_data(
            encoded_data=encoded_data,
            target_modality=target_modality,
            output_path=output_path,
            device=self.device,
            save_decoded=save_decoded
        )
    
    def decode_directory(
        self,
        car_dir: str,
        output_dir: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Decode all CAR files in a directory"""
        return decode_car_directory(
            car_dir=car_dir,
            output_dir=output_dir,
            device=self.device,
            **kwargs
        )


# Convenience functions
def decode_audio_car(car_path: str, output_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Convenience function to decode audio CAR file"""
    return decode_car_file(car_path, output_path, **kwargs)

def decode_image_car(car_path: str, output_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Convenience function to decode image CAR file"""
    return decode_car_file(car_path, output_path, **kwargs)

def decode_video_car(car_path: str, output_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Convenience function to decode video CAR file"""
    return decode_car_file(car_path, output_path, **kwargs)