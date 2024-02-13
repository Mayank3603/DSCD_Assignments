from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest1(_message.Message):
    __slots__ = ("item_name", "item_category")
    class ItemCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ELECTRONICS: _ClassVar[SearchRequest1.ItemCategory]
        FASHION: _ClassVar[SearchRequest1.ItemCategory]
        OTHERS: _ClassVar[SearchRequest1.ItemCategory]
        ANY: _ClassVar[SearchRequest1.ItemCategory]
    ELECTRONICS: SearchRequest1.ItemCategory
    FASHION: SearchRequest1.ItemCategory
    OTHERS: SearchRequest1.ItemCategory
    ANY: SearchRequest1.ItemCategory
    ITEM_NAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    item_name: str
    item_category: SearchRequest1.ItemCategory
    def __init__(self, item_name: _Optional[str] = ..., item_category: _Optional[_Union[SearchRequest1.ItemCategory, str]] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ("price", "product_name", "category", "description", "quantity", "rating")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    price: float
    product_name: str
    category: str
    description: str
    quantity: int
    rating: float
    def __init__(self, price: _Optional[float] = ..., product_name: _Optional[str] = ..., category: _Optional[str] = ..., description: _Optional[str] = ..., quantity: _Optional[int] = ..., rating: _Optional[float] = ...) -> None: ...

class SearchResponse1(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class BuyRequest1(_message.Message):
    __slots__ = ("item_id", "quantity", "buyer_address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    quantity: int
    buyer_address: str
    def __init__(self, item_id: _Optional[str] = ..., quantity: _Optional[int] = ..., buyer_address: _Optional[str] = ...) -> None: ...

class BuyResponse1(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[BuyResponse1.Status]
        FAILED: _ClassVar[BuyResponse1.Status]
    SUCCESS: BuyResponse1.Status
    FAILED: BuyResponse1.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: BuyResponse1.Status
    def __init__(self, status: _Optional[_Union[BuyResponse1.Status, str]] = ...) -> None: ...

class AddToWishListRequest1(_message.Message):
    __slots__ = ("item_id", "buyer_address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    buyer_address: str
    def __init__(self, item_id: _Optional[str] = ..., buyer_address: _Optional[str] = ...) -> None: ...

class AddToWishListResponse1(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[AddToWishListResponse1.Status]
        FAILED: _ClassVar[AddToWishListResponse1.Status]
    SUCCESS: AddToWishListResponse1.Status
    FAILED: AddToWishListResponse1.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: AddToWishListResponse1.Status
    def __init__(self, status: _Optional[_Union[AddToWishListResponse1.Status, str]] = ...) -> None: ...

class RateItemRequest1(_message.Message):
    __slots__ = ("item_id", "buyer_address", "rating")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    buyer_address: str
    rating: int
    def __init__(self, item_id: _Optional[str] = ..., buyer_address: _Optional[str] = ..., rating: _Optional[int] = ...) -> None: ...

class RateItemResponse1(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[RateItemResponse1.Status]
        FAILED: _ClassVar[RateItemResponse1.Status]
    SUCCESS: RateItemResponse1.Status
    FAILED: RateItemResponse1.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: RateItemResponse1.Status
    def __init__(self, status: _Optional[_Union[RateItemResponse1.Status, str]] = ...) -> None: ...
