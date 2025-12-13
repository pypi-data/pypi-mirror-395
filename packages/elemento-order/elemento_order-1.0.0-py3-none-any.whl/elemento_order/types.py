"""Basic data types."""

from datetime import datetime
from enum import Enum
from typing import Annotated, NewType

from msgspec import Struct, Meta

__all__ = [
    "CustomerId", "OrderId", "StoreId", "OrderStatus", "OrderStatusId", "CancelReasonId", "OrderStatusDefaults",
    "CancelReason", "OrderItem", "Order", "InternalOrderStatus", "OrderCreate", "OrderAttributes",
    "OMSOrderId",
    'DATE_MAXVALUE'
]

DATE_MAXVALUE = datetime(3000, 1, 1)

CustomerId = NewType("CustomerId", int)
OrderId = NewType("OrderId", int)
OMSOrderId = NewType("OMSOrderId", str)
StoreId = NewType("StoreId", str)
OrderStatusId = NewType("OrderStatusId", str)
CancelReasonId = NewType("CancelReasonId", str)

class OrderStatusDefaults(Enum):
    new = OrderStatusId('new')
    canceled = OrderStatusId('canceled')

class InternalOrderStatus(Enum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"

class OrderStatus(Struct):
    int_status: InternalOrderStatus
    id: OrderStatusId
    label: str
    can_cancel_order: bool

class CancelReason(Struct):
    id: CancelReasonId
    label: str

class OrderItem(Struct, omit_defaults=True):
    id: str
    quantity: Annotated[int, Meta(ge=1)]
    price: int
    label: str = None
    shock_price: bool = False

class OrderAttributes(Struct):
    phone: str
    email: str
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    call_requested: bool = False
    comment: str = None

class Order(Struct):
    created: datetime
    updated: datetime
    id: OrderId
    customer_id: CustomerId
    int_status: InternalOrderStatus
    status: OrderStatusId
    total: int
    paid: bool
    store_id: StoreId
    source_id: str
    cancel_reason_id: str | None
    items: list[OrderItem]
    attrs: OrderAttributes
    oms_id: OMSOrderId

class OrderCreate(Struct):
    customer_id: CustomerId
    total: int
    store_id: StoreId
    source_id: str
    items: list[OrderItem]
    attrs: OrderAttributes
