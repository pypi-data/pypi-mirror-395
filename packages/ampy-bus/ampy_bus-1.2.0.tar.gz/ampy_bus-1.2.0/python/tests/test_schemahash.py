from ampybus.schemahash import expected_schema_hash, verify_schema_hash

def test_expected_schema_hash_fallback():
    """Test schema hash - works with or without ampy-proto registered.
    
    When ampy-proto types are registered in the protobuf registry,
    we get a real sha256 hash. Otherwise, we get a nameonly fallback.
    Both are valid behaviors.
    """
    fqdn = "ampy.bars.v1.BarBatch"
    h = expected_schema_hash(fqdn)
    # Accept either real hash (when ampy-proto is registered) or fallback
    assert h.startswith(("sha256:", "nameonly:sha256:")), \
        f"Hash should start with sha256: or nameonly:sha256:, got: {h}"

def test_verify_ok():
    fqdn = "ampy.bars.v1.BarBatch"
    exp = expected_schema_hash(fqdn)
    verify_schema_hash(fqdn, exp)  # should not raise
