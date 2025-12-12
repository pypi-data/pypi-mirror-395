"""
Comprehensive unit tests for ToonStream with both normal and auto_mode.

Tests verify that:
1. Normal encode/decode works correctly
2. Auto_mode encode/decode works correctly
3. Both produce equivalent results for non-tensor data
4. Auto_mode correctly handles tensor data
"""

import pytest
import toonstream

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TestBasicEncodingDecoding:
    """Test basic encode/decode functionality."""
    
    def test_simple_dict_normal(self):
        """Test encoding/decoding simple dict in normal mode."""
        data = {"name": "Alice", "age": 30}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_simple_dict_auto_mode(self):
        """Test encoding/decoding simple dict with auto_mode."""
        data = {"name": "Alice", "age": 30}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_list_of_dicts_normal(self):
        """Test list of dicts in normal mode."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"}
            ]
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_list_of_dicts_auto_mode(self):
        """Test list of dicts with auto_mode."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"}
            ]
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_nested_structures_normal(self):
        """Test nested structures in normal mode."""
        data = {
            "company": {
                "dept": {
                    "team": {
                        "members": ["Alice", "Bob", "Charlie"]
                    }
                }
            }
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_nested_structures_auto_mode(self):
        """Test nested structures with auto_mode."""
        data = {
            "company": {
                "dept": {
                    "team": {
                        "members": ["Alice", "Bob", "Charlie"]
                    }
                }
            }
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data


class TestDataTypes:
    """Test various data types in both modes."""
    
    def test_strings_normal(self):
        """Test string handling in normal mode."""
        data = {"text": "Hello, World!", "multiline": "Line1\nLine2"}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_strings_auto_mode(self):
        """Test string handling with auto_mode."""
        data = {"text": "Hello, World!", "multiline": "Line1\nLine2"}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_numbers_normal(self):
        """Test number handling in normal mode."""
        data = {
            "int": 42,
            "float": 3.14,
            "negative": -100,
            "zero": 0
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_numbers_auto_mode(self):
        """Test number handling with auto_mode."""
        data = {
            "int": 42,
            "float": 3.14,
            "negative": -100,
            "zero": 0
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_booleans_normal(self):
        """Test boolean handling in normal mode."""
        data = {"active": True, "deleted": False}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_booleans_auto_mode(self):
        """Test boolean handling with auto_mode."""
        data = {"active": True, "deleted": False}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_none_values_normal(self):
        """Test None values in normal mode."""
        data = {"value": None, "other": "text"}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_none_values_auto_mode(self):
        """Test None values with auto_mode."""
        data = {"value": None, "other": "text"}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data


class TestArrayOptimization:
    """Test array/list handling in both modes."""
    
    def test_small_array_normal(self):
        """Test small array in normal mode."""
        data = {"items": [1, 2]}  # Too small for tabular
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_small_array_auto_mode(self):
        """Test small array with auto_mode."""
        data = {"items": [1, 2]}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_large_array_normal(self):
        """Test large array in normal mode (should use tabular)."""
        data = {
            "items": [
                {"id": i, "name": f"Item{i}", "value": i * 10}
                for i in range(10)
            ]
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_large_array_auto_mode(self):
        """Test large array with auto_mode (should use tabular)."""
        data = {
            "items": [
                {"id": i, "name": f"Item{i}", "value": i * 10}
                for i in range(10)
            ]
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data


class TestComparison:
    """Compare normal mode and auto_mode behavior."""
    
    def test_same_output_for_normal_data(self):
        """Verify normal mode and auto_mode produce same output for non-tensor data."""
        data = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"}
            ]
        }
        
        encoded_normal = toonstream.encode(data)
        encoded_auto = toonstream.encode(data, auto_mode=True)
        
        # Both should decode to same data
        decoded_normal = toonstream.decode(encoded_normal)
        decoded_auto = toonstream.decode(encoded_auto, auto_mode=True)
        
        assert decoded_normal == data
        assert decoded_auto == data
    
    def test_mode_consistency_simple(self):
        """Test that both modes handle simple data consistently."""
        data = {"a": 1, "b": 2, "c": 3}
        
        result_normal = toonstream.decode(toonstream.encode(data))
        result_auto = toonstream.decode(toonstream.encode(data, auto_mode=True), auto_mode=True)
        
        assert result_normal == result_auto == data
    
    def test_mode_consistency_complex(self):
        """Test that both modes handle complex data consistently."""
        data = {
            "level1": {
                "level2": {
                    "items": [
                        {"x": 1, "y": 2},
                        {"x": 3, "y": 4}
                    ]
                }
            }
        }
        
        result_normal = toonstream.decode(toonstream.encode(data))
        result_auto = toonstream.decode(toonstream.encode(data, auto_mode=True), auto_mode=True)
        
        assert result_normal == result_auto == data


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
class TestTensorModeWithAutoMode:
    """Test tensor handling with auto_mode."""
    
    def test_tensor_auto_mode_single(self):
        """Test auto_mode with single tensor."""
        data = {"weights": torch.randn(5)}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.is_tensor(decoded["weights"])
        assert torch.equal(data["weights"], decoded["weights"])
    
    def test_tensor_auto_mode_multiple(self):
        """Test auto_mode with multiple tensors."""
        data = {
            "weights": torch.randn(5),
            "bias": torch.randn(3),
            "labels": torch.tensor([0, 1, 1, 0, 1])
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(data["weights"], decoded["weights"])
        assert torch.equal(data["bias"], decoded["bias"])
        assert torch.equal(data["labels"], decoded["labels"])
    
    def test_tensor_auto_mode_multidim(self):
        """Test auto_mode with multidimensional tensors."""
        data = {
            "matrix": torch.randn(10, 5),
            "tensor_3d": torch.randn(2, 3, 4)
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(data["matrix"], decoded["matrix"])
        assert torch.equal(data["tensor_3d"], decoded["tensor_3d"])
    
    def test_tensor_auto_mode_dtypes(self):
        """Test auto_mode preserves tensor dtypes."""
        data = {
            "float32": torch.randn(5, dtype=torch.float32),
            "float16": torch.randn(5, dtype=torch.float16),
            "int64": torch.tensor([1, 2, 3, 4, 5], dtype=torch.int64)
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert decoded["float32"].dtype == torch.float32
        assert decoded["float16"].dtype == torch.float16
        assert decoded["int64"].dtype == torch.int64
    
    def test_tensor_auto_mode_mixed(self):
        """Test auto_mode with mixed tensor and normal data."""
        data = {
            "embeddings": torch.randn(100, 768),
            "labels": torch.tensor([0, 1, 1, 0] * 25),
            "metadata": {
                "model": "bert-base",
                "source": "wikipedia",
                "sample_count": 100
            },
            "config": {
                "learning_rate": 0.001,
                "epochs": 10
            }
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(data["embeddings"], decoded["embeddings"])
        assert torch.equal(data["labels"], decoded["labels"])
        assert decoded["metadata"] == data["metadata"]
        assert decoded["config"] == data["config"]
    
    def test_tensor_auto_mode_nested(self):
        """Test auto_mode with nested structures containing tensors."""
        data = {
            "models": {
                "model_a": {
                    "weights": torch.randn(10),
                    "bias": torch.randn(5),
                    "info": {"trained": True}
                },
                "model_b": {
                    "weights": torch.randn(20),
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
        assert torch.equal(
            data["models"]["model_a"]["bias"],
            decoded["models"]["model_a"]["bias"]
        )
        assert torch.equal(
            data["models"]["model_b"]["weights"],
            decoded["models"]["model_b"]["weights"]
        )
        assert decoded["models"]["model_a"]["info"] == {"trained": True}


class TestEdgeCases:
    """Test edge cases in both modes."""
    
    def test_empty_dict_normal(self):
        """Test empty dict in normal mode."""
        data = {}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_empty_dict_auto_mode(self):
        """Test empty dict with auto_mode."""
        data = {}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_empty_list_normal(self):
        """Test empty list in normal mode."""
        data = {"items": []}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_empty_list_auto_mode(self):
        """Test empty list with auto_mode."""
        data = {"items": []}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_special_characters_normal(self):
        """Test special characters in normal mode."""
        data = {
            "symbols": "@#$%^&*()",
            "quotes": 'He said "Hello"',
            "backslash": "C:\\Users\\test"
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_special_characters_auto_mode(self):
        """Test special characters with auto_mode."""
        data = {
            "symbols": "@#$%^&*()",
            "quotes": 'He said "Hello"',
            "backslash": "C:\\Users\\test"
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_very_long_string_normal(self):
        """Test very long string in normal mode."""
        data = {"text": "x" * 10000}
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_very_long_string_auto_mode(self):
        """Test very long string with auto_mode."""
        data = {"text": "x" * 10000}
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data


class TestRealWorldScenarios:
    """Test real-world use cases in both modes."""
    
    def test_user_profile_normal(self):
        """Test user profile data in normal mode."""
        data = {
            "users": [
                {
                    "id": 1,
                    "username": "alice",
                    "email": "alice@example.com",
                    "active": True,
                    "age": 30
                },
                {
                    "id": 2,
                    "username": "bob",
                    "email": "bob@example.com",
                    "active": False,
                    "age": 25
                }
            ]
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_user_profile_auto_mode(self):
        """Test user profile data with auto_mode."""
        data = {
            "users": [
                {
                    "id": 1,
                    "username": "alice",
                    "email": "alice@example.com",
                    "active": True,
                    "age": 30
                },
                {
                    "id": 2,
                    "username": "bob",
                    "email": "bob@example.com",
                    "active": False,
                    "age": 25
                }
            ]
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    def test_api_response_normal(self):
        """Test API response structure in normal mode."""
        data = {
            "status": "success",
            "code": 200,
            "data": {
                "items": [
                    {"id": i, "value": i * 10, "timestamp": "2024-01-01"}
                    for i in range(5)
                ]
            }
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    def test_api_response_auto_mode(self):
        """Test API response structure with auto_mode."""
        data = {
            "status": "success",
            "code": 200,
            "data": {
                "items": [
                    {"id": i, "value": i * 10, "timestamp": "2024-01-01"}
                    for i in range(5)
                ]
            }
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        assert decoded == data
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_ml_dataset_normal_encoding(self):
        """Test ML dataset with normal encoding (tensors become lists)."""
        # Note: Normal mode will convert tensors to lists
        data = {
            "samples": 100,
            "features": 50,
            "classes": 10
        }
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        assert decoded == data
    
    @pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")
    def test_ml_dataset_auto_mode(self):
        """Test ML dataset with auto_mode (preserves tensor metadata)."""
        data = {
            "training_data": {
                "features": torch.randn(100, 50),
                "labels": torch.randint(0, 10, (100,)),
                "sample_weights": torch.ones(100)
            },
            "metadata": {
                "samples": 100,
                "feature_count": 50,
                "classes": 10,
                "dataset_name": "training_v2"
            }
        }
        encoded = toonstream.encode(data, auto_mode=True)
        decoded = toonstream.decode(encoded, auto_mode=True)
        
        assert torch.equal(
            data["training_data"]["features"],
            decoded["training_data"]["features"]
        )
        assert torch.equal(
            data["training_data"]["labels"],
            decoded["training_data"]["labels"]
        )
        assert decoded["metadata"] == data["metadata"]
