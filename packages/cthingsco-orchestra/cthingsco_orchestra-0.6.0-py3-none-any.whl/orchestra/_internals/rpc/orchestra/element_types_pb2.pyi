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

class ElementType(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ListAllElementTypesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAllElementTypesResponse(_message.Message):
    __slots__ = ("element_types",)
    ELEMENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    element_types: _containers.RepeatedCompositeFieldContainer[ElementType]
    def __init__(
        self, element_types: _Optional[_Iterable[_Union[ElementType, _Mapping]]] = ...
    ) -> None: ...

class ElementTypeIdentifier(_message.Message):
    __slots__ = ("element_type_id", "element_id")
    ELEMENT_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    element_type_id: str
    element_id: str
    def __init__(
        self, element_type_id: _Optional[str] = ..., element_id: _Optional[str] = ...
    ) -> None: ...

class GetElementTypeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: ElementTypeIdentifier
    def __init__(self, id: _Optional[_Union[ElementTypeIdentifier, _Mapping]] = ...) -> None: ...

class CreateElementTypeRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetElementTypeByNameRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
