from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointRange(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: int
    end: int
    def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class MapPartitionRequest(_message.Message):
    __slots__ = ("points", "numMappers")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    NUMMAPPERS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[PointRange]
    numMappers: int
    def __init__(self, points: _Optional[_Iterable[_Union[PointRange, _Mapping]]] = ..., numMappers: _Optional[int] = ...) -> None: ...

class MapPartitionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InvokeReducerRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InvokeReducerResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetInputDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetInputDataResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
