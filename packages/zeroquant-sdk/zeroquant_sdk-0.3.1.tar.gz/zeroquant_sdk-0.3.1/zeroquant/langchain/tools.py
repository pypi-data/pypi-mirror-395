# packages/python-sdk/zeroquant/langchain/tools.py
"""LangChain tools for ZeroQuant vault operations.

This module provides BaseTool implementations that wrap ZeroQuant SDK functionality,
enabling LangChain agents to interact with DeFi vaults through natural language.
"""

import asyncio
from typing import TYPE_CHECKING, Any, Optional
from langchain.tools import BaseTool
from pydantic import Field

if TYPE_CHECKING:
    from zeroquant.client import ZeroQuantClient
    from zeroquant.intents.swap import SwapIntent
    from zeroquant.services.price import ChainlinkPriceService


class CreateVaultTool(BaseTool):
    """Creates a new ZeroQuant vault for managing DeFi operations."""

    name: str = "create_vault"
    description: str = """
    Creates a new ZeroQuant vault for managing DeFi operations.
    The vault has permission controls and can execute swaps, lends, and other operations.

    Args:
        salt: Unique number for deterministic address generation (any integer)

    Returns:
        The address of the newly created vault
    """

    client: Any = Field(exclude=True)

    def _run(self, salt: int) -> str:
        """Synchronous run - executes async method via asyncio."""
        address = asyncio.run(self.client.create_vault(salt))
        return f"Vault created at {address}. You can now fund and use this vault for DeFi operations."

    async def _arun(self, salt: int) -> str:
        """Asynchronous run - preferred for async contexts."""
        address = await self.client.create_vault(salt)
        return f"Vault created at {address}. You can now fund and use this vault for DeFi operations."


class ExecuteSwapTool(BaseTool):
    """Executes a token swap through Uniswap with slippage protection."""

    name: str = "execute_swap"
    description: str = """
    Swaps tokens through Uniswap with slippage protection.

    Args:
        vault_address: Address of the vault to swap from
        from_token: Address of input token (use "ETH" for native ETH)
        to_token: Address of output token
        amount: Amount to swap in wei (e.g., "1000000000000000000" for 1 ETH)
        max_slippage: Maximum slippage in percent (e.g., 0.5 for 0.5%)

    Returns:
        Description of the swap result including amounts and gas cost
    """

    client: Any = Field(exclude=True)
    swap_intent: Any = Field(exclude=True)
    price_service: Any = Field(default=None, exclude=True)

    def _run(
        self,
        vault_address: str,
        from_token: str,
        to_token: str,
        amount: str,
        max_slippage: float
    ) -> str:
        """Synchronous run - executes async method via asyncio."""
        return asyncio.run(self._arun(vault_address, from_token, to_token, amount, max_slippage))

    async def _arun(
        self,
        vault_address: str,
        from_token: str,
        to_token: str,
        amount: str,
        max_slippage: float
    ) -> str:
        """Asynchronous run - preferred for async contexts."""
        from zeroquant.models import SwapParams

        # Connect to vault
        await self.client.connect_vault(vault_address)

        # Build swap parameters
        amount_int = int(amount)

        # Get expected output from Chainlink price oracle
        if self.price_service:
            expected_out = await self.price_service.get_expected_swap_output(
                from_token, to_token, amount_int
            )
        else:
            # Fallback to mock if price service not configured
            from zeroquant.services.price import get_price_service
            try:
                price_service = get_price_service(self.client.w3)
                expected_out = await price_service.get_expected_swap_output(
                    from_token, to_token, amount_int
                )
            except Exception:
                # Last resort fallback
                expected_out = amount_int * 2000

        slippage_bps = int(max_slippage * 100)  # Convert percent to basis points
        min_out = self.swap_intent.calculate_min_output(expected_out, slippage_bps)

        params = SwapParams(
            amount_in=amount_int,
            amount_out_min=min_out,
            path=[from_token, to_token],
            to=vault_address,
            deadline=self.swap_intent.get_deadline()
        )

        # Execute swap
        execute_params = self.swap_intent.build_execute_params(params)
        receipt = await self.client.execute(
            execute_params.target,
            execute_params.value,
            execute_params.data
        )

        # Format response
        tx_hash = receipt['transactionHash'].hex() if isinstance(receipt['transactionHash'], bytes) else receipt['transactionHash']
        return f"Swapped {amount} {from_token} for tokens. Gas used: {receipt['gasUsed']}. Transaction: {tx_hash}"


class GetVaultBalanceTool(BaseTool):
    """Gets the ETH balance of a vault."""

    name: str = "get_vault_balance"
    description: str = """
    Retrieves the current ETH balance of a vault.

    Args:
        vault_address: Address of the vault to query

    Returns:
        Balance in ETH with description
    """

    client: Any = Field(exclude=True)

    def _run(self, vault_address: str) -> str:
        """Synchronous run - executes async method via asyncio."""
        return asyncio.run(self._arun(vault_address))

    async def _arun(self, vault_address: str) -> str:
        """Asynchronous run - preferred for async contexts."""
        # Connect to vault
        await self.client.connect_vault(vault_address)

        # Get balance
        balance_wei = await self.client.get_balance()
        balance_eth = balance_wei / 10**18

        # Format response
        return f"Vault balance: {balance_eth:.4f} ETH ({balance_wei} wei)"
