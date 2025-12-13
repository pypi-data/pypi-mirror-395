from msgspec import convert

from kaiju_tools.http import RPCClientService

from app.types import *


class ElementoOrderClient(RPCClientService):
    """Auto-generated ElementoOrder RPC client."""
    
    async def cancel_reasons_get_cancel_reason(self, cancel_reason_id: CancelReasonId, _max_timeout: int = None) -> CancelReason | None:
        """Call cancel_reasons.get."""
        reason = await self.call(
            method='cancel_reasons.get',
            params=dict(cancel_reason_id=cancel_reason_id),
            max_timeout=_max_timeout,
        )
        if not reason:
            return None
        return CancelReason(**reason)
    
    async def cancel_reasons_list_cancel_reasons(self, _max_timeout: int = None) -> list[CancelReason]:
        """Call cancel_reasons.list."""
        reasons = await self.call(
            method='cancel_reasons.list',
            max_timeout=_max_timeout,
        )
        return [CancelReason(**reason) for reason in reasons]
    
    async def order_status_get_order_status(self, status_id: OrderStatusId, _max_timeout: int = None) -> OrderStatus | None:
        """Call order_status.get."""
        status = await self.call(
            method='order_status.get',
            params=dict(status_id=status_id),
            max_timeout=_max_timeout
        )
        if not status:
            return None
        return OrderStatus(**status)
    
    async def order_status_list_order_status(self, _max_timeout: int = None) -> list[OrderStatus]:
        """Call order_status.list."""
        status_list = await self.call(
            method='order_status.list',
            max_timeout=_max_timeout
        )
        return [OrderStatus(**status) for status in status_list]

    async def orders_oms_sync(self, order_id: OMSOrderId, status_id: OrderStatusId = None, paid: bool = None, _max_timeout: int = None, _nowait: bool = False) -> bool:
        """Synchronise order status from OMS.

        It synchronises order status, order payment status. Unrecognised status values are ignored.
        """
        return await self.call(
            method='orders.oms.sync',
            params=dict(order_id=order_id, status_id=status_id, paid=paid),
            max_timeout=_max_timeout,
            nowait=_nowait
        )
    
    async def customer_order_get_order(self, customer_id: CustomerId, order_id: OrderId, _max_timeout: int = None) -> Order | None:
        """Get a particular order for a particular customer."""
        order = await self.call(
            method='customer.order.get',
            params=dict(customer_id=customer_id, order_id=order_id),
            max_timeout=_max_timeout,
        )
        if not order:
            return None
        return convert(order, type=Order)
    
    async def customer_order_list_orders(self, customer_id: CustomerId, offset: int = 0, limit: int = 100, _max_timeout: int = None) -> list[Order]:
        """List all customer's orders starting from the newest."""
        orders = await self.call(
            method='customer.order.list',
            params=dict(customer_id=customer_id, offset=offset, limit=limit),
            max_timeout=_max_timeout,
        )
        return [convert(order, type=Order) for order in orders]
    
    async def customer_order_create_order(self, order: OrderCreate, _max_timeout: int = None) -> Order:
        """Create a new order.

        This method will also perform checks whether this order is possible:

        - All the required fields are filled
        - there are enough items
        - the order total is greater than or equal to `order_min_total` limit
        - the store is permitted for online ordering
        """
        order = await self.call(
            method='customer.order.create',
            params=dict(order=order),
            max_timeout=_max_timeout,
        )
        return convert(order, type=Order)
    
    async def customer_order_cancel_order(self, customer_id: CustomerId, order_id: OrderId, cancel_reason_id: CancelReasonId = None, _max_timeout: int = None) -> None:
        """Cancel an order and set the cancellation reason.

        :param customer_id:
        :param order_id:
        :param cancel_reason_id: call `cancel_reasons.list` to get a list of valid reasons
        """
        await self.call(
            method='customer.order.cancel',
            params=dict(customer_id=customer_id, order_id=order_id, cancel_reason_id=cancel_reason_id),
            max_timeout=_max_timeout,
        )
    
    async def maintenance_service_organize_table_partitions(self, _max_timeout: int = None, _nowait: bool = False) -> None:
        """Call MaintenanceService.organize_tables."""
        await self.call(
            method='MaintenanceService.organize_tables',
            max_timeout=_max_timeout,
            nowait=_nowait
        )
