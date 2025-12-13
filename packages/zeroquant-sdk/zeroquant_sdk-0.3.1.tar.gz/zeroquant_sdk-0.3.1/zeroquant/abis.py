"""Contract ABIs for ZeroQuant."""

UVA_FACTORY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "salt", "type": "uint256"}
        ],
        "name": "createAccount",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "uint256", "name": "salt", "type": "uint256"}
        ],
        "name": "getAccountAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "account", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "salt", "type": "uint256"}
        ],
        "name": "AccountCreated",
        "type": "event"
    }
]

UVA_ACCOUNT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "target", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "bytes", "name": "data", "type": "bytes"}
        ],
        "name": "execute",
        "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address[]", "name": "targets", "type": "address[]"},
            {"internalType": "uint256[]", "name": "values", "type": "uint256[]"},
            {"internalType": "bytes[]", "name": "calldatas", "type": "bytes[]"}
        ],
        "name": "executeBatch",
        "outputs": [{"internalType": "bytes[]", "name": "", "type": "bytes[]"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

SWAP_INTENT_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "executeSwap",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "payable",
        "type": "function"
    }
]

PERMISSION_MANAGER_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "agent", "type": "address"},
            {"internalType": "uint256", "name": "expiresAt", "type": "uint256"},
            {"internalType": "uint256", "name": "dailyLimitUSD", "type": "uint256"},
            {"internalType": "uint256", "name": "perTxLimitUSD", "type": "uint256"},
            {"internalType": "uint256", "name": "maxPositionSizePct", "type": "uint256"},
            {"internalType": "uint256", "name": "maxSlippageBps", "type": "uint256"},
            {"internalType": "uint256", "name": "maxLeverage", "type": "uint256"},
            {"internalType": "bytes4[]", "name": "allowedOperations", "type": "bytes4[]"},
            {"internalType": "address[]", "name": "allowedProtocols", "type": "address[]"}
        ],
        "name": "createSession",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "hasActiveSession",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "sessions",
        "outputs": [
            {"internalType": "address", "name": "agent", "type": "address"},
            {"internalType": "uint256", "name": "expiresAt", "type": "uint256"},
            {"internalType": "uint256", "name": "dailyLimitUSD", "type": "uint256"},
            {"internalType": "uint256", "name": "perTxLimitUSD", "type": "uint256"},
            {"internalType": "uint256", "name": "maxPositionSizePct", "type": "uint256"},
            {"internalType": "uint256", "name": "maxSlippageBps", "type": "uint256"},
            {"internalType": "uint256", "name": "maxLeverage", "type": "uint256"},
            {"internalType": "uint256", "name": "dailySpentUSD", "type": "uint256"},
            {"internalType": "uint256", "name": "lastResetTimestamp", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "agent", "type": "address"}],
        "name": "revokeSession",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "agent", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "expiresAt", "type": "uint256"}
        ],
        "name": "SessionCreated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "agent", "type": "address"}
        ],
        "name": "SessionRevoked",
        "type": "event"
    }
]
