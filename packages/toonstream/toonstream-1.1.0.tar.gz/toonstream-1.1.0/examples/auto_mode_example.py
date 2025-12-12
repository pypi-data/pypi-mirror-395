"""
Example: Simplified auto_mode Parameter

This example demonstrates the simplified API where auto_mode automatically
chooses between normal TOON and tensor-aware conversion.
"""

import toonstream

print("=" * 70)
print("TOONSTREAM - Simplified auto_mode Parameter")
print("=" * 70)
print()

# Example 1: Default Mode (no parameters)
print("1. DEFAULT MODE - Standard TOON")
print("-" * 70)

data = {
    "users": [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Charlie", "role": "user"}
    ]
}

print("Input data:")
print(data)
print()

# No parameters = normal mode
toon_str = toonstream.encode(data)
print("Using: toonstream.encode(data)")
print("Result:")
print(toon_str)
print()

# Decode back
decoded = toonstream.decode(toon_str)
print("Using: toonstream.decode(toon_str)")
print("Match:", decoded == data)
print()

# Example 2: Auto Mode with Normal Data
print("2. AUTO MODE - With Normal Data")
print("-" * 70)

normal_data = {"name": "Alice", "age": 30, "city": "NYC"}
print("Input (normal data):")
print(normal_data)
print()

# Auto mode - no tensors, uses normal mode
toon_str = toonstream.encode(normal_data, auto_mode=True)
print("Using: toonstream.encode(data, auto_mode=True)")
print("Result:")
print(toon_str)
print()

decoded = toonstream.decode(toon_str, auto_mode=True)
print("Using: toonstream.decode(toon_str, auto_mode=True)")
print("Match:", decoded == normal_data)
print()

# Example 3: Auto Mode with Tensor Data
print("3. AUTO MODE - With Tensor Data (Auto-Detects)")
print("-" * 70)

try:
    import torch
    
    tensor_data = {
        "embeddings": torch.randn(5),
        "labels": torch.tensor([0, 1, 1, 0, 1]),
        "metadata": {
            "model": "bert-base",
            "device": "cuda:0"
        }
    }
    
    print("Input data with tensors:")
    print(f"  embeddings: shape={tensor_data['embeddings'].shape}, dtype={tensor_data['embeddings'].dtype}")
    print(f"  labels: shape={tensor_data['labels'].shape}, dtype={tensor_data['labels'].dtype}")
    print()
    
    # Auto mode - detects tensors, uses tensor mode
    toon_str = toonstream.encode(tensor_data, auto_mode=True)
    print("Using: toonstream.encode(data, auto_mode=True)")
    print("Result preview (first 100 chars):")
    print(toon_str[:100], "...")
    print()
    
    # Decode back - auto mode detects tensor encoding
    decoded = toonstream.decode(toon_str, auto_mode=True)
    print("Using: toonstream.decode(toon_str, auto_mode=True)")
    print()
    print("Verification:")
    print(f"  Embeddings preserved: {torch.equal(tensor_data['embeddings'], decoded['embeddings'])}")
    print(f"  Labels preserved: {torch.equal(tensor_data['labels'], decoded['labels'])}")
    print(f"  Metadata preserved: {decoded['metadata'] == tensor_data['metadata']}")
    print()

except ImportError:
    print("PyTorch not installed. Install with: pip install torch")
    print()

# Example 4: Mixed Data
print("4. AUTO MODE - Mixed Data (Tensors + Normal)")
print("-" * 70)

try:
    import torch
    
    mixed_data = {
        "model_weights": torch.randn(10),
        "training_info": {
            "epochs": 5,
            "batch_size": 32,
            "device": "cuda:0"
        }
    }
    
    print("Input (mixed tensors and normal data):")
    print(f"  model_weights: tensor, shape={mixed_data['model_weights'].shape}")
    print(f"  training_info: dict with normal values")
    print()
    
    # Auto mode detects tensors and uses tensor encoding
    toon_str = toonstream.encode(mixed_data, auto_mode=True)
    print("Using: toonstream.encode(data, auto_mode=True)")
    print("Result preview (first 80 chars):")
    print(toon_str[:80], "...")
    print()
    
    decoded = toonstream.decode(toon_str, auto_mode=True)
    print("Using: toonstream.decode(toon_str, auto_mode=True)")
    print()
    print("Verification:")
    print(f"  Weights preserved: {torch.equal(mixed_data['model_weights'], decoded['model_weights'])}")
    print(f"  Training info preserved: {decoded['training_info'] == mixed_data['training_info']}")
    print()

except ImportError:
    print("(PyTorch demo skipped)")
    print()

# Example 5: Comparison
print("5. COMPARISON")
print("-" * 70)

data = {"items": [{"x": 1}, {"x": 2}, {"x": 3}]}

# Without auto_mode
normal_result = toonstream.encode(data)
print("Without auto_mode:")
print(f"  toonstream.encode(data)")
print(f"  Result length: {len(normal_result)} chars")
print()

# With auto_mode
auto_result = toonstream.encode(data, auto_mode=True)
print("With auto_mode=True:")
print(f"  toonstream.encode(data, auto_mode=True)")
print(f"  Result length: {len(auto_result)} chars")
print()

print("Same result (auto_mode detects no tensors):", normal_result == auto_result)
print()

print("=" * 70)
print("API SUMMARY")
print("=" * 70)
print("""
Simple, One-Parameter API:

Default usage (normal mode):
    toonstream.encode(data)
    toonstream.decode(toon_str)

With auto_mode (auto-detects tensors):
    toonstream.encode(data, auto_mode=True)
    toonstream.decode(toon_str, auto_mode=True)

That's it! One parameter to decide:
    - auto_mode=False (default): Always use normal TOON
    - auto_mode=True: Auto-detect, use tensor mode if needed

Benefits:
    ✓ Simple - Just one parameter
    ✓ Smart - Detects tensors automatically
    ✓ Works for everyone - With or without PyTorch
    ✓ Clean - No confusing multiple options
""")
print()
