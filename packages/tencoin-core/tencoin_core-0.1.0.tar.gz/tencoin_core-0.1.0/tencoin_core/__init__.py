# tencoin-core/tencoin_core/__init__.py
"""
Tencoin Core - Official Python library for Tencoin
"""

from .constants import (
    MAINNET_HRP,
    TENOS_PER_TEC,
    DUST_LIMIT,
    DEFAULT_RPC_PORT,
    COIN_TYPE,
    DERIVATION_PATH,
    DEFAULT_RPC_TOKEN
)

from .wallet import Wallet, WalletError
from .rpc import RPCClient, RPCError
from .transaction import (
    Transaction, TxIn, TxOut, parse_transaction,
    TransactionBuilder, TransactionBuilderError,
    SegWitSigner, SigningError,
    FeeCalculator,
    decode_address, address_to_script, is_valid_address,
    get_address_type, AddressError
)

# Version
__version__ = "0.1.0"

__all__ = [
    # Constants
    "MAINNET_HRP",
    "TENOS_PER_TEC",
    "DUST_LIMIT",
    "DEFAULT_RPC_PORT",
    "DEFAULT_RPC_TOKEN",
    "COIN_TYPE",
    "DERIVATION_PATH",
    
    # Wallet
    "Wallet",
    "WalletError",
    
    # RPC
    "RPCClient",
    "RPCError",
    
    # Transaction
    "Transaction",
    "TxIn",
    "TxOut",
    "parse_transaction",
    "TransactionBuilder",
    "TransactionBuilderError",
    "SegWitSigner",
    "SigningError",
    "FeeCalculator",
    "decode_address",
    "address_to_script",
    "is_valid_address",
    "get_address_type",
    "AddressError",
    
    # Version
    "__version__",
]