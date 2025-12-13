# ZeroQuant Python SDK

Python SDK for ZeroQuant agentic DeFi vaults with built-in LangChain support.

## Installation

```bash
pip install zeroquant
```

### With LangChain support

```bash
pip install zeroquant[langchain]
```

## Quick Start

```python
import asyncio
from zeroquant import ZeroQuantClient
from zeroquant.models import VaultConfig

async def main():
    client = ZeroQuantClient(
        provider="https://sepolia.infura.io/v3/YOUR_KEY",
        config=VaultConfig(
            owner="0x...",
            permission_manager="0x...",
            factory_address="0x..."
        ),
        private_key="0x..."
    )

    # Create vault
    vault_address = await client.create_vault(salt=12345)
    print(f"Vault created: {vault_address}")

    # Check balance
    balance = await client.get_balance()
    print(f"Balance: {balance / 10**18} ETH")

asyncio.run(main())
```

## LangChain Integration

```python
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from zeroquant.langchain import CreateVaultTool, ExecuteSwapTool, GetVaultBalanceTool

tools = [
    CreateVaultTool(client=client),
    ExecuteSwapTool(client=client, swap_intent=swap_intent),
    GetVaultBalanceTool(client=client)
]

agent = initialize_agent(
    tools,
    ChatOpenAI(model="gpt-4"),
    agent=AgentType.OPENAI_FUNCTIONS
)

result = agent.run("Create a vault and swap 1 ETH for USDC")
```

## Authentication Modes

### 1. Agent Wallet
```python
client = ZeroQuantClient(
    provider="https://...",
    config=config,
    private_key="0x..."  # Agent's private key
)
```

### 2. Delegated Signing
```python
client = ZeroQuantClient(
    provider="https://...",
    config=config,
    session_key="0x...",
    delegation_proof="0x..."
)
```

### 3. API Key
```python
client = ZeroQuantClient(
    provider="https://...",
    config=config,
    api_key="zq_live_...",
    api_url="https://api.zeroquant.io"
)
```

## Features

- **Async-first** - Built with asyncio for efficient I/O
- **Type-safe** - Full Pydantic models with validation
- **LangChain tools** - Built-in tools for AI agents
- **Multi-modal auth** - Wallet, delegated, or API key
- **Comprehensive** - Feature parity with TypeScript SDK

## Examples

See `examples/` directory for complete examples:
- `basic_swap.py` - Create vault and execute swap
- `langchain_agent.py` - LangChain agent with ZeroQuant tools

## Documentation

Full documentation: https://docs.zeroquant.io

## License

MIT
