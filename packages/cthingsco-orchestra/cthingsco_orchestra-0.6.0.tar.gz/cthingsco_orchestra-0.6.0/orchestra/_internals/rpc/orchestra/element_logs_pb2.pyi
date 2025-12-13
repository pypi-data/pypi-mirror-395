from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import pagination_pb2 as _pagination_pb2
import sort_pb2 as _sort_pb2
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

class LogTag(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SingleElementLog(_message.Message):
    __slots__ = ("ts", "log", "tags")
    TS_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ts: _timestamp_pb2.Timestamp
    log: str
    tags: _containers.RepeatedCompositeFieldContainer[LogTag]
    def __init__(
        self,
        ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        log: _Optional[str] = ...,
        tags: _Optional[_Iterable[_Union[LogTag, _Mapping]]] = ...,
    ) -> None: ...

class PushManyElementLogsRequest(_message.Message):
    __slots__ = ("element_id", "logs")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    logs: _containers.RepeatedCompositeFieldContainer[SingleElementLog]
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        logs: _Optional[_Iterable[_Union[SingleElementLog, _Mapping]]] = ...,
    ) -> None: ...

class GetManyElementLogsRequest(_message.Message):
    __slots__ = ("element_id", "tags", "ts_from", "ts_to", "pagination", "sort")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TS_FROM_FIELD_NUMBER: _ClassVar[int]
    TS_TO_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    tags: _containers.RepeatedCompositeFieldContainer[LogTag]
    ts_from: _timestamp_pb2.Timestamp
    ts_to: _timestamp_pb2.Timestamp
    pagination: _pagination_pb2.PaginationRequest
    sort: _sort_pb2.SortType
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        tags: _Optional[_Iterable[_Union[LogTag, _Mapping]]] = ...,
        ts_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ts_to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationRequest, _Mapping]] = ...,
        sort: _Optional[_Union[_sort_pb2.SortType, str]] = ...,
    ) -> None: ...

class GetManyElementLogsResponse(_message.Message):
    __slots__ = ("element_id", "logs", "pagination")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    logs: _containers.RepeatedCompositeFieldContainer[SingleElementLog]
    pagination: _pagination_pb2.PaginationResponse
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        logs: _Optional[_Iterable[_Union[SingleElementLog, _Mapping]]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationResponse, _Mapping]] = ...,
    ) -> None: ...
