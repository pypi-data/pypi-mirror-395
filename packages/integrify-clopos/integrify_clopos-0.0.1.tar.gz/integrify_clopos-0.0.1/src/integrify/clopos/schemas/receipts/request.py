from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from integrify.api import PayloadBaseModel
from integrify.clopos.helpers import IsoDateTime
from integrify.clopos.schemas.common.request import ByIDRequest, PaginatedDataRequest
from integrify.clopos.schemas.enums import DiscountType, OrderStatus
from integrify.clopos.schemas.receipts.object import ReceiptProductIn
from integrify.utils import UnsetField, UnsetOrNoneField


class PaymentMethodIn(BaseModel):
    id: int
    """The unique identifier for the payment method"""

    name: str
    """The name of the payment method (e.g., "Cash", "Card")"""

    amount: Decimal
    """The amount of the payment method"""


class GetReceiptsRequest(PaginatedDataRequest):
    sort_by: UnsetField[str]
    sort_order: UnsetField[int]
    date_from: UnsetField[IsoDateTime]
    date_to: UnsetField[IsoDateTime]


class CreateReceiptRequest(PayloadBaseModel):
    model_config = {'extra': 'allow'}

    cid: str
    payment_methods: list[PaymentMethodIn]
    user_id: int
    by_cash: UnsetField[Decimal]
    by_card: UnsetField[Decimal]
    customer_discount_type: UnsetField[DiscountType]
    discount_rate: UnsetField[Decimal]
    discount_type: UnsetField[DiscountType]
    discount_value: UnsetOrNoneField[Decimal]
    delivery_fee: UnsetField[Decimal]
    gift_total: UnsetField[Decimal]
    guests: UnsetField[int]
    original_subtotal: UnsetField[Decimal]
    printed: UnsetField[bool]
    receipt_products: UnsetOrNoneField[list[ReceiptProductIn]]
    remaining: UnsetField[Decimal]
    rps_discount: UnsetField[Decimal]
    sale_type_id: UnsetField[int]
    service_charge: UnsetField[Decimal]
    service_charge_value: UnsetField[Decimal]
    status: UnsetField[int]
    subtotal: UnsetField[Decimal]
    terminal_id: UnsetField[int]
    total: UnsetField[Decimal]
    total_tax: UnsetField[Decimal]
    created_at: UnsetField[int]
    closed_at: UnsetOrNoneField[int]
    address: UnsetField[str]
    courier_id: UnsetOrNoneField[int]
    meta: UnsetField[dict]


class UpdateClosedReceiptRequest(ByIDRequest):
    order_status: UnsetField[OrderStatus]
    order_number: UnsetField[str]
    fiscal_id: UnsetField[str]
    lock: UnsetField[bool]


class UpdateReceiptMetaData(BaseModel):
    name: str
    bonus: int
    cashback: float
    balance: int
    desc: UnsetField[str]
    code: UnsetField[str]
    phone: str
    group_name: str
    group_id: int


class UpdateReceiptRequest(ByIDRequest):
    id: int
    cid: str
    delivery_fee: int
    description: str = Field(max_length=500)
    order_number: str
    order_status: OrderStatus
    guests: int
    discount_rate: int
    discount_type: DiscountType
    discount_value: Optional[Decimal] = None
    customer_id: int
    closed_at: IsoDateTime = ''
    meta_customer: UpdateReceiptMetaData

    @field_serializer('meta_customer')
    def _meta_customer(self, value: dict):
        """"""
        return {'meta': {'customer': value}}


class CloseReceiptRequest(ByIDRequest):
    id: int
    cid: str
    payment_methods: list[PaymentMethodIn]
    closed_at: IsoDateTime = ''
