"""
Pickle utilities for TOON format.

Provides functions to save TOON-encoded data to pickle files and load them back.
This combines TOON's token efficiency with pickle's binary storage for optimal
file size and fast serialization/deserialization.
"""

import pickle
from pathlib import Path
from typing import Any
from .encoder import encode
from .decoder import decode
from .exceptions import ToonError


class ToonPickleError(ToonError):
    """Raised when pickle operations fail."""
    pass


def save_toon_pickle(data: Any, filepath: str, smart_optimize: bool = True, protocol: int = pickle.HIGHEST_PROTOCOL) -> None:
    """
    Encode data to TOON format and save as a pickle file.
    
    This function provides a convenient way to save Python objects in TOON format
    using pickle for storage. The TOON format reduces token usage, which can result
    in smaller file sizes compared to plain JSON pickle.
    
    Args:
        data: Python object to encode and save (dict, list, or primitive)
        filepath: Path where the pickle file will be saved
        smart_optimize: If True, apply intelligent optimizations for better token efficiency (default: True)
        protocol: Pickle protocol version to use (default: HIGHEST_PROTOCOL)
        
    Raises:
        ToonPickleError: If saving fails
        ToonEncodeError: If TOON encoding fails
        
    Example:
        >>> data = {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}
        >>> save_toon_pickle(data, 'users.toon.pkl')
        >>> # File saved with 38-55% smaller TOON representation
    """
    try:
        # Encode to TOON format
        toon_str = encode(data, smart_optimize=smart_optimize)
        
        # Save as pickle
        filepath_obj = Path(filepath)
        filepath_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(toon_str, f, protocol=protocol)
            
    except Exception as e:
        if isinstance(e, ToonError):
            raise
        raise ToonPickleError(f"Failed to save TOON pickle to '{filepath}': {str(e)}") from e


def load_toon_pickle(filepath: str, strict: bool = True) -> Any:
    """
    Load a TOON pickle file and decode it back to Python object.
    
    This function reads a pickle file containing TOON-encoded data and
    decodes it back to the original Python object structure.
    
    Args:
        filepath: Path to the TOON pickle file to load
        strict: Whether to enforce strict TOON validation (default: True)
        
    Returns:
        Python object (dict, list, or primitive) decoded from TOON format
        
    Raises:
        ToonPickleError: If loading fails
        ToonDecodeError: If TOON decoding fails
        FileNotFoundError: If file doesn't exist
        
    Example:
        >>> data = load_toon_pickle('users.toon.pkl')
        >>> print(data)
        {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}
    """
    try:
        # Load pickle file
        with open(filepath, 'rb') as f:
            toon_str = pickle.load(f)
        
        # Validate that we loaded a string
        if not isinstance(toon_str, str):
            raise ToonPickleError(
                f"Pickle file '{filepath}' does not contain TOON string data. "
                f"Found type: {type(toon_str).__name__}"
            )
        
        # Decode from TOON format
        return decode(toon_str, strict=strict)
        
    except FileNotFoundError:
        raise
    except Exception as e:
        if isinstance(e, ToonError):
            raise
        raise ToonPickleError(f"Failed to load TOON pickle from '{filepath}': {str(e)}") from e


def save_pickle(data: Any, filepath: str, protocol: int = pickle.HIGHEST_PROTOCOL) -> None:
    """
    Save data directly as pickle without TOON encoding.
    
    This is a convenience function for standard pickle operations,
    provided for comparison and compatibility.
    
    Args:
        data: Python object to save
        filepath: Path where the pickle file will be saved
        protocol: Pickle protocol version to use (default: HIGHEST_PROTOCOL)
        
    Raises:
        ToonPickleError: If saving fails
        
    Example:
        >>> data = {'key': 'value'}
        >>> save_pickle(data, 'data.pkl')
    """
    try:
        filepath_obj = Path(filepath)
        filepath_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f, protocol=protocol)
            
    except Exception as e:
        raise ToonPickleError(f"Failed to save pickle to '{filepath}': {str(e)}") from e


def load_pickle(filepath: str) -> Any:
    """
    Load data directly from pickle without TOON decoding.
    
    This is a convenience function for standard pickle operations,
    provided for comparison and compatibility.
    
    Args:
        filepath: Path to the pickle file to load
        
    Returns:
        Python object from pickle file
        
    Raises:
        ToonPickleError: If loading fails
        FileNotFoundError: If file doesn't exist
        
    Example:
        >>> data = load_pickle('data.pkl')
        >>> print(data)
        {'key': 'value'}
    """
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
            
    except FileNotFoundError:
        raise
    except Exception as e:
        raise ToonPickleError(f"Failed to load pickle from '{filepath}': {str(e)}") from e
