# Phase 1: Setup and Core Features

This document outlines the features implemented in Phase 1 of the BasePy SDK.

## Features Implemented

1.  **Base Connection & Client**
    *   `BaseClient` class for connecting to Base Mainnet and Testnet.
    *   Automatic RPC failover.
    *   Helper methods: `get_chain_id`, `get_block_number`, `get_balance`.

2.  **Wallet Management**
    *   `Wallet` class for creating and managing wallets.
    *   Generate new wallets.
    *   Import from private key or mnemonic.
    *   Sign transactions.

3.  **Transactions**
    *   `Transactions` class for sending ETH and ERC-20 tokens.
    *   Automatic gas estimation (basic).

4.  **Smart Contract Interaction**
    *   `Contract` class for interacting with smart contracts.
    *   Read-only calls.
    *   Write transactions.

## Next Steps (Phase 2)

*   Advanced gas estimation.
*   Event listening.
*   Account Abstraction support.
