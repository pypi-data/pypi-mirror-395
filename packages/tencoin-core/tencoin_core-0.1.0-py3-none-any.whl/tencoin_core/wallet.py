# tencoin-core/tencoin_core/wallet.py
"""
Main Wallet class - High-level HD wallet interface
"""
import json
import os
from typing import Dict, List, Optional, Tuple
from .keys.bip39 import (
    generate_mnemonic, 
    mnemonic_to_seed, 
    validate_mnemonic,
    mnemonic_to_entropy
)
from .keys.bip84 import get_default_address_from_seed
from .constants import DERIVATION_PATH

class WalletError(Exception):
    """Wallet related errors"""
    pass

class Wallet:
    """
    HD Wallet for Tencoin (BIP-39 + BIP-84).
    
    Only supports SegWit native addresses (P2WPKH).
    """
    
    def __init__(self, seed: bytes, mnemonic: str = ""):
        """
        Initialize wallet from seed.
        
        Args:
            seed: 64-byte seed
            mnemonic: Optional mnemonic phrase
        """
        if len(seed) != 64:
            raise WalletError(f"Invalid seed length: {len(seed)}")
        
        self.seed = seed
        self.mnemonic = mnemonic
        
        # Derive default address
        self.private_key, self.public_key, self.address = \
            get_default_address_from_seed(seed)
        
        # Store additional info
        self.derivation_path = DERIVATION_PATH
        self.account_index = 0
        self.change_index = 0
        self.address_index = 0
    
    @classmethod
    def create(cls, strength: int = 128) -> 'Wallet':
        """
        Create a new HD wallet.
        
        Args:
            strength: Entropy strength in bits (128 for 12 words)
            
        Returns:
            Wallet instance
        """
        # Generate mnemonic
        mnemonic = generate_mnemonic(strength)
        
        # Convert to seed
        seed = mnemonic_to_seed(mnemonic)
        
        # Create wallet
        return cls(seed, mnemonic)
    
    @classmethod
    def recover(cls, mnemonic: str, passphrase: str = "") -> 'Wallet':
        """
        Recover wallet from mnemonic phrase.
        
        Args:
            mnemonic: 12, 15, 18, 21, or 24 words
            passphrase: Optional BIP-39 passphrase
            
        Returns:
            Wallet instance
        """
        # Validate mnemonic
        if not validate_mnemonic(mnemonic):
            raise WalletError("Invalid mnemonic phrase")
        
        # Convert to seed
        seed = mnemonic_to_seed(mnemonic, passphrase)
        
        # Create wallet
        return cls(seed, mnemonic)
    
    def get_private_key_hex(self) -> str:
        """Get private key as hex string"""
        return self.private_key.hex()
    
    def get_public_key_hex(self) -> str:
        """Get public key as hex string"""
        return self.public_key
    
    def get_address(self) -> str:
        """Get SegWit address"""
        return self.address
    
    def get_mnemonic(self) -> str:
        """Get mnemonic phrase"""
        if not self.mnemonic:
            raise WalletError("Mnemonic not available")
        return self.mnemonic
    
    def derive_address(self, account: int = 0, change: int = 0, index: int = 0) -> Tuple[str, str]:
        """
        Derive address at specific path.
        
        Args:
            account: Account number
            change: 0 for external, 1 for change
            index: Address index
            
        Returns:
            (private_key_hex, address)
        """
        from .keys.bip84 import derive_bip84_address_from_seed
        
        private_key, address = derive_bip84_address_from_seed(
            self.seed, account, change, index
        )
        
        return private_key.hex(), address
    
    def get_next_address(self, change: int = 0) -> Tuple[str, str]:
        """
        Get next unused address in sequence.
        
        Args:
            change: 0 for external, 1 for change
            
        Returns:
            (private_key_hex, address)
        """
        if change == 0:
            self.address_index += 1
        else:
            self.change_index += 1
        
        return self.derive_address(
            self.account_index, 
            change, 
            self.address_index if change == 0 else self.change_index
        )
    
    def to_dict(self) -> Dict:
        """Convert wallet to dictionary"""
        return {
            "mnemonic": self.mnemonic if self.mnemonic else None,
            "address": self.address,
            "public_key": self.public_key,
            "private_key": self.get_private_key_hex(),
            "derivation_path": self.derivation_path,
            "account_index": self.account_index,
            "change_index": self.change_index,
            "address_index": self.address_index,
            "seed_available": bool(self.mnemonic)
        }
    
    def save_to_file(self, filepath: str, password: Optional[str] = None):
        """
        Save wallet to encrypted file.
        
        Args:
            filepath: Path to save file
            password: Optional encryption password
        """
        data = self.to_dict()
        
        if password:
            # TODO: Implement encryption
            raise NotImplementedError("Wallet encryption not yet implemented")
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str, password: Optional[str] = None) -> 'Wallet':
        """
        Load wallet from file.
        
        Args:
            filepath: Path to wallet file
            password: Encryption password if needed
            
        Returns:
            Wallet instance
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if password:
            # TODO: Implement decryption
            raise NotImplementedError("Wallet decryption not yet implemented")
        
        if data.get("mnemonic"):
            return cls.recover(data["mnemonic"])
        else:
            raise WalletError("Cannot load wallet without mnemonic")