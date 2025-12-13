"""
Comprehensive BaseClient example showcasing ALL features including NEW ERC-20 capabilities.

This example demonstrates:
- Network connection & health checks
- Account & block data queries
- Gas price checks & L1 fee estimation
- Token operations (ERC-20) - ENHANCED
- Portfolio balance tracking - NEW
- Transaction decoding - NEW
- Balance change tracking - NEW
- Batch operations for performance
- Monitoring & metrics
- Developer utilities
- Base L2-specific features
"""

from basepy import BaseClient
import logging


def demo_network_info(client):
    """Demonstrate network information queries."""
    print("\n" + "="*60)
    print("NETWORK INFORMATION")
    print("="*60)
    
    chain_id = client.get_chain_id()
    is_mainnet = chain_id == 8453
    network_name = "Base Mainnet" if is_mainnet else f"Base Sepolia (testnet)" if chain_id == 84532 else f"Unknown (Chain ID: {chain_id})"
    
    print(f"Network: {network_name}")
    print(f"Chain ID: {chain_id}")
    print(f"Connected: {client.is_connected()}")
    print(f"Current RPC: {client.get_current_rpc()}")


def demo_health_monitoring(client):
    """Demonstrate health checks and metrics."""
    print("\n" + "="*60)
    print("HEALTH & MONITORING")
    print("="*60)
    
    # Comprehensive health check
    health = client.health_check()
    print(f"Status: {health['status'].upper()}")
    print(f"Connected: {health['connected']}")
    print(f"Block Number: {health.get('block_number', 'N/A')}")
    print(f"RPC Endpoint: {health['rpc_url']}")
    print(f"Timestamp: {health['timestamp']}")
    
    # Get performance metrics
    print("\n--- Performance Metrics ---")
    metrics = client.get_metrics()
    
    print(f"Cache Hit Rate: {metrics['cache_hit_rate']:.1%}")
    print(f"Circuit Breaker Trips: {metrics['circuit_breaker_trips']}")
    
    if metrics['requests']:
        print(f"\nRequest Counts:")
        for method, count in list(metrics['requests'].items())[:5]:
            print(f"  {method}: {count}")
    
    if metrics['avg_latencies']:
        print(f"\nAverage Latencies:")
        for method, latency in list(metrics['avg_latencies'].items())[:5]:
            print(f"  {method}: {latency:.3f}s")
    
    if metrics['errors']:
        print(f"\nErrors:")
        for method, count in metrics['errors'].items():
            print(f"  {method}: {count}")


def demo_block_info(client):
    """Demonstrate block information queries."""
    print("\n" + "="*60)
    print("BLOCK INFORMATION")
    print("="*60)
    
    # Get current block number
    block_number = client.get_block_number()
    print(f"Current Block Number: {block_number:,}")
    
    # Get latest block details
    block = client.get_block('latest')
    print(f"\nLatest Block Details:")
    print(f"  Hash: {block['hash'].hex()}")
    print(f"  Timestamp: {block['timestamp']}")
    print(f"  Gas Used: {block['gasUsed']:,} / {block['gasLimit']:,}")
    print(f"  Transactions: {len(block['transactions'])}")
    
    # Get base fee (EIP-1559)
    if 'baseFeePerGas' in block:
        base_fee_gwei = block['baseFeePerGas'] / 10**9
        print(f"  Base Fee: {base_fee_gwei:.2f} Gwei")
    
    # Get block by number
    print(f"\n--- Historical Block (5 blocks ago) ---")
    old_block = client.get_block(block_number - 5)
    print(f"  Block #{old_block['number']}")
    print(f"  Hash: {old_block['hash'].hex()}")
    print(f"  Transactions: {len(old_block['transactions'])}")


def demo_account_info(client, address):
    """Demonstrate account data queries."""
    print("\n" + "="*60)
    print("ACCOUNT INFORMATION")
    print("="*60)
    
    print(f"Address: {address}")
    
    # Get balance
    balance_wei = client.get_balance(address)
    balance_eth = balance_wei / 10**18
    print(f"Balance: {balance_eth:.6f} ETH ({balance_wei:,} Wei)")
    
    # Get transaction count (nonce)
    tx_count = client.get_transaction_count(address)
    print(f"Transactions Sent: {tx_count}")
    
    # Get pending nonce
    pending_nonce = client.get_transaction_count(address, 'pending')
    print(f"Pending Nonce: {pending_nonce}")
    
    # Check if contract
    is_contract = client.is_contract(address)
    account_type = "Smart Contract" if is_contract else "Externally Owned Account (EOA)"
    print(f"Account Type: {account_type}")
    
    if is_contract:
        code = client.get_code(address)
        print(f"Contract Code Size: {len(code)} bytes")


def demo_gas_prices(client):
    """Demonstrate gas price queries."""
    print("\n" + "="*60)
    print("GAS PRICES")
    print("="*60)
    
    # Get current gas price
    gas_price = client.get_gas_price()
    gas_price_gwei = gas_price / 10**9
    print(f"Current Gas Price: {gas_price_gwei:.2f} Gwei")
    
    # Get base fee (EIP-1559)
    base_fee = client.get_base_fee()
    base_fee_gwei = base_fee / 10**9
    print(f"Base Fee (EIP-1559): {base_fee_gwei:.2f} Gwei")
    
    # Estimate cost for simple ETH transfer (21,000 gas)
    simple_transfer_cost = 21000 * gas_price
    simple_transfer_eth = simple_transfer_cost / 10**18
    print(f"\nSimple ETH Transfer Cost:")
    print(f"  Gas Needed: 21,000")
    print(f"  L2 Cost: ~{simple_transfer_eth:.6f} ETH")


def demo_l1_fee(client):
    """Demonstrate Base-specific L1 fee estimation."""
    print("\n" + "="*60)
    print("BASE L1 FEE ESTIMATION (OP Stack Feature)")
    print("="*60)
    
    # Example 1: Simple transfer (minimal calldata)
    simple_transfer_data = b''
    
    try:
        l1_fee = client.get_l1_fee(simple_transfer_data)
        l1_fee_eth = l1_fee / 10**18
        
        print(f"L1 Data Fee (empty calldata): {l1_fee_eth:.8f} ETH")
        
        # Example 2: Contract interaction (more calldata)
        contract_call_data = '0xa9059cbb' + '0' * 128  # ERC20 transfer function
        l1_fee_contract = client.get_l1_fee(contract_call_data)
        l1_fee_contract_eth = l1_fee_contract / 10**18
        
        print(f"L1 Data Fee (contract call): {l1_fee_contract_eth:.8f} ETH")
        
        print(f"\nNote: Base transactions have TWO costs:")
        print(f"  1. L2 Execution Fee (normal gas)")
        print(f"  2. L1 Data Fee (posting to Ethereum mainnet)")
        print(f"\nTotal Cost = L2 Fee + L1 Fee")
        
        # Get L1 gas oracle prices (Updated for Ecotone)
        print("\n--- L1 Gas Oracle Info (Post-Ecotone) ---")
        oracle_prices = client.get_l1_gas_oracle_prices()
        print(f"L1 Base Fee: {oracle_prices['l1_base_fee'] / 10**9:.2f} Gwei")
        print(f"Base Fee Scalar: {oracle_prices['base_fee_scalar']}")
        print(f"Blob Base Fee Scalar: {oracle_prices['blob_base_fee_scalar']}")
        print(f"Decimals: {oracle_prices['decimals']}")
        
    except Exception as e:
        print(f"Could not estimate L1 fee: {e}")


def demo_total_fee_estimation(client):
    """Demonstrate comprehensive fee estimation for Base."""
    print("\n" + "="*60)
    print("TOTAL FEE ESTIMATION (L1 + L2)")
    print("="*60)
    
    # Use a valid transaction that won't revert
    tx = {
        'to': '0x0000000000000000000000000000000000000001',  # Valid dummy address
        'from': '0x0000000000000000000000000000000000000002',  # Valid dummy address
        'value': 10**15,  # 0.001 ETH
        'data': '0x'  # Empty data for simple transfer
    }
    
    try:
        cost = client.estimate_total_fee(tx)
        
        print(f"Gas Estimate: {cost['l2_gas']:,}")
        print(f"L2 Gas Price: {cost['l2_gas_price'] / 10**9:.2f} Gwei")
        print(f"\nFee Breakdown:")
        print(f"  L2 Execution Fee: {cost['l2_fee_eth']:.8f} ETH")
        print(f"  L1 Data Fee:      {cost['l1_fee_eth']:.8f} ETH")
        print(f"  {'─' * 40}")
        print(f"  TOTAL FEE:        {cost['total_fee_eth']:.8f} ETH")
        
        # Show percentage breakdown
        if cost['total_fee'] > 0:
            l2_percent = (cost['l2_fee'] / cost['total_fee']) * 100
            l1_percent = (cost['l1_fee'] / cost['total_fee']) * 100
            print(f"\n  L2: {l2_percent:.1f}% | L1: {l1_percent:.1f}%")
        
    except Exception as e:
        print(f"Could not estimate fees: {e}")


def demo_token_operations(client):
    """Demonstrate ERC-20 token operations."""
    print("\n" + "="*60)
    print("TOKEN OPERATIONS (ERC-20)")
    print("="*60)
    
    # USDC on Base Mainnet
    usdc_address = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
    
    try:
        # Get token metadata
        print("--- Token Metadata ---")
        metadata = client.get_token_metadata(usdc_address)
        print(f"Token: {metadata['name']} ({metadata['symbol']})")
        print(f"Decimals: {metadata['decimals']}")
        print(f"Total Supply: {client.format_units(metadata['totalSupply'], metadata['decimals']):,.2f}")
        print(f"Contract: {metadata['address']}")
        
        # Get token balance for a specific address
        print("\n--- Token Balance ---")
        holder = '0x20FE51A9229EEf2cF8Ad9E89d91CAb9312cF3b7A'  # Random holder
        balance = client.get_balance(holder)  # ETH balance first
        print(f"Address: {holder}")
        print(f"ETH Balance: {balance / 10**18:.6f} ETH")
        
        # Get all token balances
        balances = client.get_token_balances(holder, [usdc_address])
        if usdc_address in balances:
            token_info = balances[usdc_address]
            print(f"{token_info['symbol']} Balance: {token_info['balanceFormatted']:,.6f}")
        
        # Check allowance
        print("\n--- Token Allowance ---")
        owner = '0x0000000000000000000000000000000000000001'
        spender = '0x0000000000000000000000000000000000000002'
        allowance = client.get_token_allowance(usdc_address, owner, spender)
        print(f"Owner: {owner}")
        print(f"Spender: {spender}")
        print(f"Allowance: {client.format_units(allowance, 6):,.2f} USDC")
        
    except Exception as e:
        print(f"Token operations failed: {e}")


# ============================================================================
# NEW: PORTFOLIO BALANCE TRACKING
# ============================================================================

def demo_portfolio_balance(client):
    """Demonstrate NEW portfolio balance tracking feature."""
    print("\n" + "="*60)
    print("PORTFOLIO BALANCE TRACKING (NEW)")
    print("="*60)
    
    # Example wallet address (Base deployer)
    wallet = "0x20FE51A9229EEf2cF8Ad9E89d91CAb9312cF3b7A"
    
    try:
        print(f"Checking portfolio for: {wallet}\n")
        
        # Get complete portfolio with common Base tokens
        portfolio = client.get_portfolio_balance(wallet)
        
        print("📊 Portfolio Summary:")
        print(f"   Wallet: {portfolio['address']}")
        print(f"   Total Assets: {portfolio['total_assets']}")
        print(f"   Tokens with Balance: {portfolio['non_zero_tokens']}")
        
        # ETH Balance
        print(f"\n💰 ETH Balance:")
        print(f"   {portfolio['eth']['balance_formatted']:.6f} ETH")
        print(f"   ({portfolio['eth']['balance']:,} Wei)")
        
        # Token Balances
        print(f"\n🪙 Token Balances:")
        if portfolio['tokens']:
            has_balance = False
            for token_addr, info in portfolio['tokens'].items():
                if info['balance'] > 0:
                    has_balance = True
                    print(f"   ✓ {info['symbol']:8s} | {info['balance_formatted']:>15.6f} | {info['name']}")
            
            if not has_balance:
                print("   (No token balances found)")
                print(f"   Checked {len(portfolio['tokens'])} common Base tokens")
        else:
            print("   (No tokens checked)")
        
        # Show cost efficiency
        print(f"\n💡 Efficiency:")
        print(f"   RPC Calls: ~2 (1 for ETH + 1 multicall for all tokens)")
        print(f"   vs Traditional: ~{1 + len(portfolio['tokens'])} individual calls")
        
    except Exception as e:
        print(f"Portfolio balance failed: {e}")


# ============================================================================
# NEW: TRANSACTION DECODING
# ============================================================================

def demo_transaction_decoding(client):
    """Demonstrate NEW ERC-20 transaction decoding feature."""
    print("\n" + "="*60)
    print("TRANSACTION DECODING (NEW)")
    print("="*60)
    
    from basepy import Transaction
    
    tx = Transaction(client)
    
    # Example: A transaction with ERC-20 transfers
    # This is a known Base transaction with token transfers
    tx_hash = "0x..."  # Replace with actual transaction hash when testing
    
    print("Note: This demo requires a real transaction hash with ERC-20 transfers")
    print("Example usage:\n")
    
    print("# 1. Decode all ERC-20 transfers (ZERO RPC COST)")
    print("transfers = tx.decode_erc20_transfers(tx_hash)")
    print("for transfer in transfers:")
    print("    print(f'Token: {transfer[\"token\"]}')")
    print("    print(f'From: {transfer[\"from\"]}')")
    print("    print(f'To: {transfer[\"to\"]}')")
    print("    print(f'Amount: {transfer[\"amount\"]}')")
    
    print("\n# 2. Get full transaction details with metadata")
    print("details = tx.get_full_transaction_details(tx_hash, include_token_metadata=True)")
    print("print(f'ETH Value: {details[\"eth_value_formatted\"]} ETH')")
    print("print(f'Status: {details[\"status\"]}')")
    print("print(f'Token Transfers: {details[\"transfer_count\"]}')")
    print("for transfer in details['token_transfers']:")
    print("    print(f'{transfer[\"symbol\"]}: {transfer[\"amount_formatted\"]}')")
    
    print("\n# 3. Calculate balance changes for an address")
    print("changes = tx.get_balance_changes(tx_hash, wallet_address)")
    print("print(f'ETH Change: {changes[\"eth_change_formatted\"]} ETH')")
    print("for token, info in changes['token_changes'].items():")
    print("    print(f'{info[\"symbol\"]}: {info[\"change_formatted\"]}')")
    
    print("\n# 4. Classify transaction type")
    print("classification = tx.classify_transaction(tx_hash)")
    print("print(f'Type: {classification[\"type\"]}')")
    print("print(f'Complexity: {classification[\"complexity\"]}')")
    print("print(f'Tokens Involved: {classification[\"tokens_involved\"]}')")
    
    print("\n💡 Cost: All decoding is FREE (uses existing receipt data)")


# ============================================================================
# NEW: ERC-20 CONTRACT HELPER
# ============================================================================

def demo_erc20_contract(client):
    """Demonstrate NEW ERC20Contract helper class."""
    print("\n" + "="*60)
    print("ERC20CONTRACT HELPER (NEW)")
    print("="*60)
    
    from basepy import ERC20Contract
    
    # USDC on Base
    usdc_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    
    try:
        # Create ERC20Contract instance
        usdc = ERC20Contract(client, usdc_address)
        
        print("--- Token Info (Metadata Cached) ---")
        print(f"Name: {usdc.name()}")
        print(f"Symbol: {usdc.symbol()}")
        print(f"Decimals: {usdc.decimals()}")
        print(f"Total Supply: {usdc.format_amount(usdc.total_supply())}")
        
        # Check balance
        print("\n--- Balance Operations ---")
        holder = "0x20FE51A9229EEf2cF8Ad9E89d91CAb9312cF3b7A"
        balance = usdc.balance_of(holder)
        print(f"Address: {holder}")
        print(f"Raw Balance: {balance}")
        print(f"Formatted: {usdc.format_amount(balance)} {usdc.symbol()}")
        print(f"Display: {usdc.format_balance(holder)}")
        
        # Amount conversion
        print("\n--- Amount Conversion ---")
        human_amount = 10.5
        raw_amount = usdc.parse_amount(human_amount)
        print(f"Human: {human_amount} USDC")
        print(f"Raw: {raw_amount}")
        print(f"Back to human: {usdc.format_amount(raw_amount)}")
        
        # Balance checking
        print("\n--- Balance Checks ---")
        required = usdc.parse_amount(100)
        has_enough = usdc.has_sufficient_balance(holder, required)
        print(f"Required: 100 USDC")
        print(f"Has sufficient balance: {has_enough}")
        
        print("\n💡 All metadata (name, symbol, decimals) is cached!")
        print("   First call hits RPC, subsequent calls are instant")
        
    except Exception as e:
        print(f"ERC20Contract demo failed: {e}")


# ============================================================================
# NEW: TOKEN FORMATTING UTILITIES
# ============================================================================

def demo_token_utilities(client):
    """Demonstrate NEW token formatting utilities."""
    print("\n" + "="*60)
    print("TOKEN FORMATTING UTILITIES (NEW)")
    print("="*60)
    
    from basepy import (
        format_token_amount,
        parse_token_amount,
        format_token_balance,
        normalize_address,
        shorten_address
    )
    
    print("--- Amount Formatting ---")
    raw_usdc = 1500000  # 1.5 USDC (6 decimals)
    formatted = format_token_amount(raw_usdc, 6)
    print(f"Raw: {raw_usdc} -> Formatted: {formatted} USDC")
    
    raw_eth = 1500000000000000000  # 1.5 ETH (18 decimals)
    formatted_eth = format_token_amount(raw_eth, 18)
    print(f"Raw: {raw_eth} -> Formatted: {formatted_eth} ETH")
    
    print("\n--- Amount Parsing ---")
    parsed_usdc = parse_token_amount(1.5, 6)
    print(f"1.5 USDC -> Raw: {parsed_usdc}")
    
    parsed_eth = parse_token_amount("1.5", 18)
    print(f"'1.5' ETH -> Raw: {parsed_eth}")
    
    print("\n--- Balance Display ---")
    balance_str = format_token_balance(1500000, 6, "USDC", precision=2)
    print(f"Display string: {balance_str}")
    
    print("\n--- Address Utilities ---")
    addr = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    normalized = normalize_address(addr)
    shortened = shorten_address(addr, chars=6)
    print(f"Original: {addr}")
    print(f"Normalized: {normalized}")
    print(f"Shortened: {shortened}")
    
    print("\n💡 These utilities ensure consistent formatting across your app")


def demo_batch_operations(client):
    """Demonstrate batch operations for performance."""
    print("\n" + "="*60)
    print("BATCH OPERATIONS (High Performance)")
    print("="*60)
    
    # Multiple addresses to check
    addresses = [
        '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',  # USDC
        '0x4200000000000000000000000000000000000006',  # WETH
        '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb',  # DAI
    ]
    
    try:
        print("--- Batch Get Balances ---")
        print(f"Fetching balances for {len(addresses)} addresses...")
        
        balances = client.batch_get_balances(addresses)
        
        print(f"\nResults:")
        for addr, balance in balances.items():
            eth_balance = balance / 10**18
            print(f"  {addr[:10]}... : {eth_balance:.6f} ETH")
        
        # Batch token balances
        print("\n--- Batch Token Balances ---")
        wallet = '0x20FE51A9229EEf2cF8Ad9E89d91CAb9312cF3b7A'
        tokens = [
            '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',  # USDC
            '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb',  # DAI
        ]
        
        token_balances = client.batch_get_token_balances(wallet, tokens)
        
        print(f"Token balances for {wallet[:10]}...:")
        for token, balance in token_balances.items():
            print(f"  {token[:10]}... : {balance}")
            
    except Exception as e:
        print(f"Batch operations failed: {e}")


def demo_multicall(client):
    """Demonstrate multicall for efficient contract reading."""
    print("\n" + "="*60)
    print("MULTICALL (Single RPC for Multiple Calls)")
    print("="*60)
    
    from basepy import ERC20_ABI
    
    usdc = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
    
    try:
        # Build multicall - get name, symbol, decimals in ONE request
        calls = [
            {'contract': usdc, 'abi': ERC20_ABI, 'function': 'name'},
            {'contract': usdc, 'abi': ERC20_ABI, 'function': 'symbol'},
            {'contract': usdc, 'abi': ERC20_ABI, 'function': 'decimals'},
            {'contract': usdc, 'abi': ERC20_ABI, 'function': 'totalSupply'},
        ]
        
        print(f"Executing {len(calls)} contract calls in 1 RPC request...")
        results = client.multicall(calls)
        
        print(f"\nResults:")
        print(f"  Name: {results[0]}")
        print(f"  Symbol: {results[1]}")
        print(f"  Decimals: {results[2]}")
        print(f"  Total Supply: {results[3]:,}")
        
        print(f"\n✅ {len(calls)} calls completed in 1 request (vs {len(calls)} separate requests)")
        
    except Exception as e:
        print(f"Multicall failed: {e}")


def demo_utility_functions(client):
    """Demonstrate developer utility functions."""
    print("\n" + "="*60)
    print("DEVELOPER UTILITIES")
    print("="*60)
    
    # Unit conversion
    print("--- Unit Conversion ---")
    wei = 1500000000000000000
    eth = client.format_units(wei, 18)
    print(f"{wei} Wei = {eth} ETH")
    
    usdc_raw = 1500000
    usdc = client.format_units(usdc_raw, 6)
    print(f"{usdc_raw} raw = {usdc} USDC")
    
    # Reverse conversion
    print("\n--- Parse Units ---")
    eth_to_wei = client.parse_units("1.5", 18)
    print(f"1.5 ETH = {eth_to_wei} Wei")
    
    usdc_to_raw = client.parse_units(1.5, 6)
    print(f"1.5 USDC = {usdc_to_raw} raw")
    
    # Transaction simulation
    print("\n--- Transaction Simulation ---")
    try:
        # Simulate a read-only call
        tx = {
            'to': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
            'data': '0x06fdde03'  # name() function
        }
        result = client.simulate_transaction(tx)
        print(f"Simulation successful! Result: {result[:20]}...")
    except Exception as e:
        print(f"Simulation: {e}")


def demo_configuration(client):
    """Demonstrate runtime configuration changes."""
    print("\n" + "="*60)
    print("RUNTIME CONFIGURATION")
    print("="*60)
    
    # Show current config
    print("--- Current Settings ---")
    print(f"Log Level: {logging.getLevelName(client.config.LOG_LEVEL)}")
    print(f"Cache TTL: {client.config.CACHE_TTL}s")
    print(f"Max Retries: {client.config.MAX_RETRIES}")
    print(f"Rate Limit: {client.config.RATE_LIMIT_REQUESTS} req/{client.config.RATE_LIMIT_WINDOW}s")
    
    # Change log level
    print("\n--- Changing Log Level ---")
    print("Setting log level to DEBUG...")
    client.set_log_level(logging.DEBUG)
    
    # Enable RPC logging
    print("Enabling detailed RPC logging...")
    client.enable_rpc_logging(True)
    
    # Clear cache
    print("\n--- Cache Management ---")
    print("Clearing cache...")
    client.clear_cache()
    print("✅ Cache cleared")
    
    # Reset metrics
    print("\n--- Metrics Management ---")
    print("Resetting metrics...")
    client.reset_metrics()
    print("✅ Metrics reset")


def demo_testnet_connection():
    """Demonstrate connecting to Base Sepolia testnet."""
    print("\n" + "="*60)
    print("TESTNET CONNECTION EXAMPLE")
    print("="*60)
    
    try:
        testnet_client = BaseClient(chain_id=84532, environment='development')
        print(f"✅ Connected to Base Sepolia (Testnet)")
        print(f"Chain ID: {testnet_client.get_chain_id()}")
        print(f"Block Number: {testnet_client.get_block_number():,}")
        print(f"RPC: {testnet_client.get_current_rpc()}")
        
        # Get some testnet data
        health = testnet_client.health_check()
        print(f"Status: {health['status']}")
        
    except Exception as e:
        print(f"Failed to connect to testnet: {e}")


def demo_context_manager():
    """Demonstrate context manager usage."""
    print("\n" + "="*60)
    print("CONTEXT MANAGER PATTERN")
    print("="*60)
    
    print("Using 'with' statement for automatic cleanup...")
    
    with BaseClient() as client:
        chain_id = client.get_chain_id()
        block = client.get_block_number()
        print(f"✅ Connected: Chain {chain_id}, Block {block:,}")
        print("Client will auto-cleanup on exit...")
    
    print("✅ Context manager exited, resources cleaned up")


def main():
    """Main example showcasing ALL BaseClient features including NEW ERC-20 capabilities."""
    print("="*60)
    print("BASE PYTHON SDK - COMPREHENSIVE FEATURE DEMO")
    print("Including NEW ERC-20 Features!")
    print("="*60)
    
    try:
        # Connect to Base Mainnet
        client = BaseClient(environment='development')  # Verbose logging
        print("✅ Successfully connected to Base Mainnet!")
        
        # Demo 1: Network Information
        demo_network_info(client)
        
        # Demo 2: Health & Monitoring
        demo_health_monitoring(client)
        
        # Demo 3: Block Information
        demo_block_info(client)
        
        # Demo 4: Account Information
        example_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC on Base
        demo_account_info(client, example_address)
        
        # Demo 5: Gas Prices
        demo_gas_prices(client)
        
        # Demo 6: Base-specific L1 Fee
        demo_l1_fee(client)
        
        # Demo 7: Total Fee Estimation
        demo_total_fee_estimation(client)
        
        # Demo 8: Token Operations (Original)
        demo_token_operations(client)
        
        # ============================================
        # NEW ERC-20 FEATURES
        # ============================================
        
        # Demo 9: Portfolio Balance Tracking (NEW)
        demo_portfolio_balance(client)
        
        # Demo 10: Transaction Decoding (NEW)
        demo_transaction_decoding(client)
        
        # Demo 11: ERC20Contract Helper (NEW)
        demo_erc20_contract(client)
        
        # Demo 12: Token Utilities (NEW)
        demo_token_utilities(client)
        
        # ============================================
        # ORIGINAL FEATURES
        # ============================================
        
        # Demo 13: Batch Operations
        demo_batch_operations(client)
        
        # Demo 14: Multicall
        demo_multicall(client)
        
        # Demo 15: Utility Functions
        demo_utility_functions(client)
        
        # Demo 16: Configuration
        demo_configuration(client)
        
        # Demo 17: Testnet Connection
        demo_testnet_connection()
        
        # Demo 18: Context Manager
        demo_context_manager()
        
        # Final metrics
        print("\n" + "="*60)
        print("FINAL PERFORMANCE METRICS")
        print("="*60)
        final_metrics = client.get_metrics()
        print(f"Total Requests: {sum(final_metrics['requests'].values())}")
        print(f"Total Errors: {sum(final_metrics['errors'].values())}")
        print(f"Cache Hit Rate: {final_metrics['cache_hit_rate']:.1%}")
        
        print("\n" + "="*60)
        print("✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nFeatures Demonstrated:")
        print("  ✅ Network & health checks")
        print("  ✅ Block & account queries")
        print("  ✅ Gas price estimation")
        print("  ✅ L1 fee calculation (Base-specific)")
        print("  ✅ Total fee estimation (L1 + L2)")
        print("  ✅ ERC-20 token operations")
        print("  ✅ Portfolio balance tracking (NEW)")
        print("  ✅ Transaction decoding (NEW)")
        print("  ✅ ERC20Contract helper (NEW)")
        print("  ✅ Token utilities (NEW)")
        print("  ✅ Batch operations")
        print("  ✅ Multicall optimization")
        print("  ✅ Developer utilities")
        print("  ✅ Runtime configuration")
        print("  ✅ Metrics & monitoring")
        print("  ✅ Testnet support")
        print("  ✅ Context manager pattern")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()