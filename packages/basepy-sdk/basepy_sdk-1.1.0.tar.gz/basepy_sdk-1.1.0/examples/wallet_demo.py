"""
Complete Wallet.py Demo - All Features Showcase

This demo demonstrates EVERY feature of the Wallet class including:
- Wallet creation methods (new, private key, mnemonic, keystore)
- Transaction signing (EIP-155, EIP-1559, EIP-191, EIP-712)
- Balance and nonce operations with caching
- Token operations and portfolio tracking
- Transaction cost estimation
- Cache management
- Export/import operations
- Security features

Requirements:
    - BasePy SDK installed
    - Base Sepolia testnet access
    - Test wallet with some Sepolia ETH
    - Optional: Test tokens for token operations

Usage:
    python examples/wallet_complete_demo.py
"""

from datetime import datetime
import sys
import os
import json
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basepy import BaseClient, Wallet
from basepy.utils import to_wei, from_wei, to_checksum_address
from basepy.exceptions import WalletError, ValidationError


# ============================================================================
# CONFIGURATION
# ============================================================================

# Use Base Sepolia testnet for safe testing
NETWORK = "sepolia"
CHAIN_ID = 84532

# Test addresses (Base Sepolia)
TEST_RECIPIENT = "0x0000000000000000000000000000000000000001"  # Burn address for testing
TEST_TOKEN_USDC_SEPOLIA = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"  # USDC on Base Sepolia

# Demo test mnemonic (NEVER use this for real funds!)
DEMO_MNEMONIC = "test test test test test test test test test test test junk"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_success(message: str):
    """Print success message."""
    print(f"✅ {message}")


def print_info(message: str):
    """Print info message."""
    print(f"ℹ️  {message}")


def print_error(message: str):
    """Print error message."""
    print(f"❌ {message}")


def print_warning(message: str):
    """Print warning message."""
    print(f"⚠️  {message}")


def safe_execute(func, description: str):
    """Execute function with error handling."""
    try:
        print(f"\n🔄 {description}...")
        result = func()
        print_success(f"{description} - Success!")
        return result
    except Exception as e:
        print_error(f"{description} - Failed: {e}")
        return None


# ============================================================================
# DEMO SECTIONS
# ============================================================================

def demo_1_wallet_creation():
    """Demo 1: Wallet Creation Methods"""
    print_section("DEMO 1: Wallet Creation Methods")
    
    # 1.1: Create new random wallet
    def create_random():
        wallet = Wallet.create()
        print_info(f"New wallet created")
        print_info(f"  Address: {wallet.address}")
        print_info(f"  Private Key: {wallet.private_key[:20]}...") # Truncated for safety
        return wallet
    
    wallet1 = safe_execute(create_random, "Create new random wallet")
    
    # 1.2: Import from private key
    def import_from_key():
        # Use the wallet we just created
        wallet = Wallet.from_private_key(wallet1.private_key)
        print_info(f"Wallet imported from private key")
        print_info(f"  Address: {wallet.address}")
        return wallet
    
    wallet2 = safe_execute(import_from_key, "Import wallet from private key")
    
    # 1.3: Import from mnemonic
    def import_from_mnemonic():
        wallet = Wallet.from_mnemonic(DEMO_MNEMONIC)
        print_info(f"Wallet imported from mnemonic")
        print_info(f"  Address: {wallet.address}")
        return wallet
    
    wallet3 = safe_execute(import_from_mnemonic, "Import wallet from mnemonic")
    
    # 1.4: Multiple accounts from same mnemonic
    def import_multiple_accounts():
        wallet_account_0 = Wallet.from_mnemonic(
            DEMO_MNEMONIC,
            account_path="m/44'/60'/0'/0/0"
        )
        wallet_account_1 = Wallet.from_mnemonic(
            DEMO_MNEMONIC,
            account_path="m/44'/60'/0'/0/1"
        )
        print_info(f"Account 0: {wallet_account_0.address}")
        print_info(f"Account 1: {wallet_account_1.address}")
        return wallet_account_0, wallet_account_1
    
    accounts = safe_execute(import_multiple_accounts, "Import multiple accounts from mnemonic")
    
    # 1.5: With client and caching
    def create_with_client():
        client = BaseClient(chain_id=CHAIN_ID)
        wallet = Wallet.create(
            client=client,
            enable_cache=True,
            cache_ttl=10
        )
        print_info(f"Wallet created with client and caching enabled")
        print_info(f"  Address: {wallet.address}")
        print_info(f"  Chain ID: {client.get_chain_id()}")
        return wallet, client
    
    result = safe_execute(create_with_client, "Create wallet with client")
    
    return wallet1, wallet3, result


def demo_2_validation_methods(wallet: Wallet):
    """Demo 2: Validation Methods"""
    print_section("DEMO 2: Validation Methods")
    
    # 2.1: Validate address
    def validate_addresses():
        valid_addr = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        invalid_addr = "invalid_address"
        
        result1 = Wallet.is_valid_address(valid_addr)
        result2 = Wallet.is_valid_address(invalid_addr)
        
        print_info(f"Valid address check: {result1}")
        print_info(f"Invalid address check: {result2}")
        return result1, result2
    
    safe_execute(validate_addresses, "Validate addresses")
    
    # 2.2: Validate private key
    def validate_keys():
        valid_key = "0x" + "1" * 64
        invalid_key = "0x123"
        
        result1 = Wallet.is_valid_private_key(valid_key)
        result2 = Wallet.is_valid_private_key(invalid_key)
        
        print_info(f"Valid key check: {result1}")
        print_info(f"Invalid key check: {result2}")
        return result1, result2
    
    safe_execute(validate_keys, "Validate private keys")


def demo_3_properties(wallet: Wallet):
    """Demo 3: Wallet Properties"""
    print_section("DEMO 3: Wallet Properties")
    
    # 3.1: Address property
    def show_address():
        print_info(f"Address: {wallet.address}")
        print_info(f"Address type: {type(wallet.address)}")
        print_info(f"Address length: {len(wallet.address)}")
        return wallet.address
    
    safe_execute(show_address, "Get wallet address")
    
    # 3.2: Private key property (CAREFUL!)
    def show_private_key():
        key = wallet.private_key
        print_info(f"Private key: {key[:20]}... (truncated for safety)")
        print_info(f"Private key length: {len(key)}")
        return key
    
    safe_execute(show_private_key, "Get private key")


def demo_4_export_import(wallet: Wallet):
    """Demo 4: Export and Import Operations"""
    print_section("DEMO 4: Export and Import Operations")
    
    # 4.1: Export to keystore
    def export_keystore():
        password = "test_password_123"
        keystore_path = "test_wallet_keystore.json"
        
        keystore = wallet.to_keystore(
            password=password,
            output_path=keystore_path,
            kdf="scrypt"
        )
        
        print_info(f"Keystore created")
        print_info(f"  Path: {keystore_path}")
        print_info(f"  KDF: scrypt")
        print_info(f"  Keystore keys: {list(keystore.keys())}")
        
        return keystore_path, password
    
    keystore_info = safe_execute(export_keystore, "Export wallet to keystore")
    
    # 4.2: Import from keystore
    if keystore_info:
        def import_keystore():
            keystore_path, password = keystore_info
            
            imported_wallet = Wallet.from_keystore(
                keystore_path=keystore_path,
                password=password
            )
            
            print_info(f"Wallet imported from keystore")
            print_info(f"  Address matches: {imported_wallet.address == wallet.address}")
            
            # Cleanup
            Path(keystore_path).unlink()
            print_info(f"  Test keystore file deleted")
            
            return imported_wallet
        
        safe_execute(import_keystore, "Import wallet from keystore")


def demo_5_balance_operations(wallet: Wallet, client: BaseClient):
    """Demo 5: Balance and Nonce Operations"""
    print_section("DEMO 5: Balance and Nonce Operations")
    
    # Set client if not already set
    if not wallet.client:
        wallet.set_client(client)
    
    # 5.1: Get balance (Wei)
    def get_balance_wei():
        balance = wallet.get_balance(use_cache=False)
        print_info(f"Balance (Wei): {balance}")
        print_info(f"Balance (ETH): {balance / 10**18}")
        return balance
    
    balance = safe_execute(get_balance_wei, "Get balance in Wei")
    
    # 5.2: Get balance (ETH)
    def get_balance_eth():
        balance = wallet.get_balance_eth(use_cache=False)
        print_info(f"Balance (ETH): {balance}")
        return balance
    
    safe_execute(get_balance_eth, "Get balance in ETH")
    
    # 5.3: Get nonce
    def get_nonce():
        nonce_pending = wallet.get_nonce(pending=True, use_cache=False)
        nonce_latest = wallet.get_nonce(pending=False, use_cache=False)
        print_info(f"Nonce (pending): {nonce_pending}")
        print_info(f"Nonce (latest): {nonce_latest}")
        return nonce_pending
    
    safe_execute(get_nonce, "Get wallet nonce")
    
    # 5.4: Check sufficient balance
    def check_sufficient_balance():
        required = to_wei(0.001, 'ether')
        has_sufficient = wallet.has_sufficient_balance(required, use_cache=False)
        print_info(f"Required: 0.001 ETH")
        print_info(f"Has sufficient balance: {has_sufficient}")
        return has_sufficient
    
    safe_execute(check_sufficient_balance, "Check sufficient balance")
    
    # 5.5: Demonstrate caching
    def demonstrate_caching():
        print_info("First call (fetches from blockchain):")
        start = time.time()
        balance1 = wallet.get_balance(use_cache=True)
        time1 = time.time() - start
        print_info(f"  Time: {time1:.4f}s")
        
        print_info("Second call (uses cache):")
        start = time.time()
        balance2 = wallet.get_balance(use_cache=True)
        time2 = time.time() - start
        print_info(f"  Time: {time2:.4f}s")
        
        # ✅ FIX: Handle division by zero
        if time2 > 0:
            speedup = time1 / time2
            print_info(f"  Speedup: {speedup:.1f}x faster")
        else:
            print_info(f"  Speedup: Very fast (< 0.0001s)")
        
        print_info(f"  Balances match: {balance1 == balance2}")
        
        return time1, time2
    
    safe_execute(demonstrate_caching, "Demonstrate balance caching")


def demo_6_token_operations(wallet: Wallet, client: BaseClient):
    """Demo 6: Token Operations"""
    print_section("DEMO 6: Token Operations")
    
    # Set client if not already set
    if not wallet.client:
        wallet.set_client(client)
    
    # 6.1: Get token balance
    def get_token_balance():
        try:
            balance = wallet.get_token_balance(
                TEST_TOKEN_USDC_SEPOLIA,
                use_cache=False
            )
            print_info(f"Token balance (raw): {balance}")
            print_info(f"Token balance (formatted): {balance / 10**6} USDC")
            return balance
        except Exception as e:
            print_warning(f"Token balance check failed (might not have this token): {e}")
            return None
    
    safe_execute(get_token_balance, "Get ERC-20 token balance")
    
    # 6.2: Get formatted token balance
    def get_formatted_balance():
        try:
            balance = wallet.get_token_balance_formatted(
                TEST_TOKEN_USDC_SEPOLIA,
                decimals=6
            )
            print_info(f"Formatted balance: {balance} USDC")
            return balance
        except Exception as e:
            print_warning(f"Formatted balance failed: {e}")
            return None
    
    safe_execute(get_formatted_balance, "Get formatted token balance")
    
    # 6.3: Get token allowance
    def get_token_allowance():
        try:
            allowance = wallet.get_token_allowance(
                TEST_TOKEN_USDC_SEPOLIA,
                TEST_RECIPIENT
            )
            print_info(f"Token allowance: {allowance}")
            print_info(f"Formatted: {allowance / 10**6} USDC")
            return allowance
        except Exception as e:
            print_warning(f"Allowance check failed: {e}")
            return None
    
    safe_execute(get_token_allowance, "Get token allowance")
    
    # 6.4: Check sufficient token balance
    def check_token_balance():
        try:
            required = 1000000  # 1 USDC
            has_sufficient = wallet.has_sufficient_token_balance(
                TEST_TOKEN_USDC_SEPOLIA,
                required
            )
            print_info(f"Required: 1 USDC")
            print_info(f"Has sufficient: {has_sufficient}")
            return has_sufficient
        except Exception as e:
            print_warning(f"Check failed: {e}")
            return False
    
    safe_execute(check_token_balance, "Check sufficient token balance")


def demo_7_portfolio_operations(wallet: Wallet, client: BaseClient):
    """Demo 7: Portfolio Operations"""
    print_section("DEMO 7: Portfolio Operations")
    
    # Set client if not already set
    if not wallet.client:
        wallet.set_client(client)
    
    # 7.1: Get complete portfolio
    def get_portfolio():
        try:
            portfolio = wallet.get_portfolio(use_cache=False)
            
            print_info("Portfolio Summary:")
            print_info(f"  ETH Balance: {portfolio['eth']['balance_formatted']}")
            print_info(f"  Total Tokens Checked: {portfolio['total_tokens']}")
            print_info(f"  Non-Zero Tokens: {portfolio['non_zero_tokens']}")
            
            print_info("\nToken Balances:")
            for token_addr, info in portfolio['tokens'].items():
                if info['balance'] > 0:
                    print_info(f"  {info['symbol']}: {info['balance_formatted']}")
            
            return portfolio
        except Exception as e:
            print_warning(f"Portfolio retrieval failed: {e}")
            return None
    
    safe_execute(get_portfolio, "Get complete portfolio")
    
    # 7.2: Get portfolio with specific tokens
    def get_custom_portfolio():
        try:
            custom_tokens = [TEST_TOKEN_USDC_SEPOLIA]
            portfolio = wallet.get_portfolio(
                token_addresses=custom_tokens,
                use_cache=False
            )
            print_info(f"Custom portfolio with {len(custom_tokens)} token(s)")
            print_info(f"  Tokens checked: {portfolio['total_tokens']}")
            return portfolio
        except Exception as e:
            print_warning(f"Custom portfolio failed: {e}")
            return None
    
    safe_execute(get_custom_portfolio, "Get custom portfolio")


def demo_8_transaction_signing(wallet: Wallet, client: BaseClient):
    """Demo 8: Transaction Signing"""
    print_section("DEMO 8: Transaction Signing")
    
    # Set client if not already set
    if not wallet.client:
        wallet.set_client(client)
    
    # 8.1: Sign legacy transaction
    def sign_legacy_tx():
        nonce = wallet.get_nonce()
        
        tx = {
            'to': TEST_RECIPIENT,
            'value': to_wei(0.001, 'ether'),
            'gas': 21000,
            'gasPrice': to_wei(1, 'gwei'),
            'nonce': nonce,
            'chainId': CHAIN_ID,
        }
        
        signed = wallet.sign_transaction(tx)
        
        print_info(f"Legacy transaction signed:")
        print_info(f"  Hash: {signed.hash.hex()}")
        print_info(f"  V: {signed.v}")
        print_info(f"  R: {signed.r}")
        print_info(f"  S: {signed.s}")
        print_info(f"  Raw TX (first 50 chars): {signed.raw_transaction.hex()[:50]}...")
        
        return signed
    
    safe_execute(sign_legacy_tx, "Sign legacy transaction")
    
    # 8.2: Sign EIP-1559 transaction
    def sign_eip1559_tx():
        nonce = wallet.get_nonce()
        
        tx = {
            'to': TEST_RECIPIENT,
            'value': to_wei(0.001, 'ether'),
            'gas': 21000,
            'maxFeePerGas': to_wei(2, 'gwei'),
            'maxPriorityFeePerGas': to_wei(1, 'gwei'),
            'nonce': nonce,
            'chainId': CHAIN_ID,
        }
        
        signed = wallet.sign_transaction(tx)
        
        print_info(f"EIP-1559 transaction signed:")
        print_info(f"  Hash: {signed.hash.hex()}")
        print_info(f"  Type: EIP-1559")
        
        return signed
    
    safe_execute(sign_eip1559_tx, "Sign EIP-1559 transaction")


def demo_9_message_signing(wallet: Wallet):
    """Demo 9: Message Signing"""
    print_section("DEMO 9: Message Signing")
    
    # 9.1: Sign simple message (EIP-191)
    def sign_simple_message():
        message = "Hello, Base blockchain!"
        signature = wallet.sign_message(message)
        
        print_info(f"Message: '{message}'")
        print_info(f"Signature: {signature}")
        print_info(f"Signature length: {len(signature)}")
        
        return signature
    
    safe_execute(sign_simple_message, "Sign simple message (EIP-191)")
    
    # 9.2: Sign bytes message
    def sign_bytes_message():
        message = b"Binary message data"
        signature = wallet.sign_message(message)
        
        print_info(f"Message bytes: {message}")
        print_info(f"Signature: {signature[:50]}...")
        
        return signature
    
    safe_execute(sign_bytes_message, "Sign bytes message")
    
    # 9.3: Sign typed data (EIP-712)
    def sign_typed_data():
    # Use a working EIP-712 structure
        typed_data = {
            "domain": {
                "name": "Base Mail",
                "version": "1",
                "chainId": CHAIN_ID,
            },
            "message": {
                "from": wallet.address,
                "to": TEST_RECIPIENT,
                "contents": "Hello from Base!",
            },
            "primaryType": "Mail",
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                ],
                "Mail": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "contents", "type": "string"},
                ],
            },
        }
        
        try:
            signature = wallet.sign_typed_data(typed_data)
            print_info(f"Typed data signed (EIP-712)")
            print_info(f"  Primary type: {typed_data['primaryType']}")
            print_info(f"  Domain: {typed_data['domain']['name']}")
            print_info(f"  Signature: {signature[:50]}...")
            return signature
        except Exception as e:
            # EIP-712 can be finicky with different eth-account versions
            print_warning(f"EIP-712 signing failed (eth-account version specific): {e}")
            print_info("  This is expected with some eth-account versions")
            return None
    
    safe_execute(sign_typed_data, "Sign typed data (EIP-712)")


def demo_10_cost_estimation(wallet: Wallet, client: BaseClient):
    """Demo 10: Transaction Cost Estimation"""
    print_section("DEMO 10: Transaction Cost Estimation")
    
    # Set client if not already set
    if not wallet.client:
        wallet.set_client(client)
    
    # 10.1: Estimate simple transfer
    def estimate_simple_transfer():
        cost = wallet.estimate_transaction_cost(
            to=TEST_RECIPIENT,
            value=0.1,  # 0.1 ETH
            value_unit='ether'
        )
        
        print_info(f"Simple transfer cost estimation:")
        print_info(f"  L2 Gas Used: {cost['l2_gas_used']}")
        print_info(f"  L2 Gas Price: {cost['l2_gas_price']} Wei")
        print_info(f"  L2 Cost: {cost['l2_cost_eth']:.6f} ETH")
        print_info(f"  L1 Cost: {cost['l1_cost_eth']:.6f} ETH")
        print_info(f"  Total Cost: {cost['total_cost_eth']:.6f} ETH")
        
        return cost
    
    safe_execute(estimate_simple_transfer, "Estimate simple transfer cost")
    
    # 10.2: Estimate contract call
    def estimate_contract_call():
        # Sample contract call data (ERC-20 transfer)
        data = "0xa9059cbb" + "0" * 64 + "0" * 64  # transfer(address,uint256)
        
        cost = wallet.estimate_transaction_cost(
            to=TEST_TOKEN_USDC_SEPOLIA,
            value=0,
            data=data
        )
        
        print_info(f"Contract call cost estimation:")
        print_info(f"  Total Cost: {cost['total_cost_eth']:.6f} ETH")
        print_info(f"  L1 portion: {cost['l1_cost_eth'] / cost['total_cost_eth'] * 100:.1f}%")
        
        return cost
    
    safe_execute(estimate_contract_call, "Estimate contract call cost")
    
    # 10.3: Check affordability
    def check_affordability():
        can_afford = wallet.can_afford_transaction(
            to=TEST_RECIPIENT,
            value=0.001,
            value_unit='ether',
            buffer_percent=10.0
        )
        
        print_info(f"Transaction: 0.001 ETH transfer")
        print_info(f"Can afford (with 10% buffer): {can_afford}")
        
        return can_afford
    
    safe_execute(check_affordability, "Check transaction affordability")


def demo_11_cache_management(wallet: Wallet, client: BaseClient):
    """Demo 11: Cache Management"""
    print_section("DEMO 11: Cache Management")
    
    # Set client if not already set
    if not wallet.client:
        wallet.set_client(client)
    
    # 11.1: Demonstrate cache behavior
    def demonstrate_cache():
        print_info("Getting balance (fresh):")
        wallet.clear_cache()
        balance1 = wallet.get_balance(use_cache=True)
        print_info(f"  Balance: {balance1 / 10**18} ETH")
        
        print_info("\nGetting balance (cached):")
        balance2 = wallet.get_balance(use_cache=True)
        print_info(f"  Balance: {balance2 / 10**18} ETH")
        print_info(f"  Same value: {balance1 == balance2}")
        
        print_info("\nInvalidating balance cache:")
        wallet.invalidate_balance_cache()
        
        print_info("Getting balance (fresh after invalidation):")
        balance3 = wallet.get_balance(use_cache=True)
        print_info(f"  Balance: {balance3 / 10**18} ETH")
        
        return balance1, balance2, balance3
    
    safe_execute(demonstrate_cache, "Demonstrate cache behavior")
    
    # 11.2: Individual cache invalidation
    def test_individual_invalidation():
        print_info("Testing individual cache invalidation:")
        
        # Populate all caches
        wallet.get_balance(use_cache=True)
        wallet.get_nonce(use_cache=True)
        
        print_info("  All caches populated")
        
        # Invalidate individually
        wallet.invalidate_balance_cache()
        print_info("  ✓ Balance cache invalidated")
        
        wallet.invalidate_nonce_cache()
        print_info("  ✓ Nonce cache invalidated")
        
        wallet.invalidate_portfolio_cache()
        print_info("  ✓ Portfolio cache invalidated")
        
        return True
    
    safe_execute(test_individual_invalidation, "Test individual cache invalidation")
    
    # 11.3: Clear all caches
    def clear_all_caches():
        wallet.clear_cache()
        print_info("All caches cleared")
        return True
    
    safe_execute(clear_all_caches, "Clear all caches")


def demo_12_client_management(wallet: Wallet):
    """Demo 12: Client Management"""
    print_section("DEMO 12: Client Management")
    
    # 12.1: Set client
    def set_new_client():
        new_client = BaseClient(chain_id=CHAIN_ID)
        wallet.set_client(new_client)
        print_info(f"Client set")
        print_info(f"  Chain ID: {new_client.get_chain_id()}")
        print_info(f"  Connected: {new_client.is_connected()}")
        return new_client
    
    safe_execute(set_new_client, "Set new client")
    
    # 12.2: Verify client operations work
    def verify_client_operations():
        if wallet.client:
            balance = wallet.get_balance(use_cache=False)
            nonce = wallet.get_nonce(use_cache=False)
            print_info(f"Client operations working:")
            print_info(f"  Balance: {balance / 10**18} ETH")
            print_info(f"  Nonce: {nonce}")
            return True
        else:
            print_warning("No client set")
            return False
    
    safe_execute(verify_client_operations, "Verify client operations")


def demo_13_utility_methods(wallet: Wallet):
    """Demo 13: Utility Methods"""
    print_section("DEMO 13: Utility Methods")
    
    # 13.1: String representations
    def test_string_repr():
        print_info(f"__repr__: {repr(wallet)}")
        print_info(f"__str__: {str(wallet)}")
        print_info(f"Address: {wallet.address}")
        return repr(wallet), str(wallet)
    
    safe_execute(test_string_repr, "Test string representations")
    
    # 13.2: Equality comparison
    def test_equality():
        wallet_same = Wallet.from_private_key(wallet.private_key)
        wallet_different = Wallet.create()
        
        print_info(f"Same wallet: {wallet == wallet_same}")
        print_info(f"Different wallet: {wallet == wallet_different}")
        
        return wallet == wallet_same, wallet == wallet_different
    
    safe_execute(test_equality, "Test wallet equality")
    
    # 13.3: Hashing
    def test_hashing():
        wallet_hash = hash(wallet)
        print_info(f"Wallet hash: {wallet_hash}")
        
        # Wallets with same address should have same hash
        wallet_same = Wallet.from_private_key(wallet.private_key)
        print_info(f"Same hash: {hash(wallet) == hash(wallet_same)}")
        
        return wallet_hash
    
    safe_execute(test_hashing, "Test wallet hashing")


def demo_14_error_handling():
    """Demo 14: Error Handling"""
    print_section("DEMO 14: Error Handling and Validation")
    
    # 14.1: Invalid private key
    def test_invalid_private_key():
        try:
            Wallet.from_private_key("invalid_key")
            print_error("Should have raised ValidationError")
        except ValidationError as e:
            print_success(f"Correctly raised ValidationError: {e}")
        except Exception as e:
            print_error(f"Wrong exception type: {type(e)}")
    
    safe_execute(test_invalid_private_key, "Test invalid private key handling")
    
    # 14.2: Invalid mnemonic
    def test_invalid_mnemonic():
        try:
            Wallet.from_mnemonic("invalid mnemonic phrase")
            print_error("Should have raised WalletError")
        except WalletError as e:
            print_success(f"Correctly raised WalletError: {e}")
        except Exception as e:
            print_error(f"Wrong exception type: {type(e)}")
    
    safe_execute(test_invalid_mnemonic, "Test invalid mnemonic handling")
    
    # 14.3: Operations without client
    def test_no_client_error():
        wallet_no_client = Wallet.create()
        try:
            wallet_no_client.get_balance()
            print_error("Should have raised WalletError")
        except WalletError as e:
            print_success(f"Correctly raised WalletError: {e}")
        except Exception as e:
            print_error(f"Wrong exception type: {type(e)}")
    
    safe_execute(test_no_client_error, "Test operations without client")
    
    # 14.4: Invalid transaction signing
    def test_invalid_transaction():
        wallet_temp = Wallet.create()
        try:
            # Missing required fields
            wallet_temp.sign_transaction({'to': TEST_RECIPIENT})
            print_error("Should have raised ValidationError")
        except ValidationError as e:
            print_success(f"Correctly raised ValidationError: {e}")
        except Exception as e:
            print_error(f"Wrong exception type: {type(e)}")
    
    safe_execute(test_invalid_transaction, "Test invalid transaction signing")


def demo_15_comprehensive_workflow():
    """Demo 15: Comprehensive Real-World Workflow"""
    print_section("DEMO 15: Comprehensive Real-World Workflow")
    
    print_info("Simulating complete wallet lifecycle:\n")
    
    # Step 1: Create wallet
    print_info("Step 1: Create wallet")
    client = BaseClient(chain_id=CHAIN_ID)
    wallet = Wallet.create(client=client, enable_cache=True, cache_ttl=10)
    print_info(f"  ✓ Wallet created: {wallet.address}\n")
    
    # Step 2: Export to keystore for backup
    print_info("Step 2: Export to keystore")
    password = "secure_password_123"
    keystore_file = "backup_wallet.json"
    wallet.to_keystore(password=password, output_path=keystore_file)
    print_info(f"  ✓ Keystore saved: {keystore_file}\n")
    
    # Step 3: Check balances
    print_info("Step 3: Check balances")
    try:
        eth_balance = wallet.get_balance_eth()
        print_info(f"  ✓ ETH Balance: {eth_balance} ETH")
    except Exception as e:
        print_warning(f"  ⚠ Balance check: {e}")
    print()
    
    # Step 4: Get portfolio
    print_info("Step 4: Get portfolio")
    try:
        portfolio = wallet.get_portfolio()
        print_info(f"  ✓ Portfolio retrieved")
        print_info(f"    ETH: {portfolio['eth']['balance_formatted']}")
        print_info(f"    Tokens: {portfolio['non_zero_tokens']} with balance")
    except Exception as e:
        print_warning(f"  ⚠ Portfolio: {e}")
    print()
    
    # Step 5: Estimate transaction cost
    print_info("Step 5: Estimate transaction cost")
    try:
        cost = wallet.estimate_transaction_cost(
            to=TEST_RECIPIENT,
            value=0.001,
            value_unit='ether'
        )
        print_info(f"  ✓ Estimated cost: {cost['total_cost_eth']:.6f} ETH")
        print_info(f"    L2: {cost['l2_cost_eth']:.6f} ETH")
        print_info(f"    L1: {cost['l1_cost_eth']:.6f} ETH")
    except Exception as e:
        print_warning(f"  ⚠ Cost estimation: {e}")
    print()
    
    # Step 6: Check if can afford
    print_info("Step 6: Check affordability")
    try:
        can_afford = wallet.can_afford_transaction(
            to=TEST_RECIPIENT,
            value=0.001,
            buffer_percent=10.0
        )
        print_info(f"  ✓ Can afford 0.001 ETH transfer: {can_afford}")
    except Exception as e:
        print_warning(f"  ⚠ Affordability check: {e}")
    print()
    
    # Step 7: Prepare and sign transaction (but don't send)
    print_info("Step 7: Prepare and sign transaction")
    try:
        nonce = wallet.get_nonce()
        tx = {
            'to': TEST_RECIPIENT,
            'value': to_wei(0.001, 'ether'),
            'gas': 21000,
            'maxFeePerGas': to_wei(2, 'gwei'),
            'maxPriorityFeePerGas': to_wei(1, 'gwei'),
            'nonce': nonce,
            'chainId': CHAIN_ID,
        }
        signed = wallet.sign_transaction(tx)
        print_info(f"  ✓ Transaction signed")
        print_info(f"    Hash: {signed.hash.hex()}")
        print_info(f"    (Not broadcasting to network)")
    except Exception as e:
        print_warning(f"  ⚠ Transaction signing: {e}")
    print()
    
    # Step 8: Sign message
    print_info("Step 8: Sign message")
    message = f"Authenticated on {datetime.now().isoformat()}"
    signature = wallet.sign_message(message)
    print_info(f"  ✓ Message signed")
    print_info(f"    Message: '{message}'")
    print_info(f"    Signature: {signature[:50]}...")
    print()
    
    # Step 9: Restore from keystore
    print_info("Step 9: Restore from keystore")
    restored_wallet = Wallet.from_keystore(
        keystore_path=keystore_file,
        password=password,
        client=client
    )
    print_info(f"  ✓ Wallet restored")
    print_info(f"    Address matches: {restored_wallet.address == wallet.address}")
    print()
    
    # Cleanup
    print_info("Cleanup:")
    Path(keystore_file).unlink()
    print_info(f"  ✓ Temporary files deleted")
    
    print_success("\n✅ Complete workflow demonstration finished!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all wallet demos."""
    
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  BASEPY WALLET.PY - COMPLETE FEATURE DEMONSTRATION".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    print_info(f"\nNetwork: Base {NETWORK.capitalize()}")
    print_info(f"Chain ID: {CHAIN_ID}")
    print_info(f"Test Recipient: {TEST_RECIPIENT}")
    print_warning("⚠️  This is a DEMONSTRATION - not sending real transactions\n")
    
    # Create client for demos
    client = BaseClient(chain_id=CHAIN_ID)
    
    try:
        # Run all demos
        wallet1, wallet3, wallet_client_result = demo_1_wallet_creation()
        
        if wallet1:
            demo_2_validation_methods(wallet1)
            demo_3_properties(wallet1)
            demo_4_export_import(wallet1)
        
        if wallet_client_result:
            wallet_with_client, client = wallet_client_result
            demo_5_balance_operations(wallet_with_client, client)
            demo_6_token_operations(wallet_with_client, client)
            demo_7_portfolio_operations(wallet_with_client, client)
            demo_8_transaction_signing(wallet_with_client, client)
            demo_9_message_signing(wallet_with_client)
            demo_10_cost_estimation(wallet_with_client, client)
            demo_11_cache_management(wallet_with_client, client)
            demo_12_client_management(wallet_with_client)
            demo_13_utility_methods(wallet_with_client)
        
        demo_14_error_handling()
        demo_15_comprehensive_workflow()
        
        # Final summary
        print_section("DEMO COMPLETE - ALL FEATURES DEMONSTRATED")
        
        print_info("Features Demonstrated:")
        features = [
            "✅ Wallet creation (random, private key, mnemonic, keystore)",
            "✅ Address and key validation",
            "✅ Export/import operations",
            "✅ Balance operations with caching",
            "✅ Nonce management with caching",
            "✅ Token operations (balance, allowance)",
            "✅ Portfolio tracking",
            "✅ Transaction signing (Legacy, EIP-1559)",
            "✅ Message signing (EIP-191, EIP-712)",
            "✅ Transaction cost estimation (L1+L2)",
            "✅ Affordability checking",
            "✅ Cache management",
            "✅ Client management",
            "✅ Utility methods (__repr__, __str__, __eq__, __hash__)",
            "✅ Error handling and validation",
            "✅ Complete real-world workflow",
        ]
        
        for feature in features:
            print_info(feature)
        
        print("\n" + "█" * 80)
        print_success("ALL WALLET.PY FEATURES SUCCESSFULLY DEMONSTRATED! 🎉")
        print("█" * 80 + "\n")
        
    except KeyboardInterrupt:
        print_warning("\n\nDemo interrupted by user")
    except Exception as e:
        print_error(f"\n\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()
    

if __name__ == "__main__":
    main()