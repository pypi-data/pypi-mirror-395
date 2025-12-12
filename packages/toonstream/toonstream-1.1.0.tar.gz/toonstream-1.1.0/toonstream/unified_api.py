"""
Unified API for ToonStream with automatic mode detection.

Users can optionally enable auto mode, which automatically chooses between
normal TOON conversion and tensor-aware conversion based on the data.

Usage Examples:
    # Normal TOON conversion (default)
    >>> from toonstream import encode, decode
    >>> toon_str = encode(data)
    >>> decoded = decode(toon_str)
    
    # Auto mode - automatically detects and uses tensor mode if needed
    >>> toon_str = encode(data, auto_mode=True)
    >>> decoded = decode(toon_str, auto_mode=True)
"""

from typing import Any, Optional
from .encoder import encode as normal_encode
from .decoder import decode as normal_decode

# Try to import tensor utilities
try:
    from .tensor_utils import encode_with_tensors, decode_with_tensors, is_torch_available
    _TENSOR_SUPPORT = True
except ImportError:
    _TENSOR_SUPPORT = False
    encode_with_tensors = None
    decode_with_tensors = None
    is_torch_available = lambda: False


def encode(
    obj: Any,
    auto_mode: bool = False,
    **kwargs
) -> str:
    """
    Encode a Python object to TOON format.
    
    Args:
        obj: Python object to encode
        auto_mode: If True, auto-detect and use tensor mode if data contains tensors
        **kwargs: Additional arguments for encoding (compact, smart_optimize, indent, sort_keys)
    
    Returns:
        TOON formatted string
        
    Examples:
        >>> data = {'items': [{'id': 1}, {'id': 2}]}
        >>> toon_str = encode(data)  # Normal mode (default)
        >>> toon_str = encode(data, auto_mode=True)  # Auto-detect
    """
    # If auto_mode is enabled and data contains tensors, use tensor encoding
    if auto_mode and _TENSOR_SUPPORT and _contains_tensors(obj):
        return encode_with_tensors(obj, **kwargs)
    
    # Default to normal mode
    return normal_encode(obj, **kwargs)


def decode(
    toon_str: str,
    auto_mode: bool = False,
    **kwargs
) -> Any:
    """
    Decode a TOON string back to Python object.
    
    Args:
        toon_str: TOON formatted string to decode
        auto_mode: If True, auto-detect tensor encoding
        **kwargs: Additional arguments for decoding (strict)
    
    Returns:
        Decoded Python object
        
    Examples:
        >>> toon_str = "key: value"
        >>> data = decode(toon_str)  # Normal mode (default)
        >>> data = decode(toon_str, auto_mode=True)  # Auto-detect
    """
    # If auto_mode is enabled and string looks like tensor encoding, use tensor decoding
    if auto_mode and _TENSOR_SUPPORT and _looks_like_tensor_encoded(toon_str):
        return decode_with_tensors(toon_str, **kwargs)
    
    # Default to normal mode
    return normal_decode(toon_str, **kwargs)


def _contains_tensors(obj: Any) -> bool:
    """Check if object contains PyTorch tensors."""
    if not _TENSOR_SUPPORT:
        return False
    
    import torch
    
    if isinstance(obj, torch.Tensor):
        return True
    
    if isinstance(obj, dict):
        return any(_contains_tensors(v) for v in obj.values())
    
    if isinstance(obj, (list, tuple)):
        return any(_contains_tensors(item) for item in obj)
    
    return False


def _looks_like_tensor_encoded(data: str) -> bool:
    """Check if string looks like it contains tensor-encoded data."""
    if not isinstance(data, str):
        return False
    
    # Look for tensor encoding markers
    return '_type' in data and 'torch.Tensor' in data


__all__ = ['convert']
