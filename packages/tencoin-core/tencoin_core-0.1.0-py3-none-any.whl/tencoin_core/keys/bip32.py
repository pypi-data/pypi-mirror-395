# tencoin-core/tencoin_core/keys/bip32.py
"""
BIP-32: Hierarchical Deterministic Wallets
"""
import hmac
import struct
from typing import Tuple, List
from .ec import privkey_to_pubkey
from ..utils import hmac_sha512, ser_32, ser_256, parse_256

class BIP32Error(Exception):
    """BIP-32 related errors"""
    pass

# BIP-32 constants
HARDENED_OFFSET = 0x80000000
MAINNET_VERSION = 0x0488B21E  # xpub
MAINNET_PRIVATE_VERSION = 0x0488ADE4  # xprv

def derive_child_key(parent_key: bytes, parent_chain_code: bytes, 
                     index: int, is_private: bool = True) -> Tuple[bytes, bytes]:
    """
    Derive child key from parent key.
    
    Args:
        parent_key: 33-byte public key or 32-byte private key
        parent_chain_code: 32-byte chain code
        index: Child index
        is_private: Whether parent_key is private
        
    Returns:
        (child_key, child_chain_code)
    """
    if is_private:
        if len(parent_key) != 32:
            raise BIP32Error(f"Invalid private key length: {len(parent_key)}")
        
        if index >= HARDENED_OFFSET:
            # Hardened derivation
            data = b'\x00' + parent_key + struct.pack(">I", index)
        else:
            # Normal derivation
            parent_pubkey = privkey_to_pubkey(parent_key, compressed=True)
            data = parent_pubkey + struct.pack(">I", index)
    else:
        if len(parent_key) != 33:
            raise BIP32Error(f"Invalid public key length: {len(parent_key)}")
        
        if index >= HARDENED_OFFSET:
            raise BIP32Error("Cannot derive hardened child from public key")
        
        data = parent_key + struct.pack(">I", index)
    
    # HMAC-SHA512
    hmac_result = hmac_sha512(parent_chain_code, data)
    left = hmac_result[:32]
    right = hmac_result[32:]
    
    if is_private:
        # Private key derivation
        parent_key_int = parse_256(parent_key)
        left_int = parse_256(left)
        
        # n = order of secp256k1
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        
        child_key_int = (left_int + parent_key_int) % n
        if child_key_int == 0:
            raise BIP32Error("Derived invalid private key")
        
        child_key = ser_256(child_key_int)
    else:
        # Public key derivation - نیاز به پیاده‌سازی EC point addition
        # فعلاً NotImplemented
        raise NotImplementedError("Public key derivation not yet implemented")
    
    return child_key, right

def create_master_key(seed: bytes) -> Tuple[bytes, bytes]:
    """
    Create master key and chain code from seed.
    
    Args:
        seed: 64-byte seed
        
    Returns:
        (master_private_key, master_chain_code)
    """
    # HMAC-SHA512 with key "Bitcoin seed"
    hmac_result = hmac_sha512(b"Bitcoin seed", seed)
    
    master_key = hmac_result[:32]
    master_chain_code = hmac_result[32:]
    
    # Validate key
    key_int = parse_256(master_key)
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    
    if key_int == 0 or key_int >= n:
        raise BIP32Error("Invalid master key")
    
    return master_key, master_chain_code

def derive_path_from_seed(seed: bytes, path: str) -> Tuple[bytes, bytes]:
    """
    Derive key at specified path from seed.
    
    Args:
        seed: 64-byte seed
        path: Derivation path like "m/84'/5353'/0'/0/0"
        
    Returns:
        (private_key, chain_code)
    """
    # Parse path
    if not path.startswith("m/"):
        raise BIP32Error(f"Invalid path: {path}")
    
    indices = path[2:].split('/')
    if not indices:
        raise BIP32Error(f"Invalid path: {path}")
    
    # Create master key
    private_key, chain_code = create_master_key(seed)
    
    # Derive through each level
    for index_str in indices:
        if index_str.endswith("'"):
            # Hardened
            index = int(index_str[:-1]) + HARDENED_OFFSET
        else:
            # Normal
            index = int(index_str)
        
        private_key, chain_code = derive_child_key(
            private_key, chain_code, index, is_private=True
        )
    
    return private_key, chain_code

def path_to_indices(path: str) -> List[int]:
    """
    Convert derivation path string to list of indices.
    
    Args:
        path: Like "m/84'/5353'/0'/0/0"
        
    Returns:
        List of indices
    """
    if not path.startswith("m/"):
        raise BIP32Error(f"Invalid path: {path}")
    
    indices = []
    for part in path[2:].split('/'):
        if part.endswith("'"):
            indices.append(int(part[:-1]) + HARDENED_OFFSET)
        else:
            indices.append(int(part))
    
    return indices