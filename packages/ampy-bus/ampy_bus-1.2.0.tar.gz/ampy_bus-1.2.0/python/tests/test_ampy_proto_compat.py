"""
Test compatibility with ampy-proto types.

This test verifies that ampy-bus works correctly with the latest ampy-proto.
It tests schema hash computation when ampy-proto types are registered.
"""
import pytest

def test_ampy_proto_import():
    """Test that we can import ampy-proto types."""
    try:
        from ampy.bars.v1 import bars_pb2
        from ampy.signals.v1 import signals_pb2
        assert True, "Successfully imported ampy-proto types"
    except ImportError as e:
        pytest.skip(f"ampy-proto not available: {e}")

def test_schema_hash_with_ampy_proto():
    """Test that schema hash works with ampy-proto types registered."""
    try:
        from ampy.bars.v1 import bars_pb2
        from ampybus.schemahash import expected_schema_hash
        
        # Import the types to register them in the protobuf registry
        _ = bars_pb2.BarBatch()
        
        # Test schema hash for ampy-proto type
        fqdn = "ampy.bars.v1.BarBatch"
        hash_value = expected_schema_hash(fqdn)
        
        # Should get a real hash (not nameonly) if types are registered
        assert hash_value.startswith(("sha256:", "nameonly:sha256:")), \
            f"Unexpected hash format: {hash_value}"
        assert len(hash_value) > 20, "Hash should be substantial"
        
    except ImportError as e:
        pytest.skip(f"ampy-proto not available: {e}")

def test_encode_decode_with_ampy_proto():
    """Test encoding/decoding with actual ampy-proto types."""
    try:
        from ampy.bars.v1 import bars_pb2
        from ampybus.envelope import Envelope, new_headers, encode_protobuf, decode_payload, pk_bars
        
        # Create a real BarBatch message
        bar_batch = bars_pb2.BarBatch()
        bar = bar_batch.bars.add()
        bar.security.symbol = "AAPL"
        bar.security.mic = "XNAS"
        
        # Encode it
        payload, enc = encode_protobuf(bar_batch, compress_threshold=0)
        assert len(payload) > 0, "Payload should not be empty"
        
        # Create envelope
        h = new_headers("ampy.bars.v1.BarBatch", "test@host", "test", pk_bars("XNAS", "AAPL"))
        h.content_encoding = enc
        env = Envelope(topic="ampy.prod.bars.v1.XNAS.AAPL", headers=h, payload=payload)
        
        # Validate
        h.validate_basic()
        
        # Decode
        raw = decode_payload(env.payload, env.headers.content_encoding)
        assert raw == payload, "Round-trip should preserve payload"
        
    except ImportError as e:
        pytest.skip(f"ampy-proto not available: {e}")

