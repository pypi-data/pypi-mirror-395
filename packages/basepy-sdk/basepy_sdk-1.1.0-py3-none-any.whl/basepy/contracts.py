"""
Enhanced Contract abstraction with ERC-20 integration.
Integrates with: abis.py, utils.py, standards.py, transactions.py, client.py
"""

from typing import Any, Dict, Optional, List, Union
import logging
from .exceptions import ContractError

logger = logging.getLogger(__name__)


class Contract:
    """Enhanced contract with production features."""
    
    def __init__(self, client, address: str, abi: List[Dict]):
        self.client = client
        self.address = client._validate_address(address)
        self.abi = abi
        
        try:
            self.contract = self.client.w3.eth.contract(address=self.address, abi=abi)
        except Exception as e:
            raise ContractError(f"Failed to initialize contract: {str(e)}") from e
        
        logger.info(f"Contract initialized at {self.address}")

    def call(self, function_name: str, *args, block_identifier='latest') -> Any:
        """Call read-only function with better error handling."""
        try:
            func = getattr(self.contract.functions, function_name)
            result = func(*args).call(block_identifier=block_identifier)
            logger.debug(f"Called {function_name}({args}) -> {result}")
            return result
        except AttributeError:
            raise ContractError(f"Function '{function_name}' not found in ABI")
        except Exception as e:
            raise ContractError(f"Call to {function_name} failed: {str(e)}") from e

    def transact(
        self, 
        wallet, 
        function_name: str, 
        *args,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        value: int = 0,
        nonce: Optional[int] = None,
        simulate_first: bool = True,
        gas_buffer: float = 1.1
    ) -> str:
        """
        Send transaction with simulation and auto gas estimation.
        
        NEW FEATURES:
        - simulate_first: Test transaction before sending
        - gas_buffer: Add safety margin to gas estimate (default 10%)
        - Better error messages
        - Automatic nonce management
        """
        try:
            func = getattr(self.contract.functions, function_name)
            
            # Get nonce (use pending to avoid conflicts)
            if nonce is None:
                nonce = self.client.get_transaction_count(wallet.address, 'pending')
                logger.debug(f"Using nonce: {nonce}")
            
            tx_params = {
                'chainId': self.client.get_chain_id(),
                'nonce': nonce,
                'value': value,
                'from': wallet.address,
                'gasPrice': gas_price or self.client.get_gas_price()
            }
            
            # SIMULATION - Catch errors before sending
            if simulate_first:
                try:
                    func(*args).call({'from': wallet.address, 'value': value})
                    logger.info(f"✓ Simulation successful for {function_name}")
                except Exception as sim_error:
                    error_msg = str(sim_error)
                    if "insufficient funds" in error_msg.lower():
                        raise ContractError("Insufficient funds for transaction")
                    elif "execution reverted" in error_msg.lower():
                        raise ContractError(f"Transaction would revert: {error_msg}")
                    raise ContractError(f"Simulation failed: {error_msg}")
            
            # AUTO GAS ESTIMATION with buffer
            if gas is None:
                try:
                    estimated = func(*args).estimate_gas({'from': wallet.address, 'value': value})
                    gas = int(estimated * gas_buffer)  # Add 10% buffer by default
                    logger.debug(f"Estimated gas: {estimated} -> {gas} (buffer: {gas_buffer}x)")
                except Exception as gas_error:
                    logger.warning(f"Gas estimation failed: {gas_error}. Using default 100000")
                    gas = 100000
            
            tx_params['gas'] = gas
            
            # Build, sign, send
            tx = func(*args).build_transaction(tx_params)
            signed_tx = wallet.sign_transaction(tx)
            tx_hash = self.client.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            tx_hash_hex = self.client.w3.to_hex(tx_hash)
            logger.info(f"✓ Transaction sent: {tx_hash_hex}")
            return tx_hash_hex
            
        except AttributeError:
            raise ContractError(f"Function '{function_name}' not found in ABI")
        except ContractError:
            raise  # Re-raise our custom errors
        except Exception as e:
            error_msg = str(e)
            if "nonce too low" in error_msg.lower():
                raise ContractError("Nonce too low - transaction may have already been sent")
            raise ContractError(f"Transaction failed: {error_msg}") from e

    def is_erc20(self) -> bool:
        """Check if contract implements ERC-20 interface."""
        required = ['totalSupply', 'balanceOf', 'transfer', 'allowance', 'approve', 'transferFrom']
        try:
            return all(hasattr(self.contract.functions, f) for f in required)
        except:
            return False

    def __str__(self) -> str:
        contract_type = "ERC-20" if self.is_erc20() else "Contract"
        return f"{contract_type} at {self.address}"


# =============================================================================
# ERC-20 SPECIFIC CONTRACT CLASS
# =============================================================================

class ERC20Contract(Contract):
    """
    ERC-20 specific contract with helper methods.
    Integrates with utils.py for formatting.
    """
    
    def __init__(self, client, address: str):
        from .abis import ERC20_ABI
        super().__init__(client, address, ERC20_ABI)
        
        # Cache metadata
        self._name = None
        self._symbol = None
        self._decimals = None
        
        logger.info(f"ERC-20 contract initialized at {address}")
    
    def name(self) -> str:
        """Get token name (cached)."""
        if self._name is None:
            self._name = self.call('name')
        return self._name
    
    def symbol(self) -> str:
        """Get token symbol (cached)."""
        if self._symbol is None:
            self._symbol = self.call('symbol')
        return self._symbol
    
    def decimals(self) -> int:
        """Get token decimals (cached)."""
        if self._decimals is None:
            self._decimals = self.call('decimals')
        return self._decimals
    
    def total_supply(self) -> int:
        """Get total supply."""
        return self.call('totalSupply')
    
    def balance_of(self, address: str) -> int:
        """Get balance of address."""
        validated = self.client._validate_address(address)
        return self.call('balanceOf', validated)
    
    def allowance(self, owner: str, spender: str) -> int:
        """Get allowance."""
        owner_addr = self.client._validate_address(owner)
        spender_addr = self.client._validate_address(spender)
        return self.call('allowance', owner_addr, spender_addr)
    
    def format_amount(self, amount: int) -> float:
        """Format raw amount to human-readable decimal."""
        from .utils import format_token_amount
        return format_token_amount(amount, self.decimals())
    
    def parse_amount(self, amount: Union[str, float]) -> int:
        """Parse human-readable amount using utils.py."""
        from .utils import parse_token_amount
        return parse_token_amount(amount, self.decimals())
    
    def format_balance(self, address: str) -> str:
        """Get formatted balance string with symbol."""
        from .utils import format_token_balance
        balance = self.balance_of(address)
        return format_token_balance(balance, self.decimals(), self.symbol())
    
    def transfer(self, wallet, to: str, amount: int, **kwargs) -> str:
        """Transfer tokens."""
        to_addr = self.client._validate_address(to)
        return self.transact(wallet, 'transfer', to_addr, amount, **kwargs)
    
    def approve(self, wallet, spender: str, amount: int, **kwargs) -> str:
        """Approve spender."""
        spender_addr = self.client._validate_address(spender)
        return self.transact(wallet, 'approve', spender_addr, amount, **kwargs)
    
    def has_sufficient_balance(self, address: str, required_amount: int) -> bool:
        """Check if address has sufficient balance."""
        balance = self.balance_of(address)
        return balance >= required_amount
    
    def has_sufficient_allowance(self, owner: str, spender: str, required: int) -> bool:
        """Check if spender has sufficient allowance."""
        allowance = self.allowance(owner, spender)
        return allowance >= required
    
    def __str__(self) -> str:
        try:
            return f"{self.name()} ({self.symbol()}) at {self.address}"
        except:
            return f"ERC-20 Token at {self.address}"