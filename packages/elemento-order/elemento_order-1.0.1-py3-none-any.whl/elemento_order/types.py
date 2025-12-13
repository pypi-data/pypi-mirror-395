"""Basic data types."""

from datetime import datetime, date
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
    """Default status fixture for new and canceled orders."""
    new = OrderStatusId('new')
    canceled = OrderStatusId('canceled')

class InternalOrderStatus(Enum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"

class OrderStatus(Struct):
    """Order status as in OMS."""
    int_status: InternalOrderStatus
    id: OrderStatusId
    label: str
    can_cancel_order: bool

class CancelReason(Struct):
    """Order cancel reason as in OMS."""
    id: CancelReasonId
    label: str

class OrderItem(Struct, omit_defaults=True):
    id: str
    quantity: Annotated[int, Meta(ge=1)]
    price: int
    label: str = None
    shock_price: bool = False

class OrderAttributes(Struct):
    """Stored customer attributes for order create."""
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
    available_from: date | None     #: when order should be available for pickup
    available_to: date | None       #: date until the order will be available for pickup
    status: OrderStatusId
    total: int
    paid: bool                      #: order is paid
    store_id: StoreId
    source_id: str                  #: order create frontend source
    cancel_reason_id: str | None    #: is present only for cancelled orders
    items: list[OrderItem]
    attrs: OrderAttributes          #: additional profile data
    oms_id: OMSOrderId              #: order text id for OMS

class OrderCreate(Struct):
    """Order object for `customer.order.create` method."""
    customer_id: CustomerId
    total: int
    store_id: StoreId
    source_id: str                  #: order create frontend source
    items: list[OrderItem]
    attrs: OrderAttributes
