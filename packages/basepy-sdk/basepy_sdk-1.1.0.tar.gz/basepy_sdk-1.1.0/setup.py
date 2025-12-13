# File: setup.py
"""
Setup configuration for BasePy SDK.
Production-ready Python SDK for Base blockchain.
"""

from setuptools import setup, find_packages
import re
import os


# ============================================================================
# VERSION MANAGEMENT (Single source of truth)
# ============================================================================

def get_version():
    """Read version from basepy/__init__.py"""
    init_path = os.path.join(
        os.path.dirname(__file__), 
        'basepy', 
        '__init__.py'
    )
    
    try:
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(
                r'^__version__\s*=\s*["\']([^"\']+)["\']',
                content,
                re.MULTILINE
            )
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    
    # Fallback version
    return "1.1.0"


# ============================================================================
# LONG DESCRIPTION (from README)
# ============================================================================

def get_long_description():
    """Read README.md for package description"""
    readme_path = os.path.join(
        os.path.dirname(__file__), 
        'README.md'
    )
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback description if README doesn't exist yet
        return """
# BasePy SDK

Production-ready Python SDK for Base blockchain with unique zero-cost features.

## Features

- ✅ Complete read/write operations for Base L2
- ✅ Zero-cost ERC-20 transfer decoding
- ✅ 80% fewer RPC calls for portfolio operations
- ✅ Automatic retry & gas optimization
- ✅ L1+L2 fee calculation
- ✅ Production resilience (circuit breaker, rate limiting)
- ✅ Thread-safe operations
- ✅ Comprehensive error handling

## Quick Start
```python
from basepy import BaseClient, Wallet, Transaction

# Read operations (no wallet needed)
client = BaseClient()
balance = client.get_balance("0xYourAddress...")

# Write operations (wallet required)
wallet = Wallet(private_key="0x...", client=client)
tx = Transaction(client, wallet)
tx_hash = tx.send_eth("0xRecipient...", 0.1)
```

## Installation
```bash
pip install basepy-sdk
```
"""


# ============================================================================
# SETUP CONFIGURATION
# ============================================================================

setup(
    # ========================================================================
    # PACKAGE IDENTITY
    # ========================================================================
    name="basepy-sdk",
    version=get_version(),
    
    # ========================================================================
    # AUTHOR & CONTACT
    # ========================================================================
    author="BasePy Team",
    author_email="contact@basepy.dev",  # TODO: Update with real email
    maintainer="BasePy Team",
    maintainer_email="contact@basepy.dev",
    
    # ========================================================================
    # DESCRIPTION
    # ========================================================================
    description="Production-ready Python SDK for Base blockchain with zero-cost ERC-20 decoding",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    
    # ========================================================================
    # URLS
    # ========================================================================
    url="https://github.com/basepy/basepy-sdk",  # TODO: Update with real URL
    project_urls={
        "Homepage": "https://basepy.dev",
        "Documentation": "https://docs.basepy.dev",
        "Source": "https://github.com/basepy/basepy-sdk",
        "Bug Tracker": "https://github.com/basepy/basepy-sdk/issues",
        "Changelog": "https://github.com/basepy/basepy-sdk/blob/main/CHANGELOG.md",
    },
    
    # ========================================================================
    # PACKAGE DISCOVERY
    # ========================================================================
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
            "examples",
            "examples.*",
            "docs",
            "docs.*",
        ]
    ),
    
    # ========================================================================
    # CLASSIFIERS (PyPI categories)
    # ========================================================================
    classifiers=[
        # Development status
        "Development Status :: 4 - Beta",
        
        # Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        
        # Topics
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: Office/Business :: Financial",
        
        # REMOVE THIS:
        # "License :: OSI Approved :: MIT License",
        
        # Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        
        # Operating systems
        "Operating System :: OS Independent",
        
        # Other
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    
    # ========================================================================
    # KEYWORDS (for PyPI search)
    # ========================================================================
    keywords=" ".join([
        "base",
        "blockchain",
        "ethereum",
        "l2",
        "layer2",
        "optimism",
        "web3",
        "crypto",
        "cryptocurrency",
        "erc20",
        "defi",
        "smart-contracts",
        "coinbase",
    ]),
    
    # ========================================================================
    # PYTHON VERSION REQUIREMENTS
    # ========================================================================
    python_requires=">=3.8",
    
    # ========================================================================
    # DEPENDENCIES
    # ========================================================================
    install_requires=[
        "web3>=6.0.0,<7.0.0",
        "eth-account>=0.9.0",
        "eth-utils>=2.0.0",
    ],
    
    # ========================================================================
    # OPTIONAL DEPENDENCIES
    # ========================================================================
    extras_require={
        # Development tools
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "pre-commit>=3.0.0",
        ],
        
        # Documentation tools
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.22.0",
        ],
        
        # Testing tools
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.22.0",
        ],
        
        # All development dependencies
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "pre-commit>=3.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    
    # ========================================================================
    # LICENSE
    # ========================================================================
    license="MIT",
    
    # ========================================================================
    # PACKAGE DATA
    # ========================================================================
    include_package_data=True,
    package_data={
        "basepy": [
            "py.typed",  # PEP 561 - type hints
        ],
    },
    
    # ========================================================================
    # ZIP SAFE
    # ========================================================================
    zip_safe=False,  # Don't install as zip (better for debugging)
    
    # ========================================================================
    # ENTRY POINTS (Optional - CLI commands)
    # ========================================================================
    # entry_points={
    #     "console_scripts": [
    #         "basepy=basepy.cli:main",
    #     ],
    # },
)