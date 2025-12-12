"""
Test tensor utilities for ToonStream.
"""

import pytest

# Try to import torch
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Skip all tests if torch is not available
pytestmark = pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch not installed")

if TORCH_AVAILABLE:
    import toonstream
    from toonstream.tensor_utils import (
        TensorEncoder,
        TensorDecoder,
        encode_with_tensors,
        decode_with_tensors,
        is_torch_available
    )


class TestTensorEncoder:
    """Test TensorEncoder class."""
    
    def test_encode_simple_tensor(self):
        """Test encoding a simple tensor."""
        tensor = torch.tensor([1, 2, 3])
        encoder = TensorEncoder()
        
        encoded = encoder.encode_tensor(tensor)
        
        assert encoded['data'] == [1, 2, 3]
        assert encoded['shape'] == [3]
        assert 'torch' in encoded['dtype']
        assert encoded['_type'] == 'torch.Tensor'
    
    def test_encode_2d_tensor(self):
        """Test encoding a 2D tensor."""
        tensor = torch.tensor([[1, 2], [3, 4]])
        encoder = TensorEncoder()
        
        encoded = encoder.encode_tensor(tensor)
        
        assert encoded['data'] == [[1, 2], [3, 4]]
        assert encoded['shape'] == [2, 2]
    
    def test_encode_float_tensor(self):
        """Test encoding a float tensor."""
        tensor = torch.tensor([1.5, 2.5, 3.5])
        encoder = TensorEncoder()
        
        encoded = encoder.encode_tensor(tensor)
        
        assert encoded['data'] == [1.5, 2.5, 3.5]
        assert 'float' in encoded['dtype']
    
    def test_is_tensor(self):
        """Test tensor detection."""
        encoder = TensorEncoder()
        
        assert encoder.is_tensor(torch.tensor([1, 2, 3])) is True
        assert encoder.is_tensor([1, 2, 3]) is False
        assert encoder.is_tensor("string") is False
    
    def test_encode_recursive_dict(self):
        """Test recursive encoding of dictionaries with tensors."""
        data = {
            'weights': torch.tensor([1.0, 2.0]),
            'bias': torch.tensor([0.5]),
            'config': {'layers': 3}
        }
        encoder = TensorEncoder()
        
        encoded = encoder.encode_recursive(data)
        
        assert encoded['weights']['_type'] == 'torch.Tensor'
        assert encoded['bias']['_type'] == 'torch.Tensor'
        assert encoded['config']['layers'] == 3
    
    def test_encode_recursive_list(self):
        """Test recursive encoding of lists with tensors."""
        data = [
            torch.tensor([1, 2]),
            torch.tensor([3, 4]),
            {'value': torch.tensor([5])}
        ]
        encoder = TensorEncoder()
        
        encoded = encoder.encode_recursive(data)
        
        assert encoded[0]['_type'] == 'torch.Tensor'
        assert encoded[1]['_type'] == 'torch.Tensor'
        assert encoded[2]['value']['_type'] == 'torch.Tensor'


class TestTensorDecoder:
    """Test TensorDecoder class."""
    
    def test_decode_simple_tensor(self):
        """Test decoding a simple tensor."""
        tensor_dict = {
            'data': [1, 2, 3],
            'shape': [3],
            'dtype': 'torch.int64',
            'device': 'cpu',
            '_type': 'torch.Tensor'
        }
        decoder = TensorDecoder()
        
        tensor = decoder.decode_tensor(tensor_dict)
        
        assert isinstance(tensor, torch.Tensor)
        assert tensor.tolist() == [1, 2, 3]
        assert tensor.shape == torch.Size([3])
    
    def test_decode_2d_tensor(self):
        """Test decoding a 2D tensor."""
        tensor_dict = {
            'data': [[1, 2], [3, 4]],
            'shape': [2, 2],
            'dtype': 'torch.int64',
            'device': 'cpu',
            '_type': 'torch.Tensor'
        }
        decoder = TensorDecoder()
        
        tensor = decoder.decode_tensor(tensor_dict)
        
        assert tensor.tolist() == [[1, 2], [3, 4]]
        assert tensor.shape == torch.Size([2, 2])
    
    def test_decode_float_tensor(self):
        """Test decoding a float tensor."""
        tensor_dict = {
            'data': [1.5, 2.5, 3.5],
            'shape': [3],
            'dtype': 'torch.float32',
            'device': 'cpu',
            '_type': 'torch.Tensor'
        }
        decoder = TensorDecoder()
        
        tensor = decoder.decode_tensor(tensor_dict)
        
        assert tensor.tolist() == [1.5, 2.5, 3.5]
        assert tensor.dtype == torch.float32
    
    def test_is_tensor_dict(self):
        """Test tensor dictionary detection."""
        decoder = TensorDecoder()
        
        valid_dict = {
            'data': [1, 2],
            '_type': 'torch.Tensor'
        }
        invalid_dict = {'data': [1, 2]}
        
        assert decoder.is_tensor_dict(valid_dict) is True
        assert decoder.is_tensor_dict(invalid_dict) is False
        assert decoder.is_tensor_dict("not a dict") is False
    
    def test_decode_recursive_dict(self):
        """Test recursive decoding of dictionaries."""
        data = {
            'weights': {
                'data': [1.0, 2.0],
                'shape': [2],
                'dtype': 'torch.float32',
                'device': 'cpu',
                '_type': 'torch.Tensor'
            },
            'config': {'layers': 3}
        }
        decoder = TensorDecoder()
        
        decoded = decoder.decode_recursive(data)
        
        assert isinstance(decoded['weights'], torch.Tensor)
        assert decoded['weights'].tolist() == [1.0, 2.0]
        assert decoded['config']['layers'] == 3


class TestRoundTrip:
    """Test round-trip encoding and decoding."""
    
    def test_simple_tensor_roundtrip(self):
        """Test encoding and decoding a simple tensor."""
        original = torch.tensor([1, 2, 3, 4, 5])
        
        encoder = TensorEncoder()
        decoder = TensorDecoder()
        
        encoded = encoder.encode_tensor(original)
        decoded = decoder.decode_tensor(encoded)
        
        assert torch.equal(original, decoded)
    
    def test_complex_data_roundtrip(self):
        """Test encoding and decoding complex data with tensors."""
        original = {
            'model': 'transformer',
            'embeddings': torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
            'labels': torch.tensor([0, 1]),
            'config': {
                'layers': 12,
                'hidden_size': 768
            }
        }
        
        encoder = TensorEncoder()
        decoder = TensorDecoder()
        
        encoded = encoder.encode_recursive(original)
        decoded = decoder.decode_recursive(encoded)
        
        assert decoded['model'] == 'transformer'
        assert torch.equal(original['embeddings'], decoded['embeddings'])
        assert torch.equal(original['labels'], decoded['labels'])
        assert decoded['config']['layers'] == 12


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_encode_with_tensors(self):
        """Test encode_with_tensors function."""
        data = {
            'weights': torch.tensor([1.0, 2.0, 3.0]),
            'bias': 0.5
        }
        
        toon_str = encode_with_tensors(data)
        
        assert isinstance(toon_str, str)
        assert len(toon_str) > 0
    
    def test_decode_with_tensors(self):
        """Test decode_with_tensors function."""
        data = {
            'weights': torch.tensor([1.0, 2.0, 3.0]),
            'bias': 0.5
        }
        
        toon_str = encode_with_tensors(data)
        decoded = decode_with_tensors(toon_str)
        
        assert isinstance(decoded['weights'], torch.Tensor)
        assert torch.equal(data['weights'], decoded['weights'])
        assert decoded['bias'] == 0.5
    
    def test_full_roundtrip_with_tensors(self):
        """Test full round-trip with tensors."""
        original = {
            'model': 'bert-base',
            'layers': [
                {'weights': torch.tensor([[1, 2], [3, 4]]), 'bias': torch.tensor([1, 2])},
                {'weights': torch.tensor([[5, 6], [7, 8]]), 'bias': torch.tensor([3, 4])}
            ],
            'config': {'hidden_size': 768}
        }
        
        toon_str = encode_with_tensors(original)
        decoded = decode_with_tensors(toon_str)
        
        assert decoded['model'] == 'bert-base'
        assert len(decoded['layers']) == 2
        assert torch.equal(original['layers'][0]['weights'], decoded['layers'][0]['weights'])
        assert decoded['config']['hidden_size'] == 768
    
    def test_is_torch_available(self):
        """Test is_torch_available function."""
        assert is_torch_available() is True


class TestIntegration:
    """Test integration with main toonstream API."""
    
    def test_import_from_main_module(self):
        """Test that tensor utilities can be imported from main module."""
        assert hasattr(toonstream, 'encode_with_tensors')
        assert hasattr(toonstream, 'decode_with_tensors')
        assert hasattr(toonstream, 'TensorEncoder')
        assert hasattr(toonstream, 'TensorDecoder')
        assert hasattr(toonstream, 'is_torch_available')
    
    def test_regular_encode_still_works(self):
        """Test that regular encode/decode still work without tensors."""
        data = {'a': 1, 'b': [2, 3, 4]}
        
        encoded = toonstream.encode(data)
        decoded = toonstream.decode(encoded)
        
        assert data == decoded
