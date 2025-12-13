"""
Base Exchange Adapter
Abstract base class for all centralized exchange adapters
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Callable, Set
import time
import secrets

from ..orders.mvo import MinimumViableOrder, ExchangeOrderResponse
from .types import (
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
)


# Event types
ExchangeAdapterEvent = Dict[str, Any]
ExchangeAdapterListener = Callable[[ExchangeAdapterEvent], None]


class BaseExchangeAdapter(ABC):
    """
    Abstract base class for exchange adapters.
    Each exchange implementation extends this class.
    """

    def __init__(self, config: ExchangeConfig):
        """Initialize adapter with configuration."""
        self.config = config
        self._listeners: Set[ExchangeAdapterListener] = set()

    @property
    @abstractmethod
    def exchange(self) -> SupportedExchange:
        """Get exchange identifier."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Get exchange display name."""
        pass

    @abstractmethod
    def to_exchange_format(self, order: MinimumViableOrder) -> Dict[str, Any]:
        """Convert MVO to exchange-specific order format."""
        pass

    @abstractmethod
    def from_exchange_format(self, response: Dict[str, Any]) -> ExchangeOrderResponse:
        """Convert exchange response to standard format."""
        pass

    @abstractmethod
    def to_exchange_symbol(self, symbol: str) -> str:
        """Convert symbol to exchange format (e.g., 'ETH/USDC' -> 'ETHUSDC')."""
        pass

    @abstractmethod
    def from_exchange_symbol(self, symbol: str) -> str:
        """Convert symbol from exchange format."""
        pass

    @abstractmethod
    async def _submit_to_exchange(
        self,
        order: Dict[str, Any],
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Submit order to exchange."""
        pass

    @abstractmethod
    async def _cancel_on_exchange(
        self,
        order_id: str,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Dict[str, Any]:
        """Cancel order on exchange."""
        pass

    @abstractmethod
    async def _query_from_exchange(
        self,
        request: QueryOrdersRequest,
    ) -> List[Dict[str, Any]]:
        """Query orders from exchange."""
        pass

    @abstractmethod
    async def get_market_data(
        self,
        symbol: str,
        credentials: ExchangeCredentials,
    ) -> Optional[MarketData]:
        """Get market data for validation."""
        pass

    @abstractmethod
    def _create_signature(
        self,
        method: str,
        path: str,
        body: str,
        credentials: ExchangeCredentials,
    ) -> Dict[str, str]:
        """Create signed request headers."""
        pass

    async def route_order(self, request: RouteOrderRequest) -> RouteOrderResponse:
        """Route order through adapter with validation."""
        request_id = self._generate_request_id()
        timestamp = int(time.time() * 1000)

        try:
            # Validate order first (unless skipped)
            if request.skip_validation:
                validation = ValidationResult(
                    valid=True,
                    errors=[],
                    warnings=["Validation skipped"],
                )
                order_to_submit = request.order
            else:
                validation = await self.validate_order(
                    request.order,
                    request.validation_rules,
                    request.credentials,
                )

                self._emit({
                    "type": "order_validated",
                    "order": request.order.model_dump(),
                    "result": validation.model_dump(),
                })

                # If validation failed, reject order
                if not validation.valid:
                    self._emit({
                        "type": "order_rejected",
                        "order": request.order.model_dump(),
                        "errors": [e.model_dump() for e in validation.errors],
                    })

                    return RouteOrderResponse(
                        success=False,
                        validation=validation,
                        error="; ".join(e.message for e in validation.errors),
                        error_code="VALIDATION_FAILED",
                        timestamp=timestamp,
                        request_id=request_id,
                    )

                # Use adjusted order if provided
                order_to_submit = validation.adjusted_order or request.order

            # Dry run - return without submitting
            if request.dry_run:
                return RouteOrderResponse(
                    success=True,
                    validation=validation,
                    timestamp=timestamp,
                    request_id=request_id,
                )

            # Convert to exchange format and submit
            exchange_order = self.to_exchange_format(order_to_submit)

            self._emit({
                "type": "order_submitted",
                "order": order_to_submit.model_dump(),
                "exchange": self.exchange.value,
            })

            raw_response = await self._submit_to_exchange(
                exchange_order,
                request.credentials,
            )

            # Convert response to standard format
            exchange_response = self.from_exchange_format(raw_response)

            self._emit({
                "type": "order_response",
                "response": exchange_response.model_dump(),
            })

            return RouteOrderResponse(
                success=True,
                validation=validation,
                exchange_response=exchange_response,
                raw_response=raw_response,
                timestamp=timestamp,
                request_id=request_id,
            )

        except Exception as e:
            error_message = str(e)

            self._emit({
                "type": "order_error",
                "error": error_message,
            })

            return RouteOrderResponse(
                success=False,
                validation=ValidationResult(valid=False, errors=[], warnings=[]),
                error=error_message,
                error_code="SUBMISSION_ERROR",
                timestamp=timestamp,
                request_id=request_id,
            )

    async def cancel_order(self, request: CancelOrderRequest) -> CancelOrderResponse:
        """Cancel order through adapter."""
        timestamp = int(time.time() * 1000)

        try:
            order_id = request.exchange_order_id or request.order_id
            await self._cancel_on_exchange(order_id, request.symbol, request.credentials)

            return CancelOrderResponse(
                success=True,
                order_id=order_id,
                timestamp=timestamp,
            )
        except Exception as e:
            return CancelOrderResponse(
                success=False,
                error=str(e),
                timestamp=timestamp,
            )

    async def query_orders(self, request: QueryOrdersRequest) -> List[ExchangeOrderResponse]:
        """Query orders through adapter."""
        raw_orders = await self._query_from_exchange(request)
        return [self.from_exchange_format(raw) for raw in raw_orders]

    async def validate_order(
        self,
        order: MinimumViableOrder,
        rules: Optional[ValidationRules] = None,
        credentials: Optional[ExchangeCredentials] = None,
    ) -> ValidationResult:
        """Validate order against rules and exchange limits."""
        errors: List[ValidationError] = []
        warnings: List[str] = []

        # Basic required field validation
        if not order.symbol and not order.base_asset:
            errors.append(ValidationError(
                code="MISSING_SYMBOL",
                message="Order must have symbol or base_asset",
                field="symbol",
            ))

        if not order.side:
            errors.append(ValidationError(
                code="MISSING_SIDE",
                message="Order must have side (buy/sell)",
                field="side",
            ))

        if order.original_quantity_base is None:
            errors.append(ValidationError(
                code="MISSING_QUANTITY",
                message="Order must have quantity",
                field="original_quantity_base",
            ))
        elif order.original_quantity_base <= 0:
            errors.append(ValidationError(
                code="INVALID_QUANTITY",
                message="Order quantity must be positive",
                field="original_quantity_base",
                value=order.original_quantity_base,
            ))

        # Validate against rules if provided
        if rules:
            # Check allowed pairs
            if rules.allowed_pairs and order.symbol:
                normalized = order.symbol.upper().replace("/", "")
                allowed = any(
                    p.upper().replace("/", "") == normalized
                    for p in rules.allowed_pairs
                )
                if not allowed:
                    errors.append(ValidationError(
                        code="PAIR_NOT_ALLOWED",
                        message=f"Trading pair {order.symbol} is not in allowed list",
                        field="symbol",
                        value=order.symbol,
                    ))

            # Check blocked pairs
            if rules.blocked_pairs and order.symbol:
                normalized = order.symbol.upper().replace("/", "")
                blocked = any(
                    p.upper().replace("/", "") == normalized
                    for p in rules.blocked_pairs
                )
                if blocked:
                    errors.append(ValidationError(
                        code="PAIR_BLOCKED",
                        message=f"Trading pair {order.symbol} is blocked",
                        field="symbol",
                        value=order.symbol,
                    ))

            # Check per-transaction limit
            if (
                rules.per_tx_limit_usd
                and order.original_price
                and order.original_quantity_base
            ):
                order_value = order.original_price * order.original_quantity_base
                if order_value > rules.per_tx_limit_usd:
                    errors.append(ValidationError(
                        code="EXCEEDS_TX_LIMIT",
                        message=f"Order value ${order_value:.2f} exceeds per-transaction limit of ${rules.per_tx_limit_usd}",
                        field="value",
                        value=order_value,
                        limit=rules.per_tx_limit_usd,
                    ))

            # Check daily limit
            if rules.daily_limit_usd and rules.daily_spent_usd is not None:
                remaining = rules.daily_limit_usd - rules.daily_spent_usd
                if order.original_price and order.original_quantity_base:
                    order_value = order.original_price * order.original_quantity_base
                    if order_value > remaining:
                        errors.append(ValidationError(
                            code="EXCEEDS_DAILY_LIMIT",
                            message=f"Order value ${order_value:.2f} exceeds remaining daily limit of ${remaining:.2f}",
                            field="value",
                            value=order_value,
                            limit=remaining,
                        ))

            # Check max order value
            if (
                rules.max_order_value_usd
                and order.original_price
                and order.original_quantity_base
            ):
                order_value = order.original_price * order.original_quantity_base
                if order_value > rules.max_order_value_usd:
                    errors.append(ValidationError(
                        code="EXCEEDS_MAX_VALUE",
                        message=f"Order value ${order_value:.2f} exceeds maximum of ${rules.max_order_value_usd}",
                        field="value",
                        value=order_value,
                        limit=rules.max_order_value_usd,
                    ))

            # Check reduce-only requirement
            if rules.require_reduce_only and not order.reduce_only:
                errors.append(ValidationError(
                    code="REDUCE_ONLY_REQUIRED",
                    message="Orders must be reduce-only in current context",
                    field="reduce_only",
                    value=False,
                ))

        # Try to get market data for exchange-specific validation
        if credentials and order.symbol and not errors:
            try:
                market_data = await self.get_market_data(order.symbol, credentials)
                if market_data:
                    # Check min order size
                    if (
                        market_data.min_order_size
                        and order.original_quantity_base
                        and order.original_quantity_base < market_data.min_order_size
                    ):
                        errors.append(ValidationError(
                            code="BELOW_MIN_SIZE",
                            message=f"Order quantity {order.original_quantity_base} is below minimum {market_data.min_order_size}",
                            field="original_quantity_base",
                            value=order.original_quantity_base,
                            limit=market_data.min_order_size,
                        ))

                    # Check max order size
                    if (
                        market_data.max_order_size
                        and order.original_quantity_base
                        and order.original_quantity_base > market_data.max_order_size
                    ):
                        errors.append(ValidationError(
                            code="ABOVE_MAX_SIZE",
                            message=f"Order quantity {order.original_quantity_base} exceeds maximum {market_data.max_order_size}",
                            field="original_quantity_base",
                            value=order.original_quantity_base,
                            limit=market_data.max_order_size,
                        ))
            except Exception:
                warnings.append("Could not fetch market data for validation")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _infer_order_type(self, order: MinimumViableOrder) -> str:
        """Infer order type from MVO."""
        if order.original_price is None or order.original_price == 0:
            return "market"
        return "limit"

    def subscribe(self, listener: ExchangeAdapterListener) -> Callable[[], None]:
        """Subscribe to adapter events."""
        self._listeners.add(listener)
        return lambda: self._listeners.discard(listener)

    def _emit(self, event: ExchangeAdapterEvent) -> None:
        """Emit event to all listeners."""
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return f"req_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
