"""
Tests for ZeroQuant Exchange Adapters Module
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import time

from zeroquant.exchange_adapters import (
    SupportedExchange,
    ExchangeCredentials,
    ExchangeConfig,
    ValidationRules,
    ValidationResult,
    ValidationError,
    RouteOrderRequest,
    RouteOrderResponse,
    CancelOrderRequest,
    CancelOrderResponse,
    QueryOrdersRequest,
    MarketData,
    BinanceAdapter,
    CoinbaseAdapter,
    KrakenAdapter,
    ExchangeRouter,
    RouterConfig,
    RouterStats,
    create_router,
    create_agent_router,
)
from zeroquant.orders.mvo import MinimumViableOrder, ExchangeOrderResponse


class TestExchangeTypes:
    """Test exchange types and models."""

    def test_supported_exchange_enum(self):
        """Test SupportedExchange enum values."""
        assert SupportedExchange.BINANCE == "binance"
        assert SupportedExchange.COINBASE == "coinbase"
        assert SupportedExchange.KRAKEN == "kraken"

    def test_exchange_credentials_creation(self):
        """Test ExchangeCredentials creation."""
        creds = ExchangeCredentials(
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_passphrase",
        )

        assert creds.api_key == "test_key"
        assert creds.api_secret == "test_secret"
        assert creds.passphrase == "test_passphrase"

    def test_validation_rules_creation(self):
        """Test ValidationRules creation."""
        rules = ValidationRules(
            max_order_value_usd=10000,
            per_tx_limit_usd=5000,
            daily_limit_usd=50000,
            allowed_pairs=["ETH/USDC", "BTC/USDC"],
        )

        assert rules.max_order_value_usd == 10000
        assert rules.per_tx_limit_usd == 5000
        assert rules.daily_limit_usd == 50000
        assert "ETH/USDC" in rules.allowed_pairs

    def test_validation_result_success(self):
        """Test ValidationResult for success."""
        result = ValidationResult(valid=True, errors=[], warnings=[])

        assert result.valid is True
        assert len(result.errors) == 0

    def test_validation_result_failure(self):
        """Test ValidationResult for failure."""
        result = ValidationResult(
            valid=False,
            errors=[
                ValidationError(
                    code="EXCEEDS_LIMIT",
                    message="Order exceeds limit",
                    field="value",
                    value=15000,
                    limit=10000,
                )
            ],
            warnings=["Price is near limit"],
        )

        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "EXCEEDS_LIMIT"

    def test_market_data_creation(self):
        """Test MarketData creation."""
        data = MarketData(
            symbol="ETH/USDC",
            current_price=2000.0,
            min_order_size=0.01,
            max_order_size=1000.0,
            tick_size=0.01,
            step_size=0.001,
        )

        assert data.symbol == "ETH/USDC"
        assert data.current_price == 2000.0
        assert data.min_order_size == 0.01


class TestBinanceAdapter:
    """Test Binance adapter."""

    def test_adapter_creation(self):
        """Test BinanceAdapter creation."""
        adapter = BinanceAdapter(testnet=True)

        assert adapter.exchange == SupportedExchange.BINANCE
        assert adapter.display_name == "Binance"
        assert "testnet" in adapter.base_url

    def test_symbol_conversion(self):
        """Test symbol conversion."""
        adapter = BinanceAdapter()

        # To exchange format
        assert adapter.to_exchange_symbol("ETH/USDC") == "ETHUSDC"
        assert adapter.to_exchange_symbol("BTC/USDT") == "BTCUSDT"

        # From exchange format
        assert adapter.from_exchange_symbol("ETHUSDC") == "ETH/USDC"
        assert adapter.from_exchange_symbol("BTCUSDT") == "BTC/USDT"

    def test_order_conversion_market(self):
        """Test market order conversion."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=1.5,
        )

        binance_order = adapter.to_exchange_format(order)

        assert binance_order["symbol"] == "ETHUSDC"
        assert binance_order["side"] == "BUY"
        assert binance_order["type"] == "MARKET"
        assert binance_order["quantity"] == "1.5"

    def test_order_conversion_limit(self):
        """Test limit order conversion."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="sell",
            original_quantity_base=2.0,
            original_price=2100.0,
            time_in_force="gtc",
        )

        binance_order = adapter.to_exchange_format(order)

        assert binance_order["symbol"] == "ETHUSDC"
        assert binance_order["side"] == "SELL"
        assert binance_order["type"] == "LIMIT"
        assert binance_order["price"] == "2100.0"
        assert binance_order["timeInForce"] == "GTC"

    def test_response_conversion(self):
        """Test response conversion."""
        adapter = BinanceAdapter()

        binance_response = {
            "orderId": 12345,
            "status": "FILLED",
            "type": "LIMIT",
            "executedQty": "1.5",
            "cummulativeQuoteQty": "3150.0",
            "fills": [
                {
                    "price": "2100.0",
                    "qty": "1.5",
                    "commission": "1.5",
                    "commissionAsset": "USDC",
                }
            ],
        }

        response = adapter.from_exchange_format(binance_response)

        assert response.exchange_order_id == "12345"
        assert response.status == "filled"
        assert response.executed_quantity_base == 1.5
        assert response.fee_paid == 1.5
        assert response.fee_asset == "USDC"


class TestCoinbaseAdapter:
    """Test Coinbase adapter."""

    def test_adapter_creation(self):
        """Test CoinbaseAdapter creation."""
        adapter = CoinbaseAdapter(testnet=True)

        assert adapter.exchange == SupportedExchange.COINBASE
        assert adapter.display_name == "Coinbase"
        assert "sandbox" in adapter.base_url

    def test_symbol_conversion(self):
        """Test symbol conversion."""
        adapter = CoinbaseAdapter()

        # To exchange format
        assert adapter.to_exchange_symbol("ETH/USDC") == "ETH-USDC"
        assert adapter.to_exchange_symbol("BTC/USD") == "BTC-USD"

        # From exchange format
        assert adapter.from_exchange_symbol("ETH-USDC") == "ETH/USDC"

    def test_order_conversion_market(self):
        """Test market order conversion."""
        adapter = CoinbaseAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=1.0,
        )

        cb_order = adapter.to_exchange_format(order)

        assert cb_order["product_id"] == "ETH-USDC"
        assert cb_order["side"] == "BUY"
        assert "market_market_ioc" in cb_order["order_configuration"]

    def test_order_conversion_limit_gtc(self):
        """Test limit GTC order conversion."""
        adapter = CoinbaseAdapter()

        order = MinimumViableOrder(
            symbol="BTC/USDC",
            side="sell",
            original_quantity_base=0.5,
            original_price=50000.0,
            time_in_force="gtc",
        )

        cb_order = adapter.to_exchange_format(order)

        assert cb_order["product_id"] == "BTC-USDC"
        assert cb_order["side"] == "SELL"
        assert "limit_limit_gtc" in cb_order["order_configuration"]
        assert cb_order["order_configuration"]["limit_limit_gtc"]["limit_price"] == "50000.0"


class TestKrakenAdapter:
    """Test Kraken adapter."""

    def test_adapter_creation(self):
        """Test KrakenAdapter creation."""
        adapter = KrakenAdapter()

        assert adapter.exchange == SupportedExchange.KRAKEN
        assert adapter.display_name == "Kraken"

    def test_symbol_conversion(self):
        """Test symbol conversion."""
        adapter = KrakenAdapter()

        # Known mappings
        assert adapter.to_exchange_symbol("BTC/USD") == "XXBTZUSD"
        assert adapter.to_exchange_symbol("ETH/USD") == "XETHZUSD"

        # Unknown pairs pass through
        assert adapter.to_exchange_symbol("SOL/USDC") == "SOLUSDC"

    def test_order_conversion(self):
        """Test order conversion."""
        adapter = KrakenAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USD",
            side="buy",
            original_quantity_base=2.0,
            original_price=1800.0,
        )

        kraken_order = adapter.to_exchange_format(order)

        assert kraken_order["pair"] == "XETHZUSD"
        assert kraken_order["type"] == "buy"
        assert kraken_order["ordertype"] == "limit"
        assert kraken_order["volume"] == "2.0"
        assert kraken_order["price"] == "1800.0"


class TestValidation:
    """Test order validation."""

    @pytest.mark.asyncio
    async def test_validate_missing_symbol(self):
        """Test validation fails for missing symbol."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            side="buy",
            original_quantity_base=1.0,
        )

        result = await adapter.validate_order(order)

        assert result.valid is False
        assert any(e.code == "MISSING_SYMBOL" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_missing_side(self):
        """Test validation fails for missing side."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            original_quantity_base=1.0,
        )

        result = await adapter.validate_order(order)

        assert result.valid is False
        assert any(e.code == "MISSING_SIDE" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_invalid_quantity(self):
        """Test validation fails for invalid quantity."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=-1.0,
        )

        result = await adapter.validate_order(order)

        assert result.valid is False
        assert any(e.code == "INVALID_QUANTITY" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_exceeds_tx_limit(self):
        """Test validation fails when exceeding per-tx limit."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=10.0,
            original_price=2000.0,  # $20,000 order
        )

        rules = ValidationRules(per_tx_limit_usd=10000)

        result = await adapter.validate_order(order, rules)

        assert result.valid is False
        assert any(e.code == "EXCEEDS_TX_LIMIT" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_exceeds_daily_limit(self):
        """Test validation fails when exceeding daily limit."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=5.0,
            original_price=2000.0,  # $10,000 order
        )

        rules = ValidationRules(
            daily_limit_usd=15000,
            daily_spent_usd=10000,  # Only $5000 remaining
        )

        result = await adapter.validate_order(order, rules)

        assert result.valid is False
        assert any(e.code == "EXCEEDS_DAILY_LIMIT" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_blocked_pair(self):
        """Test validation fails for blocked pairs."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="DOGE/USDC",
            side="buy",
            original_quantity_base=1000.0,
            original_price=0.1,
        )

        rules = ValidationRules(blocked_pairs=["DOGE/USDC"])

        result = await adapter.validate_order(order, rules)

        assert result.valid is False
        assert any(e.code == "PAIR_BLOCKED" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_allowed_pairs(self):
        """Test validation fails for non-allowed pairs."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="XRP/USDC",
            side="buy",
            original_quantity_base=100.0,
            original_price=0.5,
        )

        rules = ValidationRules(allowed_pairs=["ETH/USDC", "BTC/USDC"])

        result = await adapter.validate_order(order, rules)

        assert result.valid is False
        assert any(e.code == "PAIR_NOT_ALLOWED" for e in result.errors)

    @pytest.mark.asyncio
    async def test_validate_success(self):
        """Test successful validation."""
        adapter = BinanceAdapter()

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=1.0,
            original_price=2000.0,
        )

        rules = ValidationRules(
            per_tx_limit_usd=10000,
            daily_limit_usd=50000,
            allowed_pairs=["ETH/USDC", "BTC/USDC"],
        )

        result = await adapter.validate_order(order, rules)

        assert result.valid is True
        assert len(result.errors) == 0


class TestExchangeRouter:
    """Test exchange router."""

    def test_router_creation(self):
        """Test ExchangeRouter creation."""
        router = ExchangeRouter()

        supported = router.get_supported_exchanges()
        assert SupportedExchange.BINANCE in supported
        assert SupportedExchange.COINBASE in supported
        assert SupportedExchange.KRAKEN in supported

    def test_router_with_config(self):
        """Test router with configuration."""
        router = ExchangeRouter(RouterConfig(
            default_validation_rules=ValidationRules(
                per_tx_limit_usd=10000,
            ),
            enable_logging=True,
        ))

        assert router.config.enable_logging is True
        assert router.config.default_validation_rules.per_tx_limit_usd == 10000

    def test_get_adapter(self):
        """Test getting adapter by exchange."""
        router = ExchangeRouter()

        binance = router.get_adapter(SupportedExchange.BINANCE)
        assert binance is not None
        assert binance.exchange == SupportedExchange.BINANCE

    def test_create_router(self):
        """Test create_router factory."""
        router = create_router(RouterConfig(enable_logging=True))

        assert router is not None
        assert router.config.enable_logging is True

    def test_create_agent_router(self):
        """Test create_agent_router factory."""
        router = create_agent_router(
            daily_limit_usd=50000,
            per_tx_limit_usd=10000,
            allowed_pairs=["ETH/USDC"],
        )

        assert router is not None
        assert router.config.default_validation_rules.daily_limit_usd == 50000
        assert router.config.default_validation_rules.per_tx_limit_usd == 10000

    @pytest.mark.asyncio
    async def test_validate_order_via_router(self):
        """Test order validation through router."""
        router = create_agent_router(
            daily_limit_usd=50000,
            per_tx_limit_usd=5000,
        )

        order = MinimumViableOrder(
            symbol="ETH/USDC",
            side="buy",
            original_quantity_base=5.0,
            original_price=2000.0,  # $10,000 - exceeds per-tx limit
        )

        result = await router.validate_order(
            order,
            SupportedExchange.BINANCE,
        )

        assert result.valid is False
        assert any(e.code == "EXCEEDS_TX_LIMIT" for e in result.errors)

    def test_router_stats(self):
        """Test router statistics."""
        router = ExchangeRouter()

        stats = router.get_stats()

        assert stats.total_orders == 0
        assert stats.successful_orders == 0
        assert stats.failed_orders == 0

    def test_router_event_subscription(self):
        """Test event subscription."""
        router = ExchangeRouter()
        events = []

        unsubscribe = router.subscribe(lambda e: events.append(e))

        # Unsubscribe
        unsubscribe()

        # Should be callable without error
        assert True


class TestRouteOrderRequest:
    """Test RouteOrderRequest."""

    def test_request_creation(self):
        """Test request creation."""
        request = RouteOrderRequest(
            order=MinimumViableOrder(
                symbol="ETH/USDC",
                side="buy",
                original_quantity_base=1.0,
            ),
            exchange=SupportedExchange.BINANCE,
            credentials=ExchangeCredentials(
                api_key="test",
                api_secret="secret",
            ),
        )

        assert request.order.symbol == "ETH/USDC"
        assert request.exchange == SupportedExchange.BINANCE
        assert request.dry_run is False

    def test_request_with_validation_rules(self):
        """Test request with validation rules."""
        request = RouteOrderRequest(
            order=MinimumViableOrder(
                symbol="ETH/USDC",
                side="buy",
                original_quantity_base=1.0,
            ),
            exchange=SupportedExchange.BINANCE,
            credentials=ExchangeCredentials(
                api_key="test",
                api_secret="secret",
            ),
            validation_rules=ValidationRules(
                per_tx_limit_usd=10000,
            ),
            dry_run=True,
        )

        assert request.validation_rules.per_tx_limit_usd == 10000
        assert request.dry_run is True


class TestDryRun:
    """Test dry run functionality."""

    @pytest.mark.asyncio
    async def test_dry_run_valid_order(self):
        """Test dry run with valid order."""
        router = ExchangeRouter()

        request = RouteOrderRequest(
            order=MinimumViableOrder(
                symbol="ETH/USDC",
                side="buy",
                original_quantity_base=1.0,
                original_price=2000.0,
            ),
            exchange=SupportedExchange.BINANCE,
            credentials=ExchangeCredentials(
                api_key="test",
                api_secret="secret",
            ),
            dry_run=True,
        )

        result = await router.route_order(request)

        # Dry run should succeed without actually submitting
        assert result.success is True
        assert result.validation.valid is True
        assert result.exchange_response is None  # Not submitted

    @pytest.mark.asyncio
    async def test_dry_run_invalid_order(self):
        """Test dry run with invalid order."""
        router = create_agent_router(
            daily_limit_usd=50000,
            per_tx_limit_usd=5000,
        )

        request = RouteOrderRequest(
            order=MinimumViableOrder(
                symbol="ETH/USDC",
                side="buy",
                original_quantity_base=10.0,
                original_price=2000.0,  # $20,000 exceeds limit
            ),
            exchange=SupportedExchange.BINANCE,
            credentials=ExchangeCredentials(
                api_key="test",
                api_secret="secret",
            ),
            dry_run=True,
        )

        result = await router.route_order(request)

        # Should fail validation even in dry run
        assert result.success is False
        assert result.validation.valid is False
