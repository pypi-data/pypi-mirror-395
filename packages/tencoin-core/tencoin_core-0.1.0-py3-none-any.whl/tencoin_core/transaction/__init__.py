# tencoin-core/tencoin_core/transaction/__init__.py
"""
Transaction creation, signing, and serialization
"""

from .core import Transaction, TxIn, TxOut, parse_transaction
from .builder import TransactionBuilder, TransactionBuilderError
from .signer import SegWitSigner, SigningError
from .fee import FeeCalculator
from .address import (
    decode_address, address_to_script, is_valid_address, 
    get_address_type, AddressError
)

__all__ = [
    # Core
    "Transaction",
    "TxIn",
    "TxOut",
    "parse_transaction",
    
    # Builder
    "TransactionBuilder",
    "TransactionBuilderError",
    
    # Signer
    "SegWitSigner",
    "SigningError",
    
    # Fee
    "FeeCalculator",
    
    # Address
    "decode_address",
    "address_to_script",
    "is_valid_address",
    "get_address_type",
    "AddressError",
]