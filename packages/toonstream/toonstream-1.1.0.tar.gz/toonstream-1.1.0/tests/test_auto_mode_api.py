"""
Unit tests for the simplified auto_mode parameter API.
"""

import pytest
import toonstream

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TestSimplifiedAPI:
    """Test the simplified encode/decode with auto_mode parameter."""
    
    def test_encode_default_normal_mode(self):
        """Test encoding with default (normal mode)."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        result = toonstream.encode(data)
        assert isinstance(result, str)
        assert "users" in result
    
    def test_decode_default_normal_mode(self):
        """Test decoding with default (normal mode)."""
        toon_str = 'users[2]{id,name}:\n1,Alice\n2,Bob'
        result = toonstream.decode(toon_str)
        assert isinstance(result, dict)
        assert "users" in result
        assert len(result["users"]) == 2
    
    def test_encode_decode_roundtrip_default(self):
        """Test encode-decode roundtrip with defaults (normal mode)."""
        original = {"items": [{"x": 1}, {"x": 2}, {"x": 3}]}
        encoded = toonstream.encode(original)
        decoded = toonstream.decode(encoded)
        assert decoded == original
    
    def test_encode_auto_mode_false_explicit(self):
        """Test explicitly setting auto_mode=False."""
        data = {"test": "data"}
        result1 = toonstream.encode(data)
        result2 = toonstream.encode(data, auto_mode=False)
        assert result1 == result2
    
    def test_decode_auto_mode_false_explicit(self):
        """Test explicitly setting auto_mode=False on decode."""
        toon_str = 'test: "data"'
        result1 = toonstream.decode(toon_str)
        result2 = toonstream.decode(toon_str, auto_mode=False)
        assert result1 == result2
    
    def test_encode_auto_mode_with_normal_data(self):
        """Test auto_mode=True with normal (non-tensor) data."""
        data = {"name": "Alice", "age": 30}
        result1 = toonstream.encode(data)
        result2 = toonstream.encode(data, auto_mode=True)
        
        # Auto mode should use normal encoding for non-tensor data
        decoded1 = toonstream.decode(result1)
        decoded2 = toonstream.decode(result2, auto_mode=True)
        
        assert decoded1 == data
        assert decoded2 == data
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_encode_auto_mode_with_tensor_data(self):
        """Test auto_mode=True auto-detects and uses tensor mode."""
        data = {
            "weights": torch.randn(5),
            "label": "test"
        }
        
        # Auto mode should detect tensor and use tensor encoding
        result = toonstream.encode(data, auto_mode=True)
        assert isinstance(result, str)
        # Tensor data should be in result
        assert "torch" in result or "dtype" in result
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_decode_auto_mode_with_tensor_encoded(self):
        """Test auto_mode=True on decode with tensor-encoded data."""
        original = {"values": torch.randn(3)}
        
        # Encode with auto_mode
        encoded = toonstream.encode(original, auto_mode=True)
        
        # Decode with auto_mode
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.is_tensor(decoded["values"])
        assert torch.equal(original["values"], decoded["values"])
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_auto_mode_roundtrip_with_tensors(self):
        """Test encode-decode roundtrip with auto_mode=True and tensors."""
        original = {
            "features": torch.randn(10, 5),
            "labels": torch.tensor([0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
            "metadata": {"source": "test"}
        }
        
        encoded = toonstream.encode(original, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(original["features"], decoded["features"])
        assert torch.equal(original["labels"], decoded["labels"])
        assert decoded["metadata"] == original["metadata"]
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_auto_mode_preserves_dtype(self):
        """Test that auto_mode=True preserves tensor dtypes."""
        original = {
            "float32": torch.randn(5, dtype=torch.float32),
            "float16": torch.randn(5, dtype=torch.float16),
            "int64": torch.tensor([1, 2, 3, 4, 5], dtype=torch.int64)
        }
        
        encoded = toonstream.encode(original, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert decoded["float32"].dtype == torch.float32
        assert decoded["float16"].dtype == torch.float16
        assert decoded["int64"].dtype == torch.int64
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_auto_mode_with_mixed_data(self):
        """Test auto_mode with both tensors and normal data."""
        data = {
            "tensor_field": torch.randn(3),
            "string_field": "hello",
            "number_field": 42,
            "list_field": [1, 2, 3]
        }
        
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(data["tensor_field"], decoded["tensor_field"])
        assert decoded["string_field"] == "hello"
        assert decoded["number_field"] == 42
        assert decoded["list_field"] == [1, 2, 3]
    
    def test_encode_with_additional_kwargs(self):
        """Test that additional kwargs are passed through."""
        data = {"a": 1, "b": 2}
        
        # Should work with auto_mode and other parameters
        result1 = toonstream.encode(data, auto_mode=False, sort_keys=True)
        result2 = toonstream.encode(data, auto_mode=False, indent=0)
        
        assert isinstance(result1, str)
        assert isinstance(result2, str)
    
    def test_encode_function_exists(self):
        """Test that encode function is properly exported."""
        assert hasattr(toonstream, 'encode')
        assert callable(toonstream.encode)
    
    def test_decode_function_exists(self):
        """Test that decode function is properly exported."""
        assert hasattr(toonstream, 'decode')
        assert callable(toonstream.decode)
    
    def test_backward_compatibility(self):
        """Test that old tensor functions still work."""
        if TORCH_AVAILABLE:
            data = {"t": torch.randn(3)}
            
            # Old API should still work
            encoded = toonstream.encode_with_tensors(data)
            decoded = toonstream.decode_with_tensors(encoded)
            assert torch.equal(data["t"], decoded["t"])


class TestAutoModeEdgeCases:
    """Test edge cases and specific scenarios."""
    
    def test_empty_dict(self):
        """Test with empty dictionary."""
        data = {}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_nested_structures(self):
        """Test with nested data structures."""
        data = {
            "level1": {
                "level2": {
                    "level3": [1, 2, 3]
                }
            }
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_nested_tensors(self):
        """Test with nested structures containing tensors."""
        data = {
            "models": {
                "model_a": {
                    "weights": torch.randn(5),
                    "config": {"layers": 3}
                }
            }
        }
        
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(
            data["models"]["model_a"]["weights"],
            decoded["models"]["model_a"]["weights"]
        )
        assert decoded["models"]["model_a"]["config"] == {"layers": 3}
    
    def test_special_characters(self):
        """Test with special characters in strings."""
        data = {
            "special": "Hello, World! @#$%",
            "items": [
                {"text": "Line 1\nLine 2"},
                {"text": "Tab\tSeparated"}
            ]
        }
        
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
