"""
Token standard implementations for Base blockchain.

Includes:
- ERC20: Complete ERC-20 token standard implementation
- Portfolio and balance tracking methods
- Batch operations for efficiency
- Comprehensive metadata retrieval

Production-ready features:
- Full error handling
- Type hints and validation
- Efficient multicall support
- Zero-cost local operations where possible
"""

from typing import Dict, Any, Optional, List
from .contracts import Contract
from .abis import ERC20_ABI
from .exceptions import ContractError, ValidationError
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ERC20 TOKEN STANDARD (Enhanced)
# ============================================================================

class ERC20(Contract):
    """
    Enhanced ERC-20 token standard implementation.
    
    Features:
    - All standard ERC-20 functions (read and write)
    - Complete metadata retrieval in one call
    - Portfolio-ready balance information
    - Allowance management
    - Error handling and validation
    
    Example:
        >>> from basepy import BaseClient, ERC20
        >>> client = BaseClient()
        >>> 
        >>> # Initialize token contract
        >>> usdc = ERC20(client, "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
        >>> 
        >>> # Get balance
        >>> balance = usdc.balance_of("0x123...")
        >>> 
        >>> # Get complete info
        >>> info = usdc.get_full_info("0x123...")
        >>> print(f"{info['balance_formatted']} {info['symbol']}")
    """
    
    def __init__(self, client, address: str):
        """
        Initialize ERC20 token contract.
        
        Args:
            client: BaseClient instance
            address: Token contract address
        """
        super().__init__(client, address, ERC20_ABI)
        self._metadata_cache = None
    
    # =========================================================================
    # STANDARD ERC-20 READ FUNCTIONS
    # =========================================================================
    
    def balance_of(self, address: str) -> int:
        """
        Get token balance for an address.
        
        Args:
            address: Wallet address
            
        Returns:
            Token balance in smallest unit (raw amount)
            
        Example:
            >>> balance = token.balance_of("0x123...")
            >>> print(f"Raw balance: {balance}")
        """
        return self.call("balanceOf", address)
    
    def get_decimals(self) -> int:
        """
        Get token decimals.
        
        Returns:
            Number of decimals (e.g., 18 for most tokens, 6 for USDC)
            
        Example:
            >>> decimals = token.get_decimals()
            >>> print(f"Token has {decimals} decimals")
        """
        return self.call("decimals")
    
    def get_symbol(self) -> str:
        """
        Get token symbol.
        
        Returns:
            Token symbol (e.g., 'USDC', 'DAI')
            
        Example:
            >>> symbol = token.get_symbol()
            >>> print(f"Token: {symbol}")
        """
        return self.call("symbol")
    
    def get_name(self) -> Optional[str]:
        """
        Get token name.
        
        Returns:
            Token name (e.g., 'USD Coin') or None if call fails
            
        Example:
            >>> name = token.get_name()
            >>> print(f"Full name: {name}")
        """
        try:
            return self.call("name")
        except Exception as e:
            logger.warning(f"Failed to get token name: {e}")
            return None
    
    def get_total_supply(self) -> Optional[int]:
        """
        Get total token supply.
        
        Returns:
            Total supply in smallest unit or None if call fails
            
        Example:
            >>> supply = token.get_total_supply()
            >>> decimals = token.get_decimals()
            >>> print(f"Supply: {supply / 10**decimals}")
        """
        try:
            return self.call("totalSupply")
        except Exception as e:
            logger.warning(f"Failed to get total supply: {e}")
            return None
    
    def allowance(self, owner: str, spender: str) -> int:
        """
        Get allowance amount.
        
        Args:
            owner: Token owner address
            spender: Spender address
            
        Returns:
            Allowance amount in smallest unit
            
        Example:
            >>> allowance = token.allowance("0xowner...", "0xspender...")
            >>> print(f"Approved: {allowance}")
        """
        return self.call("allowance", owner, spender)
    
    # =========================================================================
    # STANDARD ERC-20 WRITE FUNCTIONS
    # =========================================================================
    
    def transfer(
        self,
        wallet,
        to_address: str,
        amount: int,
        gas: Optional[int] = None
    ) -> str:
        """
        Transfer tokens to an address.
        
        Args:
            wallet: Wallet instance (from basepy.Wallet)
            to_address: Recipient address
            amount: Amount in smallest unit (raw amount)
            gas: Optional gas limit
            
        Returns:
            Transaction hash
            
        Example:
            >>> # Transfer 100 USDC (6 decimals)
            >>> amount = 100 * 10**6
            >>> tx_hash = token.transfer(wallet, "0xRecipient...", amount)
        """
        return self.transact(wallet, "transfer", to_address, amount, gas=gas)
    
    def approve(
        self,
        wallet,
        spender_address: str,
        amount: int,
        gas: Optional[int] = None
    ) -> str:
        """
        Approve spender to spend tokens.
        
        Args:
            wallet: Wallet instance
            spender_address: Spender address (e.g., DEX contract)
            amount: Amount to approve in smallest unit
            gas: Optional gas limit
            
        Returns:
            Transaction hash
            
        Example:
            >>> # Approve unlimited USDC
            >>> max_uint = 2**256 - 1
            >>> tx_hash = token.approve(wallet, "0xDEX...", max_uint)
        """
        return self.transact(wallet, "approve", spender_address, amount, gas=gas)
    
    def transfer_from(
        self,
        wallet,
        from_address: str,
        to_address: str,
        amount: int,
        gas: Optional[int] = None
    ) -> str:
        """
        Transfer tokens from one address to another (requires approval).
        
        Args:
            wallet: Wallet instance (must be approved spender)
            from_address: Token owner address
            to_address: Recipient address
            amount: Amount in smallest unit
            gas: Optional gas limit
            
        Returns:
            Transaction hash
            
        Example:
            >>> tx_hash = token.transfer_from(
            ...     wallet,
            ...     "0xOwner...",
            ...     "0xRecipient...",
            ...     amount
            ... )
        """
        return self.transact(
            wallet,
            "transferFrom",
            from_address,
            to_address,
            amount,
            gas=gas
        )
    
    # =========================================================================
    # ENHANCED METADATA METHODS (NEW)
    # =========================================================================
    
    def get_metadata(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get complete token metadata in ONE efficient call.
        
        Uses multicall to fetch all metadata in a single RPC request.
        
        Args:
            use_cache: Use cached metadata if available
            
        Returns:
            Dictionary with:
                - address: Token contract address
                - name: Token name
                - symbol: Token symbol
                - decimals: Token decimals
                - totalSupply: Total supply (raw)
                - totalSupply_formatted: Total supply (human-readable)
                
        Cost: 1 RPC call (multicall)
        
        Example:
            >>> metadata = token.get_metadata()
            >>> print(f"{metadata['name']} ({metadata['symbol']})")
            >>> print(f"Decimals: {metadata['decimals']}")
            >>> print(f"Supply: {metadata['totalSupply_formatted']}")
        """
        # Return cached if available
        if use_cache and self._metadata_cache:
            return self._metadata_cache
        
        try:
            # Use multicall for efficiency
            calls = [
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'name'},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'symbol'},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'decimals'},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'totalSupply'},
            ]
            
            results = self.client.multicall(calls)
            
            name = results[0]
            symbol = results[1]
            decimals = results[2]
            total_supply = results[3]
            
            metadata = {
                'address': self.address,
                'name': name,
                'symbol': symbol,
                'decimals': decimals,
                'totalSupply': total_supply,
                'totalSupply_formatted': total_supply / (10 ** decimals) if decimals > 0 else total_supply,
            }
            
            # Cache metadata
            self._metadata_cache = metadata
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get token metadata: {e}")
            raise ContractError(f"Metadata retrieval failed: {str(e)}") from e
    
    def get_full_balance_info(self, address: str) -> Dict[str, Any]:
        """
        Get balance with complete token metadata in ONE call.
        
        Perfect for portfolio displays - gets everything you need.
        
        Args:
            address: Wallet address
            
        Returns:
            Dictionary with:
                - token_address: Token contract address
                - holder_address: Wallet address
                - balance: Raw balance
                - balance_formatted: Human-readable balance
                - symbol: Token symbol
                - name: Token name
                - decimals: Token decimals
                
        Cost: 1 multicall = 1 RPC call
        
        Example:
            >>> info = token.get_full_balance_info("0x123...")
            >>> print(f"Balance: {info['balance_formatted']} {info['symbol']}")
            >>> print(f"Token: {info['name']}")
        """
        try:
            # Use multicall to get everything at once
            calls = [
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'balanceOf', 'args': [address]},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'symbol'},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'decimals'},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'name'},
            ]
            
            results = self.client.multicall(calls)
            
            balance = results[0]
            symbol = results[1]
            decimals = results[2]
            name = results[3]
            
            return {
                'token_address': self.address,
                'holder_address': address,
                'balance': balance,
                'balance_formatted': balance / (10 ** decimals) if decimals > 0 else balance,
                'symbol': symbol,
                'name': name,
                'decimals': decimals,
            }
            
        except Exception as e:
            logger.error(f"Failed to get balance info: {e}")
            raise ContractError(f"Balance info retrieval failed: {str(e)}") from e
    
    def get_allowance_info(
        self,
        owner: str,
        spender: str
    ) -> Dict[str, Any]:
        """
        Get allowance with token metadata.
        
        Args:
            owner: Token owner address
            spender: Spender address
            
        Returns:
            Dictionary with allowance details and token info
            
        Example:
            >>> info = token.get_allowance_info("0xowner...", "0xspender...")
            >>> print(f"Approved: {info['allowance_formatted']} {info['symbol']}")
        """
        try:
            calls = [
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'allowance', 'args': [owner, spender]},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'symbol'},
                {'contract': self.address, 'abi': ERC20_ABI, 'function': 'decimals'},
            ]
            
            results = self.client.multicall(calls)
            
            allowance = results[0]
            symbol = results[1]
            decimals = results[2]
            
            # Check if unlimited approval
            max_uint256 = 2**256 - 1
            is_unlimited = allowance >= max_uint256
            
            return {
                'token_address': self.address,
                'owner': owner,
                'spender': spender,
                'allowance': allowance,
                'allowance_formatted': allowance / (10 ** decimals) if decimals > 0 else allowance,
                'symbol': symbol,
                'decimals': decimals,
                'is_unlimited': is_unlimited,
            }
            
        except Exception as e:
            logger.error(f"Failed to get allowance info: {e}")
            raise ContractError(f"Allowance info retrieval failed: {str(e)}") from e
    
    # =========================================================================
    # HELPER METHODS (NEW)
    # =========================================================================
    
    def format_amount(self, raw_amount: int) -> float:
        """
        Convert raw amount to human-readable decimal.
        
        Args:
            raw_amount: Amount in smallest unit
            
        Returns:
            Human-readable amount
            
        Example:
            >>> raw = 1500000  # USDC has 6 decimals
            >>> formatted = token.format_amount(raw)
            >>> print(f"{formatted} USDC")  # 1.5 USDC
        """
        decimals = self.get_decimals()
        return raw_amount / (10 ** decimals) if decimals > 0 else raw_amount
    
    def parse_amount(self, amount: float) -> int:
        """
        Convert human-readable amount to raw units.
        
        Args:
            amount: Human-readable amount
            
        Returns:
            Amount in smallest unit
            
        Example:
            >>> raw = token.parse_amount(1.5)  # USDC
            >>> print(raw)  # 1500000
        """
        from decimal import Decimal
        decimals = self.get_decimals()
        return int(Decimal(str(amount)) * (10 ** decimals))
    
    def has_sufficient_balance(
        self,
        address: str,
        required_amount: int
    ) -> bool:
        """
        Check if address has sufficient balance.
        
        Args:
            address: Wallet address
            required_amount: Required amount in smallest unit
            
        Returns:
            True if balance >= required amount
            
        Example:
            >>> amount = token.parse_amount(100)  # 100 tokens
            >>> if token.has_sufficient_balance("0x123...", amount):
            ...     print("Can proceed with transfer")
        """
        try:
            balance = self.balance_of(address)
            return balance >= required_amount
        except Exception as e:
            logger.warning(f"Failed to check balance: {e}")
            return False
    
    def has_sufficient_allowance(
        self,
        owner: str,
        spender: str,
        required_amount: int
    ) -> bool:
        """
        Check if spender has sufficient allowance.
        
        Args:
            owner: Token owner address
            spender: Spender address
            required_amount: Required allowance in smallest unit
            
        Returns:
            True if allowance >= required amount
            
        Example:
            >>> amount = token.parse_amount(100)
            >>> if token.has_sufficient_allowance("0xowner...", "0xdex...", amount):
            ...     print("Approval sufficient")
        """
        try:
            allowance = self.allowance(owner, spender)
            return allowance >= required_amount
        except Exception as e:
            logger.warning(f"Failed to check allowance: {e}")
            return False
    
    def get_formatted_balance(
        self,
        address: str,
        precision: int = 4
    ) -> str:
        """
        Get formatted balance string for display.
        
        Args:
            address: Wallet address
            precision: Decimal places to show
            
        Returns:
            Formatted string (e.g., "1.5000 USDC")
            
        Example:
            >>> formatted = token.get_formatted_balance("0x123...", 2)
            >>> print(formatted)  # "1.50 USDC"
        """
        try:
            info = self.get_full_balance_info(address)
            balance_formatted = info['balance_formatted']
            symbol = info['symbol']
            
            return f"{balance_formatted:.{precision}f} {symbol}"
            
        except Exception as e:
            logger.error(f"Failed to format balance: {e}")
            return "Error"
    
    # =========================================================================
    # BATCH OPERATIONS (NEW)
    # =========================================================================
    
    def get_balances_batch(
        self,
        addresses: List[str]
    ) -> Dict[str, int]:
        """
        Get balances for multiple addresses efficiently.
        
        Args:
            addresses: List of wallet addresses
            
        Returns:
            Dictionary mapping address to balance
            
        Cost: 1 multicall = 1 RPC call (regardless of number of addresses)
        
        Example:
            >>> addresses = ['0x123...', '0x456...', '0x789...']
            >>> balances = token.get_balances_batch(addresses)
            >>> for addr, bal in balances.items():
            ...     print(f"{addr}: {bal}")
        """
        if not addresses:
            return {}
        
        try:
            # Build multicall
            calls = [
                {
                    'contract': self.address,
                    'abi': ERC20_ABI,
                    'function': 'balanceOf',
                    'args': [addr]
                }
                for addr in addresses
            ]
            
            results = self.client.multicall(calls)
            
            # Map results to addresses
            balances = {}
            for i, addr in enumerate(addresses):
                if i < len(results):
                    balances[addr] = results[i]
                else:
                    balances[addr] = 0
            
            return balances
            
        except Exception as e:
            logger.error(f"Batch balance retrieval failed: {e}")
            raise ContractError(f"Failed to get balances: {str(e)}") from e
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def clear_metadata_cache(self):
        """
        Clear cached metadata.
        
        Use this if token metadata might have changed.
        
        Example:
            >>> token.clear_metadata_cache()
            >>> metadata = token.get_metadata()  # Fetches fresh data
        """
        self._metadata_cache = None
    
    def __repr__(self) -> str:
        """String representation of token."""
        try:
            metadata = self.get_metadata()
            return (
                f"ERC20(address={self.address}, "
                f"symbol={metadata['symbol']}, "
                f"name={metadata['name']}, "
                f"decimals={metadata['decimals']})"
            )
        except Exception:
            return f"ERC20(address={self.address})"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        try:
            metadata = self.get_metadata()
            return f"{metadata['symbol']} ({metadata['name']})"
        except Exception:
            return self.address


# ============================================================================
# FUTURE TOKEN STANDARDS (Placeholders for expansion)
# ============================================================================

# TODO: Add ERC721 (NFT) implementation
# TODO: Add ERC1155 (Multi-token) implementation
# TODO: Add wrapped ETH (WETH) specific methods


# ============================================================================
# PRODUCTION ENHANCEMENTS SUMMARY
# ============================================================================
#
# ✅ ENHANCED METADATA RETRIEVAL
# - get_metadata(): Complete token info in 1 RPC call
# - get_full_balance_info(): Balance + metadata in 1 call
# - get_allowance_info(): Allowance + metadata in 1 call
# - Automatic caching for metadata
#
# ✅ HELPER METHODS
# - format_amount(): Convert raw to human-readable
# - parse_amount(): Convert human-readable to raw
# - has_sufficient_balance(): Check if enough tokens
# - has_sufficient_allowance(): Check if approval sufficient
# - get_formatted_balance(): Display-ready string
#
# ✅ BATCH OPERATIONS
# - get_balances_batch(): Get multiple balances in 1 call
# - Efficient multicall usage
# - Minimal RPC costs
#
# ✅ PRODUCTION QUALITY
# - Comprehensive error handling
# - Logging for debugging
# - Type hints throughout
# - Detailed docstrings with examples
# - Caching where appropriate
#
# ✅ DEVELOPER EXPERIENCE
# - Intuitive method names
# - Consistent return types
# - Clear examples in docstrings
# - String representations for debugging
#
# BACKWARD COMPATIBILITY:
# - All existing methods unchanged
# - New methods are purely additive
# - No breaking changes to API
#
# EFFICIENCY:
# - Multicall for batch operations
# - Metadata caching
# - Single RPC calls where possible
# - Zero-cost local operations
# ============================================================================