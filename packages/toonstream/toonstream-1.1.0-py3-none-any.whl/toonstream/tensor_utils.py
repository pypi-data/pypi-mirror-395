"""
PyTorch tensor utilities for ToonStream.

Provides seamless integration between ToonStream and PyTorch tensors,
allowing efficient serialization of tensor data with automatic type detection.
"""

from typing import Any, Dict, List, Optional, Union
import json

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TensorEncoder:
    """Encoder for PyTorch tensors to TOON-compatible format."""
    
    def __init__(self):
        """Initialize the tensor encoder."""
        if not TORCH_AVAILABLE:
            raise ImportError(
                "PyTorch is required for tensor support. "
                "Install with: pip install torch"
            )
    
    def encode_tensor(self, tensor: 'torch.Tensor') -> Dict[str, Any]:
        """
        Encode a PyTorch tensor to a dictionary format.
        
        Args:
            tensor: PyTorch tensor to encode
            
        Returns:
            Dictionary with tensor data, shape, dtype, and device
            
        Example:
            >>> import torch
            >>> from toonstream.tensor_utils import TensorEncoder
            >>> encoder = TensorEncoder()
            >>> tensor = torch.tensor([[1, 2], [3, 4]])
            >>> encoded = encoder.encode_tensor(tensor)
            >>> print(encoded)
            {
                'data': [[1, 2], [3, 4]],
                'shape': [2, 2],
                'dtype': 'torch.int64',
                'device': 'cpu'
            }
        """
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch is not available")
        
        if not isinstance(tensor, torch.Tensor):
            raise TypeError(f"Expected torch.Tensor, got {type(tensor)}")
        
        return {
            'data': tensor.tolist(),
            'shape': list(tensor.shape),
            'dtype': str(tensor.dtype),
            'device': str(tensor.device),
            '_type': 'torch.Tensor'
        }
    
    def is_tensor(self, obj: Any) -> bool:
        """
        Check if an object is a PyTorch tensor.
        
        Args:
            obj: Object to check
            
        Returns:
            True if object is a torch.Tensor
        """
        if not TORCH_AVAILABLE:
            return False
        return isinstance(obj, torch.Tensor)
    
    def encode_recursive(self, obj: Any) -> Any:
        """
        Recursively encode an object, converting tensors to dictionaries.
        
        Args:
            obj: Object to encode (can contain tensors)
            
        Returns:
            Object with tensors converted to dictionaries
            
        Example:
            >>> import torch
            >>> from toonstream.tensor_utils import TensorEncoder
            >>> encoder = TensorEncoder()
            >>> data = {
            ...     'model': 'bert',
            ...     'weights': torch.tensor([1.0, 2.0, 3.0]),
            ...     'config': {'layers': 12}
            ... }
            >>> encoded = encoder.encode_recursive(data)
        """
        if self.is_tensor(obj):
            return self.encode_tensor(obj)
        elif isinstance(obj, dict):
            return {key: self.encode_recursive(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.encode_recursive(item) for item in obj]
        else:
            return obj


class TensorDecoder:
    """Decoder for reconstructing PyTorch tensors from TOON format."""
    
    def __init__(self):
        """Initialize the tensor decoder."""
        if not TORCH_AVAILABLE:
            raise ImportError(
                "PyTorch is required for tensor support. "
                "Install with: pip install torch"
            )
    
    def decode_tensor(self, tensor_dict: Dict[str, Any]) -> 'torch.Tensor':
        """
        Decode a dictionary back to a PyTorch tensor.
        
        Args:
            tensor_dict: Dictionary with tensor data (from encode_tensor)
            
        Returns:
            Reconstructed PyTorch tensor
            
        Example:
            >>> import torch
            >>> from toonstream.tensor_utils import TensorDecoder
            >>> decoder = TensorDecoder()
            >>> tensor_dict = {
            ...     'data': [[1, 2], [3, 4]],
            ...     'shape': [2, 2],
            ...     'dtype': 'torch.int64',
            ...     'device': 'cpu',
            ...     '_type': 'torch.Tensor'
            ... }
            >>> tensor = decoder.decode_tensor(tensor_dict)
        """
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch is not available")
        
        if not isinstance(tensor_dict, dict):
            raise TypeError(f"Expected dict, got {type(tensor_dict)}")
        
        if '_type' not in tensor_dict or tensor_dict['_type'] != 'torch.Tensor':
            raise ValueError("Invalid tensor dictionary format")
        
        # Extract tensor data
        data = tensor_dict['data']
        dtype_str = tensor_dict.get('dtype', 'torch.float32')
        device_str = tensor_dict.get('device', 'cpu')
        
        # Parse dtype
        dtype = self._parse_dtype(dtype_str)
        
        # Create tensor
        tensor = torch.tensor(data, dtype=dtype)
        
        # Move to device if needed
        if device_str != 'cpu':
            try:
                tensor = tensor.to(device_str)
            except (RuntimeError, AssertionError):
                # Device not available, keep on CPU
                pass
        
        return tensor
    
    def _parse_dtype(self, dtype_str: str) -> 'torch.dtype':
        """
        Parse dtype string to torch.dtype.
        
        Args:
            dtype_str: String representation of dtype (e.g., 'torch.float32')
            
        Returns:
            torch.dtype object
        """
        dtype_map = {
            'torch.float32': torch.float32,
            'torch.float': torch.float32,
            'torch.float64': torch.float64,
            'torch.double': torch.float64,
            'torch.float16': torch.float16,
            'torch.half': torch.float16,
            'torch.bfloat16': torch.bfloat16,
            'torch.int64': torch.int64,
            'torch.long': torch.int64,
            'torch.int32': torch.int32,
            'torch.int': torch.int32,
            'torch.int16': torch.int16,
            'torch.short': torch.int16,
            'torch.int8': torch.int8,
            'torch.uint8': torch.uint8,
            'torch.bool': torch.bool,
        }
        
        return dtype_map.get(dtype_str, torch.float32)
    
    def is_tensor_dict(self, obj: Any) -> bool:
        """
        Check if a dictionary represents an encoded tensor.
        
        Args:
            obj: Object to check
            
        Returns:
            True if object is an encoded tensor dictionary
        """
        if not isinstance(obj, dict):
            return False
        return obj.get('_type') == 'torch.Tensor'
    
    def decode_recursive(self, obj: Any) -> Any:
        """
        Recursively decode an object, converting tensor dictionaries to tensors.
        
        Args:
            obj: Object to decode (can contain tensor dictionaries)
            
        Returns:
            Object with tensor dictionaries converted to tensors
            
        Example:
            >>> import torch
            >>> from toonstream.tensor_utils import TensorDecoder
            >>> decoder = TensorDecoder()
            >>> encoded_data = {
            ...     'model': 'bert',
            ...     'weights': {
            ...         'data': [1.0, 2.0, 3.0],
            ...         'shape': [3],
            ...         'dtype': 'torch.float32',
            ...         'device': 'cpu',
            ...         '_type': 'torch.Tensor'
            ...     }
            ... }
            >>> decoded = decoder.decode_recursive(encoded_data)
        """
        if self.is_tensor_dict(obj):
            return self.decode_tensor(obj)
        elif isinstance(obj, dict):
            return {key: self.decode_recursive(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.decode_recursive(item) for item in obj]
        else:
            return obj


# Convenience functions for tensor support
def encode_with_tensors(obj: Any) -> str:
    """
    Encode an object containing tensors to TOON format.
    
    This function automatically detects and converts PyTorch tensors
    to a serializable format before encoding to TOON.
    
    Args:
        obj: Object to encode (can contain tensors, dicts, lists, etc.)
        
    Returns:
        TOON formatted string
        
    Raises:
        ImportError: If PyTorch is not installed
        
    Example:
        >>> import torch
        >>> from toonstream.tensor_utils import encode_with_tensors
        >>> data = {
        ...     'embeddings': torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
        ...     'labels': [0, 1]
        ... }
        >>> toon_str = encode_with_tensors(data)
    """
    from .encoder import encode
    
    encoder = TensorEncoder()
    serializable_obj = encoder.encode_recursive(obj)
    return encode(serializable_obj)


def decode_with_tensors(toon_str: str) -> Any:
    """
    Decode a TOON string and reconstruct any tensors.
    
    This function automatically detects encoded tensors and converts
    them back to PyTorch tensors.
    
    Args:
        toon_str: TOON formatted string
        
    Returns:
        Decoded object with tensors reconstructed
        
    Raises:
        ImportError: If PyTorch is not installed
        
    Example:
        >>> from toonstream.tensor_utils import decode_with_tensors
        >>> toon_str = "..."  # TOON string with encoded tensors
        >>> data = decode_with_tensors(toon_str)
        >>> # data['embeddings'] is now a torch.Tensor
    """
    from .decoder import decode
    
    decoded_obj = decode(toon_str)
    decoder = TensorDecoder()
    return decoder.decode_recursive(decoded_obj)


# Check if PyTorch is available
def is_torch_available() -> bool:
    """
    Check if PyTorch is installed and available.
    
    Returns:
        True if PyTorch is available, False otherwise
    """
    return TORCH_AVAILABLE
