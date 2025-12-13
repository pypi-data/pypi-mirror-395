"""
Check test wallet status and balance.

This verifies:
1. .env file exists and is valid
2. Wallet can be loaded
3. Connection to Base Sepolia works
4. Balance is sufficient for testing
5. Can check any additional address balance
"""

from basepy import BaseClient, Wallet
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


def check_address_balance(client: BaseClient, address: str):
    """Check balance of any address."""
    print("\n" + "="*70)
    print(f"🔍 CHECKING ADDRESS: {address}")
    print("="*70)
    
    try:
        # Validate address
        validated_address = client._validate_address(address)
        print(f"✅ Valid address: {validated_address}")
    except Exception as e:
        print(f"❌ Invalid address: {e}")
        return
    
    # Check if it's a contract
    print("\n📝 Address Type:")
    try:
        if client.is_contract(validated_address):
            print("   📜 Smart Contract")
            code = client.get_code(validated_address)
            print(f"   Bytecode size: {len(code)} bytes")
        else:
            print("   👤 Externally Owned Account (EOA)")
    except Exception as e:
        print(f"   ⚠️  Could not determine type: {e}")
    
    # Get ETH balance
    print("\n💰 ETH Balance:")
    try:
        balance = client.get_balance(validated_address)
        balance_eth = balance / 10**18
        
        print(f"   {balance_eth:.6f} ETH")
        print(f"   ({balance:,} Wei)")
        
        if balance_eth == 0:
            print("   ℹ️  No ETH balance")
        elif balance_eth < 0.01:
            print("   ⚠️  Low balance")
        else:
            print("   ✅ Sufficient balance")
    except Exception as e:
        print(f"   ❌ Failed to get balance: {e}")
        return
    
    # Get transaction count
    print("\n📊 Transaction Count:")
    try:
        nonce = client.get_transaction_count(validated_address)
        print(f"   {nonce} transaction(s)")
        
        if nonce == 0:
            print("   ℹ️  No transactions yet")
        else:
            print(f"   ✅ Active wallet")
    except Exception as e:
        print(f"   ⚠️  Could not get transaction count: {e}")
    
    # Block explorer link
    print("\n🔗 Block Explorer:")
    explorer_url = f"https://sepolia.basescan.org/address/{validated_address}"
    print(f"   {explorer_url}")
    
    print("="*70)


def check_wallet(additional_address: str = None):
    """
    Check wallet setup and status.
    
    Args:
        additional_address: Optional address to check balance for
    """
    
    print("="*70)
    print("🔵 BASE SEPOLIA WALLET CHECKER")
    print("="*70)
    
    # Check .env file
    print("\n1️⃣  Checking .env file...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("\n💡 Run this first:")
        print("   python tools/generate_test_wallet.py")
        
        # If checking another address, we can still do that
        if additional_address:
            print("\n⚠️  Continuing with additional address check only...")
            try:
                client = BaseClient(chain_id=84532)
                check_address_balance(client, additional_address)
            except Exception as e:
                print(f"❌ Failed to check address: {e}")
        return
    
    print("✅ .env file found")
    
    # Load environment variables
    load_dotenv()
    
    # Check private key
    print("\n2️⃣  Checking environment variables...")
    private_key = os.getenv('TESTNET_PRIVATE_KEY')
    address = os.getenv('TESTNET_ADDRESS')
    
    if not private_key:
        print("❌ TESTNET_PRIVATE_KEY not found in .env")
        
        # If checking another address, we can still do that
        if additional_address:
            print("\n⚠️  Continuing with additional address check only...")
            try:
                client = BaseClient(chain_id=84532)
                check_address_balance(client, additional_address)
            except Exception as e:
                print(f"❌ Failed to check address: {e}")
        return
    
    print("✅ TESTNET_PRIVATE_KEY found")
    
    if address:
        print(f"✅ TESTNET_ADDRESS: {address}")
    
    # Connect to Base Sepolia
    print("\n3️⃣  Connecting to Base Sepolia...")
    try:
        client = BaseClient(chain_id=84532)
        chain_id = client.get_chain_id()
        block_number = client.get_block_number()
        print(f"✅ Connected!")
        print(f"   Chain ID: {chain_id}")
        print(f"   Current Block: {block_number:,}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Load wallet
    print("\n4️⃣  Loading wallet...")
    try:
        wallet = Wallet.from_private_key(private_key, client=client)
        print(f"✅ Wallet loaded!")
        print(f"   Address: {wallet.address}")
        
        # Verify address matches
        if address and wallet.address.lower() != address.lower():
            print(f"⚠️  WARNING: Address mismatch!")
            print(f"   .env has: {address}")
            print(f"   Wallet:   {wallet.address}")
    except Exception as e:
        print(f"❌ Failed to load wallet: {e}")
        return
    
    # Check balance
    print("\n5️⃣  Checking balance...")
    try:
        balance = wallet.get_balance()
        balance_eth = balance / 10**18
        
        print(f"✅ Balance retrieved!")
        print(f"   {balance_eth:.6f} ETH")
        print(f"   ({balance:,} Wei)")
        
        # Balance status
        if balance_eth == 0:
            print("\n⚠️  NO BALANCE!")
            print("   You need testnet ETH to send transactions.")
            print("\n💡 Get free testnet ETH from:")
            print("   https://www.alchemy.com/faucets/base-sepolia")
        elif balance_eth < 0.01:
            print("\n⚠️  LOW BALANCE!")
            print("   You may want to get more testnet ETH.")
            print("   Recommended: At least 0.05 ETH for testing")
        else:
            print("\n✅ BALANCE IS GOOD!")
            print("   You're ready to send transactions!")
        
    except Exception as e:
        print(f"❌ Failed to check balance: {e}")
        return
    
    # Check nonce
    print("\n6️⃣  Checking transaction count...")
    try:
        nonce = wallet.get_nonce()
        print(f"✅ Transaction count (nonce): {nonce}")
        
        if nonce == 0:
            print("   This wallet hasn't sent any transactions yet")
        else:
            print(f"   This wallet has sent {nonce} transaction(s)")
    except Exception as e:
        print(f"⚠️  Could not get nonce: {e}")
        nonce = 0
    
    # Block explorer link
    print("\n7️⃣  Block Explorer:")
    explorer_url = f"https://sepolia.basescan.org/address/{wallet.address}"
    print(f"   {explorer_url}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY - YOUR WALLET")
    print("="*70)
    print(f"   Address:  {wallet.address}")
    print(f"   Balance:  {balance_eth:.6f} ETH")
    print(f"   Nonce:    {nonce}")
    print(f"   Network:  Base Sepolia (Chain ID: {chain_id})")
    
    # Status
    if balance_eth > 0.01:
        print("\n✅ ALL CHECKS PASSED!")
        print("   You're ready to run demos!")
        print("\n🚀 Next step:")
        print("   python examples/send_demo.py")
    elif balance_eth > 0:
        print("\n⚠️  Low balance but can test small transactions")
        print("   Consider getting more testnet ETH")
    else:
        print("\n❌ Need testnet ETH to continue")
        print("   Visit: https://www.alchemy.com/faucets/base-sepolia")
    
    print("="*70)
    
    # Check additional address if provided
    if additional_address:
        check_address_balance(client, additional_address)


def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check Base Sepolia wallet status and balances',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check your test wallet
  python check_wallet.py
  
  # Check your wallet + another address
  python check_wallet.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
  
  # Check any address only (no .env needed)
  python check_wallet.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --only
  
  # Short form
  python check_wallet.py -a 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
        """
    )
    
    parser.add_argument(
        '-a', '--address',
        type=str,
        help='Additional address to check balance for',
        metavar='ADDRESS'
    )
    
    parser.add_argument(
        '--only',
        action='store_true',
        help='Only check the provided address (skip wallet check)'
    )
    
    args = parser.parse_args()
    
    # If --only flag, just check the address
    if args.only:
        if not args.address:
            print("❌ Error: --only requires --address")
            parser.print_help()
            sys.exit(1)
        
        print("="*70)
        print("🔵 BASE SEPOLIA ADDRESS CHECKER")
        print("="*70)
        
        try:
            client = BaseClient(chain_id=84532)
            print(f"\n✅ Connected to Base Sepolia")
            print(f"   Chain ID: {client.get_chain_id()}")
            print(f"   Current Block: {client.get_block_number():,}")
            
            check_address_balance(client, args.address)
        except Exception as e:
            print(f"\n❌ Failed: {e}")
            sys.exit(1)
    else:
        # Normal flow: check wallet (and optionally additional address)
        check_wallet(additional_address='0x34CFaeBbA192f74a7D51bd46b0D6A00a65A9824e')


if __name__ == "__main__":
    main()