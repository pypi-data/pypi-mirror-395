# tencoin-core/tencoin_core/transaction/signer.py
"""
SegWit (BIP-143) transaction signing for P2WPKH addresses
"""
import struct
from typing import List, Optional
from ..utils import sha256d, hash160, encode_varint
from .core import Transaction, TxIn, TxOut
from .address import decode_address

class SigningError(Exception):
    """Transaction signing errors"""
    pass

class SegWitSigner:
    """
    SegWit transaction signer (BIP-143) for P2WPKH addresses.
    
    Only supports P2WPKH (tc1q...) addresses.
    """
    
    @staticmethod
    def create_witness_signature(
        tx: Transaction,
        input_index: int,
        private_key: bytes,
        script_code: bytes,
        value: int,
        sighash_type: int = 1
    ) -> bytes:
        """
        Create witness signature for SegWit input (BIP-143).
        
        Args:
            tx: Transaction to sign
            input_index: Index of input to sign
            private_key: 32-byte private key
            script_code: Script code (P2PKH script for P2WPKH)
            value: Input value in Tenos
            sighash_type: SIGHASH type (default: SIGHASH_ALL = 1)
            
        Returns:
            DER-encoded signature with sighash byte appended
        
        Raises:
            SigningError: If signing fails
        """
        try:
            # Get BIP-143 digest
            digest = SegWitSigner.bip143_digest(
                tx, input_index, script_code, value, sighash_type
            )
            
            # Sign the digest
            from ..keys.ec import sign
            signature = sign(private_key, digest)
            
            # Append sighash type
            return signature + bytes([sighash_type])
            
        except Exception as e:
            raise SigningError(f"Failed to create witness signature: {e}")
    
    @staticmethod
    def bip143_digest(
        tx: Transaction,
        input_index: int,
        script_code: bytes,
        value: int,
        sighash_type: int = 1
    ) -> bytes:
        """
        Calculate BIP-143 digest for SegWit signing.
        
        Args:
            tx: Transaction
            input_index: Input index
            script_code: Script code
            value: Input value
            sighash_type: SIGHASH type
            
        Returns:
            32-byte digest
        """
        # Hash of all input prevouts
        prevouts = b''
        for txin in tx.vin:
            prevouts += bytes.fromhex(txin.prev_txid)[::-1] + struct.pack("<I", txin.vout)
        hashPrevouts = sha256d(prevouts)
        
        # Hash of all input sequence numbers
        sequences = b''.join(struct.pack("<I", txin.sequence) for txin in tx.vin)
        hashSequence = sha256d(sequences)
        
        # Hash of all outputs
        outputs = b''.join(txout.serialize() for txout in tx.vout)
        hashOutputs = sha256d(outputs)
        
        # Build digest
        digest = struct.pack("<I", tx.version)
        digest += hashPrevouts
        digest += hashSequence
        
        # Specific input
        txin = tx.vin[input_index]
        digest += bytes.fromhex(txin.prev_txid)[::-1]
        digest += struct.pack("<I", txin.vout)
        digest += encode_varint(len(script_code))
        digest += script_code
        digest += struct.pack("<Q", value)
        digest += struct.pack("<I", txin.sequence)
        digest += hashOutputs
        digest += struct.pack("<I", tx.locktime)
        digest += struct.pack("<I", sighash_type)
        
        return sha256d(digest)
    
    @staticmethod
    def sign_transaction(
        tx: Transaction,
        utxos: List[dict],
        private_keys: List[bytes]
    ) -> Transaction:
        """
        Sign a complete transaction with SegWit inputs.
        
        Args:
            tx: Unsigned transaction
            utxos: List of UTXO dictionaries for each input:
                [
                    {
                        "value": int,           # in Tenos
                        "script_pubkey": bytes, # scriptPubKey
                        "address": str          # address (tc1q...)
                    },
                    ...
                ]
            private_keys: List of private keys (32 bytes each)
            
        Returns:
            Signed transaction
        
        Raises:
            SigningError: If signing fails
        """
        if len(tx.vin) != len(utxos):
            raise SigningError(f"Transaction has {len(tx.vin)} inputs but {len(utxos)} UTXOs provided")
        
        if len(tx.vin) != len(private_keys):
            raise SigningError(f"Transaction has {len(tx.vin)} inputs but {len(private_keys)} private keys provided")
        
        # Verify all addresses are P2WPKH
        for i, utxo in enumerate(utxos):
            addr_type, _ = decode_address(utxo["address"])
            if addr_type != "p2wpkh":
                raise SigningError(f"UTXO {i} is not P2WPKH: {utxo['address']}")
        
        # Create a copy of the transaction
        signed_tx = Transaction(
            version=tx.version,
            vin=[TxIn(
                prev_txid=txin.prev_txid,
                vout=txin.vout,
                script_sig=txin.script_sig,
                sequence=txin.sequence
            ) for txin in tx.vin],
            vout=tx.vout[:],
            locktime=tx.locktime
        )
        
        # Set has_witness to True for SegWit transaction
        signed_tx.has_witness = True
        
        # Sign each input
        for i in range(len(signed_tx.vin)):
            try:
                SegWitSigner.sign_input(
                    signed_tx, i, utxos[i], private_keys[i]
                )
            except Exception as e:
                raise SigningError(f"Failed to sign input {i}: {e}")
        
        return signed_tx
    
    @staticmethod
    def sign_input(
        tx: Transaction,
        input_index: int,
        utxo: dict,
        private_key: bytes
    ):
        """
        Sign a single SegWit input.
        
        Args:
            tx: Transaction (will be modified)
            input_index: Input index to sign
            utxo: UTXO dictionary with keys:
                - value: int
                - script_pubkey: bytes
                - address: str (tc1q...)
            private_key: 32-byte private key
        """
        # Get public key from private key
        from ..keys.ec import privkey_to_pubkey
        public_key = privkey_to_pubkey(private_key, compressed=True)
        
        # Create script code (P2PKH script for the public key hash)
        pubkey_hash = hash160(public_key)
        script_code = bytes([0x76, 0xa9, 0x14]) + pubkey_hash + bytes([0x88, 0xac])
        
        # Create signature
        signature = SegWitSigner.create_witness_signature(
            tx, input_index, private_key, script_code, utxo["value"]
        )
        
        # Create witness
        tx.vin[input_index].witness = [signature, public_key]
        
        # Clear script_sig for SegWit (should be empty)
        tx.vin[input_index].script_sig = b""
        
        # Update has_witness flag
        tx.has_witness = True
    
    @staticmethod
    def verify_witness(
        tx: Transaction,
        input_index: int,
        public_key: bytes,
        script_code: bytes,
        value: int,
        witness: List[bytes]
    ) -> bool:
        """
        Verify witness signature.
        
        Args:
            tx: Transaction
            input_index: Input index
            public_key: Compressed public key (33 bytes)
            script_code: Script code
            value: Input value
            witness: Witness stack
            
        Returns:
            True if signature is valid
        """
        if len(witness) < 2:
            return False
        
        signature = witness[0]
        witness_pubkey = witness[1]
        
        # Check public key matches
        if witness_pubkey != public_key:
            return False
        
        # Verify signature
        if len(signature) < 1:
            return False
        
        sighash_type = signature[-1]
        signature_der = signature[:-1]
        
        # Calculate digest
        digest = SegWitSigner.bip143_digest(
            tx, input_index, script_code, value, sighash_type
        )
        
        # Verify signature
        from ..keys.ec import verify
        return verify(public_key, digest, signature_der)