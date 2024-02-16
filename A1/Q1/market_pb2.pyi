from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SellerInfo(_message.Message):
    __slots__ = ("address", "uuid")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    address: str
    uuid: str
    def __init__(self, address: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class SellerResponse(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILED: _ClassVar[SellerResponse.Status]
        SUCCESS: _ClassVar[SellerResponse.Status]
    FAILED: SellerResponse.Status
    SUCCESS: SellerResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: SellerResponse.Status
    def __init__(self, status: _Optional[_Union[SellerResponse.Status, str]] = ...) -> None: ...

class ItemDetails(_message.Message):
    __slots__ = ("item_id", "product_name", "category", "quantity", "description", "seller_address", "price_per_unit", "seller_uuid", "rating")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_UNIT_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    product_name: str
    category: str
    quantity: int
    description: str
    seller_address: str
    price_per_unit: float
    seller_uuid: str
    rating: float
    def __init__(self, item_id: _Optional[str] = ..., product_name: _Optional[str] = ..., category: _Optional[str] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., price_per_unit: _Optional[float] = ..., seller_uuid: _Optional[str] = ..., rating: _Optional[float] = ...) -> None: ...

class ItemResponse(_message.Message):
    __slots__ = ("status", "item_id")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILED: _ClassVar[ItemResponse.Status]
        SUCCESS: _ClassVar[ItemResponse.Status]
    FAILED: ItemResponse.Status
    SUCCESS: ItemResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    status: ItemResponse.Status
    item_id: str
    def __init__(self, status: _Optional[_Union[ItemResponse.Status, str]] = ..., item_id: _Optional[str] = ...) -> None: ...

class UpdateItemRequest(_message.Message):
    __slots__ = ("item_id", "new_price", "new_quantity", "seller_address", "seller_uuid")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PRICE_FIELD_NUMBER: _ClassVar[int]
    NEW_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    new_price: float
    new_quantity: int
    seller_address: str
    seller_uuid: str
    def __init__(self, item_id: _Optional[str] = ..., new_price: _Optional[float] = ..., new_quantity: _Optional[int] = ..., seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class UpdateItemResponse(_message.Message):
    __slots__ = ("status", "item_id", "new_price", "new_quantity", "seller_address", "seller_uuid")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILED: _ClassVar[UpdateItemResponse.Status]
        SUCCESS: _ClassVar[UpdateItemResponse.Status]
    FAILED: UpdateItemResponse.Status
    SUCCESS: UpdateItemResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PRICE_FIELD_NUMBER: _ClassVar[int]
    NEW_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    status: UpdateItemResponse.Status
    item_id: str
    new_price: float
    new_quantity: int
    seller_address: str
    seller_uuid: str
    def __init__(self, status: _Optional[_Union[UpdateItemResponse.Status, str]] = ..., item_id: _Optional[str] = ..., new_price: _Optional[float] = ..., new_quantity: _Optional[int] = ..., seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class DeleteItemRequest(_message.Message):
    __slots__ = ("item_id", "seller_address", "seller_uuid")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    seller_address: str
    seller_uuid: str
    def __init__(self, item_id: _Optional[str] = ..., seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class DeleteItemResponse(_message.Message):
    __slots__ = ("status", "item_id", "seller_address", "seller_uuid")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILED: _ClassVar[DeleteItemResponse.Status]
        SUCCESS: _ClassVar[DeleteItemResponse.Status]
    FAILED: DeleteItemResponse.Status
    SUCCESS: DeleteItemResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    status: DeleteItemResponse.Status
    item_id: str
    seller_address: str
    seller_uuid: str
    def __init__(self, status: _Optional[_Union[DeleteItemResponse.Status, str]] = ..., item_id: _Optional[str] = ..., seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class DisplayItemsRequest(_message.Message):
    __slots__ = ("seller_address", "seller_uuid")
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    seller_address: str
    seller_uuid: str
    def __init__(self, seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class DisplayItemsResponse(_message.Message):
    __slots__ = ("status", "items")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILED: _ClassVar[DisplayItemsResponse.Status]
        SUCCESS: _ClassVar[DisplayItemsResponse.Status]
    FAILED: DisplayItemsResponse.Status
    SUCCESS: DisplayItemsResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    status: DisplayItemsResponse.Status
    items: _containers.RepeatedCompositeFieldContainer[ItemDetails]
    def __init__(self, status: _Optional[_Union[DisplayItemsResponse.Status, str]] = ..., items: _Optional[_Iterable[_Union[ItemDetails, _Mapping]]] = ...) -> None: ...

class SearchItemRequest(_message.Message):
    __slots__ = ("item_name", "item_category")
    ITEM_NAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    item_name: str
    item_category: str
    def __init__(self, item_name: _Optional[str] = ..., item_category: _Optional[str] = ...) -> None: ...

class SearchItemResponse(_message.Message):
    __slots__ = ("status", "items")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[SearchItemResponse.Status]
        FAILED: _ClassVar[SearchItemResponse.Status]
    SUCCESS: SearchItemResponse.Status
    FAILED: SearchItemResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    status: SearchItemResponse.Status
    items: _containers.RepeatedCompositeFieldContainer[ItemDetails]
    def __init__(self, status: _Optional[_Union[SearchItemResponse.Status, str]] = ..., items: _Optional[_Iterable[_Union[ItemDetails, _Mapping]]] = ...) -> None: ...

class BuyRequest(_message.Message):
    __slots__ = ("item_id", "quantity", "buyer_address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    quantity: int
    buyer_address: str
    def __init__(self, item_id: _Optional[str] = ..., quantity: _Optional[int] = ..., buyer_address: _Optional[str] = ...) -> None: ...

class BuyResponse(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[BuyResponse.Status]
        FAILED: _ClassVar[BuyResponse.Status]
    SUCCESS: BuyResponse.Status
    FAILED: BuyResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: BuyResponse.Status
    def __init__(self, status: _Optional[_Union[BuyResponse.Status, str]] = ...) -> None: ...

class AddToWishListRequest(_message.Message):
    __slots__ = ("item_id", "buyer_address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    buyer_address: str
    def __init__(self, item_id: _Optional[str] = ..., buyer_address: _Optional[str] = ...) -> None: ...

class AddToWishListResponse(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[AddToWishListResponse.Status]
        FAILED: _ClassVar[AddToWishListResponse.Status]
    SUCCESS: AddToWishListResponse.Status
    FAILED: AddToWishListResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: AddToWishListResponse.Status
    def __init__(self, status: _Optional[_Union[AddToWishListResponse.Status, str]] = ...) -> None: ...

class RateItemRequest(_message.Message):
    __slots__ = ("item_id", "buyer_address", "rating")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    buyer_address: str
    rating: int
    def __init__(self, item_id: _Optional[str] = ..., buyer_address: _Optional[str] = ..., rating: _Optional[int] = ...) -> None: ...

class RateItemResponse(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[RateItemResponse.Status]
        FAILED: _ClassVar[RateItemResponse.Status]
    SUCCESS: RateItemResponse.Status
    FAILED: RateItemResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: RateItemResponse.Status
    def __init__(self, status: _Optional[_Union[RateItemResponse.Status, str]] = ...) -> None: ...
