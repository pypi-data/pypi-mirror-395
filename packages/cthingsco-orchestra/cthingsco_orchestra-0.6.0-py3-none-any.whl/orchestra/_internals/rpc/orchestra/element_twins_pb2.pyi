from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class ResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OK: _ClassVar[ResultCode]
    OK_NO_CHANGE: _ClassVar[ResultCode]
    FAILURE: _ClassVar[ResultCode]

OK: ResultCode
OK_NO_CHANGE: ResultCode
FAILURE: ResultCode

class ElementTwin(_message.Message):
    __slots__ = ("id", "element_type_id", "state")

    class TwinState(_message.Message):
        __slots__ = ("current", "desired")

        class State(_message.Message):
            __slots__ = ("version", "properties")
            VERSION_FIELD_NUMBER: _ClassVar[int]
            PROPERTIES_FIELD_NUMBER: _ClassVar[int]
            version: int
            properties: _struct_pb2.Struct
            def __init__(
                self,
                version: _Optional[int] = ...,
                properties: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
            ) -> None: ...
        CURRENT_FIELD_NUMBER: _ClassVar[int]
        DESIRED_FIELD_NUMBER: _ClassVar[int]
        current: ElementTwin.TwinState.State
        desired: ElementTwin.TwinState.State
        def __init__(
            self,
            current: _Optional[_Union[ElementTwin.TwinState.State, _Mapping]] = ...,
            desired: _Optional[_Union[ElementTwin.TwinState.State, _Mapping]] = ...,
        ) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    element_type_id: str
    state: ElementTwin.TwinState
    def __init__(
        self,
        id: _Optional[str] = ...,
        element_type_id: _Optional[str] = ...,
        state: _Optional[_Union[ElementTwin.TwinState, _Mapping]] = ...,
    ) -> None: ...

class Observable(_message.Message):
    __slots__ = ("key", "value", "ts")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: _struct_pb2.Value
    ts: _timestamp_pb2.Timestamp
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ElementTwinObservables(_message.Message):
    __slots__ = ("id", "observables")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBSERVABLES_FIELD_NUMBER: _ClassVar[int]
    id: str
    observables: _containers.RepeatedCompositeFieldContainer[Observable]
    def __init__(
        self,
        id: _Optional[str] = ...,
        observables: _Optional[_Iterable[_Union[Observable, _Mapping]]] = ...,
    ) -> None: ...

class TwinIdentifier(_message.Message):
    __slots__ = ("twin_id", "element_id")
    TWIN_ID_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    twin_id: str
    element_id: str
    def __init__(self, twin_id: _Optional[str] = ..., element_id: _Optional[str] = ...) -> None: ...

class CreateElementTwinRequest(_message.Message):
    __slots__ = ("element_id",)
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    def __init__(self, element_id: _Optional[str] = ...) -> None: ...

class GetElementTwinRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    def __init__(self, id: _Optional[_Union[TwinIdentifier, _Mapping]] = ...) -> None: ...

class GetElementTwinObservablesRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    def __init__(self, id: _Optional[_Union[TwinIdentifier, _Mapping]] = ...) -> None: ...

class SetElementTwinPropertiesRequest(_message.Message):
    __slots__ = ("id", "properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    properties: _struct_pb2.Struct
    def __init__(
        self,
        id: _Optional[_Union[TwinIdentifier, _Mapping]] = ...,
        properties: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class SetElementTwinObservablesRequest(_message.Message):
    __slots__ = ("id", "observables", "event_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBSERVABLES_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    observables: _struct_pb2.Struct
    event_type: str
    def __init__(
        self,
        id: _Optional[_Union[TwinIdentifier, _Mapping]] = ...,
        observables: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        event_type: _Optional[str] = ...,
    ) -> None: ...

class SetElementTwinPropertiesResponse(_message.Message):
    __slots__ = ("id", "old_version", "new_version", "result", "twin")
    ID_FIELD_NUMBER: _ClassVar[int]
    OLD_VERSION_FIELD_NUMBER: _ClassVar[int]
    NEW_VERSION_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TWIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    old_version: int
    new_version: int
    result: ResultCode
    twin: ElementTwin
    def __init__(
        self,
        id: _Optional[str] = ...,
        old_version: _Optional[int] = ...,
        new_version: _Optional[int] = ...,
        result: _Optional[_Union[ResultCode, str]] = ...,
        twin: _Optional[_Union[ElementTwin, _Mapping]] = ...,
    ) -> None: ...

class SetElementTwinObservablesResponse(_message.Message):
    __slots__ = ("id", "observables")
    ID_FIELD_NUMBER: _ClassVar[int]
    OBSERVABLES_FIELD_NUMBER: _ClassVar[int]
    id: str
    observables: _containers.RepeatedCompositeFieldContainer[Observable]
    def __init__(
        self,
        id: _Optional[str] = ...,
        observables: _Optional[_Iterable[_Union[Observable, _Mapping]]] = ...,
    ) -> None: ...

class RequestSetElementTwinPropertiesRequest(_message.Message):
    __slots__ = ("id", "properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    properties: _struct_pb2.Struct
    def __init__(
        self,
        id: _Optional[_Union[TwinIdentifier, _Mapping]] = ...,
        properties: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class RequestSetElementTwinPropertiesResponse(_message.Message):
    __slots__ = ("id", "old_desired_version", "new_desired_version", "result", "twin")
    ID_FIELD_NUMBER: _ClassVar[int]
    OLD_DESIRED_VERSION_FIELD_NUMBER: _ClassVar[int]
    NEW_DESIRED_VERSION_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TWIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    old_desired_version: int
    new_desired_version: int
    result: ResultCode
    twin: ElementTwin
    def __init__(
        self,
        id: _Optional[str] = ...,
        old_desired_version: _Optional[int] = ...,
        new_desired_version: _Optional[int] = ...,
        result: _Optional[_Union[ResultCode, str]] = ...,
        twin: _Optional[_Union[ElementTwin, _Mapping]] = ...,
    ) -> None: ...

class ValidateTwinStateChangeRequest(_message.Message):
    __slots__ = ("id", "version")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    version: int
    def __init__(
        self, id: _Optional[_Union[TwinIdentifier, _Mapping]] = ..., version: _Optional[int] = ...
    ) -> None: ...

class ValidateTwinStateChangeResponse(_message.Message):
    __slots__ = ("id", "old_version", "new_version", "result", "twin")
    ID_FIELD_NUMBER: _ClassVar[int]
    OLD_VERSION_FIELD_NUMBER: _ClassVar[int]
    NEW_VERSION_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TWIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    old_version: int
    new_version: int
    result: ResultCode
    twin: ElementTwin
    def __init__(
        self,
        id: _Optional[str] = ...,
        old_version: _Optional[int] = ...,
        new_version: _Optional[int] = ...,
        result: _Optional[_Union[ResultCode, str]] = ...,
        twin: _Optional[_Union[ElementTwin, _Mapping]] = ...,
    ) -> None: ...

class WatchElementTwinRequest(_message.Message):
    __slots__ = ("id", "suppress_current_changes")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_CURRENT_CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: TwinIdentifier
    suppress_current_changes: bool
    def __init__(
        self,
        id: _Optional[_Union[TwinIdentifier, _Mapping]] = ...,
        suppress_current_changes: bool = ...,
    ) -> None: ...

class WatchElementTwinResponse(_message.Message):
    __slots__ = ("id", "old_version", "new_version", "twin")
    ID_FIELD_NUMBER: _ClassVar[int]
    OLD_VERSION_FIELD_NUMBER: _ClassVar[int]
    NEW_VERSION_FIELD_NUMBER: _ClassVar[int]
    TWIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    old_version: int
    new_version: int
    twin: ElementTwin
    def __init__(
        self,
        id: _Optional[str] = ...,
        old_version: _Optional[int] = ...,
        new_version: _Optional[int] = ...,
        twin: _Optional[_Union[ElementTwin, _Mapping]] = ...,
    ) -> None: ...
