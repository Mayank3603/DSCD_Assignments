from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Items(_message.Message):
    __slots__ = ("item_id", "product_name", "category", "quantity", "description", "seller_address", "price_per_unit", "rating")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_UNIT_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    product_name: str
    category: str
    quantity: int
    description: str
    seller_address: str
    price_per_unit: float
    rating: float
    def __init__(self, item_id: _Optional[str] = ..., product_name: _Optional[str] = ..., category: _Optional[str] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., price_per_unit: _Optional[float] = ..., rating: _Optional[float] = ...) -> None: ...

class ItemsResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
