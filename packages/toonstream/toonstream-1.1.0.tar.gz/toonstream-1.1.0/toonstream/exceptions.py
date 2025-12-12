"""
Custom exceptions for the toonstream library.

This module defines the exception hierarchy for TOON encoding/decoding operations.
All exceptions inherit from ToonError for easy exception handling.

Example:
    try:
        toon_str = encode(data)
    except ToonEncodeError as e:
        print(f"Encoding failed: {e}")
    except ToonError as e:
        print(f"General TOON error: {e}")
"""


class ToonError(Exception):
    """
    Base exception for all TOON-related errors.
    
    All other TOON exceptions inherit from this class, allowing
    catch-all exception handling with a single except clause.
    """
    pass


class ToonEncodeError(ToonError):
    """
    Exception raised when encoding JSON to TOON fails.
    
    Common causes:
    - NaN or Infinity float values (not supported in TOON)
    - Unsupported data types
    - Internal encoding errors
    """
    pass


class ToonDecodeError(ToonError):
    """
    Exception raised when decoding TOON to JSON fails.
    
    Common causes:
    - Malformed TOON syntax
    - Invalid escape sequences
    - Unexpected end of input
    - Type conversion errors
    """
    pass


class ToonValidationError(ToonError):
    """
    Exception raised when TOON validation fails.
    
    Used for structural validation issues that don't fit
    into encoding or decoding categories.
    """
    pass
