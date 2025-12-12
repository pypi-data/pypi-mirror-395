"""
Basic example demonstrating toonstream usage.
Shows simple JSON to TOON conversion and vice versa.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import toonstream


def main():
    print("=" * 60)
    print("TOONSTREAM - Basic Example")
    print("=" * 60)
    print()
    
    # Example 1: Simple data types
    print("1. Simple Data Types")
    print("-" * 60)
    
    simple_data = {
        "name": "John Doe",
        "age": 30,
        "salary": 75000.50,
        "is_active": True,
        "department": None
    }
    
    print("Original Python object:")
    print(simple_data)
    print()
    
    # Encode to TOON (compact format)
    toon_compact = toonstream.encode(simple_data, indent=0)
    print("TOON format (compact):")
    print(toon_compact)
    print()
    
    # Encode to TOON (pretty format)
    toon_pretty = toonstream.encode(simple_data, indent=2)
    print("TOON format (pretty):")
    print(toon_pretty)
    print()
    
    # Decode back to Python
    decoded = toonstream.decode(toon_pretty)
    print("Decoded back to Python:")
    print(decoded)
    print()
    
    # Verify lossless conversion
    print(f"Lossless conversion: {simple_data == decoded}")
    print()
    
    # Example 2: Arrays
    print("2. Arrays")
    print("-" * 60)
    
    array_data = {
        "numbers": [1, 2, 3, 4, 5],
        "names": ["Alice", "Bob", "Charlie"],
        "mixed": [1, "two", 3.0, True, None]
    }
    
    print("Original Python object:")
    print(array_data)
    print()
    
    toon_array = toonstream.encode(array_data, indent=2)
    print("TOON format:")
    print(toon_array)
    print()
    
    decoded_array = toonstream.decode(toon_array)
    print(f"Lossless conversion: {array_data == decoded_array}")
    print()
    
    # Example 3: Nested structures
    print("3. Nested Structures")
    print("-" * 60)
    
    nested_data = {
        "company": "TechCorp",
        "employees": [
            {
                "id": 1,
                "name": "Alice Johnson",
                "role": "Engineer",
                "skills": ["Python", "JavaScript", "Go"]
            },
            {
                "id": 2,
                "name": "Bob Smith",
                "role": "Designer",
                "skills": ["UI/UX", "Figma", "Adobe XD"]
            }
        ],
        "metadata": {
            "created": "2025-01-01",
            "version": 1.0
        }
    }
    
    print("Original Python object:")
    print(nested_data)
    print()
    
    toon_nested = toonstream.encode(nested_data, indent=2)
    print("TOON format:")
    print(toon_nested)
    print()
    
    decoded_nested = toonstream.decode(toon_nested)
    print(f"Lossless conversion: {nested_data == decoded_nested}")
    print()
    
    # Example 4: Special characters
    print("4. Special Characters")
    print("-" * 60)
    
    special_data = {
        "newline": "Line 1\nLine 2",
        "tab": "Column1\tColumn2",
        "quote": 'He said "Hello"',
        "backslash": "C:\\Users\\Documents",
        "unicode": "Hello 世界 🎉"
    }
    
    print("Original Python object:")
    for key, value in special_data.items():
        print(f"  {key}: {repr(value)}")
    print()
    
    toon_special = toonstream.encode(special_data, indent=2)
    print("TOON format:")
    print(toon_special)
    print()
    
    decoded_special = toonstream.decode(toon_special)
    print(f"Lossless conversion: {special_data == decoded_special}")
    print()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
