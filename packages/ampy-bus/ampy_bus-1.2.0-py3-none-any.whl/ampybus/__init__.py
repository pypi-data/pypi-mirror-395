from ._version import __version__

# Core envelope and codec functionality
from .envelope import (
    CONTENT_TYPE_PROTOBUF,
    ENCODING_GZIP,
    DEFAULT_COMPRESS_THRESHOLD,
    Headers,
    Envelope,
    new_headers,
    encode_protobuf,
    decode_payload,
    pk_bars, pk_ticks, pk_news_id, pk_fx, pk_signals,
    pk_orders, pk_fills, pk_positions, pk_metrics,
)

# Schema validation
from .schemahash import expected_schema_hash, verify_schema_hash

# Tracing support
from .trace import make_traceparent

# Re-export commonly used items for convenience
__all__ = [
    '__version__',
    'CONTENT_TYPE_PROTOBUF',
    'ENCODING_GZIP',
    'DEFAULT_COMPRESS_THRESHOLD',
    'Headers',
    'Envelope',
    'new_headers',
    'encode_protobuf',
    'decode_payload',
    'pk_bars', 'pk_ticks', 'pk_news_id', 'pk_fx', 'pk_signals',
    'pk_orders', 'pk_fills', 'pk_positions', 'pk_metrics',
    'expected_schema_hash',
    'verify_schema_hash',
    'make_traceparent',
]
