# tencoin-core/tencoin_core/keys/ec.py
"""
Elliptic Curve operations for secp256k1
"""
import hashlib

# Try to import ecdsa library
try:
    from ecdsa import SigningKey, VerifyingKey, SECP256k1
    from ecdsa.util import sigencode_der, sigdecode_der
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False
    SECP256k1 = None

# Secp256k1 parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def bytes_to_int(b: bytes) -> int:
    """Convert bytes to integer (big-endian)"""
    return int.from_bytes(b, 'big')

def int_to_bytes(i: int, length: int = 32) -> bytes:
    """Convert integer to bytes (big-endian)"""
    return i.to_bytes(length, 'big')

def point_to_pubkey(x: int, y: int, compressed: bool = True) -> bytes:
    """Convert (x, y) point to public key bytes"""
    if compressed:
        prefix = b'\x02' if y % 2 == 0 else b'\x03'
        return prefix + int_to_bytes(x, 32)
    else:
        return b'\x04' + int_to_bytes(x, 32) + int_to_bytes(y, 32)

def privkey_to_pubkey(privkey: bytes, compressed: bool = True) -> bytes:
    """Convert private key to public key"""
    if not ECDSA_AVAILABLE:
        raise ImportError("ecdsa library is required. Install with: pip install ecdsa")
    
    sk = SigningKey.from_string(privkey, curve=SECP256k1)
    vk = sk.get_verifying_key()
    
    if compressed:
        # Get compressed format
        point = vk.pubkey.point
        prefix = b'\x02' if point.y() % 2 == 0 else b'\x03'
        return prefix + int_to_bytes(point.x())
    else:
        return b'\x04' + vk.to_string()

def sign(privkey: bytes, msg_hash: bytes) -> bytes:
    """Sign message hash with private key"""
    if not ECDSA_AVAILABLE:
        raise ImportError("ecdsa library is required. Install with: pip install ecdsa")
    
    sk = SigningKey.from_string(privkey, curve=SECP256k1)
    sig = sk.sign_digest(msg_hash, sigencode=sigencode_der)
    return sig

def verify(pubkey: bytes, msg_hash: bytes, sig: bytes) -> bool:
    """Verify signature"""
    if not ECDSA_AVAILABLE:
        raise ImportError("ecdsa library is required. Install with: pip install ecdsa")
    
    try:
        vk = VerifyingKey.from_string(pubkey, curve=SECP256k1)
        return vk.verify_digest(sig, msg_hash, sigdecode=sigdecode_der)
    except Exception:
        return False