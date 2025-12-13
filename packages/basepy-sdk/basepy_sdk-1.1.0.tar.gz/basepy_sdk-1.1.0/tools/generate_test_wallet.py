"""
Generate a test wallet for Base Sepolia testnet.

This script:
1. Generates a new wallet
2. Displays address and private key
3. Saves to .env file
4. Shows links to get testnet ETH
"""

from basepy import BaseClient, Wallet
from pathlib import Path
import os


def generate_test_wallet():
    """Generate a new test wallet for Base Sepolia."""
    
    print("="*70)
    print("🔵 BASE SEPOLIA TEST WALLET GENERATOR")
    print("="*70)
    
    # Connect to Base Sepolia testnet
    print("\n🔗 Connecting to Base Sepolia testnet...")
    client = BaseClient(chain_id=84532)
    
    print(f"✅ Connected! Chain ID: {client.get_chain_id()}")
    print(f"   Current Block: {client.get_block_number():,}")
    
    # Generate new wallet
    print("\n🔐 Generating new wallet...")
    wallet = Wallet.create(client=client)
    
    print("\n" + "="*70)
    print("✅ WALLET CREATED!")
    print("="*70)
    
    print(f"\n📍 Address:")
    print(f"   {wallet.address}")
    
    print(f"\n🔑 Private Key:")
    print(f"   {wallet.private_key}")
    
    print("\n⚠️  IMPORTANT:")
    print("   - This is a TEST wallet only!")
    print("   - NEVER use this wallet for real funds")
    print("   - Save the private key securely")
    print("   - Don't share the private key")
    
    # Check if .env exists
    env_path = Path('.env')
    
    if env_path.exists():
        print(f"\n📄 Found existing .env file")
        response = input("   Overwrite? (yes/no): ").strip().lower()
        if response != 'yes':
            print("\n❌ Cancelled. Your existing .env is safe.")
            print(f"\n💡 Manually add to .env:")
            print(f"   TESTNET_PRIVATE_KEY={wallet.private_key}")
            print(f"   TESTNET_ADDRESS={wallet.address}")
            return
    
    # Save to .env
    print(f"\n💾 Saving to .env file...")
    
    env_content = f"""# Base Sepolia Testnet Wallet
# Generated: {os.popen('date').read().strip()}
# WARNING: Never commit this file to git!

TESTNET_CHAIN_ID=84532
TESTNET_PRIVATE_KEY={wallet.private_key}
TESTNET_ADDRESS={wallet.address}

# Base Mainnet (leave empty for now)
MAINNET_CHAIN_ID=8453
MAINNET_PRIVATE_KEY=
MAINNET_ADDRESS=
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Saved to .env")
    
    # Check .gitignore
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        if '.env' not in gitignore_content:
            print("\n⚠️  WARNING: .env is NOT in .gitignore!")
            response = input("   Add .env to .gitignore? (yes/no): ").strip().lower()
            if response == 'yes':
                with open(gitignore_path, 'a') as f:
                    f.write('\n# Environment variables\n.env\n')
                print("✅ Added .env to .gitignore")
    else:
        print("\n⚠️  No .gitignore found!")
        print("   Creating .gitignore...")
        with open('.gitignore', 'w') as f:
            f.write('# Environment variables\n.env\n*.key\n*private*\n')
        print("✅ Created .gitignore")
    
    # Next steps
    print("\n" + "="*70)
    print("🎉 NEXT STEPS:")
    print("="*70)
    
    print("\n1️⃣  GET TESTNET ETH (FREE!)")
    print("   Choose one of these faucets:")
    print()
    print("   🔗 Alchemy (Recommended):")
    print("      https://www.alchemy.com/faucets/base-sepolia")
    print()
    print("   🔗 QuickNode:")
    print("      https://faucet.quicknode.com/base/sepolia")
    print()
    print("   🔗 Base Discord:")
    print("      https://discord.gg/buildonbase")
    print("      Channel: #faucet")
    print(f"      Command: /faucet {wallet.address}")
    
    print("\n2️⃣  VERIFY YOUR BALANCE")
    print("   After getting testnet ETH, check your balance:")
    print(f"   https://sepolia.basescan.org/address/{wallet.address}")
    
    print("\n3️⃣  TEST YOUR SETUP")
    print("   Run: python tools/check_wallet.py")
    
    print("\n4️⃣  RUN DEMOS")
    print("   Run: python examples/send_demo.py")
    
    print("\n" + "="*70)
    print("💾 WALLET INFO SAVED TO:")
    print(f"   {Path('.env').absolute()}")
    print("="*70)


if __name__ == "__main__":
    generate_test_wallet()