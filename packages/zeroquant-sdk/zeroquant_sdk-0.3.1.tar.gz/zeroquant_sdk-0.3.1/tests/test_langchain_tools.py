# packages/python-sdk/tests/test_langchain_tools.py
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from zeroquant.langchain.tools import CreateVaultTool, ExecuteSwapTool, GetVaultBalanceTool
from zeroquant.client import ZeroQuantClient
from zeroquant.intents.swap import SwapIntent
from zeroquant.models import VaultConfig


@pytest.fixture
def mock_client():
    """Creates a mock ZeroQuantClient."""
    client = Mock(spec=ZeroQuantClient)
    client.create_vault = AsyncMock(return_value="0x1234567890123456789012345678901234567890")
    client.connect_vault = AsyncMock()
    client.get_balance = AsyncMock(return_value=1000000000000000000)  # 1 ETH in wei
    client.execute = AsyncMock(return_value={
        'transactionHash': b'\x12\x34\x56\x78' * 8,
        'gasUsed': 150000
    })
    return client


@pytest.fixture
def mock_swap_intent():
    """Creates a mock SwapIntent."""
    swap_intent = Mock(spec=SwapIntent)
    swap_intent.calculate_min_output = Mock(return_value=1990000000)
    swap_intent.get_deadline = Mock(return_value=1700000000)
    swap_intent.build_execute_params = Mock()
    swap_intent.build_execute_params.return_value = Mock(
        target="0x2000000000000000000000000000000000000000",
        value=1000000000000000000,
        data=b'\x12\x34\x56\x78'
    )
    return swap_intent


class TestCreateVaultTool:
    """Tests for CreateVaultTool."""

    def test_tool_metadata(self, mock_client):
        """Test that tool has correct name and description."""
        tool = CreateVaultTool(client=mock_client)

        assert tool.name == "create_vault"
        assert "ZeroQuant vault" in tool.description
        assert "DeFi operations" in tool.description

    @pytest.mark.asyncio
    async def test_create_vault_success(self, mock_client):
        """Test successful vault creation."""
        tool = CreateVaultTool(client=mock_client)

        result = await tool._arun(salt=12345)

        mock_client.create_vault.assert_called_once_with(12345)
        assert "0x1234567890123456789012345678901234567890" in result
        assert "Vault created" in result

    def test_sync_run(self, mock_client):
        """Test synchronous run method."""
        tool = CreateVaultTool(client=mock_client)

        result = tool._run(salt=12345)

        assert "0x1234567890123456789012345678901234567890" in result


class TestExecuteSwapTool:
    """Tests for ExecuteSwapTool."""

    def test_tool_metadata(self, mock_client, mock_swap_intent):
        """Test that tool has correct name and description."""
        tool = ExecuteSwapTool(client=mock_client, swap_intent=mock_swap_intent)

        assert tool.name == "execute_swap"
        assert "swap" in tool.description.lower()
        assert "slippage" in tool.description.lower()

    @pytest.mark.asyncio
    async def test_execute_swap_success(self, mock_client, mock_swap_intent):
        """Test successful token swap."""
        tool = ExecuteSwapTool(client=mock_client, swap_intent=mock_swap_intent)

        result = await tool._arun(
            vault_address="0x1234567890123456789012345678901234567890",
            from_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            to_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            amount="1000000000000000000",
            max_slippage=0.5
        )

        mock_client.connect_vault.assert_called_once_with(
            "0x1234567890123456789012345678901234567890"
        )
        mock_swap_intent.calculate_min_output.assert_called_once()
        mock_swap_intent.build_execute_params.assert_called_once()
        mock_client.execute.assert_called_once()

        assert "Swapped" in result
        assert "Gas used" in result

    @pytest.mark.asyncio
    async def test_execute_swap_with_slippage_calculation(self, mock_client, mock_swap_intent):
        """Test that slippage is correctly converted to basis points."""
        tool = ExecuteSwapTool(client=mock_client, swap_intent=mock_swap_intent)

        await tool._arun(
            vault_address="0x1234567890123456789012345678901234567890",
            from_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            to_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            amount="1000000000000000000",
            max_slippage=0.5
        )

        # Verify slippage was converted to basis points (0.5% = 50 bps)
        call_args = mock_swap_intent.calculate_min_output.call_args
        assert call_args[0][1] == 50  # 0.5 * 100 = 50 bps


class TestGetVaultBalanceTool:
    """Tests for GetVaultBalanceTool."""

    def test_tool_metadata(self, mock_client):
        """Test that tool has correct name and description."""
        tool = GetVaultBalanceTool(client=mock_client)

        assert tool.name == "get_vault_balance"
        assert "balance" in tool.description.lower()
        assert "vault" in tool.description.lower()

    @pytest.mark.asyncio
    async def test_get_balance_success(self, mock_client):
        """Test successful balance retrieval."""
        tool = GetVaultBalanceTool(client=mock_client)

        result = await tool._arun(vault_address="0x1234567890123456789012345678901234567890")

        mock_client.connect_vault.assert_called_once_with(
            "0x1234567890123456789012345678901234567890"
        )
        mock_client.get_balance.assert_called_once()

        assert "Vault balance" in result
        assert "1.0000 ETH" in result
        assert "1000000000000000000 wei" in result

    @pytest.mark.asyncio
    async def test_get_balance_formatting(self, mock_client):
        """Test that balance is correctly formatted."""
        # Test with different balance
        mock_client.get_balance = AsyncMock(return_value=500000000000000000)  # 0.5 ETH
        tool = GetVaultBalanceTool(client=mock_client)

        result = await tool._arun(vault_address="0x1234567890123456789012345678901234567890")

        assert "0.5000 ETH" in result
        assert "500000000000000000 wei" in result
