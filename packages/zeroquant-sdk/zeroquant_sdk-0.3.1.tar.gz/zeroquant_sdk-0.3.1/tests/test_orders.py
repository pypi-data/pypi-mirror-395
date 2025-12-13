"""
Tests for ZeroQuant Order Management Module
"""

import pytest
from datetime import datetime
from zeroquant.orders import (
    Order,
    OrderFill,
    OrderFees,
    CreateOrderParams,
    OrderSide,
    OrderType,
    TimeInForce,
    OrderStatus,
    OrderQueryParams,
    PlaceOrderResult,
    CancelOrderResult,
    OrderStats,
    MinimumViableOrder,
    ExchangeOrderResponse,
    InternalOrderState,
    MVORecord,
    MVOManager,
    OrderManager,
)


class TestOrderModels:
    """Test order model classes."""

    def test_order_creation(self):
        """Test creating an Order instance."""
        order = Order(
            id="order_123",
            vault_address="0x1234567890123456789012345678901234567890",
            base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
            status=OrderStatus.PENDING,
            amount=1_000_000_000_000_000_000,
            price=2500_000_000,
            created_at=1700000000000,
            updated_at=1700000000000,
        )

        assert order.id == "order_123"
        assert order.side == OrderSide.BUY
        assert order.type == OrderType.LIMIT
        assert order.status == OrderStatus.PENDING
        assert order.remaining_amount == 1_000_000_000_000_000_000
        assert order.fill_percentage == 0.0
        assert order.is_open is True
        assert order.is_complete is False

    def test_order_fill_calculation(self):
        """Test order fill percentage calculation."""
        order = Order(
            id="order_123",
            vault_address="0x1234567890123456789012345678901234567890",
            base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            side=OrderSide.BUY,
            type=OrderType.MARKET,
            status=OrderStatus.PARTIAL_FILL,
            amount=1000,
            filled_amount=400,
            created_at=1700000000000,
            updated_at=1700000000000,
        )

        assert order.fill_percentage == 40.0
        assert order.remaining_amount == 600
        assert order.is_open is True

    def test_order_completed_states(self):
        """Test order completion state detection."""
        for status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.FAILED]:
            order = Order(
                id="order_123",
                vault_address="0x1234567890123456789012345678901234567890",
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.SELL,
                type=OrderType.MARKET,
                status=status,
                amount=1000,
                created_at=1700000000000,
                updated_at=1700000000000,
            )
            assert order.is_complete is True
            assert order.is_open is False

    def test_create_order_params_validation(self):
        """Test CreateOrderParams validation."""
        params = CreateOrderParams(
            base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
            amount=1000,
            price=2500_000_000,
        )

        assert params.side == OrderSide.BUY
        assert params.type == OrderType.LIMIT
        assert params.amount == 1000
        assert params.price == 2500_000_000

    def test_invalid_address_raises_error(self):
        """Test that invalid addresses raise validation errors."""
        with pytest.raises(ValueError):
            CreateOrderParams(
                base_token="invalid",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1000,
            )


class TestMVOManager:
    """Test MVO (Minimum Viable Order) Manager."""

    def test_place_order(self):
        """Test placing a new order."""
        manager = MVOManager()

        mvo = manager.place_order(MinimumViableOrder(
            symbol="WETH/USDC",
            exchange="zeroquant",
            base_asset="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            quote_asset="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            side="buy",
            time_in_force="gtc",
            reduce_only=False,
            original_price=2450.50,
            original_quantity_base=1.5,
        ))

        assert mvo.id.startswith("mvo_")
        assert mvo.order.symbol == "WETH/USDC"
        assert mvo.order.side == "buy"
        assert mvo.internal_state.new is True
        assert mvo.internal_state.accepted is False

    def test_mark_accepted(self):
        """Test marking order as accepted."""
        manager = MVOManager()

        mvo = manager.place_order(MinimumViableOrder(
            symbol="WETH/USDC",
            side="buy",
            original_quantity_base=1.0,
        ))

        result = manager.mark_accepted(mvo.id)
        assert result is True

        updated = manager.get_order(mvo.id)
        assert updated.internal_state.accepted is True
        assert updated.internal_state.new is False

    def test_update_from_exchange(self):
        """Test updating order from exchange response."""
        manager = MVOManager()

        mvo = manager.place_order(MinimumViableOrder(
            symbol="WETH/USDC",
            side="buy",
            original_quantity_base=1.0,
        ))

        manager.mark_accepted(mvo.id)
        manager.mark_created(mvo.id)

        result = manager.update_from_exchange(mvo.id, ExchangeOrderResponse(
            exchange_order_id="ext_12345",
            status="partially_filled",
            executed_quantity_base=0.5,
            average_price=2448.75,
            fee_paid=0.50,
        ))

        assert result is True

        updated = manager.get_order(mvo.id)
        assert updated.exchange_response.exchange_order_id == "ext_12345"
        assert updated.exchange_response.executed_quantity_base == 0.5
        assert updated.internal_state.partially_filled is True

    def test_mark_filled(self):
        """Test marking order as filled."""
        manager = MVOManager()

        mvo = manager.place_order(MinimumViableOrder(
            symbol="WETH/USDC",
            side="buy",
            original_quantity_base=1.0,
        ))

        manager.mark_filled(mvo.id)

        updated = manager.get_order(mvo.id)
        assert updated.internal_state.filled is True
        assert updated.internal_state.partially_filled is False

    def test_get_all_open_orders(self):
        """Test getting all open orders."""
        manager = MVOManager()

        # Place 3 orders
        mvo1 = manager.place_order(MinimumViableOrder(symbol="A", side="buy"))
        mvo2 = manager.place_order(MinimumViableOrder(symbol="B", side="sell"))
        mvo3 = manager.place_order(MinimumViableOrder(symbol="C", side="buy"))

        # Fill one
        manager.mark_filled(mvo2.id)

        open_orders = manager.get_all_open_orders()
        assert len(open_orders) == 2

        # Cancel another
        manager.mark_cancelled(mvo3.id)

        open_orders = manager.get_all_open_orders()
        assert len(open_orders) == 1
        assert open_orders[0].id == mvo1.id

    def test_get_all_executed_orders(self):
        """Test getting executed orders."""
        manager = MVOManager()

        mvo1 = manager.place_order(MinimumViableOrder(symbol="A", side="buy"))
        mvo2 = manager.place_order(MinimumViableOrder(symbol="B", side="sell"))

        manager.mark_filled(mvo1.id)

        executed = manager.get_all_executed_orders()
        assert len(executed) == 1
        assert executed[0].id == mvo1.id


class TestOrderManager:
    """Test full-featured Order Manager."""

    def test_create_order(self):
        """Test creating an order."""
        manager = OrderManager()

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1_000_000_000_000_000_000,
            )
        )

        assert order.id.startswith("order_")
        assert order.status == OrderStatus.PENDING
        assert order.side == OrderSide.BUY

    def test_create_limit_order_requires_price(self):
        """Test that limit orders require a price."""
        manager = OrderManager()

        with pytest.raises(ValueError, match="Limit orders require a price"):
            manager.create_order(
                "0x1234567890123456789012345678901234567890",
                CreateOrderParams(
                    base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                    side=OrderSide.BUY,
                    type=OrderType.LIMIT,
                    amount=1000,
                    price=None,
                )
            )

    def test_update_order_status(self):
        """Test updating order status."""
        manager = OrderManager()

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1000,
            )
        )

        manager.update_order_status(order.id, OrderStatus.SUBMITTED, tx_hash="0xabc")
        updated = manager.get_order(order.id)

        assert updated.status == OrderStatus.SUBMITTED
        assert updated.tx_hash == "0xabc"
        assert updated.submitted_at is not None

    def test_record_fill(self):
        """Test recording a fill."""
        manager = OrderManager()

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1000,
            )
        )

        manager.update_order_status(order.id, OrderStatus.OPEN)

        fill = manager.record_fill(order.id, {
            "amount": 400,
            "price": 2500_000_000,
            "fees": {"total": 100},
        })

        assert fill is not None
        assert fill.amount == 400
        assert fill.price == 2500_000_000

        updated = manager.get_order(order.id)
        assert updated.filled_amount == 400
        assert updated.status == OrderStatus.PARTIAL_FILL
        assert updated.average_fill_price == 2500_000_000

    def test_record_completing_fill(self):
        """Test recording a fill that completes the order."""
        manager = OrderManager()

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1000,
            )
        )

        manager.update_order_status(order.id, OrderStatus.OPEN)

        # First fill
        manager.record_fill(order.id, {"amount": 400, "price": 2500_000_000, "fees": {"total": 100}})

        # Completing fill
        manager.record_fill(order.id, {"amount": 600, "price": 2510_000_000, "fees": {"total": 150}})

        updated = manager.get_order(order.id)
        assert updated.filled_amount == 1000
        assert updated.status == OrderStatus.FILLED
        assert len(updated.fills) == 2

    def test_cancel_order(self):
        """Test cancelling an order."""
        manager = OrderManager()

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.LIMIT,
                amount=1000,
                price=2500_000_000,
            )
        )

        manager.update_order_status(order.id, OrderStatus.OPEN)

        result = manager.cancel_order(order.id, "User requested")

        assert result.success is True
        assert result.cancelled_at is not None

        updated = manager.get_order(order.id)
        assert updated.status == OrderStatus.CANCELLED

    def test_cancel_completed_order_fails(self):
        """Test that cancelling a completed order fails."""
        manager = OrderManager()

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1000,
            )
        )

        manager.update_order_status(order.id, OrderStatus.OPEN)
        manager.record_fill(order.id, {"amount": 1000, "price": 2500_000_000, "fees": {"total": 100}})

        result = manager.cancel_order(order.id)

        assert result.success is False
        assert "Cannot cancel" in result.error

    def test_get_order_stats(self):
        """Test getting order statistics."""
        manager = OrderManager()
        vault = "0x1234567890123456789012345678901234567890"

        # Create and fill order
        order1 = manager.create_order(vault, CreateOrderParams(
            base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            side=OrderSide.BUY,
            type=OrderType.MARKET,
            amount=1000,
        ))
        manager.update_order_status(order1.id, OrderStatus.OPEN)
        manager.record_fill(order1.id, {"amount": 1000, "price": 2500_000_000, "fees": {"total": 100}})

        # Create and cancel order
        order2 = manager.create_order(vault, CreateOrderParams(
            base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            side=OrderSide.SELL,
            type=OrderType.LIMIT,
            amount=500,
            price=2600_000_000,
        ))
        manager.cancel_order(order2.id)

        stats = manager.get_order_stats(vault)

        assert stats.total_orders == 2
        assert stats.filled_orders == 1
        assert stats.cancelled_orders == 1
        assert stats.total_fees == 100

    def test_event_subscription(self):
        """Test order update event subscription."""
        manager = OrderManager()
        updates = []

        order = manager.create_order(
            "0x1234567890123456789012345678901234567890",
            CreateOrderParams(
                base_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                quote_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=1000,
            )
        )

        # Subscribe after initial creation
        unsubscribe = manager.on_order_update(order.id, lambda o: updates.append(o.status))

        manager.update_order_status(order.id, OrderStatus.SUBMITTED)
        manager.update_order_status(order.id, OrderStatus.OPEN)

        assert len(updates) == 2
        assert updates[0] == OrderStatus.SUBMITTED
        assert updates[1] == OrderStatus.OPEN

        # Unsubscribe
        unsubscribe()

        manager.update_order_status(order.id, OrderStatus.FILLED)
        assert len(updates) == 2  # No new updates after unsubscribe
