# File: basepy/__init__.py
"""
BasePy SDK - Production-ready Python SDK for Base blockchain.

Features:
- Complete read/write operations for Base L2
- Zero-cost ERC-20 transfer decoding
- L1+L2 fee optimization
- Portfolio tracking with 80% fewer RPC calls
- Production resilience (circuit breaker, rate limiting, retry)
- Thread-safe operations
- Comprehensive error handling

Quick Start:
    >>> from basepy import BaseClient, Wallet, Transaction
    >>> 
    >>> # Read operations (no wallet needed)
    >>> client = BaseClient()
    >>> balance = client.get_balance("0xYourAddress...")
    >>> 
    >>> # Write operations (wallet required)
    >>> wallet = Wallet(private_key="0x...", client=client)
    >>> tx = Transaction(client, wallet)
    >>> tx_hash = tx.send_eth("0xRecipient...", 0.1)
"""

# ============================================================================
# EXCEPTIONS (CRITICAL - Must be imported first)
# ============================================================================

from .exceptions import (
    # Base exception
    BasePyError,
    
    # Network & RPC errors
    ConnectionError,
    RPCError,
    RateLimitError,
    CircuitBreakerOpenError,
    TimeoutError,
    
    # Validation errors
    ValidationError,
    InvalidAddressError,
    InvalidChainIdError,
    
    # Wallet errors
    WalletError,
    SignatureError,
    
    # Transaction errors
    TransactionError,
    InsufficientFundsError,
    GasEstimationError,
    
    # Contract errors
    ContractError,
    
    # Cache errors
    CacheError,
)


# ============================================================================
# CORE CLIENT (Public API only)
# ============================================================================

from .client import BaseClient


# ============================================================================
# WALLET & TRANSACTIONS
# ============================================================================

from .wallet import Wallet
from .transactions import Transaction


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Base utilities
from .utils import (
    to_wei,
    from_wei,
    is_address,
    to_checksum_address,
)

# Network constants
from .utils import (
    BASE_MAINNET_RPC_URLS,
    BASE_SEPOLIA_RPC_URLS,
    BASE_MAINNET_CHAIN_ID,
    BASE_SEPOLIA_CHAIN_ID,
)

# Token formatting
from .utils import (
    format_token_amount,
    parse_token_amount,
    format_token_balance,
)

# Address utilities
from .utils import (
    normalize_address,
    addresses_equal,
    shorten_address,
    is_zero_address,
)

# ERC-20 decoding (Zero RPC cost!)
from .utils import (
    decode_erc20_transfer_log,
    decode_all_erc20_transfers,
    is_erc20_transfer_log,
)

# Transfer analysis
from .utils import (
    filter_transfers_by_address,
    filter_transfers_by_token,
    get_transfer_direction,
    calculate_balance_change,
)


# ============================================================================
# ABI & CONTRACT UTILITIES
# ============================================================================

from .abis import (
    # Standard ABIs
    ERC20_ABI,
    ERC721_ABI,
    ERC1155_ABI,
    WETH_ABI,
    GAS_ORACLE_ABI,
    
    # Event topics
    ERC20_TRANSFER_TOPIC,
    ERC20_APPROVAL_TOPIC,
    
    # Utility functions
    get_common_tokens,
    get_token_addresses,
    get_contract_address,
    get_abi_by_name,
    is_erc20_transfer_topic,
)


# ============================================================================
# VERSION & METADATA
# ============================================================================

__version__ = "1.1.0"
__author__ = "BasePy Team"
__license__ = "MIT"


# ============================================================================
# PUBLIC API (What users can import)
# ============================================================================

__all__ = [
    # ========================================================================
    # EXCEPTIONS
    # ========================================================================
    "BasePyError",
    "ConnectionError",
    "RPCError",
    "ValidationError",
    "RateLimitError",
    "CircuitBreakerOpenError",
    "WalletError",
    "TransactionError",
    "ContractError",
    "InsufficientFundsError",
    "GasEstimationError",
    "SignatureError",
    "InvalidAddressError",
    "InvalidChainIdError",
    "TimeoutError",
    "CacheError",
    
    # ========================================================================
    # CORE COMPONENTS
    # ========================================================================
    "BaseClient",
    "Wallet",
    "Transaction",
    
    # ========================================================================
    # BASE UTILITIES
    # ========================================================================
    "to_wei",
    "from_wei",
    "is_address",
    "to_checksum_address",
    
    # Network constants
    "BASE_MAINNET_RPC_URLS",
    "BASE_SEPOLIA_RPC_URLS",
    "BASE_MAINNET_CHAIN_ID",
    "BASE_SEPOLIA_CHAIN_ID",
    
    # ========================================================================
    # TOKEN UTILITIES
    # ========================================================================
    # Token formatting
    "format_token_amount",
    "parse_token_amount",
    "format_token_balance",
    
    # Address utilities
    "normalize_address",
    "addresses_equal",
    "shorten_address",
    "is_zero_address",
    
    # ========================================================================
    # ERC-20 DECODING (Zero-cost features!)
    # ========================================================================
    "decode_erc20_transfer_log",
    "decode_all_erc20_transfers",
    "is_erc20_transfer_log",
    
    # Transfer analysis
    "filter_transfers_by_address",
    "filter_transfers_by_token",
    "get_transfer_direction",
    "calculate_balance_change",
    
    # ========================================================================
    # ABI & CONTRACT UTILITIES
    # ========================================================================
    # Standard ABIs
    "ERC20_ABI",
    "ERC721_ABI",
    "ERC1155_ABI",
    "WETH_ABI",
    "GAS_ORACLE_ABI",
    
    # Event topics
    "ERC20_TRANSFER_TOPIC",
    "ERC20_APPROVAL_TOPIC",
    
    # Utility functions
    "get_common_tokens",
    "get_token_addresses",
    "get_contract_address",
    "get_abi_by_name",
    "is_erc20_transfer_topic",
]


# ============================================================================
# PACKAGE INITIALIZATION
# ============================================================================

import logging

# Set up package logger (users can configure this)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # No output by default


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_version() -> str:
    """Get BasePy SDK version."""
    return __version__


def enable_logging(level=logging.INFO):
    """
    Enable BasePy SDK logging.
    
    Args:
        level: Logging level (default: INFO)
        
    Example:
        >>> import basepy
        >>> basepy.enable_logging(logging.DEBUG)
    """
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    
    # Also enable for submodules
    logging.getLogger('basepy.client').setLevel(level)
    logging.getLogger('basepy.transactions').setLevel(level)
    logging.getLogger('basepy.wallet').setLevel(level)