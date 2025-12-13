"""
Exchange Order Router
Agnostic validation and routing layer for centralized exchanges

Key Features:
- Exchange-agnostic order validation
- Routes orders to correct exchange with original credentials
- Supports agent permission limits
- Event-based tracking
"""

import time
import secrets
from typing import Optional, List, Dict, Any, Set, Callable
from pydantic import BaseModel, Field

from ..orders.mvo import MinimumViableOrder, ExchangeOrderResponse
from .types import (
    SupportedExchange,
    ExchangeCredentials,
    ValidationRules,
    ValidationResult,
    RouteOrderRequest,
    RouteOrderResponse,
    CancelOrderRequest,
    CancelOrderResponse,
    QueryOrdersRequest,
)
from .base_adapter import BaseExchangeAdapter, ExchangeAdapterListener
from .binance import BinanceAdapter
from .coinbase import CoinbaseAdapter
from .kraken import KrakenAdapter


class RouterConfig(BaseModel):
    """Router configuration."""
    default_validation_rules: Optional[ValidationRules] = Field(
        None, description="Default validation rules for all orders"
    )
    enable_logging: bool = Field(default=False, description="Enable request logging")

    class Config:
        extra = "allow"


class RouterStats(BaseModel):
    """Router statistics."""
    total_orders: int = Field(default=0)
    successful_orders: int = Field(default=0)
    failed_orders: int = Field(default=0)
    rejected_orders: int = Field(default=0)
    orders_by_exchange: Dict[str, int] = Field(default_factory=dict)
    average_validation_time: float = Field(default=0.0)
    average_routing_time: float = Field(default=0.0)
    # Internal counters for incremental average calculation
    _validation_count: int = Field(default=0, exclude=True)
    _routing_count: int = Field(default=0, exclude=True)


class OrderLogEntry(BaseModel):
    """Order log entry."""
    timestamp: int
    request_id: str
    exchange: str
    action: str
    success: bool
    duration: float
    error: Optional[str] = None


class ExchangeRouter:
    """
    Central routing layer for sending orders to centralized exchanges.
    Validates orders against agent permissions before forwarding.

    Example:
        router = ExchangeRouter(RouterConfig(
            default_validation_rules=ValidationRules(
                max_order_value_usd=10000,
                daily_limit_usd=50000,
            )
        ))

        result = await router.route_order(RouteOrderRequest(
            order=MinimumViableOrder(
                symbol="ETH/USDC",
                side="buy",
                original_quantity_base=1.5,
                original_price=2000,
            ),
            exchange=SupportedExchange.BINANCE,
            credentials=ExchangeCredentials(
                api_key=os.environ["BINANCE_API_KEY"],
                api_secret=os.environ["BINANCE_API_SECRET"],
            ),
        ))

        if result.success:
            print(f"Order placed: {result.exchange_response.exchange_order_id}")
        else:
            print(f"Order failed: {result.error}")
    """

    def __init__(
        self,
        config: Optional[RouterConfig] = None,
        custom_adapters: Optional[List[BaseExchangeAdapter]] = None,
    ):
        """
        Initialize exchange router.

        Args:
            config: Router configuration
            custom_adapters: Custom exchange adapters to register
        """
        self.config = config or RouterConfig()
        self._adapters: Dict[SupportedExchange, BaseExchangeAdapter] = {}
        self._listeners: Set[ExchangeAdapterListener] = set()
        self._order_log: List[OrderLogEntry] = []
        self._stats = RouterStats()

        # Initialize default adapters
        self._initialize_adapters()

        # Add custom adapters
        if custom_adapters:
            for adapter in custom_adapters:
                self._adapters[adapter.exchange] = adapter
                adapter.subscribe(self._handle_adapter_event)

    def _initialize_adapters(self) -> None:
        """Initialize default exchange adapters."""
        # Binance
        binance = BinanceAdapter()
        self._adapters[SupportedExchange.BINANCE] = binance
        binance.subscribe(self._handle_adapter_event)

        # Coinbase
        coinbase = CoinbaseAdapter()
        self._adapters[SupportedExchange.COINBASE] = coinbase
        coinbase.subscribe(self._handle_adapter_event)

        # Kraken
        kraken = KrakenAdapter()
        self._adapters[SupportedExchange.KRAKEN] = kraken
        kraken.subscribe(self._handle_adapter_event)

    def get_adapter(self, exchange: SupportedExchange) -> Optional[BaseExchangeAdapter]:
        """Get adapter for exchange."""
        return self._adapters.get(exchange)

    def get_supported_exchanges(self) -> List[SupportedExchange]:
        """Get all supported exchanges."""
        return list(self._adapters.keys())

    async def route_order(self, request: RouteOrderRequest) -> RouteOrderResponse:
        """
        Route order to exchange.

        This is the main entry point for order routing. It:
        1. Validates the order against rules
        2. Routes to the appropriate exchange adapter
        3. Returns unified response
        """
        start_time = time.time()

        # Get adapter for exchange
        adapter = self._adapters.get(request.exchange)
        if not adapter:
            return RouteOrderResponse(
                success=False,
                validation=ValidationResult(valid=False, errors=[], warnings=[]),
                error=f"Unsupported exchange: {request.exchange}",
                error_code="UNSUPPORTED_EXCHANGE",
                timestamp=int(time.time() * 1000),
                request_id=self._generate_request_id(),
            )

        # Merge default validation rules with request-specific rules
        validation_start = time.time()
        validation_rules = None
        if self.config.default_validation_rules or request.validation_rules:
            default_dict = self.config.default_validation_rules.model_dump() if self.config.default_validation_rules else {}
            request_dict = request.validation_rules.model_dump() if request.validation_rules else {}
            merged = {**default_dict, **request_dict}
            validation_rules = ValidationRules(**{k: v for k, v in merged.items() if v is not None})

        # Create updated request with merged rules
        updated_request = RouteOrderRequest(
            order=request.order,
            exchange=request.exchange,
            credentials=request.credentials,
            validation_rules=validation_rules,
            skip_validation=request.skip_validation,
            dry_run=request.dry_run,
        )
        validation_duration = time.time() - validation_start

        # Route through adapter
        result = await adapter.route_order(updated_request)
        total_duration = time.time() - start_time

        # Update stats with both validation and total routing time
        self._update_stats(result, request.exchange, total_duration, validation_duration)

        # Log if enabled
        if self.config.enable_logging:
            self._log_order(OrderLogEntry(
                timestamp=int(time.time() * 1000),
                request_id=result.request_id,
                exchange=request.exchange.value,
                action="route",
                success=result.success,
                duration=total_duration,
                error=result.error,
            ))

        return result

    async def validate_order(
        self,
        order: MinimumViableOrder,
        exchange: SupportedExchange,
        credentials: Optional[ExchangeCredentials] = None,
        rules: Optional[ValidationRules] = None,
    ) -> ValidationResult:
        """Validate order without submitting."""
        adapter = self._adapters.get(exchange)
        if not adapter:
            return ValidationResult(
                valid=False,
                errors=[{"code": "UNSUPPORTED_EXCHANGE", "message": f"Unsupported exchange: {exchange}"}],
                warnings=[],
            )

        # Merge rules
        merged_rules = None
        if self.config.default_validation_rules or rules:
            default_dict = self.config.default_validation_rules.model_dump() if self.config.default_validation_rules else {}
            request_dict = rules.model_dump() if rules else {}
            merged = {**default_dict, **request_dict}
            merged_rules = ValidationRules(**{k: v for k, v in merged.items() if v is not None})

        return await adapter.validate_order(order, merged_rules, credentials)

    async def cancel_order(self, request: CancelOrderRequest) -> CancelOrderResponse:
        """Cancel order on exchange."""
        start_time = time.time()

        adapter = self._adapters.get(request.exchange)
        if not adapter:
            return CancelOrderResponse(
                success=False,
                error=f"Unsupported exchange: {request.exchange}",
                timestamp=int(time.time() * 1000),
            )

        result = await adapter.cancel_order(request)

        if self.config.enable_logging:
            self._log_order(OrderLogEntry(
                timestamp=int(time.time() * 1000),
                request_id=self._generate_request_id(),
                exchange=request.exchange.value,
                action="cancel",
                success=result.success,
                duration=time.time() - start_time,
                error=result.error,
            ))

        return result

    async def query_orders(self, request: QueryOrdersRequest) -> List[ExchangeOrderResponse]:
        """Query orders from exchange."""
        adapter = self._adapters.get(request.exchange)
        if not adapter:
            raise Exception(f"Unsupported exchange: {request.exchange}")

        return await adapter.query_orders(request)

    async def route_orders_batch(
        self,
        requests: List[RouteOrderRequest],
    ) -> List[RouteOrderResponse]:
        """Batch route multiple orders."""
        import asyncio

        # Route orders in parallel
        results = await asyncio.gather(
            *[self.route_order(req) for req in requests],
            return_exceptions=True,
        )

        # Convert exceptions to failed responses
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(RouteOrderResponse(
                    success=False,
                    validation=ValidationResult(valid=False, errors=[], warnings=[]),
                    error=str(result),
                    error_code="BATCH_ERROR",
                    timestamp=int(time.time() * 1000),
                    request_id=self._generate_request_id(),
                ))
            else:
                processed_results.append(result)

        return processed_results

    def subscribe(self, listener: ExchangeAdapterListener) -> Callable[[], None]:
        """Subscribe to router events."""
        self._listeners.add(listener)
        return lambda: self._listeners.discard(listener)

    def get_stats(self) -> RouterStats:
        """Get router statistics."""
        return self._stats.model_copy()

    def get_order_log(self, limit: Optional[int] = None) -> List[OrderLogEntry]:
        """Get order log."""
        log = list(self._order_log)
        if limit:
            return log[-limit:]
        return log

    def clear_order_log(self) -> None:
        """Clear order log."""
        self._order_log = []

    def reset_stats(self) -> None:
        """Reset statistics."""
        self._stats = RouterStats()

    def _handle_adapter_event(self, event: Dict[str, Any]) -> None:
        """Handle adapter events."""
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass

    def _update_stats(
        self,
        result: RouteOrderResponse,
        exchange: SupportedExchange,
        routing_duration: float,
        validation_duration: float = 0.0,
    ) -> None:
        """Update statistics."""
        self._stats.total_orders += 1

        if result.success:
            self._stats.successful_orders += 1
        elif not result.validation.valid:
            self._stats.rejected_orders += 1
        else:
            self._stats.failed_orders += 1

        # Update by exchange
        exchange_key = exchange.value
        self._stats.orders_by_exchange[exchange_key] = (
            self._stats.orders_by_exchange.get(exchange_key, 0) + 1
        )

        # Update average routing time using incremental average
        self._stats._routing_count += 1
        n_routing = self._stats._routing_count
        self._stats.average_routing_time = (
            self._stats.average_routing_time + (routing_duration - self._stats.average_routing_time) / n_routing
        )

        # Update average validation time using incremental average
        if validation_duration > 0:
            self._stats._validation_count += 1
            n_validation = self._stats._validation_count
            self._stats.average_validation_time = (
                self._stats.average_validation_time + (validation_duration - self._stats.average_validation_time) / n_validation
            )

    def _log_order(self, entry: OrderLogEntry) -> None:
        """Log order."""
        self._order_log.append(entry)

        # Keep log size manageable
        if len(self._order_log) > 10000:
            self._order_log = self._order_log[-5000:]

    def _generate_request_id(self) -> str:
        """Generate request ID."""
        return f"router_{int(time.time() * 1000)}_{secrets.token_hex(4)}"

    async def close(self) -> None:
        """Close all adapters."""
        for adapter in self._adapters.values():
            if hasattr(adapter, 'close'):
                await adapter.close()


def create_router(config: Optional[RouterConfig] = None) -> ExchangeRouter:
    """Create a pre-configured router with common settings."""
    return ExchangeRouter(config)


def create_agent_router(
    daily_limit_usd: float,
    per_tx_limit_usd: float,
    allowed_pairs: Optional[List[str]] = None,
    **kwargs,
) -> ExchangeRouter:
    """
    Create router with agent limits.

    Args:
        daily_limit_usd: Daily spending limit in USD
        per_tx_limit_usd: Per-transaction limit in USD
        allowed_pairs: Optional list of allowed trading pairs
    """
    return ExchangeRouter(RouterConfig(
        default_validation_rules=ValidationRules(
            daily_limit_usd=daily_limit_usd,
            per_tx_limit_usd=per_tx_limit_usd,
            allowed_pairs=allowed_pairs,
        ),
        **kwargs,
    ))
