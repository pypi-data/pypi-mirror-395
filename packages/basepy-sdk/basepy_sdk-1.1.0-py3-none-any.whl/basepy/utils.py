"""
Utility functions for Base blockchain SDK.

Includes:
- Network constants and RPC URLs
- Web3 conversion utilities
- ERC-20 log decoding (zero RPC cost)
- Address formatting and validation
- Token amount formatting
- Transaction log parsing

Production-ready features:
- Thread-safe operations
- Comprehensive error handling
- Type hints and validation
- Zero external dependencies beyond web3.py
"""

from web3 import Web3
from typing import Optional, Dict, Any, List, Union
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# NETWORK CONSTANTS
# ============================================================================

BASE_MAINNET_CHAIN_ID = 8453
BASE_SEPOLIA_CHAIN_ID = 84532

BASE_MAINNET_RPC_URLS = [
    "https://mainnet.base.org",
    "https://base.gateway.tenderly.co",
    "https://base.publicnode.com",
]

BASE_SEPOLIA_RPC_URLS = [
    "https://sepolia.base.org",
    "https://base-sepolia.gateway.tenderly.co",
    "https://base-sepolia.publicnode.com",
]


# ============================================================================
# WEB3 CONVERSION UTILITIES (Existing)
# ============================================================================

def to_wei(amount: Union[int, float, str], unit: str = "ether") -> int:
    """
    Convert amount to Wei.
    
    Args:
        amount: Amount to convert
        unit: Unit name ('wei', 'gwei', 'ether')
        
    Returns:
        Amount in Wei
        
    Example:
        >>> to_wei(1, 'ether')
        1000000000000000000
        >>> to_wei(1, 'gwei')
        1000000000
    """
    return Web3.to_wei(amount, unit)


def from_wei(amount: int, unit: str = "ether") -> Union[int, Decimal]:
    """
    Convert amount from Wei.
    
    Args:
        amount: Amount in Wei
        unit: Unit name ('wei', 'gwei', 'ether')
        
    Returns:
        Converted amount
        
    Example:
        >>> from_wei(1000000000000000000, 'ether')
        Decimal('1')
    """
    return Web3.from_wei(amount, unit)


def is_address(address: str) -> bool:
    """
    Check if string is a valid Ethereum address.
    
    Args:
        address: Address to check
        
    Returns:
        True if valid address format
        
    Example:
        >>> is_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')
        True
        >>> is_address('invalid')
        False
    """
    return Web3.is_address(address)


def to_checksum_address(address: str) -> str:
    """
    Convert address to checksummed format.
    
    Args:
        address: Ethereum address
        
    Returns:
        Checksummed address
        
    Raises:
        ValueError: If address is invalid
        
    Example:
        >>> to_checksum_address('0x742d35cc6634c0532925a3b844bc9e7595f0beb')
        '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
    """
    return Web3.to_checksum_address(address)


# ============================================================================
# TOKEN AMOUNT FORMATTING (NEW)
# ============================================================================

def format_token_amount(amount: int, decimals: int) -> float:
    """
    Convert raw token amount to human-readable decimal.
    
    Args:
        amount: Raw amount in smallest unit
        decimals: Token decimals (18 for ETH, 6 for USDC, etc.)
        
    Returns:
        Human-readable amount as float
        
    Example:
        >>> format_token_amount(1000000, 6)  # USDC
        1.0
        >>> format_token_amount(1500000000000000000, 18)  # ETH
        1.5
    """
    if decimals == 0:
        return float(amount)
    return amount / (10 ** decimals)


def parse_token_amount(amount: Union[str, float, int], decimals: int) -> int:
    """
    Convert human-readable amount to raw token units.
    
    Args:
        amount: Human-readable amount
        decimals: Token decimals
        
    Returns:
        Raw amount in smallest unit
        
    Example:
        >>> parse_token_amount(1.5, 6)  # USDC
        1500000
        >>> parse_token_amount("1.5", 18)  # ETH
        1500000000000000000
    """
    if isinstance(amount, int):
        amount = str(amount)
    
    decimal_amount = Decimal(str(amount))
    return int(decimal_amount * (10 ** decimals))


def format_token_balance(
    balance: int,
    decimals: int,
    symbol: str = "",
    precision: int = 4
) -> str:
    """
    Format token balance with symbol for display.
    
    Args:
        balance: Raw balance
        decimals: Token decimals
        symbol: Token symbol (optional)
        precision: Decimal places to show
        
    Returns:
        Formatted string
        
    Example:
        >>> format_token_balance(1500000, 6, 'USDC', 2)
        '1.50 USDC'
        >>> format_token_balance(1500000000000000000, 18, 'ETH')
        '1.5000 ETH'
    """
    amount = format_token_amount(balance, decimals)
    
    if symbol:
        return f"{amount:.{precision}f} {symbol}"
    return f"{amount:.{precision}f}"


# ============================================================================
# ERC-20 LOG DECODING (NEW - Zero RPC Cost)
# ============================================================================

def extract_address_from_topic(topic: str) -> str:
    """
    Extract address from padded log topic (32 bytes -> 20 bytes).
    
    EVM stores addresses in topics as 32 bytes (padded with zeros).
    This function extracts the actual 20-byte address.
    
    Args:
        topic: 32-byte hex topic (with or without 0x prefix)
        
    Returns:
        Checksummed 20-byte address
        
    Example:
        >>> topic = '0x000000000000000000000000742d35cc6634c0532925a3b844bc9e7595f0beb'
        >>> extract_address_from_topic(topic)
        '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
    """
    # Remove 0x prefix if present
    topic = topic.replace('0x', '')
    
    # Extract last 40 characters (20 bytes = 40 hex chars)
    address = '0x' + topic[-40:]
    
    # Return checksummed address
    return to_checksum_address(address)


def decode_uint256_from_data(data: str) -> int:
    """
    Decode uint256 value from log data field.
    
    Args:
        data: Hex string data field (with or without 0x prefix)
        
    Returns:
        Decoded integer value
        
    Example:
        >>> data = '0x0000000000000000000000000000000000000000000000000000000000989680'
        >>> decode_uint256_from_data(data)
        10000000
    """
    # Remove 0x prefix if present
    data = data.replace('0x', '')
    
    # Convert hex to int
    return int(data, 16)


def is_erc20_transfer_log(log: Dict[str, Any]) -> bool:
    """
    Check if a log entry is an ERC-20 Transfer event.
    
    ERC-20 Transfer signature:
    Transfer(address indexed from, address indexed to, uint256 value)
    
    Args:
        log: Log entry from transaction receipt
        
    Returns:
        True if log is ERC-20 Transfer event
        
    Example:
        >>> log = receipt['logs'][0]
        >>> if is_erc20_transfer_log(log):
        ...     print("This is a token transfer!")
    """
    from .abis import ERC20_TRANSFER_TOPIC
    
    # Must have topics
    if 'topics' not in log or len(log['topics']) < 3:
        return False
    
    # First topic must match Transfer signature
    topic0 = log['topics'][0]
    if isinstance(topic0, bytes):
        topic0 = '0x' + topic0.hex()
    
    return topic0.lower() == ERC20_TRANSFER_TOPIC.lower()


def decode_erc20_transfer_log(log: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Decode ERC-20 Transfer event from transaction log.
    
    This function extracts transfer details WITHOUT making any RPC calls.
    Cost: FREE (local computation only)
    
    Args:
        log: Log entry from transaction receipt
        
    Returns:
        Dictionary with transfer details:
            - token: Token contract address
            - from: Sender address
            - to: Recipient address
            - amount: Transfer amount (raw, in smallest unit)
            - log_index: Position in logs array
        Returns None if log is not an ERC-20 Transfer event
        
    Example:
        >>> receipt = client.w3.eth.get_transaction_receipt('0x...')
        >>> for log in receipt['logs']:
        ...     transfer = decode_erc20_transfer_log(log)
        ...     if transfer:
        ...         print(f"Transfer: {transfer['amount']} tokens")
        ...         print(f"From: {transfer['from']}")
        ...         print(f"To: {transfer['to']}")
    """
    try:
        # Check if this is an ERC-20 Transfer event
        if not is_erc20_transfer_log(log):
            return None
        
        # Extract token contract address
        token_address = log['address']
        if isinstance(token_address, bytes):
            token_address = '0x' + token_address.hex()
        token_address = to_checksum_address(token_address)
        
        # Extract topics (addresses are indexed, stored in topics)
        topics = log['topics']
        
        # Topic 0 = event signature (already validated)
        # Topic 1 = from address (indexed)
        # Topic 2 = to address (indexed)
        
        from_topic = topics[1]
        to_topic = topics[2]
        
        # Convert bytes to hex string if needed
        if isinstance(from_topic, bytes):
            from_topic = '0x' + from_topic.hex()
        if isinstance(to_topic, bytes):
            to_topic = '0x' + to_topic.hex()
        
        from_address = extract_address_from_topic(from_topic)
        to_address = extract_address_from_topic(to_topic)
        
        # Extract amount from data field (not indexed)
        data = log['data']
        if isinstance(data, bytes):
            data = '0x' + data.hex()
        
        amount = decode_uint256_from_data(data)
        
        # Get log index
        log_index = log.get('logIndex', 0)
        if isinstance(log_index, bytes):
            log_index = int.from_bytes(log_index, byteorder='big')
        
        return {
            'token': token_address,
            'from': from_address,
            'to': to_address,
            'amount': amount,
            'log_index': log_index,
        }
        
    except Exception as e:
        logger.warning(f"Failed to decode ERC-20 transfer log: {e}")
        return None


def decode_all_erc20_transfers(receipt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Decode all ERC-20 Transfer events from a transaction receipt.
    
    Cost: FREE (local computation only)
    
    Args:
        receipt: Transaction receipt
        
    Returns:
        List of decoded transfer dictionaries
        
    Example:
        >>> receipt = client.w3.eth.get_transaction_receipt('0x...')
        >>> transfers = decode_all_erc20_transfers(receipt)
        >>> print(f"Found {len(transfers)} token transfers")
        >>> for transfer in transfers:
        ...     print(f"{transfer['token']}: {transfer['amount']}")
    """
    transfers = []
    
    if 'logs' not in receipt:
        return transfers
    
    for log in receipt['logs']:
        transfer = decode_erc20_transfer_log(log)
        if transfer:
            transfers.append(transfer)
    
    return transfers


def filter_transfers_by_address(
    transfers: List[Dict[str, Any]],
    address: str,
    direction: str = 'both'
) -> List[Dict[str, Any]]:
    """
    Filter transfers by address and direction.
    
    Args:
        transfers: List of decoded transfers
        address: Address to filter by
        direction: 'sent', 'received', or 'both'
        
    Returns:
        Filtered list of transfers
        
    Example:
        >>> transfers = decode_all_erc20_transfers(receipt)
        >>> my_address = '0x123...'
        >>> 
        >>> # Get only received transfers
        >>> received = filter_transfers_by_address(transfers, my_address, 'received')
        >>> 
        >>> # Get only sent transfers
        >>> sent = filter_transfers_by_address(transfers, my_address, 'sent')
    """
    address = to_checksum_address(address)
    
    filtered = []
    for transfer in transfers:
        if direction == 'both':
            if transfer['from'] == address or transfer['to'] == address:
                filtered.append(transfer)
        elif direction == 'sent':
            if transfer['from'] == address:
                filtered.append(transfer)
        elif direction == 'received':
            if transfer['to'] == address:
                filtered.append(transfer)
    
    return filtered


def filter_transfers_by_token(
    transfers: List[Dict[str, Any]],
    token_address: str
) -> List[Dict[str, Any]]:
    """
    Filter transfers by token contract address.
    
    Args:
        transfers: List of decoded transfers
        token_address: Token contract address
        
    Returns:
        Filtered list of transfers for specified token
        
    Example:
        >>> transfers = decode_all_erc20_transfers(receipt)
        >>> usdc_address = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
        >>> usdc_transfers = filter_transfers_by_token(transfers, usdc_address)
    """
    token_address = to_checksum_address(token_address)
    return [t for t in transfers if t['token'] == token_address]


# ============================================================================
# ADDRESS UTILITIES (NEW)
# ============================================================================

def normalize_address(address: str) -> str:
    """
    Normalize address to lowercase with 0x prefix.
    
    Args:
        address: Ethereum address
        
    Returns:
        Normalized address (lowercase)
        
    Example:
        >>> normalize_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')
        '0x742d35cc6634c0532925a3b844bc9e7595f0beb'
    """
    address = address.strip()
    if not address.startswith('0x'):
        address = '0x' + address
    return address.lower()


def addresses_equal(addr1: str, addr2: str) -> bool:
    """
    Compare two addresses (case-insensitive).
    
    Args:
        addr1: First address
        addr2: Second address
        
    Returns:
        True if addresses are equal
        
    Example:
        >>> addr1 = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
        >>> addr2 = '0x742D35CC6634C0532925A3B844BC9E7595F0BEB'
        >>> addresses_equal(addr1, addr2)
        True
    """
    return normalize_address(addr1) == normalize_address(addr2)


def shorten_address(address: str, chars: int = 4) -> str:
    """
    Shorten address for display (e.g., 0x742d...0bEb).
    
    Args:
        address: Full address
        chars: Number of characters to show on each side
        
    Returns:
        Shortened address
        
    Example:
        >>> shorten_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')
        '0x742d...0bEb'
        >>> shorten_address('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb', 6)
        '0x742d35...5f0bEb'
    """
    if len(address) <= (chars * 2 + 3):
        return address
    
    return f"{address[:2+chars]}...{address[-chars:]}"


def is_zero_address(address: str) -> bool:
    """
    Check if address is the zero address (0x0000...0000).
    
    Args:
        address: Address to check
        
    Returns:
        True if zero address
        
    Example:
        >>> is_zero_address('0x0000000000000000000000000000000000000000')
        True
    """
    return normalize_address(address) == '0x' + ('0' * 40)


# ============================================================================
# TRANSACTION UTILITIES (NEW)
# ============================================================================

def get_transfer_direction(
    transfer: Dict[str, Any],
    address: str
) -> str:
    """
    Determine transfer direction relative to an address.
    
    Args:
        transfer: Decoded transfer dictionary
        address: Address to check against
        
    Returns:
        'sent', 'received', 'self', or 'unknown'
        
    Example:
        >>> transfer = decode_erc20_transfer_log(log)
        >>> my_address = '0x123...'
        >>> direction = get_transfer_direction(transfer, my_address)
        >>> if direction == 'received':
        ...     print("I received tokens!")
    """
    address = to_checksum_address(address)
    
    from_addr = transfer['from']
    to_addr = transfer['to']
    
    if from_addr == address and to_addr == address:
        return 'self'
    elif from_addr == address:
        return 'sent'
    elif to_addr == address:
        return 'received'
    else:
        return 'unknown'


def calculate_balance_change(
    transfers: List[Dict[str, Any]],
    address: str,
    token_address: Optional[str] = None
) -> int:
    """
    Calculate net balance change from transfers.
    
    Args:
        transfers: List of decoded transfers
        address: Address to calculate for
        token_address: Optional token filter
        
    Returns:
        Net balance change (positive = received, negative = sent)
        
    Example:
        >>> transfers = decode_all_erc20_transfers(receipt)
        >>> my_address = '0x123...'
        >>> change = calculate_balance_change(transfers, my_address)
        >>> if change > 0:
        ...     print(f"Received {change} tokens")
        >>> else:
        ...     print(f"Sent {abs(change)} tokens")
    """
    address = to_checksum_address(address)
    
    # Filter by token if specified
    if token_address:
        transfers = filter_transfers_by_token(transfers, token_address)
    
    balance_change = 0
    
    for transfer in transfers:
        direction = get_transfer_direction(transfer, address)
        
        if direction == 'received':
            balance_change += transfer['amount']
        elif direction == 'sent':
            balance_change -= transfer['amount']
        # 'self' transfers don't change balance
    
    return balance_change


# ============================================================================
# HEXBYTES CONVERSION (NEW)
# ============================================================================

def convert_hex_bytes(obj: Any) -> Any:
    """
    Recursively convert HexBytes objects to hex strings for JSON serialization.
    
    This is critical for API responses that need to be JSON serialized.
    
    Args:
        obj: Any object that may contain HexBytes
        
    Returns:
        Object with all HexBytes converted to hex strings
        
    Example:
        >>> receipt = client.w3.eth.get_transaction_receipt('0x...')
        >>> json_safe = convert_hex_bytes(dict(receipt))
        >>> import json
        >>> json.dumps(json_safe)  # Now works!
    """
    if hasattr(obj, 'hex'):
        # Convert HexBytes to hex string
        return obj.hex()
    elif isinstance(obj, dict):
        # Recursively convert dictionary values
        return {k: convert_hex_bytes(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        # Recursively convert list/tuple items
        return [convert_hex_bytes(item) for item in obj]
    elif isinstance(obj, bytes):
        # Convert raw bytes to hex string
        return '0x' + obj.hex()
    return obj


# ============================================================================
# VALIDATION UTILITIES (NEW)
# ============================================================================

def validate_transaction_hash(tx_hash: str) -> str:
    """
    Validate and normalize transaction hash.
    
    Args:
        tx_hash: Transaction hash
        
    Returns:
        Normalized hash (with 0x prefix, lowercase)
        
    Raises:
        ValueError: If hash format is invalid
        
    Example:
        >>> validate_transaction_hash('0x123abc...')
        '0x123abc...'
        >>> validate_transaction_hash('invalid')
        ValueError: Invalid transaction hash format
    """
    if not isinstance(tx_hash, str):
        raise ValueError(f"Transaction hash must be string, got {type(tx_hash)}")
    
    tx_hash = tx_hash.strip()
    
    if not tx_hash.startswith('0x'):
        tx_hash = '0x' + tx_hash
    
    if len(tx_hash) != 66:  # 0x + 64 hex chars
        raise ValueError(
            f"Invalid transaction hash length: {len(tx_hash)} (expected 66)"
        )
    
    # Verify hex format
    try:
        int(tx_hash, 16)
    except ValueError:
        raise ValueError(f"Invalid hex format: {tx_hash}")
    
    return tx_hash.lower()


def validate_block_identifier(block_id: Union[int, str]) -> Union[int, str]:
    """
    Validate block identifier.
    
    Args:
        block_id: Block number, 'latest', 'earliest', 'pending', or block hash
        
    Returns:
        Validated block identifier
        
    Raises:
        ValueError: If identifier is invalid
    """
    if isinstance(block_id, int):
        if block_id < 0:
            raise ValueError(f"Block number must be non-negative, got {block_id}")
        return block_id
    
    if isinstance(block_id, str):
        valid_strings = ['latest', 'earliest', 'pending']
        
        if block_id.lower() in valid_strings:
            return block_id.lower()
        
        # Check if it's a block hash
        if block_id.startswith('0x') and len(block_id) == 66:
            try:
                int(block_id, 16)
                return block_id.lower()
            except ValueError:
                pass
        
        raise ValueError(
            f"Invalid block identifier: {block_id}. "
            f"Expected int, 'latest', 'earliest', 'pending', or block hash"
        )
    
    raise ValueError(f"Block identifier must be int or str, got {type(block_id)}")


# ============================================================================
# PRODUCTION ENHANCEMENTS SUMMARY
# ============================================================================
#
# ✅ ERC-20 LOG DECODING (Zero RPC Cost)
# - decode_erc20_transfer_log(): Extract transfer details from logs
# - decode_all_erc20_transfers(): Process entire receipt
# - is_erc20_transfer_log(): Quick event type checking
# - extract_address_from_topic(): Parse padded addresses
# - decode_uint256_from_data(): Parse amounts from data field
#
# ✅ TRANSFER FILTERING & ANALYSIS
# - filter_transfers_by_address(): Get sent/received transfers
# - filter_transfers_by_token(): Filter by token contract
# - get_transfer_direction(): Determine transfer direction
# - calculate_balance_change(): Net balance change calculation
#
# ✅ TOKEN AMOUNT FORMATTING
# - format_token_amount(): Raw to human-readable
# - parse_token_amount(): Human-readable to raw
# - format_token_balance(): Display with symbol
#
# ✅ ADDRESS UTILITIES
# - normalize_address(): Lowercase with 0x prefix
# - addresses_equal(): Case-insensitive comparison
# - shorten_address(): Display-friendly format
# - is_zero_address(): Check for burn address
#
# ✅ VALIDATION HELPERS
# - validate_transaction_hash(): Ensure valid tx hash
# - validate_block_identifier(): Validate block IDs
#
# ✅ DATA CONVERSION
# - convert_hex_bytes(): JSON serialization compatibility
#
# DESIGN PRINCIPLES:
# - Zero RPC calls: All decoding is local computation
# - Production-ready: Comprehensive error handling
# - Well-documented: Examples in every docstring
# - Type-safe: Full type hints
# - Thread-safe: No shared mutable state
#
# BACKWARD COMPATIBILITY:
# - All existing functions unchanged
# - New functions are purely additive
# - No breaking changes
# ============================================================================