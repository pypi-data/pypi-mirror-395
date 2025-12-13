# Tencoin Core

Official Python library for Tencoin - HD wallets, transactions, and RPC client.

## Features

- **HD Wallets**: BIP-39 (seed phrases) + BIP-84 (SegWit native addresses)
- **Address Generation**: Only P2WPKH (tc1q...) addresses
- **Key Derivation**: Standard path `m/84'/5353'/0'/0/0`
- **Seed Phrases**: 12-word English mnemonics
- **Wallet Recovery**: From mnemonic phrases

## Installation

```bash
pip install tencoin-core