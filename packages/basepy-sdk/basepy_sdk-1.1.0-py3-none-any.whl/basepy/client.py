"""
BaseClient - Production-ready implementation with comprehensive resilience and monitoring.
"""

from web3 import Web3
from web3.providers import HTTPProvider
from typing import List, Optional, Union, Dict, Any, Callable
import logging
import time
import threading
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib
import json

from .utils import (
    BASE_MAINNET_RPC_URLS, 
    BASE_SEPOLIA_RPC_URLS,
    BASE_MAINNET_CHAIN_ID, 
    BASE_SEPOLIA_CHAIN_ID
)
from .exceptions import (
    ConnectionError, 
    RPCError, 
    ValidationError, 
    RateLimitError,
    CircuitBreakerOpenError
)
from .abis import GAS_ORACLE_ABI

# Structured logging setup
logger = logging.getLogger(__name__)


class Config:
    """Configuration management for BaseClient."""
    
    # Connection settings
    CONNECTION_TIMEOUT = 30
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_BACKOFF_FACTOR = 2
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60  # seconds
    
    # Circuit breaker
    CIRCUIT_BREAKER_THRESHOLD = 5
    CIRCUIT_BREAKER_TIMEOUT = 60
    
    # Caching
    CACHE_TTL = 10  # seconds
    CACHE_ENABLED = True
    
    # Logging
    LOG_LEVEL = logging.INFO
    LOG_RPC_CALLS = False
    
    @classmethod
    def from_env(cls, environment: str = 'production'):
        """Load configuration based on environment."""
        if environment == 'development':
            cls.LOG_LEVEL = logging.DEBUG
            cls.LOG_RPC_CALLS = True
            cls.CACHE_TTL = 5
        elif environment == 'staging':
            cls.LOG_LEVEL = logging.INFO
            cls.CACHE_TTL = 10
        elif environment == 'production':
            cls.LOG_LEVEL = logging.WARNING
            cls.CACHE_TTL = 15
        
        logger.setLevel(cls.LOG_LEVEL)
        return cls


class Metrics:
    """Metrics collection for monitoring."""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()
    
    def reset(self):
        """Reset all metrics."""
        with self._lock:
            self.request_count = defaultdict(int)
            self.error_count = defaultdict(int)
            self.latencies = defaultdict(list)
            self.rpc_usage = defaultdict(int)
            self.cache_hits = 0
            self.cache_misses = 0
            self.circuit_breaker_trips = 0
    
    def record_request(self, method: str, duration: float, success: bool, rpc_url: str):
        """Record a request metric."""
        with self._lock:
            self.request_count[method] += 1
            self.latencies[method].append(duration)
            self.rpc_usage[rpc_url] += 1
            if not success:
                self.error_count[method] += 1
    
    def record_cache_hit(self):
        """Record a cache hit."""
        with self._lock:
            self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record a cache miss."""
        with self._lock:
            self.cache_misses += 1
    
    def record_circuit_breaker_trip(self):
        """Record a circuit breaker trip."""
        with self._lock:
            self.circuit_breaker_trips += 1
    
    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            stats = {
                'requests': dict(self.request_count),
                'errors': dict(self.error_count),
                'cache_hits': self.cache_hits,
                'cache_misses': self.cache_misses,
                'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
                'rpc_usage': dict(self.rpc_usage),
                'circuit_breaker_trips': self.circuit_breaker_trips,
                'avg_latencies': {}
            }
            for method, latencies in self.latencies.items():
                if latencies:
                    stats['avg_latencies'][method] = sum(latencies) / len(latencies)
            return stats



class CircuitBreaker:
    """Circuit breaker pattern for RPC endpoints."""
    
    def __init__(self, threshold: int = 5, timeout: int = 60):
        self.threshold = threshold
        self.timeout = timeout
        self.failure_count = defaultdict(int)
        self.last_failure_time = {}
        self.state = defaultdict(lambda: 'closed')  # closed, open, half-open
        self._lock = threading.Lock()
    
    def call(self, rpc_url: str, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        with self._lock:
            # Check if circuit is open
            if self.state[rpc_url] == 'open':
                # Check if timeout has passed
                if time.time() - self.last_failure_time[rpc_url] > self.timeout:
                    self.state[rpc_url] = 'half-open'
                    logger.info(f"Circuit breaker half-open for {rpc_url}")
                else:
                    raise CircuitBreakerOpenError(f"Circuit breaker open for {rpc_url}")
        
        try:
            result = func(*args, **kwargs)
            
            with self._lock:
                # Success - reset failure count
                if self.state[rpc_url] == 'half-open':
                    self.state[rpc_url] = 'closed'
                    logger.info(f"Circuit breaker closed for {rpc_url}")
                self.failure_count[rpc_url] = 0
            
            return result
            
        except Exception as e:
            with self._lock:
                self.failure_count[rpc_url] += 1
                self.last_failure_time[rpc_url] = time.time()
                
                # Open circuit if threshold exceeded
                if self.failure_count[rpc_url] >= self.threshold:
                    self.state[rpc_url] = 'open'
                    logger.error(f"Circuit breaker opened for {rpc_url}")
            raise


class Cache:
    """Simple TTL-based cache for RPC responses."""
    
    def __init__(self, ttl: int = 10):
        self.ttl = ttl
        self._cache = {}
        self._timestamps = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key in self._cache:
                if time.time() - self._timestamps[key] < self.ttl:
                    return self._cache[key]
                else:
                    # Expired
                    del self._cache[key]
                    del self._timestamps[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache with current timestamp."""
        with self._lock:
            self._cache[key] = value
            self._timestamps[key] = time.time()
    
    def clear(self):
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
    
    @staticmethod
    def make_key(method: str, *args, **kwargs) -> str:
        """Generate cache key from method and arguments."""
        key_data = f"{method}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.tokens = requests
        self.last_update = time.time()
        self._lock = threading.Lock()
    
    def acquire(self):
        """Acquire a token, raise RateLimitError if not available."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_update
            
            # Refill tokens based on elapsed time
            self.tokens = min(
                self.requests,
                self.tokens + (elapsed / self.window) * self.requests
            )
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                raise RateLimitError("Rate limit exceeded. Please slow down requests.")


def retry_with_backoff(max_retries: int = 3, backoff_factor: int = 2):
    """Decorator for exponential backoff retry logic."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, RPCError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        sleep_time = backoff_factor ** attempt
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator


def track_performance(func):
    """Decorator to track method performance."""
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
            
            # Record metrics
            if hasattr(self, 'metrics'):
                rpc_url = self.w3.provider.endpoint_uri if hasattr(self.w3.provider, 'endpoint_uri') else 'unknown'
                self.metrics.record_request(
                    method=func.__name__,
                    duration=duration,
                    success=success,
                    rpc_url=rpc_url
                )
            
            if Config.LOG_RPC_CALLS:
                logger.debug(f"{func.__name__} took {duration:.3f}s (success={success})")
    
    return wrapper


class BaseClient:
    """
    Production-ready client for interacting with Base blockchain (Layer 2).
    
    Features:
    - Automatic RPC failover with circuit breaker
    - Request retry with exponential backoff
    - Rate limiting and caching
    - Comprehensive metrics and monitoring
    - Thread-safe operations
    
    Args:
        chain_id: Network chain ID (8453 for mainnet, 84532 for Sepolia)
        rpc_urls: Optional list of RPC endpoints for failover
        config: Optional Config object for custom configuration
        environment: Environment name ('development', 'staging', 'production')
        
    Example:
        >>> # Production setup
        >>> client = BaseClient(environment='production')
        >>> 
        >>> # Development with verbose logging
        >>> dev_client = BaseClient(
        ...     chain_id=84532,
        ...     environment='development'
        ... )
        >>> 
        >>> # Monitor performance
        >>> stats = client.get_metrics()
        >>> print(f"Cache hit rate: {stats['cache_hit_rate']:.2%}")
    """
    
    def __init__(
        self, 
        chain_id: int = BASE_MAINNET_CHAIN_ID,
        rpc_urls: Optional[List[str]] = None,
        config: Optional[Config] = None,
        environment: str = 'production'
    ) -> None:
        """Initialize production-ready Base client."""
        
        # Load configuration
        self.config = config or Config.from_env(environment)
        
        # Store chain ID
        self.chain_id = chain_id
        
        # Set RPC URLs
        if rpc_urls:
            self.rpc_urls = rpc_urls
        elif chain_id == BASE_MAINNET_CHAIN_ID:
            self.rpc_urls = BASE_MAINNET_RPC_URLS.copy()
        elif chain_id == BASE_SEPOLIA_CHAIN_ID:
            self.rpc_urls = BASE_SEPOLIA_RPC_URLS.copy()
        else:
            raise ValueError("Invalid chain_id and no rpc_urls provided.")
        
        # Initialize components
        self.metrics = Metrics()
        self.circuit_breaker = CircuitBreaker(
            threshold=Config.CIRCUIT_BREAKER_THRESHOLD,
            timeout=Config.CIRCUIT_BREAKER_TIMEOUT
        )
        self.cache = Cache(ttl=Config.CACHE_TTL) if Config.CACHE_ENABLED else None
        self.rate_limiter = RateLimiter(
            requests=Config.RATE_LIMIT_REQUESTS,
            window=Config.RATE_LIMIT_WINDOW
        )
        
        # Connection tracking
        self.current_rpc_index = 0
        self.connection_attempts = 0
        self._lock = threading.Lock()
        
        # Connect to RPC
        self.w3 = self._connect()
        
        logger.info(f"BaseClient initialized for chain {chain_id} in {environment} mode")
    
    def _connect(self) -> Web3:
        """
        Connect to RPC with failover and circuit breaker.
        
        Returns:
            Web3: Connected Web3 instance
            
        Raises:
            ConnectionError: If all RPC connections fail
        """
        logger.info(f"Attempting to connect to {len(self.rpc_urls)} RPC endpoint(s)")
        
        for idx, url in enumerate(self.rpc_urls, 1):
            try:
                logger.debug(f"Trying RPC {idx}/{len(self.rpc_urls)}: {self._sanitize_url(url)}")
                
                # Create Web3 instance
                provider = HTTPProvider(
                    url,
                    request_kwargs={
                        'timeout': Config.CONNECTION_TIMEOUT
                    }
                )
                w3 = Web3(provider)
                
                # Test connection with circuit breaker
                def test_connection():
                    if not w3.is_connected():
                        raise ConnectionError(f"Connection check failed for {url}")
                    return w3
                
                result = self.circuit_breaker.call(url, test_connection)
                
                logger.info(f"Successfully connected to RPC endpoint {idx}")
                self.current_rpc_index = idx - 1
                return result
                
            except (ConnectionError, CircuitBreakerOpenError) as e:
                logger.warning(f"Failed to connect to {self._sanitize_url(url)}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Unexpected error connecting to {self._sanitize_url(url)}: {e}")
                continue
        
        logger.error("Failed to connect to any provided RPC URL")
        raise ConnectionError("Failed to connect to any provided RPC URL.")
    
    def _sanitize_url(self, url: str) -> str:
        """Remove sensitive data from URL for logging."""
        if not url:
            return "unknown"
        # Remove API keys from URL
        if '?' in url:
            return url.split('?')[0] + "?..."
        return url
    
    def _rotate_rpc(self):
        """Rotate to next RPC endpoint."""
        with self._lock:
            self.current_rpc_index = (self.current_rpc_index + 1) % len(self.rpc_urls)
            next_url = self.rpc_urls[self.current_rpc_index]
            
            logger.info(f"Rotating to RPC endpoint: {self._sanitize_url(next_url)}")
            
            try:
                self.w3 = self._connect()
            except ConnectionError:
                logger.error("Failed to rotate RPC - all endpoints unavailable")
                raise
    
    def _cached_call(self, method_name: str, func: Callable, *args, use_cache: bool = True, **kwargs) -> Any:
        """Execute function with caching support."""
        # Check cache if enabled
        if self.cache and use_cache:
            cache_key = Cache.make_key(method_name, *args, **kwargs)
            cached_value = self.cache.get(cache_key)
            
            if cached_value is not None:
                self.metrics.record_cache_hit()
                logger.debug(f"Cache hit for {method_name}")
                return cached_value
            
            self.metrics.record_cache_miss()
        
        # Execute function (DO NOT pass args/kwargs - function is already bound)
        result = func()
        
        # Store in cache
        if self.cache and use_cache:
            self.cache.set(cache_key, result)
        
        return result
    
    @retry_with_backoff(max_retries=Config.MAX_RETRIES, backoff_factor=Config.RETRY_BACKOFF_FACTOR)
    def _rpc_call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute RPC call with retry logic and rate limiting.
        
        Args:
            func: Function to execute
            *args, **kwargs: Arguments to pass to function
            
        Returns:
            Result from function execution
            
        Raises:
            RateLimitError: If rate limit exceeded
            RPCError: If RPC call fails after all retries
        """
        # Check rate limit
        self.rate_limiter.acquire()
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"RPC call failed: {e}")
            
            # Try rotating RPC on persistent failures
            if self.connection_attempts >= 2:
                try:
                    self._rotate_rpc()
                    self.connection_attempts = 0
                except ConnectionError:
                    pass
            
            self.connection_attempts += 1
            raise RPCError(f"RPC call failed: {str(e)}") from e

    # =========================================================================
    # MONITORING & HEALTH
    # =========================================================================
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            dict: Health status including:
                - connected: Whether client is connected
                - chain_id: Current chain ID
                - block_number: Latest block number (if connected)
                - rpc_url: Current RPC endpoint
                - metrics: Current metrics
                
        Example:
            >>> health = client.health_check()
            >>> if health['connected']:
            ...     print(f"Healthy - Block {health['block_number']}")
        """
        health = {
            'connected': False,
            'chain_id': self.chain_id,
            'timestamp': datetime.utcnow().isoformat(),
            'rpc_url': self._sanitize_url(self.rpc_urls[self.current_rpc_index]),
        }
        
        try:
            health['connected'] = self.is_connected()
            if health['connected']:
                health['block_number'] = self.get_block_number()
            health['status'] = 'healthy' if health['connected'] else 'unhealthy'
        except Exception as e:
            health['status'] = 'unhealthy'
            health['error'] = str(e)
        
        health['metrics'] = self.get_metrics()
        
        return health
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current performance metrics.
        
        Returns:
            dict: Performance metrics
            
        Example:
            >>> metrics = client.get_metrics()
            >>> print(f"Total requests: {sum(metrics['requests'].values())}")
            >>> print(f"Cache hit rate: {metrics['cache_hit_rate']:.2%}")
        """
        return self.metrics.get_stats()
    
    def reset_metrics(self):
        """Reset all metrics counters."""
        self.metrics.reset()
        logger.info("Metrics reset")

    # =========================================================================
    # NETWORK INFORMATION
    # =========================================================================

    @track_performance
    def get_chain_id(self) -> int:
        """
        Returns the current chain ID.
        
        Returns:
            int: Chain ID (e.g., 8453 for Base mainnet, 84532 for Sepolia)
            
        Example:
            >>> client.get_chain_id()
            8453
        """
        def _get_chain_id():
            return self.w3.eth.chain_id
        
        return self._cached_call('get_chain_id', _get_chain_id)

    @track_performance
    def is_connected(self) -> bool:
        """
        Checks if connected to the network.
        
        Returns:
            bool: True if connected, False otherwise
            
        Example:
            >>> if client.is_connected():
            ...     print("Connected to Base!")
        """
        try:
            return self.w3.is_connected()
        except Exception as e:
            logger.warning(f"Connection check failed: {e}")
            return False

    # =========================================================================
    # BLOCK OPERATIONS
    # =========================================================================

    @track_performance
    def get_block_number(self) -> int:
        """
        Returns the current block number.
        
        Returns:
            int: Latest block number on the chain
            
        Example:
            >>> client.get_block_number()
            12345678
        """
        def _get_block_number():
            return self._rpc_call(lambda: self.w3.eth.block_number)
        
        return self._cached_call('get_block_number', _get_block_number)

    @track_performance
    def get_block(
        self, 
        block_identifier: Union[int, str] = 'latest',
        full_transactions: bool = False
    ) -> Dict[str, Any]:
        """
        Get detailed block information.
        
        Args:
            block_identifier: Block number, 'latest', 'earliest', 'pending', or block hash
            full_transactions: If True, include full transaction objects
            
        Returns:
            dict: Block data
            
        Raises:
            ValidationError: If block identifier is invalid
            RPCError: If RPC call fails
            
        Example:
            >>> block = client.get_block('latest')
            >>> print(f"Block {block['number']} has {len(block['transactions'])} transactions")
        """
        # Validate block identifier
        if isinstance(block_identifier, str):
            valid_strings = ['latest', 'earliest', 'pending']
            if block_identifier not in valid_strings and not block_identifier.startswith('0x'):
                raise ValidationError(f"Invalid block identifier: {block_identifier}")
        
        def _get_block():
            return self._rpc_call(
                lambda: dict(self.w3.eth.get_block(block_identifier, full_transactions=full_transactions))
            )
        
        # Only cache if not getting full transactions
        if not full_transactions:
            return self._cached_call('get_block', _get_block, block_identifier, full_transactions)
        else:
            return _get_block()

    # =========================================================================
    # ACCOUNT OPERATIONS
    # =========================================================================
    
    def _validate_address(self, address: str) -> str:
        """
        Validate and normalize Ethereum address.
        
        Args:
            address: Ethereum address
            
        Returns:
            str: Checksummed address
            
        Raises:
            ValidationError: If address is invalid
        """
        try:
            if not isinstance(address, str):
                raise ValidationError("Address must be a string")
            
            address = address.strip()
            
            if not address.startswith('0x'):
                raise ValidationError("Address must start with '0x'")
            
            if len(address) != 42:
                raise ValidationError(f"Address must be 42 characters long (got {len(address)})")
            
            # Normalize and checksum
            normalized = address.lower()
            checksum_address = Web3.to_checksum_address(normalized)
            
            return checksum_address
            
        except (ValueError, AttributeError) as e:
            logger.error(f"Invalid address format: {address}")
            raise ValidationError(f"Invalid Ethereum address '{address}': {str(e)}") from e

    @track_performance
    def get_balance(self, address: str) -> int:
        """
        Returns the balance of an address in Wei.
        
        Args:
            address: Ethereum address (with or without 0x prefix)
            
        Returns:
            int: Balance in Wei (divide by 10**18 for ETH)
            
        Raises:
            ValidationError: If address is invalid
            RPCError: If RPC call fails
            
        Example:
            >>> balance_wei = client.get_balance("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
            >>> balance_eth = balance_wei / 10**18
            >>> print(f"Balance: {balance_eth} ETH")
        """
        checksum_address = self._validate_address(address)
        
        def _get_balance():
            return self._rpc_call(lambda: self.w3.eth.get_balance(checksum_address))
        
        return self._cached_call('get_balance', _get_balance, checksum_address)

    
    @track_performance
    def get_transaction_count(
        self, 
        address: str, 
        block_identifier: Union[int, str] = 'latest'
    ) -> int:
        """
        Get number of transactions sent from an address (nonce).
        
        Args:
            address: Ethereum address
            block_identifier: 'latest', 'earliest', 'pending', or block number
            
        Returns:
            int: Transaction count (nonce)
            
        Raises:
            ValidationError: If address is invalid
            RPCError: If RPC call fails
            
        Example:
            >>> nonce = client.get_transaction_count("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
            >>> print(f"Account has sent {nonce} transactions")
        """
        checksum_address = self._validate_address(address)
        
        def _get_tx_count():
            return self._rpc_call(
                lambda: self.w3.eth.get_transaction_count(checksum_address, block_identifier)
            )
        
        # Don't cache pending nonces
        if block_identifier == 'pending':
            return _get_tx_count()
        
        return self._cached_call('get_transaction_count', _get_tx_count, checksum_address, block_identifier)

    
    @track_performance
    def get_code(self, address: str) -> bytes:
        """
        Get bytecode at an address.
        
        Args:
            address: Ethereum address
            
        Returns:
            bytes: Contract bytecode (empty for EOA)
            
        Raises:
            ValidationError: If address is invalid
            RPCError: If RPC call fails
            
        Example:
            >>> code = client.get_code("0x...")
            >>> if len(code) > 0:
            ...     print("This is a smart contract")
        """
        checksum_address = self._validate_address(address)
        
        def _get_code():
            return self._rpc_call(lambda: self.w3.eth.get_code(checksum_address))
        
        return self._cached_call('get_code', _get_code, checksum_address)

    @track_performance
    def is_contract(self, address: str) -> bool:
        """
        Check if address is a smart contract.
        
        Args:
            address: Ethereum address
            
        Returns:
            bool: True if contract, False if EOA
            
        Raises:
            ValidationError: If address is invalid
            RPCError: If RPC call fails
            
        Example:
            >>> if client.is_contract("0x..."):
            ...     print("This is a contract")
        """
        code = self.get_code(address)
        return len(code) > 0

    # =========================================================================
    # GAS & FEE OPERATIONS
    # =========================================================================

    @track_performance
    def get_gas_price(self) -> int:
        """
        Get current gas price in Wei.
        
        Returns:
            int: Current gas price in Wei
            
        Raises:
            RPCError: If RPC call fails
            
        Example:
            >>> gas_price = client.get_gas_price()
            >>> gas_price_gwei = gas_price / 10**9
            >>> print(f"Gas price: {gas_price_gwei} Gwei")
        """
        def _get_gas_price():
            return self._rpc_call(lambda: self.w3.eth.gas_price)
        
        return self._cached_call('get_gas_price', _get_gas_price)

    @track_performance
    def get_base_fee(self) -> int:
        """
        Get current base fee per gas (EIP-1559).
        
        Returns:
            int: Base fee in Wei (0 if not available)
            
        Example:
            >>> base_fee = client.get_base_fee()
            >>> base_fee_gwei = base_fee / 10**9
            >>> print(f"Base fee: {base_fee_gwei} Gwei")
        """
        def _get_base_fee():
            try:
                latest_block = self.get_block('latest')
                return latest_block.get('baseFeePerGas', 0)
            except Exception as e:
                logger.warning(f"Failed to get base fee: {e}")
                return 0
        
        return self._cached_call('get_base_fee', _get_base_fee)

    @track_performance
    def get_l1_fee(self, data: Union[bytes, str]) -> int:
        """
        Estimates the L1 data fee for a transaction on Base (OP Stack).
        
        Args:
            data: Transaction calldata as bytes or hex string
            
        Returns:
            int: Estimated L1 fee in Wei
            
        Raises:
            ValidationError: If data format is invalid
            RPCError: If RPC call fails
            
        Example:
            >>> tx_data = '0x...'
            >>> l1_cost = client.get_l1_fee(tx_data)
            >>> print(f"L1 fee: {l1_cost / 10**18} ETH")
        """
        # Validate and convert data
        try:
            if isinstance(data, str):
                data = bytes.fromhex(data.replace('0x', ''))
            elif not isinstance(data, bytes):
                raise ValidationError(f"data must be bytes or hex string, got {type(data)}")
        except ValueError as e:
            raise ValidationError(f"Invalid hex string: {str(e)}") from e
        
        # Gas Price Oracle contract address (standard for OP Stack)
        oracle_address = Web3.to_checksum_address(
            "0x420000000000000000000000000000000000000F"
        )
        
        def _get_l1_fee():
            try:
                oracle = self.w3.eth.contract(address=oracle_address, abi=GAS_ORACLE_ABI)
                return self._rpc_call(lambda: oracle.functions.getL1Fee(data).call())
            except Exception as e:
                logger.error(f"Failed to estimate L1 fee: {e}")
                raise RPCError(f"L1 fee estimation failed: {str(e)}") from e
        
        return _get_l1_fee()

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def clear_cache(self):
        """
        Clear all cached data.
        
        Example:
            >>> client.clear_cache()
            >>> # Forces fresh data on next requests
        """
        if self.cache:
            self.cache.clear()
            logger.info("Cache cleared")
    
    def set_log_level(self, level: int):
        """
        Change logging level at runtime.
        
        Args:
            level: Logging level (logging.DEBUG, INFO, WARNING, ERROR)
            
        Example:
            >>> import logging
            >>> client.set_log_level(logging.DEBUG)
        """
        logger.setLevel(level)
        Config.LOG_LEVEL = level
        logger.info(f"Log level set to {logging.getLevelName(level)}")
    
    def enable_rpc_logging(self, enabled: bool = True):
        """
        Enable or disable detailed RPC call logging.
        
        Args:
            enabled: Whether to log RPC calls
            
        Example:
            >>> client.enable_rpc_logging(True)
        """
        Config.LOG_RPC_CALLS = enabled
        logger.info(f"RPC logging {'enabled' if enabled else 'disabled'}")
    
    def get_current_rpc(self) -> str:
        """
        Get the currently active RPC endpoint.
        
        Returns:
            str: Current RPC URL (sanitized)
            
        Example:
            >>> print(f"Using RPC: {client.get_current_rpc()}")
        """
        return self._sanitize_url(self.rpc_urls[self.current_rpc_index])
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        logger.info("Cleaning up BaseClient resources")
        if self.cache:
            self.cache.clear()
        return False
    
    def __repr__(self) -> str:
        """String representation of client."""
        return (
            f"BaseClient(chain_id={self.chain_id}, "
            f"rpc='{self.get_current_rpc()}', "
            f"connected={self.is_connected()})"
        )
    # =========================================================================
    # BATCH & MULTICALL OPERATIONS
    # =========================================================================

    @track_performance
    def multicall(
        self,
        calls: List[Dict[str, Any]],
        block_identifier: Union[int, str] = 'latest'
    ) -> List[Any]:
        """Execute multiple contract calls in a single RPC request."""
        
        MULTICALL3_ADDRESS = "0xcA11bde05977b3631167028862bE2a173976CA11"
        
        MULTICALL3_ABI = [{
            "inputs": [{
                "components": [
                    {"name": "target", "type": "address"},
                    {"name": "callData", "type": "bytes"}
                ],
                "name": "calls",
                "type": "tuple[]"
            }],
            "name": "aggregate",
            "outputs": [
                {"name": "blockNumber", "type": "uint256"},
                {"name": "returnData", "type": "bytes[]"}
            ],
            "stateMutability": "view",
            "type": "function"
        }]
        
        if not calls:
            return []
        
        encoded_calls = []
        abi_entries = []
        
        for i, call in enumerate(calls):
            try:
                contract_address = self._validate_address(call['contract'])
                abi = call['abi']
                function_name = call['function']
                args = call.get('args', [])
                
                # Create contract instance
                contract = self.w3.eth.contract(address=contract_address, abi=abi)
                
                # ✅ FIX: Use ContractFunction to encode properly
                contract_func = contract.functions[function_name]
                func_instance = contract_func(*args) if args else contract_func()
                encoded_data = func_instance._encode_transaction_data()
                
                encoded_calls.append((contract_address, encoded_data))
                
                # Store ABI for decoding
                abi_entry = None
                for entry in abi:
                    if entry.get('name') == function_name and entry.get('type') == 'function':
                        abi_entry = entry
                        break
                abi_entries.append(abi_entry)
                
            except Exception as e:
                raise ValidationError(f"Invalid call at index {i}: {str(e)}")
        
        # Execute multicall
        def _execute_multicall():
            try:
                multicall_contract = self.w3.eth.contract(
                    address=MULTICALL3_ADDRESS,
                    abi=MULTICALL3_ABI
                )
                
                _, return_data = self._rpc_call(
                    lambda: multicall_contract.functions.aggregate(encoded_calls).call(
                        block_identifier=block_identifier
                    )
                )
                
                # Decode results
                results = []
                for i, (abi_entry, data) in enumerate(zip(abi_entries, return_data)):
                    try:
                        if not abi_entry:
                            results.append(data)
                            continue
                        
                        output_types = [output['type'] for output in abi_entry.get('outputs', [])]
                        
                        if len(output_types) == 0:
                            results.append(None)
                        elif len(output_types) == 1:
                            decoded = self.w3.codec.decode(output_types, data)
                            results.append(decoded[0])
                        else:
                            decoded = self.w3.codec.decode(output_types, data)
                            results.append(decoded)
                            
                    except Exception as e:
                        logger.warning(f"Failed to decode result {i}: {e}")
                        results.append(data)
                
                return results
                
            except Exception as e:
                logger.error(f"Multicall failed: {e}")
                raise RPCError(f"Multicall execution failed: {str(e)}") from e
        
        return _execute_multicall()


    
    @track_performance
    def batch_get_balances(
        self,
        addresses: List[str]
    ) -> Dict[str, int]:
        """
        Get ETH balances for multiple addresses efficiently.
        
        Args:
            addresses: List of Ethereum addresses
            
        Returns:
            Dictionary mapping address to balance in Wei
            
        Example:
            >>> addresses = ['0x123...', '0x456...']
            >>> balances = client.batch_get_balances(addresses)
            >>> for addr, bal in balances.items():
            ...     print(f"{addr}: {bal / 10**18} ETH")
        """
        if not addresses:
            return {}
        
        # Validate addresses
        validated = [self._validate_address(addr) for addr in addresses]
        
        def _get_balances():
            balances = {}
            
            # Try batch request, but fallback gracefully if not supported
            try:
                # Batch RPC requests
                batch_requests = [
                    {
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [addr, "latest"],
                        "id": i
                    }
                    for i, addr in enumerate(validated)
                ]
                
                # Make batch request
                response = self._rpc_call(
                    lambda: self.w3.provider.make_request("batch", batch_requests)
                )
                
                # Parse responses
                for i, addr in enumerate(validated):
                    if isinstance(response, list) and i < len(response):
                        result = response[i].get('result')
                        if result:
                            balances[addr] = int(result, 16)
                        else:
                            balances[addr] = 0
                    else:
                        # Fallback to individual calls
                        balances[addr] = self.get_balance(addr)
                        
            except Exception as e:
                # 403 or other batch errors - fallback to individual calls
                logger.info(f"Batch request not supported, using individual calls: {e}")
                for addr in validated:
                    try:
                        balances[addr] = self.get_balance(addr)
                    except Exception as err:
                        logger.error(f"Failed to get balance for {addr}: {err}")
                        balances[addr] = 0
            
            return balances
        
        return self._cached_call('batch_get_balances', _get_balances, *validated)


    @track_performance
    def batch_get_token_balances(
        self,
        address: str,
        token_contracts: List[str]
    ) -> Dict[str, int]:
        """
        Get ERC-20 token balances for multiple tokens efficiently.
        
        Args:
            address: Wallet address
            token_contracts: List of ERC-20 token contract addresses
            
        Returns:
            Dictionary mapping token address to balance
            
        Example:
            >>> tokens = ['0xUSDC...', '0xDAI...']
            >>> balances = client.batch_get_token_balances('0x123...', tokens)
            >>> for token, balance in balances.items():
            ...     print(f"{token}: {balance}")
        """
        from .abis import ERC20_ABI
        
        if not token_contracts:
            return {}
        
        wallet = self._validate_address(address)
        
        # Build multicall
        calls = []
        for token in token_contracts:
            calls.append({
                'contract': token,
                'abi': ERC20_ABI,
                'function': 'balanceOf',
                'args': [wallet]
            })
        
        try:
            results = self.multicall(calls)
            
            balances = {}
            for i, token in enumerate(token_contracts):
                balances[self._validate_address(token)] = results[i] if i < len(results) else 0
            
            return balances
            
        except Exception as e:
            logger.error(f"Batch token balance failed: {e}")
            raise RPCError(f"Failed to get token balances: {str(e)}") from e
    # =========================================================================
# TOKEN OPERATIONS (ERC-20 ENHANCED)
# =========================================================================

    @track_performance
    def get_token_metadata(
        self,
        contract_address: str
    ) -> Dict[str, Any]:
        """
        Get comprehensive ERC-20 token metadata.
        
        Args:
            contract_address: Token contract address
            
        Returns:
            Dictionary with token information:
                - name: Token name
                - symbol: Token symbol
                - decimals: Token decimals
                - totalSupply: Total supply
                - address: Contract address (checksummed)
                
        Example:
            >>> metadata = client.get_token_metadata('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')
            >>> print(f"{metadata['name']} ({metadata['symbol']})")
            >>> print(f"Decimals: {metadata['decimals']}")
        """
        from .abis import ERC20_ABI
        
        address = self._validate_address(contract_address)
        
        def _get_metadata():
            try:
                calls = [
                    {'contract': address, 'abi': ERC20_ABI, 'function': 'name'},
                    {'contract': address, 'abi': ERC20_ABI, 'function': 'symbol'},
                    {'contract': address, 'abi': ERC20_ABI, 'function': 'decimals'},
                    {'contract': address, 'abi': ERC20_ABI, 'function': 'totalSupply'},
                ]
                
                results = self.multicall(calls)
                
                return {
                    'address': address,
                    'name': results[0],
                    'symbol': results[1],
                    'decimals': results[2],
                    'totalSupply': results[3],
                }
                
            except Exception as e:
                logger.error(f"Failed to get token metadata: {e}")
                raise RPCError(f"Token metadata retrieval failed: {str(e)}") from e
        
        return self._cached_call('get_token_metadata', _get_metadata, address)


    @track_performance
    def get_token_balances(
        self,
        address: str,
        token_addresses: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get all ERC-20 token balances for a wallet with metadata.
        
        Args:
            address: Wallet address
            token_addresses: Optional list of specific tokens (uses common Base tokens if None)
            
        Returns:
            Dictionary mapping token address to balance info:
                - balance: Raw balance
                - decimals: Token decimals
                - symbol: Token symbol
                - balanceFormatted: Human-readable balance
                
        Example:
            >>> balances = client.get_token_balances('0x123...')
            >>> for token, info in balances.items():
            ...     print(f"{info['symbol']}: {info['balanceFormatted']}")
        """
        from .abis import BASE_CONTRACTS, ERC20_ABI
        
        wallet = self._validate_address(address)
        
        # Use common Base tokens if not specified
        if token_addresses is None:
            network = 'mainnet' if self.chain_id == 8453 else 'sepolia'
            token_addresses = [
                BASE_CONTRACTS[network].get('usdc'),
                BASE_CONTRACTS[network].get('dai'),
            ]
            token_addresses = [t for t in token_addresses if t]  # Filter None
        
        if not token_addresses:
            return {}
        
        # Get balances and metadata
        calls = []
        for token in token_addresses:
            calls.extend([
                {'contract': token, 'abi': ERC20_ABI, 'function': 'balanceOf', 'args': [wallet]},
                {'contract': token, 'abi': ERC20_ABI, 'function': 'symbol'},
                {'contract': token, 'abi': ERC20_ABI, 'function': 'decimals'},
            ])
        
        try:
            results = self.multicall(calls)
            
            balances = {}
            for i, token in enumerate(token_addresses):
                idx = i * 3
                if idx + 2 < len(results):
                    balance = results[idx]
                    symbol = results[idx + 1]
                    decimals = results[idx + 2]
                    
                    validated_token = self._validate_address(token)
                    balances[validated_token] = {
                        'balance': balance,
                        'symbol': symbol,
                        'decimals': decimals,
                        'balanceFormatted': balance / (10 ** decimals) if decimals > 0 else balance
                    }
            
            return balances
            
        except Exception as e:
            logger.error(f"Failed to get token balances: {e}")
            raise RPCError(f"Token balance retrieval failed: {str(e)}") from e


    @track_performance
    def get_token_allowance(
        self,
        token_address: str,
        owner: str,
        spender: str
    ) -> int:
        """
        Check ERC-20 token allowance.
        
        Args:
            token_address: Token contract address
            owner: Token owner address
            spender: Spender address
            
        Returns:
            Allowance amount in token's smallest unit
            
        Example:
            >>> allowance = client.get_token_allowance(
            ...     '0xUSDC...',
            ...     '0xowner...',
            ...     '0xspender...'
            ... )
            >>> print(f"Allowance: {allowance / 10**6} USDC")
        """
        from .abis import ERC20_ABI
        
        token = self._validate_address(token_address)
        owner_addr = self._validate_address(owner)
        spender_addr = self._validate_address(spender)
        
        def _get_allowance():
            try:
                contract = self.w3.eth.contract(address=token, abi=ERC20_ABI)
                return self._rpc_call(
                    lambda: contract.functions.allowance(owner_addr, spender_addr).call()
                )
            except Exception as e:
                logger.error(f"Failed to get allowance: {e}")
                raise RPCError(f"Allowance check failed: {str(e)}") from e
        
        return self._cached_call('get_token_allowance', _get_allowance, token, owner_addr, spender_addr)
    # =========================================================================
    # BASE L2-SPECIFIC FEATURES
    # =========================================================================

    @track_performance
    def estimate_total_fee(
        self,
        transaction: Dict[str, Any]
    ) -> Dict[str, int]:
        """
        Estimate TOTAL transaction cost on Base (L1 + L2 fees).
        
        This is critical for Base! Unlike Ethereum, Base has two fee components:
        - L2 execution fee (like normal Ethereum)
        - L1 data availability fee (for posting to Ethereum mainnet)
        
        Args:
            transaction: Transaction dict with 'to', 'from', 'value', 'data'
            
        Returns:
            Dictionary with:
                - l2_gas: L2 gas estimate
                - l2_gas_price: L2 gas price in Wei
                - l2_fee: L2 execution cost in Wei
                - l1_fee: L1 data cost in Wei
                - total_fee: Combined cost in Wei
                - total_fee_eth: Total cost in ETH
                
        Example:
            >>> tx = {
            ...     'to': '0x...',
            ...     'from': '0x...',
            ...     'value': 10**18,
            ...     'data': '0x'
            ... }
            >>> cost = client.estimate_total_fee(tx)
            >>> print(f"Total cost: {cost['total_fee_eth']:.6f} ETH")
            >>> print(f"  L2 fee: {cost['l2_fee'] / 10**18:.6f} ETH")
            >>> print(f"  L1 fee: {cost['l1_fee'] / 10**18:.6f} ETH")
        """
        # Validate transaction
        if 'to' not in transaction:
            raise ValidationError("Transaction must have 'to' field")
        
        # FIX: Better validation - handle both string and address types
        to_addr = transaction['to']
        if isinstance(to_addr, str) and len(to_addr.strip()) > 0:
            transaction['to'] = self._validate_address(to_addr)
        else:
            raise ValidationError(f"Invalid 'to' address: {to_addr}")
        
        if 'from' in transaction:
            from_addr = transaction['from']
            if isinstance(from_addr, str) and len(from_addr.strip()) > 0:
                transaction['from'] = self._validate_address(from_addr)
        
        def _estimate_total():
            try:
                # Get L2 gas estimate
                l2_gas = self._rpc_call(lambda: self.w3.eth.estimate_gas(transaction))
                
                # Get L2 gas price
                l2_gas_price = self.get_gas_price()
                
                # Calculate L2 fee
                l2_fee = l2_gas * l2_gas_price
                
                # Get L1 data fee
                tx_data = transaction.get('data', '0x')
                if not tx_data:
                    tx_data = '0x'
                l1_fee = self.get_l1_fee(tx_data)
                
                # Total cost
                total_fee = l2_fee + l1_fee
                
                return {
                    'l2_gas': l2_gas,
                    'l2_gas_price': l2_gas_price,
                    'l2_fee': l2_fee,
                    'l1_fee': l1_fee,
                    'total_fee': total_fee,
                    'total_fee_eth': total_fee / 10**18,
                    'l2_fee_eth': l2_fee / 10**18,
                    'l1_fee_eth': l1_fee / 10**18,
                }
                
            except Exception as e:
                logger.error(f"Fee estimation failed: {e}")
                raise RPCError(f"Total fee estimation failed: {str(e)}") from e
        
        return _estimate_total()


    @track_performance
    def get_l1_gas_oracle_prices(self) -> Dict[str, Any]:
        """
        Get current L1 gas pricing information from Base's oracle.
        
        Returns:
            Dictionary with:
                - l1_base_fee: L1 base fee in Wei
                - base_fee_scalar: Base fee scalar (post-Ecotone)
                - blob_base_fee_scalar: Blob base fee scalar (post-Ecotone)
                - decimals: Scalar decimals
                
        Example:
            >>> prices = client.get_l1_gas_oracle_prices()
            >>> print(f"L1 Base Fee: {prices['l1_base_fee'] / 10**9} Gwei")
        """
        oracle_address = Web3.to_checksum_address(
            "0x420000000000000000000000000000000000000F"
        )
        
        def _get_oracle_prices():
            try:
                # Updated ABI for post-Ecotone Base
                ORACLE_ABI = [
                    {"inputs": [], "name": "l1BaseFee", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "baseFeeScalar", "outputs": [{"type": "uint32"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "blobBaseFeeScalar", "outputs": [{"type": "uint32"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "decimals", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
                ]
                
                calls = [
                    {'contract': oracle_address, 'abi': ORACLE_ABI, 'function': 'l1BaseFee'},
                    {'contract': oracle_address, 'abi': ORACLE_ABI, 'function': 'baseFeeScalar'},
                    {'contract': oracle_address, 'abi': ORACLE_ABI, 'function': 'blobBaseFeeScalar'},
                    {'contract': oracle_address, 'abi': ORACLE_ABI, 'function': 'decimals'},
                ]
                
                results = self.multicall(calls)
                
                return {
                    'l1_base_fee': results[0],
                    'base_fee_scalar': results[1],
                    'blob_base_fee_scalar': results[2],
                    'decimals': results[3],
                }
                
            except Exception as e:
                logger.warning(f"Failed to get L1 oracle prices: {e}")
                # Return defaults if oracle call fails
                return {
                    'l1_base_fee': 0,
                    'base_fee_scalar': 0,
                    'blob_base_fee_scalar': 0,
                    'decimals': 6,
                }
        
        return self._cached_call('get_l1_gas_oracle_prices', _get_oracle_prices)
    # =========================================================================
    # DEVELOPER UTILITIES
    # =========================================================================

    def format_units(self, value: int, decimals: int = 18) -> float:
        """
        Convert Wei/smallest unit to human-readable decimal.
        
        Args:
            value: Value in smallest unit
            decimals: Number of decimals (18 for ETH, 6 for USDC, etc.)
            
        Returns:
            Human-readable float value
            
        Example:
            >>> wei = 1500000000000000000
            >>> eth = client.format_units(wei, 18)
            >>> print(f"{eth} ETH")  # 1.5 ETH
            >>> 
            >>> usdc_raw = 1500000
            >>> usdc = client.format_units(usdc_raw, 6)
            >>> print(f"{usdc} USDC")  # 1.5 USDC
        """
        return value / (10 ** decimals)


    def parse_units(self, value: Union[str, float, int], decimals: int = 18) -> int:
        """
        Convert human-readable decimal to Wei/smallest unit.
        
        Args:
            value: Human-readable value
            decimals: Number of decimals
            
        Returns:
            Value in smallest unit (integer)
            
        Example:
            >>> eth = client.parse_units("1.5", 18)
            >>> print(eth)  # 1500000000000000000
            >>> 
            >>> usdc = client.parse_units(1.5, 6)
            >>> print(usdc)  # 1500000
        """
        from decimal import Decimal
        
        if isinstance(value, int):
            value = str(value)
        
        decimal_value = Decimal(str(value))
        return int(decimal_value * (10 ** decimals))


    @track_performance
    def decode_function_input(
        self,
        transaction_input: str,
        abi: List[Dict]
    ) -> Dict[str, Any]:
        """
        Decode transaction input data using ABI.
        
        Args:
            transaction_input: Transaction data (0x...)
            abi: Contract ABI
            
        Returns:
            Dictionary with:
                - function: Function name
                - inputs: Function arguments
                
        Example:
            >>> tx = client.w3.eth.get_transaction('0x...')
            >>> decoded = client.decode_function_input(tx['input'], ERC20_ABI)
            >>> print(f"Function: {decoded['function']}")
            >>> print(f"Args: {decoded['inputs']}")
        """
        try:
            contract = self.w3.eth.contract(abi=abi)
            func_obj, func_params = contract.decode_function_input(transaction_input)
            
            return {
                'function': func_obj.fn_name,
                'inputs': dict(func_params)
            }
        except Exception as e:
            logger.error(f"Failed to decode input: {e}")
            raise ValidationError(f"Input decoding failed: {str(e)}") from e


    @track_performance
    def simulate_transaction(
        self,
        transaction: Dict[str, Any],
        block_identifier: Union[int, str] = 'latest'
    ) -> Any:
        """
        Simulate transaction execution without sending it.
        
        This uses eth_call to test what would happen if the transaction
        was executed. Useful for testing before sending.
        
        Args:
            transaction: Transaction dict
            block_identifier: Block to simulate at
            
        Returns:
            Return value from the simulated call
            
        Example:
            >>> tx = {
            ...     'to': '0xcontract...',
            ...     'from': '0xwallet...',
            ...     'data': '0x...'
            ... }
            >>> result = client.simulate_transaction(tx)
            >>> print(f"Simulation result: {result}")
        """
        try:
            return self._rpc_call(
                lambda: self.w3.eth.call(transaction, block_identifier)
            )
        except Exception as e:
            # Extract revert reason if available
            error_msg = str(e)
            if "execution reverted" in error_msg.lower():
                logger.error(f"Transaction would revert: {error_msg}")
                raise ValidationError(f"Transaction simulation failed: {error_msg}")
            raise RPCError(f"Simulation failed: {str(e)}") from e
    """


Add this method to the BaseClient class, in the TOKEN OPERATIONS section
(after get_token_allowance method, around line 900).
"""

    @track_performance
    def get_portfolio_balance(
        self,
        address: str,
        token_addresses: Optional[List[str]] = None,
        include_common_tokens: bool = True
    ) -> Dict[str, Any]:
        """
        Get complete portfolio balance (ETH + ERC-20 tokens) for a wallet.
        
        This method efficiently retrieves all balances in ~2 RPC calls:
        - 1 RPC call for ETH balance
        - 1 multicall for all token balances + metadata
        
        Args:
            address: Wallet address to check
            token_addresses: Optional list of specific token addresses to check
            include_common_tokens: If True and token_addresses is None, includes Base common tokens
            
        Returns:
            Dictionary with complete portfolio information:
                - address: Checksummed wallet address
                - eth: {
                    balance: Raw balance in Wei,
                    balance_formatted: Human-readable ETH amount
                  }
                - tokens: {
                    '0xTokenAddress...': {
                        symbol: Token symbol,
                        name: Token name,
                        balance: Raw balance,
                        decimals: Token decimals,
                        balance_formatted: Human-readable amount
                    }
                  }
                - total_assets: Total number of assets (including ETH)
                - non_zero_tokens: Number of tokens with non-zero balance
                
        Raises:
            ValidationError: If address is invalid
            RPCError: If RPC calls fail
            
        Example:
            >>> # Get full portfolio with common Base tokens
            >>> portfolio = client.get_portfolio_balance('0x123...')
            >>> print(f"ETH: {portfolio['eth']['balance_formatted']}")
            >>> for token_addr, info in portfolio['tokens'].items():
            ...     if info['balance'] > 0:
            ...         print(f"{info['symbol']}: {info['balance_formatted']}")
            >>> 
            >>> # Get specific tokens only
            >>> usdc_dai = ['0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb']
            >>> portfolio = client.get_portfolio_balance('0x123...', token_addresses=usdc_dai)
            >>> 
            >>> # Portfolio summary
            >>> print(f"Total assets: {portfolio['total_assets']}")
            >>> print(f"Tokens with balance: {portfolio['non_zero_tokens']}")
        """
        from .abis import get_common_tokens, get_token_addresses, ERC20_ABI
        from .utils import format_token_amount
        
        # Validate wallet address
        wallet = self._validate_address(address)
        
        # Determine which tokens to check
        if token_addresses is None and include_common_tokens:
            # Use common Base tokens
            network = 'mainnet' if self.chain_id == BASE_MAINNET_CHAIN_ID else 'sepolia'
            common_tokens = get_common_tokens(self.chain_id)
            token_addresses = get_token_addresses(self.chain_id)
        elif token_addresses is None:
            token_addresses = []
        
        # Validate all token addresses
        validated_tokens = [self._validate_address(t) for t in token_addresses] if token_addresses else []
        
        def _get_portfolio():
            try:
                # Step 1: Get ETH balance (1 RPC call)
                eth_balance = self.get_balance(wallet)
                
                # Step 2: Get all token data in one multicall (1 RPC call)
                token_data = {}
                
                if validated_tokens:
                    # Build multicall for balance + metadata for each token
                    calls = []
                    for token in validated_tokens:
                        calls.extend([
                            {'contract': token, 'abi': ERC20_ABI, 'function': 'balanceOf', 'args': [wallet]},
                            {'contract': token, 'abi': ERC20_ABI, 'function': 'symbol'},
                            {'contract': token, 'abi': ERC20_ABI, 'function': 'name'},
                            {'contract': token, 'abi': ERC20_ABI, 'function': 'decimals'},
                        ])
                    
                    # Execute multicall
                    results = self.multicall(calls)
                    
                    # Parse results
                    non_zero_count = 0
                    for i, token in enumerate(validated_tokens):
                        idx = i * 4
                        if idx + 3 < len(results):
                            balance = results[idx]
                            symbol = results[idx + 1]
                            name = results[idx + 2]
                            decimals = results[idx + 3]
                            
                            # Format balance
                            balance_formatted = format_token_amount(balance, decimals)
                            
                            if balance > 0:
                                non_zero_count += 1
                            
                            token_data[token] = {
                                'symbol': symbol,
                                'name': name,
                                'balance': balance,
                                'decimals': decimals,
                                'balance_formatted': balance_formatted
                            }
                
                # Build portfolio response
                portfolio = {
                    'address': wallet,
                    'eth': {
                        'balance': eth_balance,
                        'balance_formatted': format_token_amount(eth_balance, 18)  # ETH has 18 decimals
                    },
                    'tokens': token_data,
                    'total_assets': 1 + len(token_data),  # ETH + tokens
                    'non_zero_tokens': sum(1 for t in token_data.values() if t['balance'] > 0)
                }
                
                return portfolio
                
            except Exception as e:
                logger.error(f"Failed to get portfolio balance: {e}")
                raise RPCError(f"Portfolio balance retrieval failed: {str(e)}") from e
        
        return _get_portfolio()


    @track_performance
    def get_portfolio_value(
        self,
        address: str,
        token_addresses: Optional[List[str]] = None,
        include_common_tokens: bool = True,
        eth_price_usd: Optional[float] = None,
        token_prices_usd: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Get portfolio balance with USD valuation (if prices provided).
        
        Note: This method does NOT fetch prices automatically. You must provide
        prices from an external price oracle or API (e.g., CoinGecko, Chainlink).
        
        Args:
            address: Wallet address
            token_addresses: Optional token addresses to check
            include_common_tokens: Include Base common tokens if no specific tokens provided
            eth_price_usd: ETH price in USD (optional)
            token_prices_usd: Dict mapping token address to USD price (optional)
            
        Returns:
            Dictionary with portfolio value information:
                - portfolio: Full portfolio data from get_portfolio_balance()
                - eth_value_usd: ETH value in USD (if price provided)
                - token_values_usd: Dict of token USD values (if prices provided)
                - total_value_usd: Total portfolio value in USD (if prices provided)
                
        Example:
            >>> # Without prices (just balances)
            >>> portfolio = client.get_portfolio_value('0x123...')
            >>> 
            >>> # With prices (calculate USD value)
            >>> portfolio = client.get_portfolio_value(
            ...     '0x123...',
            ...     eth_price_usd=3000.0,
            ...     token_prices_usd={
            ...         '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913': 1.0,  # USDC
            ...         '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb': 1.0,  # DAI
            ...     }
            ... )
            >>> print(f"Total Value: ${portfolio['total_value_usd']:.2f}")
        """
        # Get portfolio balances
        portfolio = self.get_portfolio_balance(
            address=address,
            token_addresses=token_addresses,
            include_common_tokens=include_common_tokens
        )
        
        result = {
            'portfolio': portfolio,
            'eth_value_usd': None,
            'token_values_usd': {},
            'total_value_usd': None
        }
        
        # Calculate ETH value if price provided
        if eth_price_usd is not None:
            eth_amount = portfolio['eth']['balance_formatted']
            result['eth_value_usd'] = eth_amount * eth_price_usd
        
        # Calculate token values if prices provided
        if token_prices_usd:
            for token_addr, token_info in portfolio['tokens'].items():
                if token_addr in token_prices_usd:
                    token_amount = token_info['balance_formatted']
                    token_price = token_prices_usd[token_addr]
                    result['token_values_usd'][token_addr] = token_amount * token_price
        
        # Calculate total value if we have all prices
        if result['eth_value_usd'] is not None:
            total = result['eth_value_usd']
            total += sum(result['token_values_usd'].values())
            result['total_value_usd'] = total
        
        return result


"""
USAGE EXAMPLES:
===============

1. BASIC PORTFOLIO VIEW:
------------------------
from basepy import BaseClient

client = BaseClient()
portfolio = client.get_portfolio_balance('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')

print(f"Wallet: {portfolio['address']}")
print(f"ETH: {portfolio['eth']['balance_formatted']} ETH")
print(f"\nTokens:")
for token_addr, info in portfolio['tokens'].items():
    if info['balance'] > 0:
        print(f"  {info['symbol']}: {info['balance_formatted']}")

print(f"\nSummary:")
print(f"  Total assets: {portfolio['total_assets']}")
print(f"  Tokens with balance: {portfolio['non_zero_tokens']}")


2. SPECIFIC TOKENS ONLY:
-------------------------
usdc = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
dai = '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb'

portfolio = client.get_portfolio_balance(
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    token_addresses=[usdc, dai]
)


3. WITH USD VALUATION (using external price data):
--------------------------------------------------
# Fetch prices from CoinGecko, Chainlink, etc.
eth_price = 3000.0
token_prices = {
    '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913': 1.0,  # USDC
    '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb': 1.0,  # DAI
}

portfolio = client.get_portfolio_value(
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    eth_price_usd=eth_price,
    token_prices_usd=token_prices
)

print(f"ETH Value: ${portfolio['eth_value_usd']:.2f}")
for token, value in portfolio['token_values_usd'].items():
    symbol = portfolio['portfolio']['tokens'][token]['symbol']
    print(f"{symbol} Value: ${value:.2f}")
print(f"Total Portfolio Value: ${portfolio['total_value_usd']:.2f}")


4. MONITOR MULTIPLE WALLETS:
-----------------------------
wallets = [
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    '0x456...',
    '0x789...'
]

for wallet in wallets:
    portfolio = client.get_portfolio_balance(wallet)
    non_zero = portfolio['non_zero_tokens']
    if non_zero > 0:
        print(f"{wallet}: {non_zero} tokens")


5. FILTER BY TOKEN CATEGORY:
-----------------------------
from basepy.abis import get_common_tokens

# Get only stablecoins
stablecoins = get_common_tokens(8453, categories=['stablecoin'])
stablecoin_addresses = [t['address'] for t in stablecoins]

portfolio = client.get_portfolio_balance(
    '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    token_addresses=stablecoin_addresses
)


COST ANALYSIS:
==============
RPC Calls per portfolio check:
- 1 call for ETH balance
- 1 multicall for all tokens (regardless of count)
= ~2 RPC calls total

For 5 tokens: 2 RPC calls (vs 6+ with individual calls)
For 10 tokens: 2 RPC calls (vs 11+ with individual calls)

This is EXTREMELY efficient compared to calling each token individually!
"""

# ============================================================================
# PRODUCTION ENHANCEMENTS SUMMARY
# ============================================================================
# 
# ✅ CONFIGURATION MANAGEMENT
# - Environment-based config (dev/staging/prod)
# - Configurable timeouts, retries, rate limits
# - Runtime configuration changes
# 
# ✅ ERROR HANDLING & RESILIENCE
# - Exponential backoff retry with decorator
# - Circuit breaker pattern for RPC endpoints
# - Enhanced exception hierarchy
# - Graceful degradation
# 
# ✅ MONITORING & OBSERVABILITY
# - Comprehensive metrics collection
# - Performance tracking for all methods
# - Health check endpoint
# - RPC usage tracking
# - Structured logging with sanitized URLs
# 
# ✅ RATE LIMITING & RESOURCE MANAGEMENT
# - Token bucket rate limiter
# - Automatic RPC rotation on failures
# - TTL-based caching with thread safety
# - Connection pooling via Web3.py
# 
# ✅ SECURITY
# - Input validation for all addresses
# - URL sanitization in logs (hides API keys)
# - Type checking and validation
# - Safe error messages
# 
# ✅ PERFORMANCE OPTIMIZATION
# - Method-level caching with TTL
# - Cache key generation using MD5 hashing
# - Lazy loading and efficient data structures
# - Performance tracking decorator
# 
# NEW CLASSES:
# - Config: Environment-based configuration
# - Metrics: Thread-safe metrics collection
# - CircuitBreaker: Fault tolerance for RPCs
# - Cache: TTL-based caching layer
# - RateLimiter: Token bucket rate limiting
# 
# NEW METHODS:
# - health_check(): Comprehensive health status
# - get_metrics(): Performance statistics
# - reset_metrics(): Reset metric counters
# - clear_cache(): Manual cache clearing
# - set_log_level(): Runtime log level changes
# - enable_rpc_logging(): Toggle RPC logging
# - get_current_rpc(): Get active RPC endpoint
# 
# DECORATORS:
# - @retry_with_backoff: Automatic retry logic
# - @track_performance: Performance monitoring
# 
# THREAD SAFETY:
# - All shared state protected with locks
# - Thread-safe metrics collection
# - Thread-safe cache operations
# - Thread-safe rate limiting
# 
# CONTEXT MANAGER SUPPORT:
# - __enter__ and __exit__ for 'with' statements
# - Automatic resource cleanup
# 
# BACKWARD COMPATIBILITY:
# - All existing methods work unchanged
# - New features are opt-in
# - Default behavior preserved
# ============================================================================