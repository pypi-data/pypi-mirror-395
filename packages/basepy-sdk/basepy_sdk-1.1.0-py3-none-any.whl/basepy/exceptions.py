"""
Custom exceptions for BasePy SDK.
Provides a comprehensive exception hierarchy for better error handling.
"""


class BasePyError(Exception):
    """
    Base exception for BasePy SDK.
    All SDK exceptions inherit from this class.
    """
    
    def __init__(self, message: str = None, details: dict = None):
        """
        Initialize base exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message or "An error occurred in BasePy SDK"
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        """String representation of the error."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message
    
    def to_dict(self):
        """Convert exception to dictionary for logging/serialization."""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'details': self.details
        }


class ConnectionError(BasePyError):
    """Raised when connection to Base RPC fails."""
    
    def __init__(self, message: str = None, rpc_url: str = None, attempt: int = None):
        """
        Initialize connection error.
        
        Args:
            message: Error message
            rpc_url: RPC URL that failed
            attempt: Connection attempt number
        """
        details = {}
        if rpc_url:
            details['rpc_url'] = rpc_url
        if attempt:
            details['attempt'] = attempt
        
        super().__init__(
            message or "Failed to connect to Base RPC",
            details
        )
        self.rpc_url = rpc_url
        self.attempt = attempt


class RPCError(BasePyError):
    """Raised when an RPC call fails."""
    
    def __init__(self, message: str = None, method: str = None, error_code: int = None):
        """
        Initialize RPC error.
        
        Args:
            message: Error message
            method: RPC method that failed
            error_code: RPC error code
        """
        details = {}
        if method:
            details['method'] = method
        if error_code:
            details['error_code'] = error_code
        
        super().__init__(
            message or "RPC call failed",
            details
        )
        self.method = method
        self.error_code = error_code


class ValidationError(BasePyError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str = None, field: str = None, value: any = None):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            field: Field name that failed validation
            value: Invalid value
        """
        details = {}
        if field:
            details['field'] = field
        if value is not None:
            details['value'] = str(value)
        
        super().__init__(
            message or "Validation failed",
            details
        )
        self.field = field
        self.value = value


class RateLimitError(BasePyError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = None, limit: int = None, window: int = None, retry_after: float = None):
        """
        Initialize rate limit error.
        
        Args:
            message: Error message
            limit: Rate limit (requests per window)
            window: Time window in seconds
            retry_after: Seconds until retry is allowed
        """
        details = {}
        if limit:
            details['limit'] = limit
        if window:
            details['window'] = window
        if retry_after:
            details['retry_after'] = retry_after
        
        super().__init__(
            message or "Rate limit exceeded",
            details
        )
        self.limit = limit
        self.window = window
        self.retry_after = retry_after


class CircuitBreakerOpenError(BasePyError):
    """Raised when circuit breaker is open and blocking requests."""
    
    def __init__(self, message: str = None, rpc_url: str = None, retry_after: int = None):
        """
        Initialize circuit breaker error.
        
        Args:
            message: Error message
            rpc_url: RPC URL with open circuit
            retry_after: Seconds until circuit may close
        """
        details = {}
        if rpc_url:
            details['rpc_url'] = rpc_url
        if retry_after:
            details['retry_after'] = retry_after
        
        super().__init__(
            message or "Circuit breaker is open",
            details
        )
        self.rpc_url = rpc_url
        self.retry_after = retry_after


class WalletError(BasePyError):
    """Raised when there is an issue with wallet operations."""
    
    def __init__(self, message: str = None, address: str = None):
        """
        Initialize wallet error.
        
        Args:
            message: Error message
            address: Wallet address
        """
        details = {}
        if address:
            details['address'] = address
        
        super().__init__(
            message or "Wallet operation failed",
            details
        )
        self.address = address


class TransactionError(BasePyError):
    """Raised when a transaction fails."""
    
    def __init__(self, message: str = None, tx_hash: str = None, reason: str = None):
        """
        Initialize transaction error.
        
        Args:
            message: Error message
            tx_hash: Transaction hash
            reason: Failure reason
        """
        details = {}
        if tx_hash:
            details['tx_hash'] = tx_hash
        if reason:
            details['reason'] = reason
        
        super().__init__(
            message or "Transaction failed",
            details
        )
        self.tx_hash = tx_hash
        self.reason = reason


class ContractError(BasePyError):
    """Raised when a smart contract interaction fails."""
    
    def __init__(self, message: str = None, contract_address: str = None, function: str = None):
        """
        Initialize contract error.
        
        Args:
            message: Error message
            contract_address: Contract address
            function: Function name that failed
        """
        details = {}
        if contract_address:
            details['contract_address'] = contract_address
        if function:
            details['function'] = function
        
        super().__init__(
            message or "Contract interaction failed",
            details
        )
        self.contract_address = contract_address
        self.function = function


class InsufficientFundsError(TransactionError):
    """Raised when account has insufficient funds for transaction."""
    
    def __init__(self, message: str = None, required: int = None, available: int = None, address: str = None):
        """
        Initialize insufficient funds error.
        
        Args:
            message: Error message
            required: Required amount in Wei
            available: Available balance in Wei
            address: Account address
        """
        details = {}
        if required is not None:
            details['required'] = required
            details['required_eth'] = required / 10**18
        if available is not None:
            details['available'] = available
            details['available_eth'] = available / 10**18
        if address:
            details['address'] = address
        
        msg = message or "Insufficient funds for transaction"
        if required and available:
            shortage = required - available
            msg += f" (short by {shortage / 10**18:.6f} ETH)"
        
        super().__init__(msg)
        self.details.update(details)
        self.required = required
        self.available = available
        self.address = address


class GasEstimationError(TransactionError):
    """Raised when gas estimation fails."""
    
    def __init__(self, message: str = None, transaction: dict = None, reason: str = None):
        """
        Initialize gas estimation error.
        
        Args:
            message: Error message
            transaction: Transaction data
            reason: Estimation failure reason
        """
        details = {}
        if transaction:
            details['transaction'] = {
                'to': transaction.get('to'),
                'value': transaction.get('value'),
                'data': transaction.get('data', '')[:20] + '...' if transaction.get('data') else None
            }
        if reason:
            details['reason'] = reason
        
        super().__init__(
            message or "Gas estimation failed",
            reason=reason
        )
        self.details.update(details)
        self.transaction = transaction


class SignatureError(WalletError):
    """Raised when transaction signing fails."""
    
    def __init__(self, message: str = None, transaction: dict = None):
        """
        Initialize signature error.
        
        Args:
            message: Error message
            transaction: Transaction that failed to sign
        """
        details = {}
        if transaction:
            details['transaction'] = {
                'to': transaction.get('to'),
                'value': transaction.get('value'),
                'nonce': transaction.get('nonce')
            }
        
        super().__init__(
            message or "Failed to sign transaction"
        )
        self.details.update(details)
        self.transaction = transaction


class InvalidAddressError(ValidationError):
    """Raised when an Ethereum address is invalid."""
    
    def __init__(self, message: str = None, address: str = None):
        """
        Initialize invalid address error.
        
        Args:
            message: Error message
            address: Invalid address
        """
        super().__init__(
            message or f"Invalid Ethereum address: {address}",
            field='address',
            value=address
        )
        self.address = address


class InvalidChainIdError(ValidationError):
    """Raised when chain ID is invalid."""
    
    def __init__(self, message: str = None, chain_id: int = None, expected: list = None):
        """
        Initialize invalid chain ID error.
        
        Args:
            message: Error message
            chain_id: Invalid chain ID
            expected: List of valid chain IDs
        """
        details = {}
        if expected:
            details['expected'] = expected
        
        super().__init__(
            message or f"Invalid chain ID: {chain_id}",
            field='chain_id',
            value=chain_id
        )
        self.details.update(details)
        self.chain_id = chain_id
        self.expected = expected


class TimeoutError(BasePyError):
    """Raised when an operation times out."""
    
    def __init__(self, message: str = None, operation: str = None, timeout: float = None):
        """
        Initialize timeout error.
        
        Args:
            message: Error message
            operation: Operation that timed out
            timeout: Timeout duration in seconds
        """
        details = {}
        if operation:
            details['operation'] = operation
        if timeout:
            details['timeout'] = timeout
        
        super().__init__(
            message or f"Operation timed out after {timeout}s",
            details
        )
        self.operation = operation
        self.timeout = timeout


class CacheError(BasePyError):
    """Raised when cache operation fails."""
    
    def __init__(self, message: str = None, key: str = None, operation: str = None):
        """
        Initialize cache error.
        
        Args:
            message: Error message
            key: Cache key
            operation: Cache operation (get, set, delete)
        """
        details = {}
        if key:
            details['key'] = key
        if operation:
            details['operation'] = operation
        
        super().__init__(
            message or "Cache operation failed",
            details
        )
        self.key = key
        self.operation = operation


# Exception hierarchy:
# BasePyError (root)
# ├── ConnectionError
# ├── RPCError
# ├── ValidationError
# │   ├── InvalidAddressError
# │   └── InvalidChainIdError
# ├── RateLimitError
# ├── CircuitBreakerOpenError
# ├── TimeoutError
# ├── CacheError
# ├── WalletError
# │   └── SignatureError
# ├── TransactionError
# │   ├── InsufficientFundsError
# │   └── GasEstimationError
# └── ContractError