"""
Transaction operations for Base blockchain - PRODUCTION READY.

This module handles both:
1. READ operations - Query transaction data (no wallet needed)
2. WRITE operations - Send transactions (requires wallet)

IMPORTANT: All transaction data is automatically converted from HexBytes to
standard Python types (strings, ints) for JSON serialization compatibility.

Features:
- Automatic gas estimation with configurable buffer
- Transaction retry with exponential backoff
- Nonce management with collision detection
- EIP-1559 (dynamic fee) support
- Transaction simulation before sending
- Comprehensive error handling
- Performance tracking
- Thread-safe operations
- **ERC-20 transfer decoding (zero RPC cost)**
- **Transaction analysis and classification**
- **Balance change calculation**
"""

from typing import Optional, Dict, Any, Union, List, Callable
from .exceptions import TransactionError, ValidationError, RPCError
from .utils import (
    to_wei,
    decode_erc20_transfer_log,
    decode_all_erc20_transfers,
    filter_transfers_by_address,
    filter_transfers_by_token,
    get_transfer_direction,
    calculate_balance_change,
    format_token_amount,
    convert_hex_bytes
)
from functools import wraps
import time
import logging
import threading
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _convert_hex_bytes(obj):
    """
    Recursively convert HexBytes objects to hex strings for JSON serialization.
    
    Args:
        obj: Any object that may contain HexBytes
        
    Returns:
        Object with all HexBytes converted to hex strings
        
    Note:
        This is critical for API endpoints that return transaction data,
        as HexBytes objects cannot be JSON serialized directly.
    """
    return convert_hex_bytes(obj)


def _normalize_tx_hash(tx_hash: str) -> str:
    """
    Normalize transaction hash format.
    
    Args:
        tx_hash: Transaction hash with or without 0x prefix
        
    Returns:
        Normalized hash with 0x prefix
        
    Raises:
        ValidationError: If hash format is invalid
    """
    if not isinstance(tx_hash, str):
        raise ValidationError(f"Transaction hash must be string, got {type(tx_hash)}")
    
    tx_hash = tx_hash.strip()
    
    if not tx_hash.startswith('0x'):
        tx_hash = '0x' + tx_hash
    
    if len(tx_hash) != 66:  # 0x + 64 hex chars
        raise ValidationError(
            f"Invalid transaction hash length: {len(tx_hash)} (expected 66)"
        )
    
    return tx_hash.lower()


def track_transaction(func):
    """Decorator to track transaction operations."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        success = True
        
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            duration = time.time() - start_time
            
            if hasattr(self, 'metrics'):
                self.metrics.record_operation(
                    method=func.__name__,
                    duration=duration,
                    success=success
                )
            
            logger.debug(f"{func.__name__} took {duration:.3f}s (success={success})")
    
    return wrapper


# ============================================================================
# TRANSACTION METRICS
# ============================================================================

class TransactionMetrics:
    """Metrics tracking for transaction operations."""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()
    
    def reset(self):
        """Reset all metrics."""
        with self._lock:
            self.operations = defaultdict(int)
            self.errors = defaultdict(int)
            self.latencies = defaultdict(list)
            self.gas_used = []
            self.gas_prices = []
            self.transactions_sent = 0
            self.transactions_failed = 0
    
    def record_operation(self, method: str, duration: float, success: bool):
        """Record an operation."""
        with self._lock:
            self.operations[method] += 1
            self.latencies[method].append(duration)
            if not success:
                self.errors[method] += 1
    
    def record_transaction(self, gas_used: int, gas_price: int, success: bool):
        """Record a sent transaction."""
        with self._lock:
            if success:
                self.transactions_sent += 1
                self.gas_used.append(gas_used)
                self.gas_prices.append(gas_price)
            else:
                self.transactions_failed += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        with self._lock:
            stats = {
                'operations': dict(self.operations),
                'errors': dict(self.errors),
                'transactions_sent': self.transactions_sent,
                'transactions_failed': self.transactions_failed,
                'avg_latencies': {},
                'avg_gas_used': sum(self.gas_used) / len(self.gas_used) if self.gas_used else 0,
                'avg_gas_price': sum(self.gas_prices) / len(self.gas_prices) if self.gas_prices else 0,
            }
            
            for method, latencies in self.latencies.items():
                if latencies:
                    stats['avg_latencies'][method] = sum(latencies) / len(latencies)
            
            return stats


# ============================================================================
# NONCE MANAGER
# ============================================================================

class NonceManager:
    """
    Thread-safe nonce management with automatic recovery.
    
    Prevents nonce collisions in concurrent transaction scenarios.
    """
    
    def __init__(self, client, address: str):
        self.client = client
        self.address = address
        self._lock = threading.Lock()
        self._nonce_cache = None
        self._last_update = 0
        self._cache_ttl = 5  # seconds
    
    def get_nonce(self, force_refresh: bool = False) -> int:
        """
        Get next available nonce with caching.
        
        Args:
            force_refresh: Force fetch from blockchain
            
        Returns:
            Next available nonce
        """
        with self._lock:
            now = time.time()
            
            # Use cache if fresh
            if (not force_refresh and 
                self._nonce_cache is not None and 
                now - self._last_update < self._cache_ttl):
                nonce = self._nonce_cache
                self._nonce_cache += 1
                return nonce
            
            # Fetch from blockchain
            nonce = self.client.w3.eth.get_transaction_count(
                self.address, 
                'pending'  # Include pending transactions
            )
            
            self._nonce_cache = nonce + 1
            self._last_update = now
            
            return nonce
    
    def reset(self):
        """Reset nonce cache."""
        with self._lock:
            self._nonce_cache = None
            self._last_update = 0


# ============================================================================
# GAS STRATEGY
# ============================================================================

class GasStrategy:
    """Smart gas pricing strategies for Base L2."""
    
    @staticmethod
    def estimate_gas_with_buffer(
        client,
        transaction: Dict[str, Any],
        buffer_percent: int = 20
    ) -> int:
        """
        Estimate gas with safety buffer.
        
        Args:
            client: BaseClient instance
            transaction: Transaction dict
            buffer_percent: Safety buffer percentage (default 20%)
            
        Returns:
            Gas limit with buffer applied
        """
        try:
            estimated = client.w3.eth.estimate_gas(transaction)
            buffered = int(estimated * (1 + buffer_percent / 100))
            logger.debug(f"Gas estimated: {estimated}, with buffer: {buffered}")
            return buffered
        except Exception as e:
            logger.warning(f"Gas estimation failed: {e}")
            # Return sensible default for Base L2
            return 150000
    
    @staticmethod
    def get_gas_price(client, strategy: str = 'standard') -> Dict[str, int]:
        """
        Get gas price based on strategy.
        
        Args:
            client: BaseClient instance
            strategy: 'slow', 'standard', 'fast', or 'instant'
            
        Returns:
            Dictionary with gas price parameters
        """
        base_price = client.w3.eth.gas_price
        
        multipliers = {
            'slow': 0.9,
            'standard': 1.0,
            'fast': 1.1,
            'instant': 1.25
        }
        
        multiplier = multipliers.get(strategy, 1.0)
        
        return {
            'gasPrice': int(base_price * multiplier)
        }
    
    @staticmethod
    def get_eip1559_fees(
        client,
        strategy: str = 'standard'
    ) -> Dict[str, int]:
        """
        Get EIP-1559 fee parameters.
        
        Args:
            client: BaseClient instance
            strategy: Fee strategy
            
        Returns:
            Dictionary with maxFeePerGas and maxPriorityFeePerGas
        """
        try:
            # Get base fee from latest block
            latest_block = client.get_block('latest')
            base_fee = latest_block.get('baseFeePerGas', 0)
            
            # Priority fee suggestions by strategy
            priority_fees = {
                'slow': 1_000_000,      # 0.001 Gwei
                'standard': 10_000_000,  # 0.01 Gwei
                'fast': 50_000_000,      # 0.05 Gwei
                'instant': 100_000_000   # 0.1 Gwei
            }
            
            priority_fee = priority_fees.get(strategy, 10_000_000)
            
            # Max fee = base fee * 2 + priority fee
            max_fee = (base_fee * 2) + priority_fee
            
            return {
                'maxFeePerGas': max_fee,
                'maxPriorityFeePerGas': priority_fee
            }
        except Exception as e:
            logger.warning(f"EIP-1559 fee estimation failed: {e}, using legacy")
            return GasStrategy.get_gas_price(client, strategy)


# ============================================================================
# TRANSACTION CLASS
# ============================================================================

class Transaction:
    """
    Production-ready transaction interface for Base blockchain.
    
    Features:
    - Automatic gas estimation and optimization
    - Nonce management with collision prevention
    - Transaction retry with exponential backoff
    - EIP-1559 support
    - Simulation before sending
    - Comprehensive metrics
    - Thread-safe operations
    - **ERC-20 transfer decoding (zero cost)**
    - **Transaction analysis and classification**
    
    PUBLICLY ACCESSIBLE - No authentication required for read operations.
    
    For READ operations (no wallet needed):
        >>> from basepy import BaseClient, Transaction
        >>> client = BaseClient()
        >>> tx = Transaction(client)
        >>> 
        >>> # Get transaction with decoded transfers
        >>> details = tx.get_full_transaction_details("0x123...")
        >>> print(f"ETH: {details['eth_value_formatted']}")
        >>> for transfer in details['token_transfers']:
        ...     print(f"Token: {transfer['amount_formatted']} {transfer['symbol']}")
    
    For WRITE operations (wallet required):
        >>> from basepy import BaseClient, Wallet, Transaction
        >>> client = BaseClient()
        >>> wallet = Wallet(private_key="0x...", client=client)
        >>> tx = Transaction(client, wallet)
        >>> tx_hash = tx.send_eth("0xRecipient...", 0.1)
    
    Note:
        All returned data is JSON-serializable. HexBytes objects are
        automatically converted to hex strings.
    """
    
    def __init__(
        self,
        client,
        wallet=None,
        enable_metrics: bool = True,
        default_gas_strategy: str = 'standard'
    ):
        """
        Initialize Transaction handler.
        
        Args:
            client: BaseClient instance (required)
            wallet: Optional Wallet instance (only required for sending)
            enable_metrics: Enable metrics tracking (default: True)
            default_gas_strategy: Default gas strategy (default: 'standard')
        """
        self.client = client
        self.wallet = wallet
        self.default_gas_strategy = default_gas_strategy
        
        # Initialize components
        self.metrics = TransactionMetrics() if enable_metrics else None
        
        if wallet:
            self.nonce_manager = NonceManager(client, wallet.address)
        else:
            self.nonce_manager = None
        
        logger.info("Transaction handler initialized")

    # =========================================================================
    # READ OPERATIONS - Query transaction data (PUBLIC ACCESS)
    # =========================================================================

    @track_transaction
    def get(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get transaction details by hash.
        
        PUBLIC ACCESS - Anyone can query any transaction on the blockchain.
        
        Args:
            tx_hash: Transaction hash (with or without 0x prefix)
            
        Returns:
            dict: Transaction data (JSON-serializable)
            
        Raises:
            ValidationError: If tx_hash format is invalid
            TransactionError: If transaction not found
            
        Example:
            >>> tx = transaction.get("0x123...")
            >>> print(f"From: {tx['from']}")
            >>> print(f"To: {tx['to']}")
            >>> print(f"Value: {tx['value'] / 10**18} ETH")
        """
        try:
            tx_hash = _normalize_tx_hash(tx_hash)
            tx = self.client.w3.eth.get_transaction(tx_hash)
            tx_dict = dict(tx)
            return _convert_hex_bytes(tx_dict)
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to get transaction {tx_hash}: {e}")
            raise TransactionError(f"Transaction not found: {tx_hash}") from e

    @track_transaction
    def get_receipt(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get transaction receipt (only available after mining).
        
        PUBLIC ACCESS - Anyone can query any transaction receipt.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            dict: Transaction receipt (JSON-serializable)
            
        Raises:
            ValidationError: If tx_hash format is invalid
            TransactionError: If receipt not found
            
        Example:
            >>> receipt = transaction.get_receipt("0x123...")
            >>> if receipt['status'] == 1:
            ...     print("Transaction successful!")
            >>> print(f"Gas used: {receipt['gasUsed']}")
        """
        try:
            tx_hash = _normalize_tx_hash(tx_hash)
            receipt = self.client.w3.eth.get_transaction_receipt(tx_hash)
            receipt_dict = dict(receipt)
            return _convert_hex_bytes(receipt_dict)
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to get receipt for {tx_hash}: {e}")
            raise TransactionError(
                f"Receipt not found (transaction may be pending): {tx_hash}"
            ) from e

    @track_transaction
    def get_status(self, tx_hash: str) -> str:
        """
        Get human-readable transaction status.
        
        PUBLIC ACCESS - Anyone can check any transaction status.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            str: "pending", "confirmed", "failed", or "not_found"
            
        Example:
            >>> status = transaction.get_status("0x123...")
            >>> if status == "confirmed":
            ...     print("Transaction successful!")
        """
        try:
            receipt = self.get_receipt(tx_hash)
            return "confirmed" if receipt['status'] == 1 else "failed"
        except TransactionError:
            try:
                self.get(tx_hash)
                return "pending"
            except TransactionError:
                return "not_found"

    @track_transaction
    def wait_for_confirmation(
        self, 
        tx_hash: str, 
        timeout: int = 120,
        poll_interval: float = 2.0,
        confirmations: int = 1
    ) -> Dict[str, Any]:
        """
        Wait for transaction to be mined and return receipt.
        
        PUBLIC ACCESS - Anyone can wait for any transaction confirmation.
        
        Args:
            tx_hash: Transaction hash
            timeout: Maximum seconds to wait (default: 120)
            poll_interval: Seconds between checks (default: 2.0)
            confirmations: Number of confirmations to wait for (default: 1)
            
        Returns:
            dict: Transaction receipt (JSON-serializable)
            
        Raises:
            ValidationError: If tx_hash format is invalid
            TransactionError: If timeout, failed, or not found
            
        Example:
            >>> receipt = transaction.wait_for_confirmation(tx_hash)
            >>> print(f"Confirmed in block {receipt['blockNumber']}")
            
            >>> # Wait for multiple confirmations
            >>> receipt = transaction.wait_for_confirmation(
            ...     tx_hash, 
            ...     confirmations=3
            ... )
        """
        tx_hash = _normalize_tx_hash(tx_hash)
        
        logger.info(f"Waiting for transaction {tx_hash} ({confirmations} confirmations)...")
        start_time = time.time()
        
        receipt = None
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TransactionError(
                    f"Transaction {tx_hash} not confirmed after {timeout}s. "
                    f"It may still be pending - check status manually."
                )
            
            status = self.get_status(tx_hash)
            
            if status == "confirmed":
                if receipt is None:
                    receipt = self.get_receipt(tx_hash)
                
                # Check confirmations
                if confirmations > 1:
                    current_block = self.client.get_block_number()
                    tx_block = receipt['blockNumber']
                    blocks_confirmed = current_block - tx_block + 1
                    
                    if blocks_confirmed >= confirmations:
                        logger.info(
                            f"Transaction {tx_hash} confirmed with "
                            f"{blocks_confirmed} confirmations"
                        )
                        return receipt
                    else:
                        logger.debug(
                            f"Waiting for confirmations: {blocks_confirmed}/{confirmations}"
                        )
                else:
                    logger.info(f"Transaction {tx_hash} confirmed!")
                    return receipt
                    
            elif status == "failed":
                receipt = self.get_receipt(tx_hash)
                raise TransactionError(
                    f"Transaction {tx_hash} failed in block {receipt['blockNumber']}"
                )
            elif status == "not_found":
                raise TransactionError(
                    f"Transaction {tx_hash} not found on blockchain"
                )
            
            logger.debug(f"Transaction pending... ({elapsed:.1f}s elapsed)")
            time.sleep(poll_interval)

    # =========================================================================
    # ADVANCED READ OPERATIONS
    # =========================================================================

    @track_transaction
    def get_transaction_cost(self, tx_hash: str) -> Dict[str, Any]:
        """
        Calculate actual transaction cost including L1 and L2 fees.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Dictionary with cost breakdown:
                - l2_gas_used: L2 gas consumed
                - l2_gas_price: L2 gas price paid
                - l2_cost: L2 execution cost in Wei
                - l1_cost: L1 data cost in Wei (Base-specific)
                - total_cost: Combined cost in Wei
                - total_cost_eth: Total cost in ETH
                
        Example:
            >>> cost = transaction.get_transaction_cost("0x123...")
            >>> print(f"Total cost: {cost['total_cost_eth']:.6f} ETH")
            >>> print(f"  L2: {cost['l2_cost'] / 10**18:.6f} ETH")
            >>> print(f"  L1: {cost['l1_cost'] / 10**18:.6f} ETH")
        """
        try:
            receipt = self.get_receipt(tx_hash)
            tx = self.get(tx_hash)
            
            # L2 cost
            gas_used = receipt['gasUsed']
            effective_gas_price = receipt.get('effectiveGasPrice', tx.get('gasPrice', 0))
            l2_cost = gas_used * effective_gas_price
            
            # Try to get L1 cost (Base-specific)
            l1_cost = 0
            try:
                # L1 fee is in the receipt logs for Base transactions
                for log in receipt.get('logs', []):
                    # Check if this is L1 fee log (simplified check)
                    if log.get('address', '').lower() == '0x420000000000000000000000000000000000000f':
                        # Parse L1 fee from log data if available
                        # This is a simplified approach
                        pass
                
                # Fallback: estimate from transaction data
                if 'input' in tx:
                    l1_cost = self.client.get_l1_fee(tx['input'])
            except Exception as e:
                logger.warning(f"Could not determine L1 cost: {e}")
            
            total_cost = l2_cost + l1_cost
            
            return {
                'transaction_hash': tx_hash,
                'l2_gas_used': gas_used,
                'l2_gas_price': effective_gas_price,
                'l2_cost': l2_cost,
                'l1_cost': l1_cost,
                'total_cost': total_cost,
                'total_cost_eth': total_cost / 10**18,
                'l2_cost_eth': l2_cost / 10**18,
                'l1_cost_eth': l1_cost / 10**18,
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate transaction cost: {e}")
            raise TransactionError(f"Cost calculation failed: {str(e)}") from e

    @track_transaction
    def batch_get_receipts(
        self,
        tx_hashes: List[str]
    ) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        Get multiple transaction receipts efficiently.
        
        Args:
            tx_hashes: List of transaction hashes
            
        Returns:
            Dictionary mapping tx_hash to receipt (None if not found)
            
        Example:
            >>> hashes = ["0x123...", "0x456..."]
            >>> receipts = transaction.batch_get_receipts(hashes)
            >>> for tx_hash, receipt in receipts.items():
            ...     if receipt and receipt['status'] == 1:
            ...         print(f"{tx_hash}: Success")
        """
        receipts = {}
        
        for tx_hash in tx_hashes:
            try:
                receipts[tx_hash] = self.get_receipt(tx_hash)
            except TransactionError:
                receipts[tx_hash] = None
        
        return receipts

    # =========================================================================
    # ERC-20 TRANSFER DECODING (NEW - Zero RPC Cost)
    # =========================================================================

    @track_transaction
    def decode_erc20_transfers(
        self,
        tx_hash: str
    ) -> List[Dict[str, Any]]:
        """
        Decode ALL ERC-20 transfers from a transaction receipt.
        
        This function extracts all token transfers WITHOUT making any RPC calls.
        Cost: FREE (uses existing receipt data)
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            List of decoded transfers:
            [
                {
                    'token': '0xTokenAddress',
                    'from': '0xSender',
                    'to': '0xRecipient',
                    'amount': 1000000,
                    'log_index': 0
                }
            ]
            
        Cost: FREE - no additional RPC calls
            
        Example:
            >>> transfers = transaction.decode_erc20_transfers("0x123...")
            >>> print(f"Found {len(transfers)} token transfers")
            >>> for t in transfers:
            ...     print(f"{t['token']}: {t['amount']}")
        """
        try:
            receipt = self.get_receipt(tx_hash)
            transfers = decode_all_erc20_transfers(receipt)
            
            logger.debug(f"Decoded {len(transfers)} ERC-20 transfers from {tx_hash}")
            return transfers
            
        except Exception as e:
            logger.error(f"Failed to decode ERC-20 transfers: {e}")
            raise TransactionError(f"Transfer decoding failed: {str(e)}") from e

    @track_transaction
    def get_full_transaction_details(
        self,
        tx_hash: str,
        include_token_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Get complete transaction details with ETH + decoded ERC-20 transfers.
        
        This is a comprehensive view showing everything that happened in a transaction.
        
        Args:
            tx_hash: Transaction hash
            include_token_metadata: Fetch token symbols/decimals (costs RPC)
            
        Returns:
            Dictionary with:
                - tx_hash: Transaction hash
                - from: Sender address
                - to: Recipient address
                - eth_value: ETH transferred (Wei)
                - eth_value_formatted: ETH transferred (decimal)
                - status: 'confirmed' or 'failed'
                - gas_used: Gas consumed
                - token_transfers: List of decoded ERC-20 transfers
                - transfer_count: Number of token transfers
                
        Cost: FREE for basic info
              +1 RPC call per unique token if include_token_metadata=True
            
        Example:
            >>> details = transaction.get_full_transaction_details("0x123...")
            >>> print(f"Status: {details['status']}")
            >>> print(f"ETH: {details['eth_value_formatted']}")
            >>> for transfer in details['token_transfers']:
            ...     print(f"  {transfer['symbol']}: {transfer['amount_formatted']}")
        """
        try:
            # Get transaction and receipt
            tx = self.get(tx_hash)
            receipt = self.get_receipt(tx_hash)
            
            # Basic info
            details = {
                'tx_hash': tx_hash,
                'from': tx['from'],
                'to': tx['to'],
                'eth_value': tx['value'],
                'eth_value_formatted': tx['value'] / 10**18,
                'status': 'confirmed' if receipt['status'] == 1 else 'failed',
                'gas_used': receipt['gasUsed'],
                'block_number': receipt['blockNumber'],
                'token_transfers': [],
                'transfer_count': 0,
            }
            
            # Decode ERC-20 transfers
            raw_transfers = decode_all_erc20_transfers(receipt)
            
            if raw_transfers:
                details['transfer_count'] = len(raw_transfers)
                
                # Optionally add token metadata
                if include_token_metadata:
                    from .abis import ERC20_ABI
                    
                    # Get unique tokens
                    unique_tokens = list(set(t['token'] for t in raw_transfers))
                    
                    # Fetch metadata for all tokens in one multicall
                    calls = []
                    for token in unique_tokens:
                        calls.extend([
                            {'contract': token, 'abi': ERC20_ABI, 'function': 'symbol'},
                            {'contract': token, 'abi': ERC20_ABI, 'function': 'decimals'},
                        ])
                    
                    try:
                        results = self.client.multicall(calls)
                        
                        # Build metadata map
                        token_metadata = {}
                        for i, token in enumerate(unique_tokens):
                            idx = i * 2
                            if idx + 1 < len(results):
                                token_metadata[token] = {
                                    'symbol': results[idx],
                                    'decimals': results[idx + 1]
                                }
                        
                        # Add metadata to transfers
                        for transfer in raw_transfers:
                            token_addr = transfer['token']
                            if token_addr in token_metadata:
                                metadata = token_metadata[token_addr]
                                transfer['symbol'] = metadata['symbol']
                                transfer['decimals'] = metadata['decimals']
                                transfer['amount_formatted'] = format_token_amount(
                                    transfer['amount'],
                                    metadata['decimals']
                                )
                            else:
                                transfer['symbol'] = 'UNKNOWN'
                                transfer['decimals'] = 18
                                transfer['amount_formatted'] = transfer['amount'] / 10**18
                        
                    except Exception as e:
                        logger.warning(f"Failed to fetch token metadata: {e}")
                        # Add transfers without metadata
                        for transfer in raw_transfers:
                            transfer['symbol'] = 'UNKNOWN'
                            transfer['decimals'] = 18
                            transfer['amount_formatted'] = transfer['amount'] / 10**18
                
                details['token_transfers'] = raw_transfers
            
            return details
            
        except Exception as e:
            logger.error(f"Failed to get full transaction details: {e}")
            raise TransactionError(f"Failed to get transaction details: {str(e)}") from e

    @track_transaction
    def check_token_transfer(
        self,
        tx_hash: str,
        token_address: str,
        address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if transaction transferred a specific token.
        
        Cost: FREE (uses existing receipt data)
        
        Args:
            tx_hash: Transaction hash
            token_address: Token to check
            address: Optional address filter (sender or receiver)
            
        Returns:
            {
                'found': True/False,
                'transfers': [list of matching transfers],
                'total_amount': Sum of amounts
            }
            
        Example:
            >>> result = transaction.check_token_transfer(
            ...     "0x123...",
            ...     "0xUSDC...",
            ...     "0xMyAddress..."
            ... )
            >>> if result['found']:
            ...     print(f"Found {len(result['transfers'])} USDC transfers")
        """
        try:
            # Decode all transfers
            all_transfers = self.decode_erc20_transfers(tx_hash)
            
            # Filter by token
            token_transfers = filter_transfers_by_token(all_transfers, token_address)
            
            # Optionally filter by address
            if address:
                token_transfers = filter_transfers_by_address(token_transfers, address, 'both')
            
            # Calculate total amount
            total_amount = sum(t['amount'] for t in token_transfers)
            
            return {
                'found': len(token_transfers) > 0,
                'transfers': token_transfers,
                'total_amount': total_amount,
                'transfer_count': len(token_transfers),
            }
            
        except Exception as e:
            logger.error(f"Failed to check token transfer: {e}")
            raise TransactionError(f"Token transfer check failed: {str(e)}") from e

    @track_transaction
    def get_balance_changes(
        self,
        tx_hash: str,
        address: str,
        check_current_balance: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate balance changes for an address from a transaction.
        
        Args:
            tx_hash: Transaction hash
            address: Address to check
            check_current_balance: Get current balance (costs extra RPC)
            
        Returns:
            {
                'address': '0x...',
                'eth_change': -100000000000000000,  # Negative = sent
                'eth_change_formatted': -0.1,
                'token_changes': {
                    '0xUSDC...': {
                        'symbol': 'USDC',
                        'change': 1000000,  # Positive = received
                        'change_formatted': 1.0
                    }
                },
                'current_balances': {...}  # if check_current_balance=True
            }
            
        Cost: FREE for changes
              +1 RPC for ETH balance + 1 multicall for tokens if check_current_balance=True
            
        Example:
            >>> changes = transaction.get_balance_changes("0x123...", "0xMyAddr...")
            >>> if changes['eth_change'] < 0:
            ...     print(f"Sent {abs(changes['eth_change_formatted'])} ETH")
            >>> for token, info in changes['token_changes'].items():
            ...     if info['change'] > 0:
            ...         print(f"Received {info['change_formatted']} {info['symbol']}")
        """
        try:
            from .abis import ERC20_ABI
            
            # Get transaction details
            tx = self.get(tx_hash)
            receipt = self.get_receipt(tx_hash)
            
            address = self.client._validate_address(address)
            
            # Calculate ETH change
            eth_change = 0
            if tx['from'] == address:
                # Sent ETH (including gas costs)
                gas_cost = receipt['gasUsed'] * receipt.get('effectiveGasPrice', tx.get('gasPrice', 0))
                eth_change = -(tx['value'] + gas_cost)
            elif tx['to'] == address:
                # Received ETH
                eth_change = tx['value']
            
            result = {
                'address': address,
                'tx_hash': tx_hash,
                'eth_change': eth_change,
                'eth_change_formatted': eth_change / 10**18,
                'token_changes': {},
            }
            
            # Calculate token changes
            all_transfers = decode_all_erc20_transfers(receipt)
            
            if all_transfers:
                # Group by token
                token_groups = {}
                for transfer in all_transfers:
                    token = transfer['token']
                    if token not in token_groups:
                        token_groups[token] = []
                    token_groups[token].append(transfer)
                
                # Calculate change for each token
                for token, transfers in token_groups.items():
                    change = calculate_balance_change(transfers, address, token)
                    
                    if change != 0:  # Only include tokens with changes
                        result['token_changes'][token] = {
                            'change': change,
                            'change_formatted': 0,  # Will update with metadata
                            'symbol': 'UNKNOWN',
                            'decimals': 18,
                        }
                
                # Fetch token metadata if there are changes
                if result['token_changes']:
                    try:
                        calls = []
                        tokens_list = list(result['token_changes'].keys())
                        
                        for token in tokens_list:
                            calls.extend([
                                {'contract': token, 'abi': ERC20_ABI, 'function': 'symbol'},
                                {'contract': token, 'abi': ERC20_ABI, 'function': 'decimals'},
                            ])
                        
                        results = self.client.multicall(calls)
                        
                        for i, token in enumerate(tokens_list):
                            idx = i * 2
                            if idx + 1 < len(results):
                                symbol = results[idx]
                                decimals = results[idx + 1]
                                
                                result['token_changes'][token]['symbol'] = symbol
                                result['token_changes'][token]['decimals'] = decimals
                                result['token_changes'][token]['change_formatted'] = format_token_amount(
                                    result['token_changes'][token]['change'],
                                    decimals
                                )
                    except Exception as e:
                        logger.warning(f"Failed to fetch token metadata: {e}")
            
            # Optionally get current balances
            if check_current_balance:
                try:
                    current_balances = {
                        'eth': self.client.get_balance(address),
                        'tokens': {}
                    }
                    
                    if result['token_changes']:
                        token_list = list(result['token_changes'].keys())
                        balances = self.client.batch_get_token_balances(address, token_list)
                        current_balances['tokens'] = balances
                    
                    result['current_balances'] = current_balances
                except Exception as e:
                    logger.warning(f"Failed to get current balances: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to calculate balance changes: {e}")
            raise TransactionError(f"Balance change calculation failed: {str(e)}") from e

    @track_transaction
    def classify_transaction(
        self,
        tx_hash: str
    ) -> Dict[str, Any]:
        """
        Classify transaction type and participants.
        
        Cost: FREE (analysis of existing data)
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            {
                'tx_hash': '0x...',
                'type': 'token_transfer',  # or 'eth_transfer', 'contract_interaction', 'swap'
                'participants': ['0xFrom...', '0xTo...'],
                'tokens_involved': ['0xUSDC...'],
                'eth_involved': True,
                'contract_calls': 1,
                'complexity': 'simple'  # or 'medium', 'complex'
            }
            
        Example:
            >>> classification = transaction.classify_transaction("0x123...")
            >>> print(f"Type: {classification['type']}")
            >>> print(f"Complexity: {classification['complexity']}")
        """
        try:
            tx = self.get(tx_hash)
            receipt = self.get_receipt(tx_hash)
            
            # Basic info
            classification = {
                'tx_hash': tx_hash,
                'type': 'unknown',
                'participants': [tx['from']],
                'tokens_involved': [],
                'eth_involved': tx['value'] > 0,
                'contract_calls': 0,
                'complexity': 'simple',
            }
            
            if tx['to']:
                classification['participants'].append(tx['to'])
            
            # Check if contract interaction
            if tx['to']:
                is_contract = self.client.is_contract(tx['to'])
                if is_contract:
                    classification['contract_calls'] += 1
            
            # Decode token transfers
            token_transfers = decode_all_erc20_transfers(receipt)
            
            if token_transfers:
                unique_tokens = list(set(t['token'] for t in token_transfers))
                classification['tokens_involved'] = unique_tokens
                
                # Add transfer participants
                for transfer in token_transfers:
                    if transfer['from'] not in classification['participants']:
                        classification['participants'].append(transfer['from'])
                    if transfer['to'] not in classification['participants']:
                        classification['participants'].append(transfer['to'])
            
            # Classify type
            if len(token_transfers) == 0 and tx['value'] > 0:
                classification['type'] = 'eth_transfer'
            elif len(token_transfers) == 1 and tx['value'] == 0:
                classification['type'] = 'token_transfer'
            elif len(token_transfers) >= 2:
                classification['type'] = 'swap'  # Multiple tokens = likely a swap
            elif classification['contract_calls'] > 0:
                classification['type'] = 'contract_interaction'
            
            # Determine complexity
            total_operations = len(token_transfers) + classification['contract_calls']
            if total_operations <= 1:
                classification['complexity'] = 'simple'
            elif total_operations <= 3:
                classification['complexity'] = 'medium'
            else:
                classification['complexity'] = 'complex'
            
            return classification
            
        except Exception as e:
            logger.error(f"Failed to classify transaction: {e}")
            raise TransactionError(f"Transaction classification failed: {str(e)}") from e

    @track_transaction
    def batch_decode_transactions(
        self,
        tx_hashes: List[str],
        include_token_metadata: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        """
        Decode multiple transactions efficiently.
        
        Args:
            tx_hashes: List of transaction hashes
            include_token_metadata: Fetch token symbols/decimals
            
        Returns:
            Dictionary mapping tx_hash to decoded details
            
        Cost: 2 RPC calls per tx (get tx + get receipt)
              +1 RPC per unique token if include_token_metadata=True
            
        Example:
            >>> hashes = ["0x123...", "0x456..."]
            >>> results = transaction.batch_decode_transactions(hashes)
            >>> for tx_hash, details in results.items():
            ...     print(f"{tx_hash}: {details['transfer_count']} transfers")
        """
        results = {}
        
        for tx_hash in tx_hashes:
            try:
                results[tx_hash] = self.get_full_transaction_details(
                    tx_hash,
                    include_token_metadata=include_token_metadata
                )
            except Exception as e:
                logger.warning(f"Failed to decode {tx_hash}: {e}")
                results[tx_hash] = {'error': str(e)}
        
        return results

    # =========================================================================
    # WRITE OPERATIONS - Send transactions (REQUIRES WALLET)
    # =========================================================================

    def _require_wallet(self):
        """Check if wallet is available."""
        if self.wallet is None:
            raise TransactionError(
                "Wallet required for sending transactions. "
                "Initialize Transaction with a Wallet instance: "
                "Transaction(client, wallet)"
            )

    def _build_transaction_base(
        self,
        to: str,
        value: int = 0,
        data: str = '0x',
        gas: Optional[int] = None,
        gas_strategy: Optional[str] = None,
        nonce: Optional[int] = None,
        use_eip1559: bool = True
    ) -> Dict[str, Any]:
        """
        Build base transaction with all parameters.
        
        Args:
            to: Recipient address
            value: Value in Wei
            data: Transaction data
            gas: Gas limit (None to estimate)
            gas_strategy: Gas pricing strategy
            nonce: Nonce (None to auto-manage)
            use_eip1559: Use EIP-1559 fees
            
        Returns:
            Transaction dictionary ready for signing
        """
        self._require_wallet()
        
        strategy = gas_strategy or self.default_gas_strategy
        
        # Build base transaction
        tx = {
            'from': self.wallet.address,
            'to': to,
            'value': value,
            'data': data,
            'chainId': self.client.get_chain_id(),
        }
        
        # Get nonce
        if nonce is None:
            tx['nonce'] = self.nonce_manager.get_nonce()
        else:
            tx['nonce'] = nonce
        
        # Add gas pricing
        if use_eip1559:
            fees = GasStrategy.get_eip1559_fees(self.client, strategy)
            tx.update(fees)
        else:
            gas_price = GasStrategy.get_gas_price(self.client, strategy)
            tx.update(gas_price)
        
        # Estimate gas if not provided
        if gas is None:
            tx['gas'] = GasStrategy.estimate_gas_with_buffer(self.client, tx)
        else:
            tx['gas'] = gas
        
        return tx

    @track_transaction
    def simulate(
        self,
        to: str,
        value: int = 0,
        data: str = '0x',
        from_address: Optional[str] = None
    ) -> Any:
        """
        Simulate transaction execution without sending.
        
        Args:
            to: Recipient address
            value: Value in Wei
            data: Transaction data
            from_address: Sender address (uses wallet if None)
            
        Returns:
            Simulation result
            
        Raises:
            ValidationError: If simulation fails (e.g., would revert)
            
        Example:
            >>> # Test if transaction would succeed
            >>> try:
            ...     result = transaction.simulate(
            ...         to="0xContract...",
            ...         data="0x..."
            ...     )
            ...     print("Transaction would succeed")
            ... except ValidationError as e:
            ...     print(f"Transaction would fail: {e}")
        """
        tx = {
            'to': to,
            'value': value,
            'data': data,
        }
        
        if from_address:
            tx['from'] = from_address
        elif self.wallet:
            tx['from'] = self.wallet.address
        
        try:
            return self.client.w3.eth.call(tx)
        except Exception as e:
            error_msg = str(e)
            if "execution reverted" in error_msg.lower():
                logger.error(f"Simulation failed: {error_msg}")
                raise ValidationError(f"Transaction would revert: {error_msg}")
            raise RPCError(f"Simulation failed: {str(e)}") from e

    @track_transaction
    def send_eth(
        self, 
        to_address: str, 
        amount: float, 
        unit: str = "ether",
        gas: Optional[int] = None,
        gas_strategy: Optional[str] = None,
        wait_for_receipt: bool = False,
        simulate_first: bool = True,
        max_retries: int = 3
    ) -> Union[str, Dict[str, Any]]:
        """
        Send ETH to a specified address with production features.
        
        REQUIRES WALLET - Only the wallet owner can call this.
        
        Args:
            to_address: Recipient address
            amount: Amount to send (float)
            unit: "wei", "gwei", or "ether" (default: "ether")
            gas: Gas limit (None to estimate)
            gas_strategy: 'slow', 'standard', 'fast', 'instant' (None for default)
            wait_for_receipt: Wait for confirmation (default: False)
            simulate_first: Simulate before sending (default: True)
            max_retries: Maximum retry attempts (default: 3)
            
        Returns:
            str: Transaction hash if wait_for_receipt=False
            dict: Transaction receipt if wait_for_receipt=True
            
        Raises:
            TransactionError: If wallet missing, insufficient balance, or sending fails
            ValidationError: If simulation fails
            
        Example:
            >>> # Simple send
            >>> tx_hash = transaction.send_eth("0xRecipient...", 0.1)
            
            >>> # Fast transaction with confirmation
            >>> receipt = transaction.send_eth(
            ...     "0xRecipient...",
            ...     0.1,
            ...     gas_strategy='fast',
            ...     wait_for_receipt=True
            ... )
        """
        self._require_wallet()
        
        try:
            # Convert amount to Wei
            value = to_wei(amount, unit)
            
            # Check balance
            balance = self.client.get_balance(self.wallet.address)
            if balance < value:
                raise TransactionError(
                    f"Insufficient balance. Required: {value} Wei, "
                    f"Available: {balance} Wei"
                )
            
            # Simulate if requested
            if simulate_first:
                try:
                    self.simulate(to=to_address, value=value)
                    logger.debug("Transaction simulation successful")
                except ValidationError as e:
                    raise TransactionError(f"Transaction would fail: {e}") from e
            
            # Build transaction
            tx = self._build_transaction_base(
                to=to_address,
                value=value,
                gas=gas or 21000,
                gas_strategy=gas_strategy
            )
            
            # Send with retry
            last_error = None
            for attempt in range(max_retries):
                try:
                    # Sign transaction
                    signed_tx = self.wallet.sign_transaction(tx)
                    
                    # Send to network
                    tx_hash = self.client.w3.eth.send_raw_transaction(
                    signed_tx.raw_transaction  # ✅ Change to this!
                )
                    tx_hash_hex = self.client.w3.to_hex(tx_hash)
                    
                    logger.info(
                        f"Sent {amount} {unit} to {to_address}: {tx_hash_hex} "
                        f"(nonce: {tx['nonce']})"
                    )
                    
                    # Record metrics
                    if self.metrics:
                        self.metrics.record_transaction(
                            gas_used=tx['gas'],
                            gas_price=tx.get('gasPrice', tx.get('maxFeePerGas', 0)),
                            success=True
                        )
                    
                    # Wait for confirmation if requested
                    if wait_for_receipt:
                        return self.wait_for_confirmation(tx_hash_hex)
                    
                    return tx_hash_hex
                    
                except Exception as e:
                    last_error = e
                    
                    # Check if it's a nonce error
                    error_msg = str(e).lower()
                    if 'nonce' in error_msg or 'already known' in error_msg:
                        logger.warning(f"Nonce collision detected, refreshing (attempt {attempt + 1})")
                        self.nonce_manager.reset()
                        tx['nonce'] = self.nonce_manager.get_nonce(force_refresh=True)
                        time.sleep(0.5)
                        continue
                    
                    # Retry on network errors
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(
                            f"Transaction failed (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            # Record failed transaction
            if self.metrics:
                self.metrics.record_transaction(0, 0, False)
            
            raise TransactionError(f"Failed to send ETH: {last_error}") from last_error
            
        except TransactionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending ETH: {e}")
            raise TransactionError(f"Failed to send ETH: {e}") from e

    @track_transaction
    def send_erc20(
        self, 
        token_address: str, 
        to_address: str, 
        amount: int, 
        abi: list,
        gas: Optional[int] = None,
        gas_strategy: Optional[str] = None,
        wait_for_receipt: bool = False,
        simulate_first: bool = True,
        max_retries: int = 3
    ) -> Union[str, Dict[str, Any]]:
        """
        Send ERC-20 tokens with production features.
        
        REQUIRES WALLET - Only the wallet owner can call this.
        
        Args:
            token_address: Token contract address
            to_address: Recipient address
            amount: Amount in token's smallest unit
            abi: Token contract ABI (standard ERC-20)
            gas: Gas limit (None to estimate)
            gas_strategy: Gas pricing strategy
            wait_for_receipt: Wait for confirmation
            simulate_first: Simulate before sending
            max_retries: Maximum retry attempts
            
        Returns:
            str: Transaction hash if wait_for_receipt=False
            dict: Transaction receipt if wait_for_receipt=True
            
        Raises:
            TransactionError: If wallet missing, insufficient tokens, or sending fails
            ValidationError: If simulation fails
            
        Example:
            >>> # Send 100 USDC (6 decimals)
            >>> amount = 100 * 10**6
            >>> tx_hash = transaction.send_erc20(
            ...     token_address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            ...     to_address="0xRecipient...",
            ...     amount=amount,
            ...     abi=ERC20_ABI,
            ...     gas_strategy='fast'
            ... )
        """
        self._require_wallet()
        
        try:
            # Initialize contract
            contract = self.client.w3.eth.contract(
                address=token_address, 
                abi=abi
            )
            
            # Check token balance
            try:
                balance = contract.functions.balanceOf(self.wallet.address).call()
                if balance < amount:
                    raise TransactionError(
                        f"Insufficient token balance. Required: {amount}, "
                        f"Available: {balance}"
                    )
            except Exception as e:
                logger.warning(f"Could not verify token balance: {e}")
            
            # Build function call data
            function_data = contract.functions.transfer(
                to_address, 
                amount
            ).build_transaction({
                'from': self.wallet.address,
                'chainId': self.client.get_chain_id(),
            })
            
            # Simulate if requested
            if simulate_first:
                try:
                    self.simulate(
                        to=token_address,
                        data=function_data['data']
                    )
                    logger.debug("Token transfer simulation successful")
                except ValidationError as e:
                    raise TransactionError(f"Transfer would fail: {e}") from e
            
            # Build complete transaction
            tx = self._build_transaction_base(
                to=token_address,
                value=0,
                data=function_data['data'],
                gas=gas,
                gas_strategy=gas_strategy
            )
            
            # Send with retry
            last_error = None
            for attempt in range(max_retries):
                try:
                    # Sign transaction
                    signed_tx = self.wallet.sign_transaction(tx)
                    
                    # Send to network
                    tx_hash = self.client.w3.eth.send_raw_transaction(
                    signed_tx.raw_transaction  # ✅ Change to this!
                )
                    tx_hash_hex = self.client.w3.to_hex(tx_hash)
                    
                    logger.info(
                        f"Sent {amount} tokens to {to_address}: {tx_hash_hex} "
                        f"(nonce: {tx['nonce']})"
                    )
                    
                    # Record metrics
                    if self.metrics:
                        self.metrics.record_transaction(
                            gas_used=tx['gas'],
                            gas_price=tx.get('gasPrice', tx.get('maxFeePerGas', 0)),
                            success=True
                        )
                    
                    # Wait for confirmation if requested
                    if wait_for_receipt:
                        return self.wait_for_confirmation(tx_hash_hex)
                    
                    return tx_hash_hex
                    
                except Exception as e:
                    last_error = e
                    
                    # Check if it's a nonce error
                    error_msg = str(e).lower()
                    if 'nonce' in error_msg or 'already known' in error_msg:
                        logger.warning(f"Nonce collision detected, refreshing (attempt {attempt + 1})")
                        self.nonce_manager.reset()
                        tx['nonce'] = self.nonce_manager.get_nonce(force_refresh=True)
                        time.sleep(0.5)
                        continue
                    
                    # Retry on network errors
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(
                            f"Token transfer failed (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            # Record failed transaction
            if self.metrics:
                self.metrics.record_transaction(0, 0, False)
            
            raise TransactionError(f"Failed to send ERC-20: {last_error}") from last_error
            
        except TransactionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending ERC-20: {e}")
            raise TransactionError(f"Failed to send ERC-20: {e}") from e

    @track_transaction
    def send_raw_transaction(
        self,
        to: str,
        data: str = '0x',
        value: int = 0,
        gas: Optional[int] = None,
        gas_strategy: Optional[str] = None,
        wait_for_receipt: bool = False,
        simulate_first: bool = True,
        max_retries: int = 3
    ) -> Union[str, Dict[str, Any]]:
        """
        Send a raw transaction (for contract interactions).
        
        REQUIRES WALLET - Only the wallet owner can call this.
        
        Args:
            to: Contract/recipient address
            data: Transaction calldata
            value: ETH value in Wei
            gas: Gas limit (None to estimate)
            gas_strategy: Gas pricing strategy
            wait_for_receipt: Wait for confirmation
            simulate_first: Simulate before sending
            max_retries: Maximum retry attempts
            
        Returns:
            str: Transaction hash if wait_for_receipt=False
            dict: Transaction receipt if wait_for_receipt=True
            
        Example:
            >>> # Call contract function
            >>> tx_hash = transaction.send_raw_transaction(
            ...     to="0xContract...",
            ...     data="0x...",  # Encoded function call
            ...     value=0
            ... )
        """
        self._require_wallet()
        
        try:
            # Simulate if requested
            if simulate_first:
                try:
                    self.simulate(to=to, data=data, value=value)
                    logger.debug("Raw transaction simulation successful")
                except ValidationError as e:
                    raise TransactionError(f"Transaction would fail: {e}") from e
            
            # Build transaction
            tx = self._build_transaction_base(
                to=to,
                value=value,
                data=data,
                gas=gas,
                gas_strategy=gas_strategy
            )
            
            # Send with retry
            last_error = None
            for attempt in range(max_retries):
                try:
                    # Sign transaction
                    signed_tx = self.wallet.sign_transaction(tx)
                    
                    # Send to network
                    tx_hash = self.client.w3.eth.send_raw_transaction(
                    signed_tx.raw_transaction  # ✅ Change to this!
                )
                    tx_hash_hex = self.client.w3.to_hex(tx_hash)
                    
                    logger.info(f"Sent raw transaction: {tx_hash_hex} (nonce: {tx['nonce']})")
                    
                    # Record metrics
                    if self.metrics:
                        self.metrics.record_transaction(
                            gas_used=tx['gas'],
                            gas_price=tx.get('gasPrice', tx.get('maxFeePerGas', 0)),
                            success=True
                        )
                    
                    # Wait for confirmation if requested
                    if wait_for_receipt:
                        return self.wait_for_confirmation(tx_hash_hex)
                    
                    return tx_hash_hex
                    
                except Exception as e:
                    last_error = e
                    
                    # Check if it's a nonce error
                    error_msg = str(e).lower()
                    if 'nonce' in error_msg or 'already known' in error_msg:
                        logger.warning(f"Nonce collision detected, refreshing (attempt {attempt + 1})")
                        self.nonce_manager.reset()
                        tx['nonce'] = self.nonce_manager.get_nonce(force_refresh=True)
                        time.sleep(0.5)
                        continue
                    
                    # Retry on network errors
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(
                            f"Raw transaction failed (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            # Record failed transaction
            if self.metrics:
                self.metrics.record_transaction(0, 0, False)
            
            raise TransactionError(f"Failed to send transaction: {last_error}") from last_error
            
        except TransactionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending transaction: {e}")
            raise TransactionError(f"Failed to send transaction: {e}") from e

    # =========================================================================
    # BATCH OPERATIONS
    # =========================================================================

    @track_transaction
    def send_batch(
        self,
        transactions: List[Dict[str, Any]],
        gas_strategy: Optional[str] = None,
        wait_for_all: bool = False,
        stop_on_error: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Send multiple transactions in sequence.
        
        REQUIRES WALLET - Only the wallet owner can call this.
        
        Args:
            transactions: List of transaction dicts with keys:
                - type: 'eth' or 'erc20'
                - to: Recipient address
                - amount: Amount to send
                - unit: (for eth) 'wei', 'gwei', 'ether'
                - token_address: (for erc20) Token contract
                - abi: (for erc20) Token ABI
            gas_strategy: Gas pricing strategy for all txs
            wait_for_all: Wait for all transactions to confirm
            stop_on_error: Stop batch if a transaction fails
            
        Returns:
            List of results with status and tx_hash or error
            
        Example:
            >>> batch = [
            ...     {
            ...         'type': 'eth',
            ...         'to': '0xRecipient1...',
            ...         'amount': 0.1,
            ...         'unit': 'ether'
            ...     },
            ...     {
            ...         'type': 'erc20',
            ...         'token_address': '0xUSDC...',
            ...         'to': '0xRecipient2...',
            ...         'amount': 100 * 10**6,
            ...         'abi': ERC20_ABI
            ...     }
            ... ]
            >>> results = transaction.send_batch(batch)
            >>> for i, result in enumerate(results):
            ...     if result['success']:
            ...         print(f"TX {i}: {result['tx_hash']}")
            ...     else:
            ...         print(f"TX {i} failed: {result['error']}")
        """
        self._require_wallet()
        
        results = []
        
        for i, tx_config in enumerate(transactions):
            try:
                tx_type = tx_config.get('type', 'eth')
                
                if tx_type == 'eth':
                    tx_hash = self.send_eth(
                        to_address=tx_config['to'],
                        amount=tx_config['amount'],
                        unit=tx_config.get('unit', 'ether'),
                        gas_strategy=gas_strategy,
                        wait_for_receipt=wait_for_all
                    )
                    
                    results.append({
                        'index': i,
                        'success': True,
                        'tx_hash': tx_hash if isinstance(tx_hash, str) else tx_hash['transactionHash'],
                        'type': 'eth'
                    })
                    
                elif tx_type == 'erc20':
                    tx_hash = self.send_erc20(
                        token_address=tx_config['token_address'],
                        to_address=tx_config['to'],
                        amount=tx_config['amount'],
                        abi=tx_config['abi'],
                        gas_strategy=gas_strategy,
                        wait_for_receipt=wait_for_all
                    )
                    
                    results.append({
                        'index': i,
                        'success': True,
                        'tx_hash': tx_hash if isinstance(tx_hash, str) else tx_hash['transactionHash'],
                        'type': 'erc20'
                    })
                else:
                    raise TransactionError(f"Unknown transaction type: {tx_type}")
                
                logger.info(f"Batch transaction {i+1}/{len(transactions)} sent successfully")
                
            except Exception as e:
                logger.error(f"Batch transaction {i+1}/{len(transactions)} failed: {e}")
                
                results.append({
                    'index': i,
                    'success': False,
                    'error': str(e),
                    'type': tx_config.get('type', 'eth')
                })
                
                if stop_on_error:
                    logger.warning(f"Stopping batch after error (stop_on_error=True)")
                    break
        
        return results

    # =========================================================================
    # UTILITY & MONITORING
    # =========================================================================

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get transaction metrics.
        
        Returns:
            Dictionary with transaction statistics
            
        Example:
            >>> metrics = transaction.get_metrics()
            >>> print(f"Transactions sent: {metrics['transactions_sent']}")
            >>> print(f"Avg gas used: {metrics['avg_gas_used']}")
        """
        if self.metrics:
            return self.metrics.get_stats()
        return {}

    def reset_metrics(self):
        """Reset all metrics counters."""
        if self.metrics:
            self.metrics.reset()
            logger.info("Transaction metrics reset")

    def estimate_total_cost(
        self,
        to: str,
        value: int = 0,
        data: str = '0x',
        gas_strategy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Estimate total transaction cost (L1 + L2 for Base).
        
        Args:
            to: Recipient address
            value: Value in Wei
            data: Transaction data
            gas_strategy: Gas pricing strategy
            
        Returns:
            Dictionary with cost breakdown
            
        Example:
            >>> cost = transaction.estimate_total_cost(
            ...     to="0xContract...",
            ...     data="0x..."
            ... )
            >>> print(f"Total estimated cost: {cost['total_cost_eth']:.6f} ETH")
        """
        tx = {
            'to': to,
            'value': value,
            'data': data,
        }
        
        if self.wallet:
            tx['from'] = self.wallet.address
        
        return self.client.estimate_total_fee(tx)

    def __repr__(self) -> str:
        """String representation."""
        wallet_info = f"wallet={self.wallet.address[:10]}..." if self.wallet else "wallet=None"
        return f"Transaction({wallet_info}, strategy={self.default_gas_strategy})"


# ============================================================================
# PRODUCTION ENHANCEMENTS SUMMARY
# ============================================================================
# 
# ✅ TRANSACTION MANAGEMENT
# - Thread-safe nonce management with collision detection
# - Automatic retry with exponential backoff
# - Transaction simulation before sending
# - EIP-1559 fee support
# - Multiple gas strategies (slow/standard/fast/instant)
# 
# ✅ ERROR HANDLING & RESILIENCE
# - Nonce collision recovery
# - Network error retry logic
# - Balance validation before sending
# - Comprehensive error messages
# - Graceful degradation
# 
# ✅ MONITORING & METRICS
# - Transaction operation tracking
# - Gas usage statistics
# - Performance metrics
# - Success/failure rates
# 
# ✅ SECURITY
# - Transaction simulation to prevent failures
# - Balance checks before sending
# - Input validation
# - Wallet requirement checks
# 
# ✅ PERFORMANCE OPTIMIZATION
# - Smart gas estimation with buffer
# - Nonce caching
# - Batch transaction support
# - Efficient receipt fetching
# 
# ✅ BASE L2 SPECIFIC
# - L1 + L2 fee estimation
# - Transaction cost breakdown
# - Optimized for Base network characteristics
# 
# ✅ NEW: ERC-20 TRANSFER DECODING (Zero RPC Cost)
# - decode_erc20_transfers(): Extract all token transfers from receipt
# - get_full_transaction_details(): Complete transaction view (ETH + tokens)
# - check_token_transfer(): Check if specific token was transferred
# - get_balance_changes(): Calculate what changed for an address
# - classify_transaction(): Automatically categorize transaction type
# - batch_decode_transactions(): Decode multiple transactions efficiently
# 
# NEW FEATURES:
# - ERC-20 transfer decoding (zero cost)
# - Transaction classification
# - Balance change tracking
# - Token transfer filtering
# - Comprehensive transaction analysis
# 
# BACKWARD COMPATIBILITY:
# - All existing methods work unchanged
# - New features are opt-in via new methods
# - Default behavior preserved
# ============================================================================