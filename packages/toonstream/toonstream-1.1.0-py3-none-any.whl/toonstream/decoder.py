"""
TOON to JSON decoder implementation.
Parses Token Oriented Object Notation (TOON) back to Python objects.

TOON Format Examples:
    1. Dictionary:
       name: "John"
       age: 30
       
    2. Array of objects (tabular):
       data[3]{id,name}:
       1,Alice
       2,Bob
       3,Carol
       
    3. Empty dictionary:
       (empty string)
"""

import re
import json
from typing import Any, Dict, List
from .exceptions import ToonDecodeError, ToonValidationError


class ToonDecoder:
    """Decoder for converting TOON format to Python objects."""
    
    def __init__(self, strict: bool = True):
        """
        Initialize the TOON decoder.
        
        Args:
            strict: Whether to enforce strict TOON validation
        """
        self.strict = strict
    
    def decode(self, toon_str: str) -> Any:
        """
        Decode a TOON string to a Python object.
        
        TOON format has multiple patterns:
        1. Primitives: JSON format (42, "hello", true, false, null)
        2. key: value (dictionary format)
        3. key[count]{fields}: followed by CSV rows (tabular array format)
        4. {...} or [...] JSON format for objects/arrays
        5. Mixed format: combination of tabular and key:value sections
        
        Args:
            toon_str: TOON formatted string
            
        Returns:
            Python object (dict, list, or primitive)
            
        Raises:
            ToonDecodeError: If decoding fails
            ToonValidationError: If validation fails
        """
        if not isinstance(toon_str, str):
            raise ToonDecodeError("Input must be a string")
        
        # Handle empty string - raise error for truly empty strings
        if not toon_str:
            raise ToonDecodeError("Cannot decode empty string")
        
        toon_str = toon_str.strip()
        
        # After stripping, if empty, raise error
        if not toon_str:
            raise ToonDecodeError("Cannot decode empty or whitespace-only string")
        
        try:
            # Check for invalid keywords like 'undefined'
            if 'undefined' in toon_str and not '"undefined"' in toon_str:
                raise ToonDecodeError("Invalid value: 'undefined' is not supported")
            
            # Check if this is JSON format (objects/arrays or primitives)
            if toon_str.startswith(('{', '[', '"')) or toon_str in ('true', 'false', 'null') or self._is_json_number(toon_str):
                try:
                    return json.loads(toon_str)
                except json.JSONDecodeError as e:
                    raise ToonDecodeError(f"Invalid JSON/TOON format: {str(e)}") from e
            
            # Check if this is a pure tabular format (single array at top level)
            # This is when the entire document starts with key[count]{fields}:
            # and has ONLY data rows after it (no other key: value pairs)
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\[\d+\]\{', toon_str):
                # Check if there are any subsequent key: value lines after the tabular section
                lines = toon_str.split('\n')
                # Find where the tabular section ends
                tabular_end = self._find_tabular_end(lines)
                
                # If entire document is tabular, parse as tabular
                if tabular_end == len(lines):
                    return self._parse_tabular(toon_str)
                
                # Otherwise, it's a mixed format dictionary - parse as dict
                return self._parse_mixed_dict(toon_str)
            
            # Otherwise, parse as key: value dictionary format
            return self._parse_dict(toon_str)
            
        except (ToonDecodeError, ToonValidationError):
            raise
        except Exception as e:
            raise ToonDecodeError(f"Failed to decode TOON: {str(e)}") from e
    
    def _find_tabular_end(self, lines: List[str]) -> int:
        """
        Find where a tabular section ends in the lines.
        
        Args:
            lines: List of lines from the TOON string
            
        Returns:
            Index of the first line after the tabular section ends
        """
        if not lines:
            return 0
        
        # First line should be the header
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\[\d+\]\{', lines[0]):
            return 0
        
        # Extract count from header
        match = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\[(\d+)\]', lines[0])
        if not match:
            return 1
        
        count = int(match.group(1))
        
        # Tabular section should have header + count rows
        expected_end = 1 + count
        
        # Also check for empty lines and other key: value patterns
        for i in range(1, len(lines)):
            line = lines[i].strip()
            
            # Empty line might signal end of section
            if not line:
                return i
            
            # If we see another key: value pattern, tabular section ended
            if ':' in line and not self._looks_like_csv_row(line):
                return i
            
            # If we've processed all the expected data rows
            if i >= expected_end:
                return i
        
        return len(lines)
    
    def _looks_like_csv_row(self, line: str) -> bool:
        """Check if a line looks like a CSV data row vs a key:value pair."""
        # CSV rows typically don't have unescaped colons except in JSON values
        # key:value pairs have a colon early in the line
        if not ':' in line:
            return True  # No colon = probably CSV
        
        colon_pos = line.index(':')
        # If colon is very early and not escaped, probably key:value
        if colon_pos < 20 and not line[colon_pos-1:colon_pos] == '\\':
            # Check if the part before colon looks like a key (no commas)
            before_colon = line[:colon_pos].strip()
            if ',' not in before_colon and before_colon.replace('_', '').replace('-', '').isalnum():
                return False  # Looks like key:value
        
        return True  # Probably CSV
    
    def _is_json_number(self, s: str) -> bool:
        """Check if string represents a JSON number."""
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def _parse_mixed_dict(self, toon_str: str) -> Dict:
        """
        Parse TOON mixed format (combination of tabular and key:value sections).
        
        Format:
            key1[count]{fields}:
            row1
            row2
            
            key2: value2
            key3: value3
            
        Args:
            toon_str: TOON string in mixed format
            
        Returns:
            Dictionary with all sections parsed
        """
        result = {}
        lines = toon_str.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Check if this is a tabular section header
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\[\d+\]\{', line):
                # Find where this tabular section ends
                section_lines = [line]
                match = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\[(\d+)\]', line)
                count = int(match.group(1))
                
                # Collect the data rows for this tabular section
                i += 1
                rows_collected = 0
                while i < len(lines) and rows_collected < count:
                    if lines[i].strip():
                        section_lines.append(lines[i])
                        rows_collected += 1
                    i += 1
                
                # Parse this tabular section
                section_str = '\n'.join(section_lines)
                parsed = self._parse_tabular(section_str)
                
                # If it returned a dict with one key, merge it
                if isinstance(parsed, dict):
                    result.update(parsed)
                else:
                    # If it returned a list (key was 'data'), we have a problem
                    # This shouldn't happen in mixed format
                    raise ToonDecodeError("Unexpected list result in mixed format")
            else:
                # This should be a key: value line
                if ':' not in line:
                    i += 1
                    continue
                
                colon_pos = self._find_key_colon(line)
                if colon_pos == -1:
                    i += 1
                    continue
                
                key = line[:colon_pos].strip()
                value_str = line[colon_pos + 1:].strip()
                
                value = self._parse_json_value(value_str)
                result[key] = value
                i += 1
        
        return result
    
    def _parse_dict(self, toon_str: str) -> Dict:
        """
        Parse TOON dictionary format (key: value pairs).
        
        Format:
            key1: value1
            
            key2: value2
            
        Args:
            toon_str: TOON string in dictionary format
            
        Returns:
            Dictionary with parsed key-value pairs
        """
        result = {}
        
        # Split by double newline (section separator) or single newline
        sections = re.split(r'\n\n+', toon_str.strip())
        
        for section in sections:
            if not section.strip():
                continue
            
            # Parse each key: value line
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Find the first colon that's not inside quotes
                colon_pos = self._find_key_colon(line)
                if colon_pos == -1:
                    raise ToonDecodeError(f"Invalid TOON format: missing colon in '{line}'")
                
                key = line[:colon_pos].strip()
                value_str = line[colon_pos + 1:].strip()
                
                # Parse the value (could be JSON, string, number, etc.)
                value = self._parse_json_value(value_str)
                result[key] = value
        
        return result
    
    def _find_key_colon(self, line: str) -> int:
        """
        Find the position of the colon separating key from value.
        Must not be inside quotes.
        
        Args:
            line: Line to search
            
        Returns:
            Position of colon, or -1 if not found
        """
        in_quotes = False
        escape_next = False
        
        for i, char in enumerate(line):
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            if char == '"':
                in_quotes = not in_quotes
            elif char == ':' and not in_quotes:
                return i
        
        return -1
    
    def _parse_tabular(self, toon_str: str) -> Any:
        """
        Parse TOON tabular format (array of objects).
        
        Format:
            key[count]{field1,field2}:
            value1,value2
            value3,value4
            
        Returns single key-value pair if key is not 'data',
        or returns list if key is 'data'.
        
        Args:
            toon_str: TOON string in tabular format
            
        Returns:
            Dictionary with single key mapping to list, or just the list
        """
        lines = toon_str.strip().split('\n')
        if not lines:
            raise ToonDecodeError("Empty tabular TOON")
        
        # Parse header: key[count]{field1,field2,...}:
        header = lines[0]
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]\{([^}]*)\}:$', header)
        if not match:
            raise ToonDecodeError(f"Invalid TOON tabular header: {header}")
        
        key = match.group(1)
        count = int(match.group(2))
        fields_str = match.group(3)
        
        # Parse fields
        fields = [f.strip() for f in fields_str.split(',') if f.strip()]
        
        # Parse data rows
        objects = []
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            
            # Parse CSV values with escaping support
            values = self._parse_csv_row(line)
            
            if len(values) != len(fields):
                raise ToonDecodeError(
                    f"Row {i} has {len(values)} values but expected {len(fields)}"
                )
            
            # Build object
            obj = {}
            for field, value in zip(fields, values):
                obj[field] = self._parse_csv_value(value)
            
            objects.append(obj)
        
        # Validate count
        if len(objects) != count:
            raise ToonDecodeError(
                f"Expected {count} rows but got {len(objects)}"
            )
        
        # If key is 'data', return the list directly (for top-level arrays)
        if key == 'data':
            return objects
        
        # Otherwise return as dictionary
        return {key: objects}
    
    def _parse_csv_row(self, line: str) -> List[str]:
        """
        Parse a CSV row with escape sequence support.
        
        Escapes:
            \\, → ,
            \\\\ → \\
            \\n → newline
            \\r → carriage return
            
        Args:
            line: CSV row string
            
        Returns:
            List of unescaped values
        """
        values = []
        current = []
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char == '\\' and i + 1 < len(line):
                next_char = line[i + 1]
                if next_char == ',':
                    current.append(',')
                    i += 2
                elif next_char == '\\':
                    current.append('\\')
                    i += 2
                elif next_char == 'n':
                    current.append('\n')
                    i += 2
                elif next_char == 'r':
                    current.append('\r')
                    i += 2
                else:
                    current.append(char)
                    i += 1
            elif char == ',':
                values.append(''.join(current))
                current = []
                i += 1
            else:
                current.append(char)
                i += 1
        
        # Add last value
        values.append(''.join(current))
        
        return values
    
    def _parse_csv_value(self, value: str) -> Any:
        """
        Parse a single CSV cell value.
        
        Values can be:
        - Empty string → None
        - 'true' or 'false' → boolean
        - Number → int or float
        - JSON object/array → parsed object
        - String → string
        
        Args:
            value: String value from CSV cell
            
        Returns:
            Parsed Python value
        """
        value = value.strip()
        
        # Empty → None
        if not value:
            return None
        
        # Booleans
        if value == 'true':
            return True
        if value == 'false':
            return False
        
        # Try to parse as JSON (for nested objects/arrays)
        if value.startswith('{') or value.startswith('['):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        
        # Try number
        try:
            if '.' in value or 'e' in value.lower():
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _parse_json_value(self, value_str: str) -> Any:
        """
        Parse a value string (could be JSON or primitive).
        
        Args:
            value_str: String representation of value
            
        Returns:
            Parsed Python value
        """
        value_str = value_str.strip()
        
        if not value_str:
            return None
        
        # Try to parse as JSON
        try:
            return json.loads(value_str)
        except json.JSONDecodeError:
            # If it fails, return as string
            return value_str


def decode(toon_str: str, strict: bool = True) -> Any:
    """
    Convenience function to decode a TOON string to a Python object.
    
    Args:
        toon_str: TOON formatted string
        strict: Whether to enforce strict TOON validation
        
    Returns:
        Python object
        
    Raises:
        ToonDecodeError: If decoding fails
        ToonValidationError: If validation fails
    """
    decoder = ToonDecoder(strict=strict)
    return decoder.decode(toon_str)

