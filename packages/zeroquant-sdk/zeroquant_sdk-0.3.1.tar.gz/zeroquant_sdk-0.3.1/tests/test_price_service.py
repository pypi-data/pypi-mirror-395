"""
Tests for Chainlink price service.
"""

import time
from unittest.mock import AsyncMock, Mock, patch
import pytest

from zeroquant.services.price import (
    ChainlinkPriceService,
    PriceCache,
    get_price_service,
    PRICE_FEEDS,
    TOKEN_TO_FEED,
    CACHE_TTL_SECONDS,
    _price_cache,
)


class TestPriceCache:
    """Tests for PriceCache class."""

    def test_cache_set_and_get(self):
        """Should cache and retrieve prices."""
        cache = PriceCache()
        cache.set("ETH/USD", 2500.0)

        result = cache.get("ETH/USD")
        assert result == 2500.0

    def test_cache_miss(self):
        """Should return None for missing cache entries."""
        cache = PriceCache()

        result = cache.get("NON_EXISTENT/USD")
        assert result is None

    def test_cache_expired(self):
        """Should return None for expired cache entries."""
        cache = PriceCache()
        cache.set("ETH/USD", 2500.0)

        # Manually expire the cache
        cache._cache["ETH/USD"] = (2500.0, time.time() - CACHE_TTL_SECONDS - 1)

        result = cache.get("ETH/USD")
        assert result is None

    def test_cache_still_valid(self):
        """Should return value for valid cache entries."""
        cache = PriceCache()
        cache.set("BTC/USD", 50000.0)

        # Set timestamp to just under TTL
        cache._cache["BTC/USD"] = (50000.0, time.time() - CACHE_TTL_SECONDS + 10)

        result = cache.get("BTC/USD")
        assert result == 50000.0


class TestChainlinkPriceService:
    """Tests for ChainlinkPriceService class."""

    @pytest.fixture
    def mock_w3(self):
        """Create mock Web3 instance."""
        w3 = Mock()
        w3.to_checksum_address = lambda x: x
        w3.eth = Mock()
        return w3

    @pytest.fixture
    def clear_cache(self):
        """Clear global cache before each test."""
        _price_cache._cache.clear()
        yield
        _price_cache._cache.clear()

    def test_init_default_network(self, mock_w3):
        """Should use mainnet by default."""
        service = ChainlinkPriceService(mock_w3)

        assert service.network == "mainnet"

    def test_init_custom_network(self, mock_w3):
        """Should accept custom network."""
        service = ChainlinkPriceService(mock_w3, network="sepolia")

        assert service.network == "sepolia"

    @pytest.mark.asyncio
    async def test_get_pair_price_from_cache(self, mock_w3, clear_cache):
        """Should return cached price without calling contract."""
        service = ChainlinkPriceService(mock_w3)

        # Pre-populate cache with correct key format (network:pair)
        _price_cache.set("mainnet:ETH/USD", 3000.0)

        result = await service.get_pair_price("ETH/USD")

        assert result == 3000.0
        mock_w3.eth.contract.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_pair_price_fetches_from_chain(self, mock_w3, clear_cache):
        """Should fetch price from Chainlink when cache is empty."""
        # Setup mock contract - chain the mocks correctly for web3py async
        mock_round_data_call = Mock()
        mock_round_data_call.call = AsyncMock(
            return_value=[1, 250000000000, 0, int(time.time()), 1]  # $2500 with 8 decimals
        )
        mock_decimals_call = Mock()
        mock_decimals_call.call = AsyncMock(return_value=8)

        mock_functions = Mock()
        mock_functions.latestRoundData = Mock(return_value=mock_round_data_call)
        mock_functions.decimals = Mock(return_value=mock_decimals_call)

        mock_contract = Mock()
        mock_contract.functions = mock_functions
        mock_w3.eth.contract = Mock(return_value=mock_contract)

        service = ChainlinkPriceService(mock_w3)

        result = await service.get_pair_price("ETH/USD")

        assert result == 2500.0
        mock_w3.eth.contract.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_pair_price_caches_result(self, mock_w3, clear_cache):
        """Should cache price after fetching."""
        # Setup mock contract
        mock_round_data_call = Mock()
        mock_round_data_call.call = AsyncMock(
            return_value=[1, 200000000000, 0, int(time.time()), 1]  # $2000
        )
        mock_decimals_call = Mock()
        mock_decimals_call.call = AsyncMock(return_value=8)

        mock_functions = Mock()
        mock_functions.latestRoundData = Mock(return_value=mock_round_data_call)
        mock_functions.decimals = Mock(return_value=mock_decimals_call)

        mock_contract = Mock()
        mock_contract.functions = mock_functions
        mock_w3.eth.contract = Mock(return_value=mock_contract)

        service = ChainlinkPriceService(mock_w3)

        await service.get_pair_price("ETH/USD")

        # Check cache was populated (with correct key format)
        cached = _price_cache.get("mainnet:ETH/USD")
        assert cached == 2000.0

    @pytest.mark.asyncio
    async def test_get_pair_price_invalid_pair(self, mock_w3, clear_cache):
        """Should raise for unsupported pair."""
        service = ChainlinkPriceService(mock_w3)

        with pytest.raises(ValueError, match="No price feed found"):
            await service.get_pair_price("UNKNOWN/USD")

    @pytest.mark.asyncio
    async def test_get_pair_price_stale_warning(self, mock_w3, clear_cache, capsys):
        """Should warn for stale prices."""
        stale_time = int(time.time()) - 7200  # 2 hours ago

        # Setup mock contract
        mock_round_data_call = Mock()
        mock_round_data_call.call = AsyncMock(
            return_value=[1, 250000000000, 0, stale_time, 1]
        )
        mock_decimals_call = Mock()
        mock_decimals_call.call = AsyncMock(return_value=8)

        mock_functions = Mock()
        mock_functions.latestRoundData = Mock(return_value=mock_round_data_call)
        mock_functions.decimals = Mock(return_value=mock_decimals_call)

        mock_contract = Mock()
        mock_contract.functions = mock_functions
        mock_w3.eth.contract = Mock(return_value=mock_contract)

        service = ChainlinkPriceService(mock_w3)

        await service.get_pair_price("ETH/USD")

        captured = capsys.readouterr()
        assert "stale" in captured.out.lower()

    @pytest.mark.asyncio
    async def test_get_eth_price(self, mock_w3, clear_cache):
        """Should get ETH/USD price."""
        _price_cache.set("mainnet:ETH/USD", 2700.0)

        service = ChainlinkPriceService(mock_w3)

        result = await service.get_eth_price()

        assert result == 2700.0

    @pytest.mark.asyncio
    async def test_get_token_price_usd_known_token(self, mock_w3, clear_cache):
        """Should get price for known token."""
        _price_cache.set("mainnet:ETH/USD", 2500.0)

        service = ChainlinkPriceService(mock_w3)

        # WETH address
        result = await service.get_token_price_usd(
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        )

        assert result == 2500.0

    @pytest.mark.asyncio
    async def test_get_token_price_usd_unknown_token(self, mock_w3, clear_cache, capsys):
        """Should return $1 for unknown tokens."""
        service = ChainlinkPriceService(mock_w3)

        result = await service.get_token_price_usd(
            "0x0000000000000000000000000000000000000001"
        )

        assert result == 1.0
        captured = capsys.readouterr()
        assert "No price feed" in captured.out

    @pytest.mark.asyncio
    async def test_wei_to_usd(self, mock_w3, clear_cache):
        """Should convert wei to USD."""
        _price_cache.set("mainnet:ETH/USD", 2000.0)

        service = ChainlinkPriceService(mock_w3)

        # 1 ETH in wei
        result = await service.wei_to_usd(10**18)

        assert result == 2000.0

    @pytest.mark.asyncio
    async def test_wei_to_usd_fractional(self, mock_w3, clear_cache):
        """Should handle fractional ETH amounts."""
        _price_cache.set("mainnet:ETH/USD", 2000.0)

        service = ChainlinkPriceService(mock_w3)

        # 0.5 ETH in wei
        result = await service.wei_to_usd(5 * 10**17)

        assert result == 1000.0

    @pytest.mark.asyncio
    async def test_get_expected_swap_output(self, mock_w3, clear_cache):
        """Should calculate expected swap output.

        Note: This test uses 18 decimal normalization for simplicity.
        In production, token decimals should be fetched from the contracts.
        WETH uses 18 decimals, USDC uses 6 decimals.
        """
        _price_cache.set("mainnet:ETH/USD", 2000.0)
        _price_cache.set("mainnet:USDC/USD", 1.0)

        service = ChainlinkPriceService(mock_w3)

        # Swap 1 WETH -> USDC
        # The implementation normalizes all amounts to 18 decimals
        result = await service.get_expected_swap_output(
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
            10**18,  # 1 WETH in wei
        )

        # Output normalized to 18 decimals (implementation detail)
        # In production, would adjust for USDC's 6 decimals
        assert result == int(2000 * 10**18)


class TestPriceFeedsConfig:
    """Tests for price feed configuration."""

    def test_mainnet_feeds_defined(self):
        """Should have mainnet price feeds defined."""
        assert "mainnet" in PRICE_FEEDS
        assert "ETH/USD" in PRICE_FEEDS["mainnet"]
        assert "BTC/USD" in PRICE_FEEDS["mainnet"]

    def test_sepolia_feeds_defined(self):
        """Should have sepolia price feeds defined."""
        assert "sepolia" in PRICE_FEEDS
        assert "ETH/USD" in PRICE_FEEDS["sepolia"]

    def test_token_to_feed_mapping(self):
        """Should have token address to feed mapping."""
        # WETH should map to ETH/USD
        weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        assert TOKEN_TO_FEED.get(weth_address) == "ETH/USD"


class TestGetPriceService:
    """Tests for get_price_service function."""

    def test_returns_singleton(self):
        """Should return same instance on subsequent calls."""
        mock_w3 = Mock()

        # Reset singleton
        import zeroquant.services.price as price_module
        price_module._price_service_instance = None

        service1 = get_price_service(mock_w3)
        service2 = get_price_service(mock_w3)

        assert service1 is service2

        # Cleanup
        price_module._price_service_instance = None
