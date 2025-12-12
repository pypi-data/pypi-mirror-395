"""
Example demonstrating PyTorch tensor support in ToonStream.

This example shows how to use ToonStream with PyTorch tensors,
including encoding, decoding, and integration with ML workflows.
"""

# Check if PyTorch is available
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️  PyTorch not installed. Install with: pip install torch")
    print("This example requires PyTorch to run.")
    exit(1)

import toonstream

print("=" * 60)
print("TOONSTREAM - PyTorch Tensor Support Example")
print("=" * 60)
print()

# Example 1: Simple Tensor Encoding
print("1. Simple Tensor Encoding")
print("-" * 60)

# Create a simple tensor
weights = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
print(f"Original tensor: {weights}")
print(f"Tensor shape: {weights.shape}")
print(f"Tensor dtype: {weights.dtype}")
print()

# Encode with tensor support
data = {'weights': weights, 'model': 'simple_nn'}
toon_str = toonstream.encode_with_tensors(data)
print("TOON format:")
print(toon_str)
print()

# Decode back to tensor
decoded = toonstream.decode_with_tensors(toon_str)
print(f"Decoded tensor: {decoded['weights']}")
print(f"Tensors match: {torch.equal(weights, decoded['weights'])}")
print()

# Example 2: Multi-dimensional Tensors
print("2. Multi-dimensional Tensors")
print("-" * 60)

embeddings = torch.tensor([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0]
])

data = {
    'embeddings': embeddings,
    'vocab_size': 50000,
    'hidden_dim': 768
}

print(f"Original embeddings shape: {embeddings.shape}")
toon_str = toonstream.encode_with_tensors(data)
print("TOON encoded (first 200 chars):")
print(toon_str[:200] + "...")
print()

decoded = toonstream.decode_with_tensors(toon_str)
print(f"Decoded shape: {decoded['embeddings'].shape}")
print(f"Match: {torch.equal(embeddings, decoded['embeddings'])}")
print()

# Example 3: Mixed Data with Tensors
print("3. Mixed Data with Tensors")
print("-" * 60)

model_data = {
    'architecture': 'transformer',
    'layers': [
        {
            'name': 'layer_1',
            'weights': torch.tensor([[1, 2], [3, 4]]),
            'bias': torch.tensor([1, 2])
        },
        {
            'name': 'layer_2',
            'weights': torch.tensor([[5, 6], [7, 8]]),
            'bias': torch.tensor([3, 4])
        }
    ],
    'config': {
        'num_layers': 2,
        'hidden_size': 768,
        'attention_heads': 12
    }
}

print("Original data structure:")
print(f"  Architecture: {model_data['architecture']}")
print(f"  Layers: {len(model_data['layers'])}")
print(f"  Layer 1 weights shape: {model_data['layers'][0]['weights'].shape}")
print()

# Encode
toon_str = toonstream.encode_with_tensors(model_data)
print(f"TOON string length: {len(toon_str)} characters")
print()

# Decode
decoded = toonstream.decode_with_tensors(toon_str)
print("Decoded data:")
print(f"  Architecture: {decoded['architecture']}")
print(f"  Layers: {len(decoded['layers'])}")
print(f"  Layer 1 weights type: {type(decoded['layers'][0]['weights'])}")
print(f"  Match: {torch.equal(model_data['layers'][0]['weights'], decoded['layers'][0]['weights'])}")
print()

# Example 4: Training Logs with Tensors
print("4. Training Logs with Tensors")
print("-" * 60)

training_logs = [
    {
        'epoch': 1,
        'loss': 0.5234,
        'accuracy': 0.8543,
        'gradients': torch.tensor([0.01, 0.02, 0.015])
    },
    {
        'epoch': 2,
        'loss': 0.3421,
        'accuracy': 0.9012,
        'gradients': torch.tensor([0.008, 0.012, 0.009])
    },
    {
        'epoch': 3,
        'loss': 0.2103,
        'accuracy': 0.9345,
        'gradients': torch.tensor([0.005, 0.007, 0.006])
    }
]

print("Original training logs:")
for log in training_logs:
    print(f"  Epoch {log['epoch']}: loss={log['loss']:.4f}, acc={log['accuracy']:.4f}")
print()

# Encode
toon_str = toonstream.encode_with_tensors(training_logs)
print(f"TOON encoded length: {len(toon_str)} characters")
print()

# Decode
decoded_logs = toonstream.decode_with_tensors(toon_str)
print("Decoded logs:")
for log in decoded_logs:
    print(f"  Epoch {log['epoch']}: gradients shape={log['gradients'].shape}")
print()

# Example 5: Token Savings with Tensors
print("5. Token Savings Comparison")
print("-" * 60)

import json

data = {
    'model': 'bert-base',
    'parameters': torch.randn(10, 10),  # 10x10 random tensor
    'config': {'layers': 12, 'hidden': 768}
}

# Regular JSON (without tensor support)
json_data = {
    'model': data['model'],
    'parameters': data['parameters'].tolist(),
    'config': data['config']
}
json_str = json.dumps(json_data)

# TOON format
toon_str = toonstream.encode_with_tensors(data)

print(f"JSON length: {len(json_str)} characters")
print(f"TOON length: {len(toon_str)} characters")
print(f"Savings: {((len(json_str) - len(toon_str)) / len(json_str) * 100):.1f}%")
print()

# Verify lossless conversion
decoded = toonstream.decode_with_tensors(toon_str)
print(f"Lossless: {torch.allclose(data['parameters'], decoded['parameters'])}")
print()

# Example 6: Batch Data with Tensors
print("6. Batch Data Processing")
print("-" * 60)

batch_data = {
    'batch_size': 32,
    'inputs': torch.randn(32, 128),  # 32 samples, 128 features
    'targets': torch.randint(0, 10, (32,)),  # 32 labels
    'metadata': {
        'dataset': 'MNIST',
        'split': 'train'
    }
}

print(f"Batch inputs shape: {batch_data['inputs'].shape}")
print(f"Batch targets shape: {batch_data['targets'].shape}")
print()

# Encode
toon_str = toonstream.encode_with_tensors(batch_data)
print(f"Encoded batch data: {len(toon_str)} characters")
print()

# Decode
decoded_batch = toonstream.decode_with_tensors(toon_str)
print(f"Decoded inputs shape: {decoded_batch['inputs'].shape}")
print(f"Decoded targets shape: {decoded_batch['targets'].shape}")
print(f"Match: {torch.equal(batch_data['targets'], decoded_batch['targets'])}")
print()

print("=" * 60)
print("✓ All tensor examples completed successfully!")
print("=" * 60)
print()
print("Key Features:")
print("  ✓ Automatic tensor detection and encoding")
print("  ✓ Lossless round-trip conversion")
print("  ✓ Preserves tensor dtype and shape")
print("  ✓ Works with nested data structures")
print("  ✓ Token-efficient serialization")
print()
