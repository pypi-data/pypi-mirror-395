from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Element(_message.Message):
    __slots__ = ("id", "name", "element_type_id", "twin_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    TWIN_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    element_type_id: str
    twin_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        element_type_id: _Optional[str] = ...,
        twin_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ListAllElementsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAllElementsResponse(_message.Message):
    __slots__ = ("elements",)
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[Element]
    def __init__(self, elements: _Optional[_Iterable[_Union[Element, _Mapping]]] = ...) -> None: ...

class GetElementRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreateElementRequest(_message.Message):
    __slots__ = ("name", "element_type_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    element_type_id: str
    def __init__(
        self, name: _Optional[str] = ..., element_type_id: _Optional[str] = ...
    ) -> None: ...

class DeleteElementRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class WatchElementRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class WatchElementResponse(_message.Message):
    __slots__ = ("id", "twin_id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TWIN_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    twin_id: str
    type: str
    def __init__(
        self, id: _Optional[str] = ..., twin_id: _Optional[str] = ..., type: _Optional[str] = ...
    ) -> None: ...
