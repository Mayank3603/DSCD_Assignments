from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ELECTRONICS: _ClassVar[Category]
    FASHION: _ClassVar[Category]
    OTHERS: _ClassVar[Category]
    ANY: _ClassVar[Category]
ELECTRONICS: Category
FASHION: Category
OTHERS: Category
ANY: Category

class SellerInfo(_message.Message):
    __slots__ = ("address", "uuid")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    address: str
    uuid: str
    def __init__(self, address: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("status",)
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FAILED: _ClassVar[Response.Status]
        SUCCESS: _ClassVar[Response.Status]
    FAILED: Response.Status
    SUCCESS: Response.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Response.Status
    def __init__(self, status: _Optional[_Union[Response.Status, str]] = ...) -> None: ...

class ItemDetails(_message.Message):
    __slots__ = ("product_name", "category", "quantity", "description", "seller_address", "price_per_unit", "seller_uuid", "rating")
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_UNIT_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    product_name: str
    category: Category
    quantity: int
    description: str
    seller_address: str
    price_per_unit: float
    seller_uuid: str
    rating: str
    def __init__(self, product_name: _Optional[str] = ..., category: _Optional[_Union[Category, str]] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., price_per_unit: _Optional[float] = ..., seller_uuid: _Optional[str] = ..., rating: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("product_name", "category_name", "quantity", "description", "seller_address", "price_per_unit", "seller_uuid", "rating")
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_UNIT_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    product_name: str
    category_name: str
    quantity: int
    description: str
    seller_address: str
    price_per_unit: float
    seller_uuid: str
    rating: str
    def __init__(self, product_name: _Optional[str] = ..., category_name: _Optional[str] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., price_per_unit: _Optional[float] = ..., seller_uuid: _Optional[str] = ..., rating: _Optional[str] = ...) -> None: ...
