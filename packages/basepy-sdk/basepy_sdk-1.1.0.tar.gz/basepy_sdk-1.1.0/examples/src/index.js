import React, { useState, useEffect } from 'react';
import { Search, Activity, Wallet, DollarSign, TrendingUp, RefreshCw, AlertCircle, CheckCircle, Clock, Copy, ExternalLink } from 'lucide-react';

const BaseBlockchainDashboard = () => {
  const [activeTab, setActiveTab] = useState('network');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Network State
  const [networkInfo, setNetworkInfo] = useState({
    chainId: 8453,
    blockNumber: 0,
    gasPrice: 0,
    baseFee: 0
  });
  
  // Account State
  const [accountAddress, setAccountAddress] = useState('');
  const [accountData, setAccountData] = useState(null);
  
  // Transaction State
  const [txHash, setTxHash] = useState('');
  const [txData, setTxData] = useState(null);
  
  // Token State
  const [tokenAddress, setTokenAddress] = useState('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'); // USDC default
  const [tokenData, setTokenData] = useState(null);
  const [tokenHolder, setTokenHolder] = useState('');

  // API Base URL
  const API_BASE_URL = 'http://localhost:5000/api';

  // Fetch Network Data from Backend
  const fetchNetworkData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch network info
      const networkResponse = await fetch(`${API_BASE_URL}/network/info`);
      const networkResult = await networkResponse.json();
      
      // Fetch gas prices
      const gasResponse = await fetch(`${API_BASE_URL}/network/gas`);
      const gasResult = await gasResponse.json();
      
      if (networkResult.success && gasResult.success) {
        setNetworkInfo({
          chainId: networkResult.data.chainId,
          blockNumber: networkResult.data.blockNumber,
          gasPrice: gasResult.data.gasPriceGwei.toFixed(4),
          baseFee: gasResult.data.baseFeeGwei.toFixed(4),
          connected: networkResult.data.connected
        });
      } else {
        setError('Failed to fetch network data');
      }
    } catch (err) {
      setError(`Backend connection failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const lookupAccount = async () => {
    if (!accountAddress) return;
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/account/lookup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ address: accountAddress })
      });
      
      const result = await response.json();
      
      if (result.success) {
        setAccountData({
          address: result.data.address,
          balance: result.data.balanceEth.toFixed(6),
          txCount: result.data.transactionCount,
          isContract: result.data.isContract,
          codeSize: result.data.codeSize
        });
      } else {
        setError(result.error || 'Failed to lookup account');
      }
    } catch (err) {
      setError(`Request failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const lookupTransaction = async () => {
    if (!txHash) return;
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/transaction/lookup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ txHash: txHash })
      });
      
      const result = await response.json();
      
      if (result.success) {
        setTxData({
          hash: txHash,
          status: result.data.status,
          from: result.data.from,
          to: result.data.to,
          value: result.data.valueEth.toFixed(6),
          blockNumber: result.data.blockNumber,
          gasUsed: result.data.gasUsed,
          gasPrice: result.data.gasPriceGwei.toFixed(4),
          l2Cost: result.data.l2CostEth.toFixed(8),
          l1Cost: result.data.l1FeeEth.toFixed(8),
          totalCost: result.data.totalCostEth.toFixed(8)
        });
      } else {
        setError(result.error || 'Failed to lookup transaction');
      }
    } catch (err) {
      setError(`Request failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const lookupToken = async () => {
    if (!tokenAddress) return;
    setLoading(true);
    setError(null);
    
    try {
      // First get token info
      const infoResponse = await fetch(`${API_BASE_URL}/token/info`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tokenAddress: tokenAddress })
      });
      
      const infoResult = await infoResponse.json();
      
      if (!infoResult.success) {
        setError(infoResult.error || 'Failed to lookup token');
        setLoading(false);
        return;
      }
      
      let holderBalance = null;
      
      // If holder address provided, get balance
      if (tokenHolder && tokenHolder.trim()) {
        try {
          const balanceResponse = await fetch(`${API_BASE_URL}/token/balance`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              tokenAddress: tokenAddress,
              holderAddress: tokenHolder 
            })
          });
          
          const balanceResult = await balanceResponse.json();
          
          if (balanceResult.success) {
            holderBalance = balanceResult.data.balanceFormatted.toFixed(2);
          }
        } catch (err) {
          console.error('Failed to fetch holder balance:', err);
        }
      }
      
      setTokenData({
        address: tokenAddress,
        symbol: infoResult.data.symbol,
        name: infoResult.data.name,
        decimals: infoResult.data.decimals,
        totalSupply: infoResult.data.totalSupplyFormatted.toString(),
        holderBalance: holderBalance
      });
      
    } catch (err) {
      setError(`Request failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const formatAddress = (addr) => {
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
  };

  useEffect(() => {
    fetchNetworkData();
  }, []);

  const StatusBadge = ({ status }) => {
    const configs = {
      confirmed: { icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50', text: 'Confirmed' },
      pending: { icon: Clock, color: 'text-yellow-500', bg: 'bg-yellow-50', text: 'Pending' },
      failed: { icon: AlertCircle, color: 'text-red-500', bg: 'bg-red-50', text: 'Failed' }
    };
    
    const config = configs[status] || configs.confirmed;
    const Icon = config.icon;
    
    return (
      <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${config.bg}`}>
        <Icon className={`w-4 h-4 ${config.color}`} />
        <span className={`font-medium ${config.color}`}>{config.text}</span>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Base Blockchain Dashboard</h1>
                <p className="text-sm text-gray-500">Professional blockchain monitoring & analytics</p>
              </div>
            </div>
            <button 
              onClick={fetchNetworkData}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Network Status Bar */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-3">
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-gray-600">Network:</span>
              <span className="font-semibold text-gray-900">Base Mainnet</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600">Block:</span>
              <span className="font-semibold text-gray-900">#{networkInfo.blockNumber.toLocaleString()}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600">Gas:</span>
              <span className="font-semibold text-gray-900">{networkInfo.gasPrice} Gwei</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600">Base Fee:</span>
              <span className="font-semibold text-gray-900">{networkInfo.baseFee} Gwei</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-2 mb-6 bg-white p-1 rounded-lg shadow-sm border border-gray-200">
          {[
            { id: 'network', icon: Activity, label: 'Network Info' },
            { id: 'account', icon: Wallet, label: 'Account Lookup' },
            { id: 'transaction', icon: Search, label: 'Transaction' },
            { id: 'token', icon: DollarSign, label: 'Token Info' }
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-md transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-red-900">Error</p>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Network Info Tab */}
        {activeTab === 'network' && (
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-600" />
                Network Details
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center py-3 border-b border-gray-100">
                  <span className="text-gray-600">Chain ID</span>
                  <span className="font-semibold text-gray-900">{networkInfo.chainId}</span>
                </div>
                <div className="flex justify-between items-center py-3 border-b border-gray-100">
                  <span className="text-gray-600">Network Name</span>
                  <span className="font-semibold text-gray-900">Base Mainnet</span>
                </div>
                <div className="flex justify-between items-center py-3 border-b border-gray-100">
                  <span className="text-gray-600">Connection Status</span>
                  <StatusBadge status="confirmed" />
                </div>
                <div className="flex justify-between items-center py-3">
                  <span className="text-gray-600">Network Type</span>
                  <span className="font-semibold text-gray-900">Layer 2 (OP Stack)</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-green-600" />
                Gas Prices
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center py-3 border-b border-gray-100">
                  <span className="text-gray-600">Current Gas Price</span>
                  <span className="font-semibold text-gray-900">{networkInfo.gasPrice} Gwei</span>
                </div>
                <div className="flex justify-between items-center py-3 border-b border-gray-100">
                  <span className="text-gray-600">Base Fee (EIP-1559)</span>
                  <span className="font-semibold text-gray-900">{networkInfo.baseFee} Gwei</span>
                </div>
                <div className="flex justify-between items-center py-3 border-b border-gray-100">
                  <span className="text-gray-600">ETH Transfer Cost</span>
                  <span className="font-semibold text-gray-900">~{(networkInfo.gasPrice * 21000 / 1e9).toFixed(8)} ETH</span>
                </div>
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-900">
                    <strong>Note:</strong> Base transactions include L2 execution + L1 data fees
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Account Lookup Tab */}
        {activeTab === 'account' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Lookup</h3>
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="Enter Ethereum address (0x...)"
                  value={accountAddress}
                  onChange={(e) => setAccountAddress(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && lookupAccount()}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
                <button
                  onClick={lookupAccount}
                  disabled={loading}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                  <Search className="w-5 h-5" />
                  {loading ? 'Searching...' : 'Lookup'}
                </button>
              </div>
            </div>

            {accountData && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-gray-900">Account Information</h3>
                  <button
                    onClick={() => copyToClipboard(accountData.address)}
                    className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <Copy className="w-4 h-4" />
                    Copy Address
                  </button>
                </div>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Address</span>
                    <span className="font-mono text-sm text-gray-900">{formatAddress(accountData.address)}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Balance</span>
                    <span className="font-semibold text-gray-900">{accountData.balance} ETH</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Transactions Sent</span>
                    <span className="font-semibold text-gray-900">{accountData.txCount.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Account Type</span>
                    <span className="font-semibold text-gray-900">
                      {accountData.isContract ? 'Smart Contract' : 'EOA (Wallet)'}
                    </span>
                  </div>
                  {accountData.isContract && (
                    <div className="flex justify-between items-center py-3">
                      <span className="text-gray-600">Contract Code Size</span>
                      <span className="font-semibold text-gray-900">{accountData.codeSize.toLocaleString()} bytes</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Transaction Tab */}
        {activeTab === 'transaction' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Transaction Lookup</h3>
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="Enter transaction hash (0x...)"
                  value={txHash}
                  onChange={(e) => setTxHash(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && lookupTransaction()}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
                <button
                  onClick={lookupTransaction}
                  disabled={loading}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                  <Search className="w-5 h-5" />
                  {loading ? 'Searching...' : 'Lookup'}
                </button>
              </div>
            </div>

            {txData && (
              <div className="grid grid-cols-2 gap-6">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Transaction Details</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">Status</span>
                      <StatusBadge status={txData.status} />
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">From</span>
                      <span className="font-mono text-sm text-gray-900">{formatAddress(txData.from)}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">To</span>
                      <span className="font-mono text-sm text-gray-900">{formatAddress(txData.to)}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">Value</span>
                      <span className="font-semibold text-gray-900">{txData.value} ETH</span>
                    </div>
                    {txData.blockNumber && (
                      <div className="flex justify-between items-center py-3">
                        <span className="text-gray-600">Block Number</span>
                        <span className="font-semibold text-gray-900">#{txData.blockNumber.toLocaleString()}</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Cost Breakdown</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">Gas Used</span>
                      <span className="font-semibold text-gray-900">{txData.gasUsed.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">Gas Price</span>
                      <span className="font-semibold text-gray-900">{txData.gasPrice} Gwei</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">L2 Execution Fee</span>
                      <span className="font-semibold text-gray-900">{txData.l2Cost} ETH</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-gray-100">
                      <span className="text-gray-600">L1 Data Fee</span>
                      <span className="font-semibold text-gray-900">{txData.l1Cost} ETH</span>
                    </div>
                    <div className="flex justify-between items-center py-3 bg-blue-50 rounded-lg px-3">
                      <span className="font-semibold text-gray-900">Total Cost</span>
                      <span className="font-bold text-blue-600">{txData.totalCost} ETH</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Token Info Tab */}
        {activeTab === 'token' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">ERC-20 Token Lookup</h3>
              <div className="space-y-3">
                <div className="flex gap-3">
                  <input
                    type="text"
                    placeholder="Enter token contract address (0x...)"
                    value={tokenAddress}
                    onChange={(e) => setTokenAddress(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && lookupToken()}
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                  <button
                    onClick={lookupToken}
                    disabled={loading}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                  >
                    <Search className="w-5 h-5" />
                    {loading ? 'Searching...' : 'Lookup'}
                  </button>
                </div>
                <input
                  type="text"
                  placeholder="Optional: Check holder balance (0x...)"
                  value={tokenHolder}
                  onChange={(e) => setTokenHolder(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
              </div>
            </div>

            {tokenData && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Token Information</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Token Symbol</span>
                    <span className="font-bold text-xl text-gray-900">{tokenData.symbol}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Token Name</span>
                    <span className="font-semibold text-gray-900">{tokenData.name}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Decimals</span>
                    <span className="font-semibold text-gray-900">{tokenData.decimals}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-gray-100">
                    <span className="text-gray-600">Total Supply</span>
                    <span className="font-semibold text-gray-900">{parseFloat(tokenData.totalSupply).toLocaleString()} {tokenData.symbol}</span>
                  </div>
                  {tokenData.holderBalance && (
                    <div className="flex justify-between items-center py-3 bg-green-50 rounded-lg px-3">
                      <span className="font-semibold text-gray-900">Holder Balance</span>
                      <span className="font-bold text-green-600">{parseFloat(tokenData.holderBalance).toLocaleString()} {tokenData.symbol}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <p>Base Blockchain Professional Dashboard © 2024</p>
            <div className="flex items-center gap-4">
              <a href="https://docs.base.org" target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
                <ExternalLink className="w-4 h-4" />
                Documentation
              </a>
              <a href="https://basescan.org" target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 hover:text-blue-600 transition-colors">
                <ExternalLink className="w-4 h-4" />
                BaseScan
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BaseBlockchainDashboard;