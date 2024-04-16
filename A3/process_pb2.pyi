from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Point(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class MapPartitionRequest(_message.Message):
    __slots__ = ("start", "end", "numMappers", "numReducers", "centroids")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    NUMMAPPERS_FIELD_NUMBER: _ClassVar[int]
    NUMREDUCERS_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    start: int
    end: int
    numMappers: int
    numReducers: int
    centroids: _containers.RepeatedCompositeFieldContainer[Point]
    def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ..., numMappers: _Optional[int] = ..., numReducers: _Optional[int] = ..., centroids: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...) -> None: ...

class MapPartitionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class ReduceRequest(_message.Message):
    __slots__ = ("numMappers", "numReducers")
    NUMMAPPERS_FIELD_NUMBER: _ClassVar[int]
    NUMREDUCERS_FIELD_NUMBER: _ClassVar[int]
    numMappers: int
    numReducers: int
    def __init__(self, numMappers: _Optional[int] = ..., numReducers: _Optional[int] = ...) -> None: ...

class ReduceResponse(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: str
    data: str
    def __init__(self, status: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class GetInputRequest(_message.Message):
    __slots__ = ("reducer_id",)
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    def __init__(self, reducer_id: _Optional[int] = ...) -> None: ...

class GetInputResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...
