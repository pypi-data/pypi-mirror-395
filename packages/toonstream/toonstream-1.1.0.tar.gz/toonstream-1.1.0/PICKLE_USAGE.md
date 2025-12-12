# TOON Pickle Utilities

Save and load Python data using TOON format with pickle serialization.

## Quick Start

```python
from toonstream import save_toon_pickle, load_toon_pickle

# Save data
data = {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}
save_toon_pickle(data, 'data.toon.pkl')

# Load data
loaded = load_toon_pickle('data.toon.pkl')
print(loaded)  # {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}
```

## Functions

### save_toon_pickle(data, filepath, smart_optimize=True, protocol=HIGHEST_PROTOCOL)

Encode data to TOON format and save as pickle file.

**Parameters:**
- `data`: Python object (dict, list, primitive)
- `filepath`: Path to save pickle file
- `smart_optimize`: Enable TOON optimizations (default: True)
- `protocol`: Pickle protocol version (default: HIGHEST_PROTOCOL)

**Example:**
```python
save_toon_pickle(data, 'output/users.toon.pkl')
```

### load_toon_pickle(filepath, strict=True)

Load pickle file and decode from TOON format.

**Parameters:**
- `filepath`: Path to TOON pickle file
- `strict`: Enforce strict TOON validation (default: True)

**Returns:** Decoded Python object

**Example:**
```python
data = load_toon_pickle('output/users.toon.pkl')
```

### save_pickle(data, filepath, protocol=HIGHEST_PROTOCOL)

Save data as standard pickle (no TOON encoding).

**Example:**
```python
save_pickle(data, 'output/data.pkl')
```

### load_pickle(filepath)

Load standard pickle file (no TOON decoding).

**Example:**
```python
data = load_pickle('output/data.pkl')
```

## Benefits

### File Size Reduction
TOON format reduces token/character count, which can result in smaller pickle files:

```python
# Example with 50 employee records:
# TOON pickle:    310 bytes
# Regular pickle: 350 bytes
# Savings:        11.4%
```

### Token Efficiency
When using pickled data in LLM contexts:
- Flat data: 38-55% fewer tokens vs JSON
- Arrays of objects: 30-40% fewer tokens

### Lossless Conversion
Perfect round-trip conversion:
```python
assert load_toon_pickle('data.toon.pkl') == original_data
```

## Use Cases

1. **Caching LLM Context:**
   ```python
   # Save processed context
   save_toon_pickle(context_data, 'cache/context.toon.pkl')
   
   # Load for reuse (smaller token count)
   context = load_toon_pickle('cache/context.toon.pkl')
   ```

2. **Data Pipeline Storage:**
   ```python
   # Save intermediate results
   save_toon_pickle(processed_data, 'pipeline/step1.toon.pkl')
   
   # Load for next step
   data = load_toon_pickle('pipeline/step1.toon.pkl')
   ```

3. **Configuration Files:**
   ```python
   config = {'settings': {...}, 'users': [...]}
   save_toon_pickle(config, 'config.toon.pkl')
   ```

## Exceptions

- `ToonPickleError`: Raised when pickle operations fail
- `ToonEncodeError`: Raised when TOON encoding fails
- `ToonDecodeError`: Raised when TOON decoding fails
- `FileNotFoundError`: Raised when file doesn't exist

## Complete Example

See `examples/pickle_example.py` for a comprehensive example with:
- Saving TOON pickle
- Saving regular pickle
- File size comparison
- Data integrity verification
- TOON format preview

Run it:
```bash
python examples/pickle_example.py
```
