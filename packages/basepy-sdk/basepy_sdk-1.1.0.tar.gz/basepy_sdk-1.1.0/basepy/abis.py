"""
ABI definitions for Base blockchain smart contracts.
Includes standard token ABIs, Base-specific contract ABIs, and event signatures.

Production-ready features:
- Complete standard ABIs (ERC-20, ERC-721, ERC-1155, WETH)
- Base-specific contract addresses
- Event topic signatures for efficient log parsing
- Common token lists for portfolio tracking
- Utility functions for ABI/address lookup
"""

# ============================================================================
# EVENT SIGNATURES (Keccak-256 hashes for log filtering)
# ============================================================================

# ERC-20 Transfer event signature: Transfer(address indexed from, address indexed to, uint256 value)
ERC20_TRANSFER_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

# ERC-20 Approval event signature: Approval(address indexed owner, address indexed spender, uint256 value)
ERC20_APPROVAL_TOPIC = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'

# ERC-721 Transfer event signature: Transfer(address indexed from, address indexed to, uint256 indexed tokenId)
ERC721_TRANSFER_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

# ERC-1155 TransferSingle event signature
ERC1155_TRANSFER_SINGLE_TOPIC = '0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62'

# ERC-1155 TransferBatch event signature
ERC1155_TRANSFER_BATCH_TOPIC = '0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb'

# WETH Deposit event signature: Deposit(address indexed dst, uint256 wad)
WETH_DEPOSIT_TOPIC = '0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c'

# WETH Withdrawal event signature: Withdrawal(address indexed src, uint256 wad)
WETH_WITHDRAWAL_TOPIC = '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65'


# ============================================================================
# ERC-20 TOKEN ABI (Complete Standard)
# ============================================================================

ERC20_ABI = [
    # Read Functions
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    
    # Write Functions
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    
    # Events
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "spender", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
]


# ============================================================================
# GAS PRICE ORACLE ABI (Base/OP Stack Specific)
# ============================================================================

GAS_ORACLE_ABI = [
    {
        "inputs": [{"internalType": "bytes", "name": "_data", "type": "bytes"}],
        "name": "getL1Fee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes", "name": "_data", "type": "bytes"}],
        "name": "getL1GasUsed",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "l1BaseFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "baseFeeScalar",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "blobBaseFeeScalar",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "gasPrice",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "overhead",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "scalar",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "version",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]


# ============================================================================
# ERC-721 NFT ABI (Standard)
# ============================================================================

ERC721_ABI = [
    # Read Functions
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_operator", "type": "address"}
        ],
        "name": "isApprovedForAll",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "getApproved",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    
    # Write Functions
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_tokenId", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_tokenId", "type": "uint256"}
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_approved", "type": "address"},
            {"name": "_tokenId", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_operator", "type": "address"},
            {"name": "_approved", "type": "bool"}
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    
    # Events
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": True, "name": "tokenId", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "approved", "type": "address"},
            {"indexed": True, "name": "tokenId", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "operator", "type": "address"},
            {"indexed": False, "name": "approved", "type": "bool"},
        ],
        "name": "ApprovalForAll",
        "type": "event",
    },
]


# ============================================================================
# ERC-1155 MULTI-TOKEN ABI (Standard)
# ============================================================================

ERC1155_ABI = [
    # Read Functions
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_id", "type": "uint256"}
        ],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owners", "type": "address[]"},
            {"name": "_ids", "type": "uint256[]"}
        ],
        "name": "balanceOfBatch",
        "outputs": [{"name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_operator", "type": "address"}
        ],
        "name": "isApprovedForAll",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_id", "type": "uint256"}],
        "name": "uri",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    
    # Write Functions
    {
        "constant": False,
        "inputs": [
            {"name": "_operator", "type": "address"},
            {"name": "_approved", "type": "bool"}
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_id", "type": "uint256"},
            {"name": "_value", "type": "uint256"},
            {"name": "_data", "type": "bytes"}
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_ids", "type": "uint256[]"},
            {"name": "_values", "type": "uint256[]"},
            {"name": "_data", "type": "bytes"}
        ],
        "name": "safeBatchTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    
    # Events
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "operator", "type": "address"},
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "id", "type": "uint256"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "TransferSingle",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "operator", "type": "address"},
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "ids", "type": "uint256[]"},
            {"indexed": False, "name": "values", "type": "uint256[]"},
        ],
        "name": "TransferBatch",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "owner", "type": "address"},
            {"indexed": True, "name": "operator", "type": "address"},
            {"indexed": False, "name": "approved", "type": "bool"},
        ],
        "name": "ApprovalForAll",
        "type": "event",
    },
]


# ============================================================================
# WRAPPED ETH (WETH) ABI
# ============================================================================

WETH_ABI = [
    # ERC-20 functions
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    
    # WETH-specific functions
    {
        "constant": False,
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "wad", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    
    # Events
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "dst", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Deposit",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Withdrawal",
        "type": "event",
    },
]


# ============================================================================
# COMMON CONTRACT ADDRESSES ON BASE
# ============================================================================

BASE_CONTRACTS = {
    "mainnet": {
        "gas_oracle": "0x420000000000000000000000000000000000000F",
        "weth": "0x4200000000000000000000000000000000000006",
        "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "dai": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
        "usdt": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
        "cbeth": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
        "reth": "0xB6fe221Fe9EeF5aBa221c348bA20A1Bf5e73624c",
        "multicall3": "0xcA11bde05977b3631167028862bE2a173976CA11",
    },
    "sepolia": {
        "gas_oracle": "0x420000000000000000000000000000000000000F",
        "weth": "0x4200000000000000000000000000000000000006",
        "multicall3": "0xcA11bde05977b3631167028862bE2a173976CA11",
    }
}


# ============================================================================
# COMMON TOKEN LISTS (For Portfolio Tracking)
# ============================================================================

# Default tokens to check for portfolio view (when user doesn't specify tokens)
BASE_COMMON_TOKENS = {
    "mainnet": [
        {
            "symbol": "USDC",
            "name": "USD Coin",
            "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "decimals": 6,
            "category": "stablecoin"
        },
        {
            "symbol": "DAI",
            "name": "Dai Stablecoin",
            "address": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
            "decimals": 18,
            "category": "stablecoin"
        },
        {
            "symbol": "USDT",
            "name": "Tether USD",
            "address": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
            "decimals": 6,
            "category": "stablecoin"
        },
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0x4200000000000000000000000000000000000006",
            "decimals": 18,
            "category": "wrapped"
        },
        {
            "symbol": "cbETH",
            "name": "Coinbase Wrapped Staked ETH",
            "address": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
            "decimals": 18,
            "category": "liquid_staking"
        },
        {
            "symbol": "rETH",
            "name": "Rocket Pool ETH",
            "address": "0xB6fe221Fe9EeF5aBa221c348bA20A1Bf5e73624c",
            "decimals": 18,
            "category": "liquid_staking"
        },
    ],
    "sepolia": [
        {
            "symbol": "WETH",
            "name": "Wrapped Ether",
            "address": "0x4200000000000000000000000000000000000006",
            "decimals": 18,
            "category": "wrapped"
        },
    ]
}


# ============================================================================
# TOKEN CATEGORIES (For Filtering/Organization)
# ============================================================================

TOKEN_CATEGORIES = {
    "stablecoin": ["USDC", "DAI", "USDT", "FRAX", "LUSD"],
    "wrapped": ["WETH", "WBTC"],
    "liquid_staking": ["cbETH", "rETH", "wstETH", "stETH"],
    "governance": ["UNI", "AAVE", "COMP", "SNX"],
    "defi": ["LINK", "MKR", "CRV", "BAL"],
}


# ============================================================================
# ABI UTILITIES
# ============================================================================

def get_contract_address(chain_id: int, contract_name: str) -> str:
    """
    Get contract address for a given chain and contract name.
    
    Args:
        chain_id: Chain ID (8453 for mainnet, 84532 for sepolia)
        contract_name: Name of contract (e.g., 'gas_oracle', 'weth', 'usdc')
        
    Returns:
        Contract address
        
    Raises:
        ValueError: If chain_id or contract_name is invalid
        
    Example:
        >>> from basepy.abis import get_contract_address
        >>> usdc_address = get_contract_address(8453, 'usdc')
        >>> print(usdc_address)
        '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
    """
    network = "mainnet" if chain_id == 8453 else "sepolia" if chain_id == 84532 else None
    
    if not network:
        raise ValueError(f"Invalid chain_id: {chain_id}. Expected 8453 (mainnet) or 84532 (sepolia)")
    
    if contract_name not in BASE_CONTRACTS[network]:
        available = ", ".join(BASE_CONTRACTS[network].keys())
        raise ValueError(f"Contract '{contract_name}' not found on {network}. Available: {available}")
    
    return BASE_CONTRACTS[network][contract_name]


def get_abi_by_name(abi_name: str) -> list:
    """
    Get ABI by name.
    
    Args:
        abi_name: ABI name ('erc20', 'erc721', 'erc1155', 'weth', 'gas_oracle')
        
    Returns:
        ABI list
        
    Raises:
        ValueError: If ABI name is invalid
        
    Example:
        >>> from basepy.abis import get_abi_by_name
        >>> erc20_abi = get_abi_by_name('erc20')
    """
    abis = {
        'erc20': ERC20_ABI,
        'erc721': ERC721_ABI,
        'erc1155': ERC1155_ABI,
        'weth': WETH_ABI,
        'gas_oracle': GAS_ORACLE_ABI,
    }
    
    abi_name = abi_name.lower()
    if abi_name not in abis:
        available = ", ".join(abis.keys())
        raise ValueError(f"ABI '{abi_name}' not found. Available: {available}")
    
    return abis[abi_name]


def get_common_tokens(chain_id: int, categories: list = None) -> list:
    """
    Get common token list for portfolio tracking.
    
    Args:
        chain_id: Chain ID (8453 for mainnet, 84532 for sepolia)
        categories: Optional list of categories to filter by
                   (e.g., ['stablecoin', 'wrapped'])
        
    Returns:
        List of token dictionaries with address, symbol, decimals, etc.
        
    Example:
        >>> from basepy.abis import get_common_tokens
        >>> # Get all common tokens
        >>> tokens = get_common_tokens(8453)
        >>> 
        >>> # Get only stablecoins
        >>> stables = get_common_tokens(8453, categories=['stablecoin'])
        >>> for token in stables:
        ...     print(f"{token['symbol']}: {token['address']}")
    """
    network = "mainnet" if chain_id == 8453 else "sepolia" if chain_id == 84532 else None
    
    if not network:
        raise ValueError(f"Invalid chain_id: {chain_id}. Expected 8453 (mainnet) or 84532 (sepolia)")
    
    tokens = BASE_COMMON_TOKENS[network]
    
    # Filter by categories if specified
    if categories:
        categories_lower = [cat.lower() for cat in categories]
        tokens = [t for t in tokens if t.get('category', '').lower() in categories_lower]
    
    return tokens


def get_token_addresses(chain_id: int, categories: list = None) -> list:
    """
    Get list of common token addresses (for batch balance checks).
    
    Args:
        chain_id: Chain ID
        categories: Optional list of categories to filter by
        
    Returns:
        List of token addresses
        
    Example:
        >>> from basepy.abis import get_token_addresses
        >>> addresses = get_token_addresses(8453)
        >>> # Use with client.batch_get_token_balances()
    """
    tokens = get_common_tokens(chain_id, categories)
    return [token['address'] for token in tokens]


def is_erc20_transfer_topic(topic: str) -> bool:
    """
    Check if a log topic is an ERC-20 Transfer event.
    
    Args:
        topic: Topic hash (with or without 0x prefix)
        
    Returns:
        True if topic matches ERC-20 Transfer signature
        
    Example:
        >>> from basepy.abis import is_erc20_transfer_topic
        >>> topic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
        >>> is_erc20_transfer_topic(topic)
        True
    """
    if not topic.startswith('0x'):
        topic = '0x' + topic
    return topic.lower() == ERC20_TRANSFER_TOPIC.lower()


def get_event_topic(event_name: str) -> str:
    """
    Get event topic hash by name.
    
    Args:
        event_name: Event name (e.g., 'erc20_transfer', 'erc20_approval')
        
    Returns:
        Topic hash
        
    Raises:
        ValueError: If event name is invalid
        
    Example:
        >>> from basepy.abis import get_event_topic
        >>> topic = get_event_topic('erc20_transfer')
        >>> print(topic)
        '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
    """
    topics = {
        'erc20_transfer': ERC20_TRANSFER_TOPIC,
        'erc20_approval': ERC20_APPROVAL_TOPIC,
        'erc721_transfer': ERC721_TRANSFER_TOPIC,
        'erc1155_transfer_single': ERC1155_TRANSFER_SINGLE_TOPIC,
        'erc1155_transfer_batch': ERC1155_TRANSFER_BATCH_TOPIC,
        'weth_deposit': WETH_DEPOSIT_TOPIC,
        'weth_withdrawal': WETH_WITHDRAWAL_TOPIC,
    }
    
    event_name = event_name.lower()
    if event_name not in topics:
        available = ", ".join(topics.keys())
        raise ValueError(f"Event '{event_name}' not found. Available: {available}")
    
    return topics[event_name]


# ============================================================================
# PRODUCTION ENHANCEMENTS SUMMARY
# ============================================================================
#
# ✅ EVENT SIGNATURES
# - Added ERC-20, ERC-721, ERC-1155, WETH event topic hashes
# - Enables efficient log filtering and parsing
# - Zero RPC cost for identifying event types
#
# ✅ COMMON TOKEN LISTS
# - BASE_COMMON_TOKENS: Curated list of popular tokens on Base
# - Includes stablecoins, wrapped assets, liquid staking tokens
# - Organized by category for easy filtering
# - Perfect for default portfolio views
#
# ✅ TOKEN CATEGORIES
# - Predefined categories for organizing tokens
# - Useful for filtering (e.g., show only stablecoins)
# - Extensible for custom categorization
#
# ✅ ENHANCED CONTRACT ADDRESSES
# - Added USDT, cbETH, rETH, Multicall3
# - Complete coverage of major Base ecosystem tokens
# - Both mainnet and testnet support
#
# ✅ UTILITY FUNCTIONS
# - get_common_tokens(): Get token list with optional filtering
# - get_token_addresses(): Extract addresses for batch operations
# - is_erc20_transfer_topic(): Quick event type checking
# - get_event_topic(): Get topic hash by human-readable name
#
# ✅ DOCUMENTATION
# - Complete docstrings with examples
# - Clear parameter descriptions
# - Usage patterns for common scenarios
#
# BACKWARD COMPATIBILITY:
# - All existing constants and functions unchanged
# - New features are purely additive
# - No breaking changes
# ============================================================================