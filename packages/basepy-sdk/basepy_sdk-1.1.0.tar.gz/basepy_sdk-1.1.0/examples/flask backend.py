"""
Base Blockchain Professional Dashboard - Backend Server
Flask API that connects to Base blockchain using basepy library

Installation:
pip install flask flask-cors basepy web3

Run:
python backend_server.py

API Endpoints:
- GET  /api/network/info          - Get network information
- GET  /api/network/gas           - Get gas prices
- POST /api/account/lookup        - Lookup account details
- POST /api/transaction/lookup    - Lookup transaction details
- POST /api/transaction/receipt   - Get transaction receipt
- POST /api/token/info            - Get ERC-20 token information
- POST /api/token/balance         - Get token balance for address
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from basepy.client import BaseClient
from basepy.transactions import Transaction
from basepy.standards import ERC20
import traceback
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize Base client (global instance)
try:
    client = BaseClient()
    print(f"✅ Connected to Base Mainnet (Chain ID: {client.get_chain_id()})")
except Exception as e:
    print(f"❌ Failed to connect to Base: {e}")
    client = None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
# ============================================================================
# ROOT ROUTES (Fix 404 on / and /api)
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Homepage – shows basic info"""
    return jsonify({
        "message": "BasePy Backend Running",
        "status": "ok",
        "endpoints": [
            "/api/health",
            "/api/network/info",
            "/api/network/gas",
            "/api/account/lookup",
            "/api/transaction/lookup",
            "/api/transaction/receipt",
            "/api/token/info",
            "/api/token/balance",
        ]
    })


@app.route('/api', methods=['GET'])
def api_root():
    """API root – avoids 404 on /api"""
    return jsonify({
        "message": "BasePy API Root",
        "usage": "Use /api/health or other endpoints"
    })

def handle_error(error, status_code=500):
    """Standard error response handler"""
    return jsonify({
        'success': False,
        'error': str(error),
        'traceback': traceback.format_exc()
    }), status_code


def validate_address(address):
    """Validate Ethereum address format"""
    if not address or not isinstance(address, str):
        return False
    if not address.startswith('0x'):
        return False
    if len(address) != 42:
        return False
    try:
        int(address, 16)  # Check if valid hex
        return True
    except ValueError:
        return False


def validate_tx_hash(tx_hash):
    """Validate transaction hash format"""
    if not tx_hash or not isinstance(tx_hash, str):
        return False
    if not tx_hash.startswith('0x'):
        return False
    if len(tx_hash) != 66:
        return False
    try:
        int(tx_hash, 16)  # Check if valid hex
        return True
    except ValueError:
        return False


# ============================================================================
# NETWORK ENDPOINTS
# ============================================================================

@app.route('/api/network/info', methods=['GET'])
def get_network_info():
    """Get basic network information"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        chain_id = client.get_chain_id()
        block_number = client.get_block_number()
        is_connected = client.is_connected()
        
        # Get latest block for timestamp
        latest_block = client.get_block('latest')
        
        network_name = "Base Mainnet" if chain_id == 8453 else \
                      "Base Sepolia" if chain_id == 84532 else \
                      f"Unknown Network"
        
        return jsonify({
            'success': True,
            'data': {
                'chainId': chain_id,
                'networkName': network_name,
                'blockNumber': block_number,
                'timestamp': latest_block.get('timestamp', 0),
                'connected': is_connected,
                'networkType': 'Layer 2 (OP Stack)'
            }
        })
    except Exception as e:
        return handle_error(e)


@app.route('/api/network/gas', methods=['GET'])
def get_gas_prices():
    """Get current gas prices"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        gas_price = client.get_gas_price()
        base_fee = client.get_base_fee()
        
        # Get latest block for additional info
        block = client.get_block('latest')
        
        # Calculate estimated costs for simple transfer
        simple_transfer_gas = 21000
        simple_transfer_cost = simple_transfer_gas * gas_price
        
        # Estimate L1 fee for simple transfer
        try:
            l1_fee = client.get_l1_fee(b'')  # Empty calldata
        except:
            l1_fee = 0
        
        return jsonify({
            'success': True,
            'data': {
                'gasPrice': gas_price,
                'gasPriceGwei': gas_price / 10**9,
                'baseFee': base_fee,
                'baseFeeGwei': base_fee / 10**9,
                'simpleTransferCost': simple_transfer_cost,
                'simpleTransferCostEth': simple_transfer_cost / 10**18,
                'l1FeeEstimate': l1_fee,
                'l1FeeEstimateEth': l1_fee / 10**18,
                'blockGasUsed': block.get('gasUsed', 0),
                'blockGasLimit': block.get('gasLimit', 0)
            }
        })
    except Exception as e:
        return handle_error(e)


# ============================================================================
# ACCOUNT ENDPOINTS
# ============================================================================

@app.route('/api/account/lookup', methods=['POST'])
def lookup_account():
    """Lookup account information"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not validate_address(address):
            return handle_error("Invalid Ethereum address format", 400)
        
        # Get account information
        balance = client.get_balance(address)
        tx_count = client.get_transaction_count(address)
        is_contract = client.is_contract(address)
        
        code_size = 0
        if is_contract:
            code = client.get_code(address)
            code_size = len(code)
        
        return jsonify({
            'success': True,
            'data': {
                'address': address,
                'balance': balance,
                'balanceEth': balance / 10**18,
                'transactionCount': tx_count,
                'isContract': is_contract,
                'codeSize': code_size,
                'accountType': 'Smart Contract' if is_contract else 'EOA (Wallet)'
            }
        })
    except Exception as e:
        return handle_error(e)


# ============================================================================
# TRANSACTION ENDPOINTS
# ============================================================================

@app.route('/api/transaction/lookup', methods=['POST'])
def lookup_transaction():
    """Lookup transaction details"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        data = request.get_json()
        tx_hash = data.get('txHash', '').strip()
        
        if not validate_tx_hash(tx_hash):
            return handle_error("Invalid transaction hash format", 400)
        
        tx_handler = Transaction(client)
        
        # Get transaction details
        tx = tx_handler.get(tx_hash)
        
        # Try to get receipt (might not exist if pending)
        receipt = None
        status = 'pending'
        try:
            receipt = tx_handler.get_receipt(tx_hash)
            status = 'confirmed' if receipt['status'] == 1 else 'failed'
        except:
            pass
        
        # Calculate costs if receipt exists
        gas_used = receipt['gasUsed'] if receipt else 0
        effective_gas_price = receipt.get('effectiveGasPrice', tx.get('gasPrice', 0)) if receipt else 0
        l2_cost = gas_used * effective_gas_price
        
        # Try to estimate L1 fee
        l1_fee = 0
        try:
            if tx.get('input'):
                l1_fee = client.get_l1_fee(tx['input'])
        except:
            pass
        
        total_cost = l2_cost + l1_fee
        
        return jsonify({
            'success': True,
            'data': {
                'hash': tx_hash,
                'from': tx['from'],
                'to': tx['to'],
                'value': tx['value'],
                'valueEth': tx['value'] / 10**18,
                'gasLimit': tx['gas'],
                'gasPrice': tx.get('gasPrice', 0),
                'gasPriceGwei': tx.get('gasPrice', 0) / 10**9,
                'nonce': tx['nonce'],
                'blockNumber': tx.get('blockNumber'),
                'status': status,
                'input': tx.get('input', '0x'),
                'isContractInteraction': tx.get('input', '0x') != '0x',
                'gasUsed': gas_used,
                'effectiveGasPrice': effective_gas_price,
                'l2Cost': l2_cost,
                'l2CostEth': l2_cost / 10**18,
                'l1Fee': l1_fee,
                'l1FeeEth': l1_fee / 10**18,
                'totalCost': total_cost,
                'totalCostEth': total_cost / 10**18
            }
        })
    except Exception as e:
        return handle_error(e)


@app.route('/api/transaction/receipt', methods=['POST'])
def get_transaction_receipt():
    """Get transaction receipt with full details"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        data = request.get_json()
        tx_hash = data.get('txHash', '').strip()
        
        if not validate_tx_hash(tx_hash):
            return handle_error("Invalid transaction hash format", 400)
        
        tx_handler = Transaction(client)
        receipt = tx_handler.get_receipt(tx_hash)
        
        return jsonify({
            'success': True,
            'data': {
                'transactionHash': receipt['transactionHash'].hex() if isinstance(receipt['transactionHash'], bytes) else receipt['transactionHash'],
                'blockNumber': receipt['blockNumber'],
                'status': receipt['status'],
                'gasUsed': receipt['gasUsed'],
                'effectiveGasPrice': receipt['effectiveGasPrice'],
                'effectiveGasPriceGwei': receipt['effectiveGasPrice'] / 10**9,
                'totalCost': receipt['gasUsed'] * receipt['effectiveGasPrice'],
                'totalCostEth': (receipt['gasUsed'] * receipt['effectiveGasPrice']) / 10**18,
                'contractAddress': receipt.get('contractAddress'),
                'logsCount': len(receipt.get('logs', []))
            }
        })
    except Exception as e:
        return handle_error(e)


# ============================================================================
# TOKEN ENDPOINTS
# ============================================================================

@app.route('/api/token/info', methods=['POST'])
def get_token_info():
    """Get ERC-20 token information"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        data = request.get_json()
        token_address = data.get('tokenAddress', '').strip()
        
        if not validate_address(token_address):
            return handle_error("Invalid token address format", 400)
        
        # Initialize ERC-20 token
        token = ERC20(client, token_address)
        
        # Get token information
        symbol = token.get_symbol()
        name = token.get_name()
        decimals = token.get_decimals()
        total_supply = token.get_total_supply()
        
        return jsonify({
            'success': True,
            'data': {
                'address': token_address,
                'symbol': symbol,
                'name': name,
                'decimals': decimals,
                'totalSupply': total_supply,
                'totalSupplyFormatted': total_supply / (10 ** decimals)
            }
        })
    except Exception as e:
        return handle_error(e)


@app.route('/api/token/balance', methods=['POST'])
def get_token_balance():
    """Get token balance for an address"""
    try:
        if not client:
            return handle_error("Client not initialized", 503)
        
        data = request.get_json()
        token_address = data.get('tokenAddress', '').strip()
        holder_address = data.get('holderAddress', '').strip()
        
        if not validate_address(token_address):
            return handle_error("Invalid token address format", 400)
        
        if not validate_address(holder_address):
            return handle_error("Invalid holder address format", 400)
        
        # Initialize ERC-20 token
        token = ERC20(client, token_address)
        
        # Get balance
        balance = token.balance_of(holder_address)
        decimals = token.get_decimals()
        symbol = token.get_symbol()
        
        return jsonify({
            'success': True,
            'data': {
                'tokenAddress': token_address,
                'holderAddress': holder_address,
                'balance': balance,
                'balanceFormatted': balance / (10 ** decimals),
                'symbol': symbol,
                'decimals': decimals
            }
        })
    except Exception as e:
        return handle_error(e)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if not client:
            return jsonify({
                'status': 'unhealthy',
                'message': 'Client not initialized'
            }), 503
        
        is_connected = client.is_connected()
        block_number = client.get_block_number()
        
        return jsonify({
            'status': 'healthy',
            'connected': is_connected,
            'blockNumber': block_number,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*60)
    print("BASE BLOCKCHAIN PROFESSIONAL DASHBOARD - BACKEND SERVER")
    print("="*60)
    print("\n📡 Starting Flask API server...")
    print("\n🔗 Available Endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/network/info")
    print("   GET  /api/network/gas")
    print("   POST /api/account/lookup")
    print("   POST /api/transaction/lookup")
    print("   POST /api/transaction/receipt")
    print("   POST /api/token/info")
    print("   POST /api/token/balance")
    print("\n" + "="*60)
    print("🚀 Server running on http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )