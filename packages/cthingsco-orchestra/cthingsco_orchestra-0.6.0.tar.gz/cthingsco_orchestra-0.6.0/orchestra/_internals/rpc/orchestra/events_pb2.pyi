from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class PushEventRequest(_message.Message):
    __slots__ = ("event_tag", "data")
    EVENT_TAG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    event_tag: str
    data: _struct_pb2.Struct
    def __init__(
        self,
        event_tag: _Optional[str] = ...,
        data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class WatchEventsRequest(_message.Message):
    __slots__ = ("consumer_name",)
    CONSUMER_NAME_FIELD_NUMBER: _ClassVar[int]
    consumer_name: str
    def __init__(self, consumer_name: _Optional[str] = ...) -> None: ...

class DeclareSubscriberRequest(_message.Message):
    __slots__ = ("consumer_name", "event_tags")
    CONSUMER_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    consumer_name: str
    event_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, consumer_name: _Optional[str] = ..., event_tags: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class DeclareSubscriberResponse(_message.Message):
    __slots__ = ("consumer_name", "event_tags")
    CONSUMER_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    consumer_name: str
    event_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, consumer_name: _Optional[str] = ..., event_tags: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class EventResponse(_message.Message):
    __slots__ = ("event_id", "event_tag", "data", "created_at")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TAG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    event_tag: str
    data: _struct_pb2.Struct
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        event_id: _Optional[str] = ...,
        event_tag: _Optional[str] = ...,
        data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class UnsubscribeRequest(_message.Message):
    __slots__ = ("consumer_name", "event_tags")
    CONSUMER_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    consumer_name: str
    event_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, consumer_name: _Optional[str] = ..., event_tags: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class UnsubscribeResponse(_message.Message):
    __slots__ = ("consumer_name", "unsubscribed_event_tags")
    CONSUMER_NAME_FIELD_NUMBER: _ClassVar[int]
    UNSUBSCRIBED_EVENT_TAGS_FIELD_NUMBER: _ClassVar[int]
    consumer_name: str
    unsubscribed_event_tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        consumer_name: _Optional[str] = ...,
        unsubscribed_event_tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
