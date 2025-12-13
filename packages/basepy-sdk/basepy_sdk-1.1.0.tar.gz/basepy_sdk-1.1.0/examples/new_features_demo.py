from basepy.client import BaseClient
from basepy.standards import ERC20

def main():
    # 1. Connect to Base Mainnet
    client = BaseClient()
    print(f"Connected to Base Mainnet (Chain ID: {client.get_chain_id()})")

    # 2. Use the new L1 Fee Logic
    # Let's pretend we are sending a simple transaction (empty data)
    dummy_data = b'' 
    l1_fee = client.get_l1_fee(dummy_data)
    print(f"Current L1 Security Fee for a simple tx: {l1_fee} wei")

    # 3. Use the new ERC-20 Wrapper
    # USDC on Base Mainnet: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
    usdc_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    usdc = ERC20(client, usdc_address)
    
    symbol = usdc.get_symbol()
    decimals = usdc.get_decimals()
    print(f"Token Found: {symbol} (Decimals: {decimals})")

    # Check balance of a random whale address (Binance Hot Wallet for example)
    # Just using a random address for demo purposes
    random_address = "0x4200000000000000000000000000000000000006" # WETH contract
    balance = usdc.balance_of(random_address)
    print(f"Balance of {random_address}: {balance} {symbol}")

if __name__ == "__main__":
    main()
