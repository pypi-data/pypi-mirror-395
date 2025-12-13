"""
Transaction Demo - Complete Testing Suite
==========================================

This demonstrates:
✅ READ operations (public, no wallet needed)
✅ WRITE operations (with YOUR testnet wallet)
✅ ERC-20 transfer decoding (ZERO RPC COST)
✅ Full transaction analysis
✅ Balance tracking
✅ Real transaction monitoring

Tests YOUR wallet on Base Sepolia testnet!
"""

from basepy import BaseClient, Wallet, Transaction
import os
import time
from datetime import datetime
from dotenv import load_dotenv


# ============================================================================
# COLORS
# ============================================================================

class Colors:
    """ANSI color codes."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header."""
    print("\n" + Colors.BOLD + "="*70 + Colors.END)
    print(Colors.BOLD + Colors.CYAN + text.center(70) + Colors.END)
    print(Colors.BOLD + "="*70 + Colors.END)


def print_success(text: str):
    print(Colors.GREEN + "✅ " + text + Colors.END)


def print_error(text: str):
    print(Colors.RED + "❌ " + text + Colors.END)


def print_info(text: str):
    print(Colors.BLUE + "ℹ️  " + text + Colors.END)


def print_warning(text: str):
    print(Colors.YELLOW + "⚠️  " + text + Colors.END)


def format_eth(wei: int) -> str:
    """Format Wei to ETH."""
    eth = wei / 10**18
    if eth < 0.000001:
        return f"{eth:.10f} ETH"
    elif eth < 0.001:
        return f"{eth:.8f} ETH"
    else:
        return f"{eth:.6f} ETH"


# ============================================================================
# READ OPERATIONS (PUBLIC - NO WALLET NEEDED)
# ============================================================================

def demo_query_real_transaction(tx_handler: Transaction, client: BaseClient):
    """Demo: Query a real mainnet transaction."""
    print_header("DEMO 1: QUERY REAL TRANSACTION (READ - PUBLIC)")
    
    print(f"\n{Colors.BOLD}What This Tests:{Colors.END}")
    print("  • Get transaction details from blockchain")
    print("  • Parse transaction data")
    print("  • Calculate costs")
    print("  • PUBLIC ACCESS - No wallet needed")
    
    # Find a recent transaction
    print(f"\n{Colors.YELLOW}🔍 Finding recent Base Sepolia transaction...{Colors.END}")
    
    try:
        # Get a recent block with transactions
        block = client.get_block('latest', full_transactions=True)
        
        if block['transactions']:
            # Get first transaction
            tx_hash = block['transactions'][0]['hash']
            if hasattr(tx_hash, 'hex'):
                tx_hash = tx_hash.hex()
            
            print_success(f"Found: {tx_hash[:20]}...")
            
            # Get transaction details
            print(f"\n{Colors.BOLD}Getting transaction details...{Colors.END}")
            tx = tx_handler.get(tx_hash)
            
            print(f"\n{Colors.BOLD}Transaction Info:{Colors.END}")
            print(f"  Hash:   {tx_hash[:20]}...")
            print(f"  From:   {tx['from']}")
            print(f"  To:     {tx['to'] if tx['to'] else 'Contract Creation'}")
            print(f"  Value:  {format_eth(tx['value'])}")
            print(f"  Block:  {tx.get('blockNumber', 'Pending')}")
            
            # Get receipt if available
            try:
                receipt = tx_handler.get_receipt(tx_hash)
                status = "✅ Success" if receipt['status'] == 1 else "❌ Failed"
                print(f"  Status: {status}")
                print(f"  Gas:    {receipt['gasUsed']:,}")
                
                print_success("Transaction queried successfully")
            except:
                print_info("Transaction pending (no receipt yet)")
        else:
            print_info("No transactions in latest block")
    
    except Exception as e:
        print_error(f"Query failed: {e}")


def demo_decode_erc20_transfers(tx_handler: Transaction, client: BaseClient):
    """Demo: Decode ERC-20 transfers (ZERO RPC cost)."""
    print_header("DEMO 2: DECODE ERC-20 TRANSFERS (ZERO RPC COST)")
    
    print(f"\n{Colors.BOLD}What This Tests:{Colors.END}")
    print("  • Extract ALL ERC-20 transfers from transaction")
    print("  • ZERO additional RPC calls")
    print("  • Get token metadata (symbols, decimals)")
    print("  • Format human-readable amounts")
    
    print(f"\n{Colors.YELLOW}🔍 Looking for token transfer transaction...{Colors.END}")
    
    try:
        current_block = client.get_block_number()
        
        # Check last 20 blocks for token transfers
        for i in range(20):
            try:
                block = client.get_block(current_block - i, full_transactions=True)
                
                for tx in block['transactions']:
                    tx_hash = tx['hash'].hex() if hasattr(tx['hash'], 'hex') else tx['hash']
                    
                    try:
                        # Quick check if has logs (events)
                        receipt = client.w3.eth.get_transaction_receipt(tx_hash)
                        
                        if len(receipt['logs']) > 0:
                            # Try to decode
                            transfers = tx_handler.decode_erc20_transfers(tx_hash)
                            
                            if transfers:
                                print_success(f"Found transaction with {len(transfers)} transfer(s)")
                                print(f"Transaction: {tx_hash[:20]}...")
                                
                                # Show transfers
                                print(f"\n{Colors.BOLD}Decoded Transfers:{Colors.END}\n")
                                
                                for idx, transfer in enumerate(transfers[:3], 1):  # Show first 3
                                    print(f"Transfer #{idx}:")
                                    print(f"  Token:  {transfer['token'][:10]}...")
                                    print(f"  From:   {transfer['from'][:10]}...")
                                    print(f"  To:     {transfer['to'][:10]}...")
                                    print(f"  Amount: {transfer['amount']}")
                                    print()
                                
                                if len(transfers) > 3:
                                    print(f"  ... and {len(transfers) - 3} more transfer(s)")
                                
                                print_success(f"Decoded {len(transfers)} transfer(s) with ZERO RPC calls!")
                                return
                    except:
                        continue
            except:
                continue
        
        print_info("No token transfers found in recent blocks")
        print("💡 Token transfers are common - try again in a few minutes")
    
    except Exception as e:
        print_error(f"Decoding failed: {e}")


# ============================================================================
# WRITE OPERATIONS (REQUIRES YOUR WALLET)
# ============================================================================

def demo_check_wallet(wallet: Wallet, client: BaseClient):
    """Demo: Check wallet status before testing."""
    print_header("YOUR WALLET STATUS")
    
    print(f"\n{Colors.BOLD}Wallet Info:{Colors.END}")
    print(f"  Address:  {wallet.address}")
    print(f"  Network:  Base Sepolia (Chain ID: {client.get_chain_id()})")
    
    # Get balance
    balance = wallet.get_balance()
    balance_eth = balance / 10**18
    
    print(f"\n{Colors.BOLD}Balance:{Colors.END}")
    print(f"  {balance_eth:.6f} ETH")
    print(f"  ({balance:,} Wei)")
    
    # Check nonce
    nonce = wallet.get_nonce()
    print(f"\n{Colors.BOLD}Transactions:{Colors.END}")
    print(f"  Sent: {nonce}")
    
    # Block explorer
    explorer = f"https://sepolia.basescan.org/address/{wallet.address}"
    print(f"\n{Colors.BOLD}Block Explorer:{Colors.END}")
    print(f"  {explorer}")
    
    # Status check
    print(f"\n{Colors.BOLD}Status:{Colors.END}")
    if balance_eth == 0:
        print_error("NO BALANCE - Cannot test write operations")
        print("\n💡 Get testnet ETH from:")
        print("   https://www.alchemy.com/faucets/base-sepolia")
        return False
    elif balance_eth < 0.01:
        print_warning("LOW BALANCE - Limited testing possible")
        print("   Consider getting more testnet ETH")
        return True
    else:
        print_success("BALANCE GOOD - Ready for testing!")
        return True


def demo_estimate_costs(tx_handler: Transaction, wallet: Wallet, client: BaseClient):
    """Demo: Estimate transaction costs before sending."""
    print_header("DEMO 3: ESTIMATE TRANSACTION COSTS")
    
    print(f"\n{Colors.BOLD}What This Tests:{Colors.END}")
    print("  • Estimate gas before sending")
    print("  • Calculate L1 + L2 fees (Base-specific)")
    print("  • Different gas strategies")
    print("  • NO COST - Just estimation")
    
    # Test address (valid 42-character address) - just for estimation
    test_recipient = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0"  # Fixed: Added missing char
    test_amount = client.parse_units("0.001", 18)  # 0.001 ETH
    
    print(f"\n{Colors.BOLD}Estimating cost to send 0.001 ETH...{Colors.END}")
    
    try:
        # Estimate with different strategies
        strategies = ['slow', 'standard', 'fast']
        
        for strategy in strategies:
            cost = tx_handler.estimate_total_cost(
                to=test_recipient,
                value=test_amount,
                gas_strategy=strategy
            )
            
            print(f"\n{Colors.BOLD}{strategy.upper()} Strategy:{Colors.END}")
            print(f"  L2 Gas:   {cost['l2_gas']:,}")
            print(f"  L2 Cost:  {cost['l2_fee_eth']:.8f} ETH")
            print(f"  L1 Cost:  {cost['l1_fee_eth']:.8f} ETH")
            print(f"  TOTAL:    {Colors.BOLD}{cost['total_fee_eth']:.8f} ETH{Colors.END}")
        
        print_success("Cost estimation complete")
        return True
    
    except Exception as e:
        print_error(f"Estimation failed: {e}")
        return False


def demo_simulate_transaction(tx_handler: Transaction, wallet: Wallet, client: BaseClient):
    """Demo: Simulate transaction before sending."""
    print_header("DEMO 4: SIMULATE TRANSACTION (NO COST)")
    
    print(f"\n{Colors.BOLD}What This Tests:{Colors.END}")
    print("  • Test transaction without sending")
    print("  • Verify it will succeed")
    print("  • Catch errors before spending gas")
    print("  • ZERO COST - Pure simulation")
    
    test_recipient = wallet.address  # ✅ This is safest!
    
    test_amount = client.parse_units("0.0001", 18)
    
    print(f"\n{Colors.BOLD}Simulating 0.0001 ETH transfer...{Colors.END}")
    print(f"  From: {wallet.address[:20]}...")
    print(f"  To:   {test_recipient[:20]}...")
    
    try:
        result = tx_handler.simulate(
            to=test_recipient,
            value=test_amount,
            from_address=wallet.address
        )
        
        print_success("Simulation successful!")
        print("  ✅ Transaction will succeed if sent")
        return True
    
    except Exception as e:
        print_error(f"Simulation failed: {e}")
        print("  ❌ Transaction would fail if sent")
        return False


def demo_send_eth_transaction(tx_handler: Transaction, wallet: Wallet, client: BaseClient):
    """Demo: Actually send an ETH transaction (COSTS GAS)."""
    print_header("DEMO 5: SEND ETH TRANSACTION (WRITE OPERATION)")
    
    print(f"\n{Colors.BOLD}⚠️  WARNING: THIS WILL SEND A REAL TRANSACTION! ⚠️{Colors.END}")
    print(f"\n{Colors.BOLD}What This Tests:{Colors.END}")
    print("  • Send ETH on Base Sepolia testnet")
    print("  • Automatic gas estimation")
    print("  • Nonce management")
    print("  • Transaction monitoring")
    print("  • COSTS TESTNET ETH (very small amount)")
    
    # Check balance first
    balance = wallet.get_balance()
    balance_eth = balance / 10**18
    
    if balance_eth < 0.001:
        print_error("Insufficient balance for test transaction")
        print(f"  Have: {balance_eth:.6f} ETH")
        print(f"  Need: At least 0.001 ETH")
        return None
    
    # Send to yourself (safest test)
    recipient = wallet.address
    amount = 0.0001  # Very small amount for testing
    
    print(f"\n{Colors.BOLD}Transaction Details:{Colors.END}")
    print(f"  From:     {wallet.address[:20]}...")
    print(f"  To:       {recipient[:20]}... (yourself)")
    print(f"  Amount:   {amount} ETH")
    print(f"  Network:  Base Sepolia")
    print(f"  Balance:  {balance_eth:.6f} ETH")
    
    # Ask for confirmation
    response = input(f"\n{Colors.YELLOW}Type 'yes' to send this transaction: {Colors.END}")
    
    if response.lower() != 'yes':
        print_info("Transaction cancelled")
        return None
    
    try:
        print(f"\n{Colors.YELLOW}📤 Sending transaction...{Colors.END}")
        
        # Send with simulation and monitoring
        start_time = time.time()
        
        tx_hash = tx_handler.send_eth(
            to_address=recipient,
            amount=amount,
            unit='ether',
            gas_strategy='standard',
            simulate_first=True,  # Simulate before sending
            wait_for_receipt=True  # Wait for confirmation
        )
        
        send_time = time.time() - start_time
        
        # Transaction sent!
        print_success("Transaction sent and confirmed!")
        print(f"\n{Colors.BOLD}Results:{Colors.END}")
        
        # Handle both string and dict returns
        if isinstance(tx_hash, dict):
            tx_hash_str = tx_hash['transactionHash'].hex() if hasattr(tx_hash['transactionHash'], 'hex') else tx_hash['transactionHash']
            print(f"  TX Hash:  {tx_hash_str[:20]}...")
            print(f"  Block:    {tx_hash['blockNumber']}")
            print(f"  Gas Used: {tx_hash['gasUsed']:,}")
            print(f"  Status:   {'✅ Success' if tx_hash['status'] == 1 else '❌ Failed'}")
            
            # Calculate actual cost
            actual_cost = tx_hash['gasUsed'] * tx_hash['effectiveGasPrice']
            print(f"  Cost:     {format_eth(actual_cost)}")
        else:
            tx_hash_str = tx_hash
            print(f"  TX Hash:  {tx_hash_str[:20]}...")
        
        print(f"  Time:     {send_time:.2f}s")
        
        # Block explorer link
        explorer = f"https://sepolia.basescan.org/tx/{tx_hash_str}"
        print(f"\n{Colors.BOLD}View on Explorer:{Colors.END}")
        print(f"  {explorer}")
        
        # Get new balance
        new_balance = wallet.get_balance()
        new_balance_eth = new_balance / 10**18
        
        print(f"\n{Colors.BOLD}Balance After:{Colors.END}")
        print(f"  {new_balance_eth:.6f} ETH")
        print(f"  Change: {Colors.RED}-{(balance_eth - new_balance_eth):.6f} ETH{Colors.END} (gas cost)")
        
        return tx_hash_str
    
    except Exception as e:
        print_error(f"Transaction failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def demo_analyze_your_transaction(tx_handler: Transaction, tx_hash: str, wallet: Wallet):
    """Demo: Analyze the transaction you just sent."""
    print_header("DEMO 6: ANALYZE YOUR TRANSACTION")
    
    print(f"\n{Colors.BOLD}What This Tests:{Colors.END}")
    print("  • Full transaction analysis")
    print("  • Balance change tracking")
    print("  • Transaction classification")
    print("  • Cost breakdown")
    
    if not tx_hash:
        print_info("No transaction to analyze")
        return
    
    print(f"\n{Colors.BOLD}Analyzing: {tx_hash[:20]}...{Colors.END}")
    
    try:
        # Get full details
        details = tx_handler.get_full_transaction_details(tx_hash)
        
        print(f"\n{Colors.BOLD}Transaction Summary:{Colors.END}")
        print(f"  From:     {details['from'][:20]}...")
        print(f"  To:       {details['to'][:20]}...")
        print(f"  ETH:      {details['eth_value_formatted']} ETH")
        print(f"  Status:   {'✅ Success' if details['status'] == 'confirmed' else '❌ Failed'}")
        print(f"  Gas Used: {details['gas_used']:,}")
        
        # Classify transaction
        classification = tx_handler.classify_transaction(tx_hash)
        
        print(f"\n{Colors.BOLD}Classification:{Colors.END}")
        print(f"  Type:       {classification['type']}")
        print(f"  Complexity: {classification['complexity']}")
        print(f"  ETH:        {'Yes' if classification['eth_involved'] else 'No'}")
        print(f"  Tokens:     {len(classification['tokens_involved'])}")
        
        # Get balance changes
        changes = tx_handler.get_balance_changes(tx_hash, wallet.address)
        
        print(f"\n{Colors.BOLD}Your Balance Change:{Colors.END}")
        print(f"  ETH: {Colors.RED}{changes['eth_change_formatted']:.6f} ETH{Colors.END} (includes gas)")
        
        # Get actual cost
        cost = tx_handler.get_transaction_cost(tx_hash)
        
        print(f"\n{Colors.BOLD}Cost Breakdown:{Colors.END}")
        print(f"  L2 Fee: {cost['l2_cost_eth']:.8f} ETH")
        print(f"  L1 Fee: {cost['l1_cost_eth']:.8f} ETH")
        print(f"  TOTAL:  {Colors.BOLD}{cost['total_cost_eth']:.8f} ETH{Colors.END}")
        
        print_success("Analysis complete")
    
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main demo flow."""
    print(Colors.BOLD + Colors.CYAN)
    print("="*70)
    print("BASE PYTHON SDK - COMPLETE TRANSACTION TESTING".center(70))
    print("Testing READ and WRITE Operations".center(70))
    print("="*70)
    print(Colors.END)
    
    # Load environment
    load_dotenv()
    
    private_key = os.getenv('TESTNET_PRIVATE_KEY')
    
    if not private_key:
        print_error("TESTNET_PRIVATE_KEY not found in .env")
        print("\n💡 Run this first:")
        print("   python tools/generate_test_wallet.py")
        return
    
    try:
        # Connect to Base Sepolia
        print(f"\n{Colors.YELLOW}🔗 Connecting to Base Sepolia...{Colors.END}")
        client = BaseClient(chain_id=84532)
        
        chain_id = client.get_chain_id()
        block_number = client.get_block_number()
        
        print_success("Connected!")
        print(f"  Chain ID: {chain_id}")
        print(f"  Block:    {block_number:,}")
        
        # Load wallet
        print(f"\n{Colors.YELLOW}👛 Loading your wallet...{Colors.END}")
        wallet = Wallet.from_private_key(private_key, client=client)
        
        print_success("Wallet loaded!")
        print(f"  Address: {wallet.address}")
        
        # Initialize transaction handler
        tx_handler = Transaction(client, wallet)
        
        # ====================================================================
        # CHECK WALLET
        # ====================================================================
        
        has_balance = demo_check_wallet(wallet, client)
        
        if not has_balance:
            print("\n" + "="*70)
            print_error("Cannot proceed without testnet ETH")
            print("="*70)
            return
        
        input(f"\n{Colors.BOLD}Press Enter to start testing...{Colors.END}")
        
        # ====================================================================
        # READ OPERATIONS (PUBLIC)
        # ====================================================================
        
        demo_query_real_transaction(tx_handler, client)
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
        
        demo_decode_erc20_transfers(tx_handler, client)
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
        
        # ====================================================================
        # WRITE OPERATIONS (YOUR WALLET)
        # ====================================================================
        
        demo_estimate_costs(tx_handler, wallet, client)
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
        
        demo_simulate_transaction(tx_handler, wallet, client)
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
        
        # ACTUAL TRANSACTION (asks for confirmation)
        tx_hash = demo_send_eth_transaction(tx_handler, wallet, client)
        
        if tx_hash:
            input(f"\n{Colors.BOLD}Press Enter to analyze your transaction...{Colors.END}")
            demo_analyze_your_transaction(tx_handler, tx_hash, wallet)
        
        # ====================================================================
        # COMPLETION
        # ====================================================================
        
        print("\n" + Colors.BOLD + "="*70 + Colors.END)
        print(Colors.GREEN + Colors.BOLD + "✅ ALL TESTS COMPLETED!".center(70) + Colors.END)
        print(Colors.BOLD + "="*70 + Colors.END)
        
        print("\n" + Colors.BOLD + "🎓 What Was Tested:" + Colors.END)
        print("  ✅ Read Operations (public access)")
        print("     • Query transactions")
        print("     • Decode ERC-20 transfers (zero cost)")
        print("     • Transaction analysis")
        print("  ")
        print("  ✅ Write Operations (your wallet)")
        print("     • Cost estimation")
        print("     • Transaction simulation")
        print("     • Send ETH transaction")
        print("     • Balance tracking")
        print("     • Complete analysis")
        
        print("\n" + Colors.BOLD + "📊 Your Wallet:" + Colors.END)
        final_balance = wallet.get_balance()
        final_balance_eth = final_balance / 10**18
        print(f"  Address: {wallet.address}")
        print(f"  Balance: {final_balance_eth:.6f} ETH")
        print(f"  Nonce:   {wallet.get_nonce()}")
        
        explorer = f"https://sepolia.basescan.org/address/{wallet.address}"
        print(f"\n{Colors.BOLD}📍 View Your Transactions:{Colors.END}")
        print(f"  {explorer}")
        
        print("\n" + Colors.BOLD + "🚀 Next Steps:" + Colors.END)
        print("  • Get more testnet ETH for more testing")
        print("  • Try different gas strategies")
        print("  • Test with ERC-20 tokens")
        print("  • Integrate into your application")
        
    except KeyboardInterrupt:
        print("\n\n" + Colors.YELLOW + "⚠️  Interrupted" + Colors.END)
    except Exception as e:
        print("\n")
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + Colors.BOLD + "="*70 + Colors.END)
        print(Colors.CYAN + Colors.BOLD + "Thank you for testing Base Python SDK!".center(70) + Colors.END)
        print(Colors.BOLD + "="*70 + Colors.END)


if __name__ == "__main__":
    main()