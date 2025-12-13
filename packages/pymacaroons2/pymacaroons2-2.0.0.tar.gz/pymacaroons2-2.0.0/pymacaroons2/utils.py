import base64
from hashlib import sha256
import hmac
import binascii
import secrets
from cryptography.hazmat.primitives import hashes, hmac as crypto_hmac
from cryptography.hazmat.backends import default_backend

_BACKEND = default_backend()

# Try to import Rust extension for performance-critical operations
try:
    import pymacaroons2_rs as _rs

    _HAS_RUST = True
except ImportError:
    _rs = None
    _HAS_RUST = False


def convert_to_bytes(obj) -> bytes:
    """Convert string/bytes to bytes."""
    if isinstance(obj, str):
        return obj.encode("utf-8")
    elif isinstance(obj, bytes):
        return obj
    elif obj is None:
        return b""
    else:
        return str(obj).encode("utf-8")


def convert_to_string(obj) -> str:
    """Convert string/bytes to string."""
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    elif isinstance(obj, str):
        return obj
    elif obj is None:
        return ""
    else:
        return str(obj)


def truncate_or_pad(byte_string, size=None):
    if size is None:
        size = 32
    byte_array = bytearray(byte_string)
    length = len(byte_array)
    if length > size:
        return bytes(byte_array[:size])
    elif length < size:
        return bytes(byte_array + b"\0" * (size - length))
    else:
        return byte_string


def generate_derived_key(key):
    """Generate derived key using HMAC-SHA256.

    Uses Rust implementation if available for better performance.
    """
    if _HAS_RUST:
        return _rs.generate_derived_key(key)
    return _hmac_digest_python(b"macaroons-key-generator", key)


def _hmac_digest_python(key: bytes, data: bytes) -> bytes:
    """Pure Python HMAC-SHA256 implementation using cryptography library."""
    h = crypto_hmac.HMAC(key, hashes.SHA256(), backend=_BACKEND)
    h.update(data)
    return h.finalize()


def hmac_digest(key: bytes, data: bytes) -> bytes:
    """Constant-time HMAC-SHA256.

    Uses Rust implementation if available for better performance.
    """
    if _HAS_RUST:
        return _rs.hmac_digest(key, data)
    return _hmac_digest_python(key, data)


def hmac_hex(key, data):
    dig = hmac_digest(key, data)
    return binascii.hexlify(dig)


def create_initial_signature(key, identifier):
    derived_key = generate_derived_key(key)
    return hmac_hex(derived_key, identifier)


def hmac_concat(key, data1, data2):
    hash1 = hmac_digest(key, data1)
    hash2 = hmac_digest(key, data2)
    return hmac_hex(key, hash1 + hash2)


def sign_first_party_caveat(signature, predicate):
    return hmac_hex(signature, predicate)


def sign_third_party_caveat(signature, verification_id, caveat_id):
    return hmac_concat(signature, verification_id, caveat_id)


def add_base64_padding(b):
    """Add padding to base64 encoded bytes.

    Padding can be removed when sending the messages.

    @param b bytes to be padded.
    @return a padded bytes.
    """
    return b + b"=" * (-len(b) % 4)


def raw_b64decode(s):
    if "_" or "-" in s:
        return raw_urlsafe_b64decode(s)
    else:
        return base64.b64decode(add_base64_padding(s))


def raw_urlsafe_b64decode(s):
    """Base64 decode with added padding and conversion to bytes.

    @param s string decode
    @return bytes decoded
    """
    if isinstance(s, str):
        s_bytes = s.encode("ascii")
    else:
        s_bytes = s

    # FIX: Proper check for URL-safe chars
    if b"_" in s_bytes or b"-" in s_bytes:
        return base64.urlsafe_b64decode(s_bytes + b"=" * (-len(s_bytes) % 4))
    return base64.b64decode(s_bytes + b"=" * (-len(s_bytes) % 4))


def raw_urlsafe_b64encode(b):
    """Base64 encode with padding removed.

    @param s string decode
    @return bytes decoded
    """
    return base64.urlsafe_b64encode(b).rstrip(b"=")


def constant_time_compare(val1: bytes, val2: bytes) -> bool:
    """Secure constant-time comparison.

    Uses Rust implementation if available for better performance.
    """
    if _HAS_RUST:
        return _rs.constant_time_compare(val1, val2)
    return secrets.compare_digest(val1, val2)
