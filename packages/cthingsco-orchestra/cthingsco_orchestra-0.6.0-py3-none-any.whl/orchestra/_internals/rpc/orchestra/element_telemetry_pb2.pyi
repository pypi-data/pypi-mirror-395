from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import pagination_pb2 as _pagination_pb2
import sort_pb2 as _sort_pb2
import timeseries_granularity_pb2 as _timeseries_granularity_pb2
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

class SingleElementTelemetry(_message.Message):
    __slots__ = ("ts", "data")
    TS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ts: _timestamp_pb2.Timestamp
    data: _struct_pb2.Struct
    def __init__(
        self,
        ts: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class MultipleElementTelemetry(_message.Message):
    __slots__ = ("element_id", "telemetry")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    telemetry: SingleElementTelemetry
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        telemetry: _Optional[_Union[SingleElementTelemetry, _Mapping]] = ...,
    ) -> None: ...

class ElementPartition(_message.Message):
    __slots__ = ("element_id", "partition")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    partition: str
    def __init__(
        self, element_id: _Optional[str] = ..., partition: _Optional[str] = ...
    ) -> None: ...

class MultipleElementPartitionTelemetry(_message.Message):
    __slots__ = ("element_partition", "telemetry")
    ELEMENT_PARTITION_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    element_partition: ElementPartition
    telemetry: SingleElementTelemetry
    def __init__(
        self,
        element_partition: _Optional[_Union[ElementPartition, _Mapping]] = ...,
        telemetry: _Optional[_Union[SingleElementTelemetry, _Mapping]] = ...,
    ) -> None: ...

class GetElementTelemetryRequest(_message.Message):
    __slots__ = ("element_id", "ts_from", "ts_to", "pagination", "sort", "granularity", "partition")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TS_FROM_FIELD_NUMBER: _ClassVar[int]
    TS_TO_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    ts_from: _timestamp_pb2.Timestamp
    ts_to: _timestamp_pb2.Timestamp
    pagination: _pagination_pb2.PaginationRequest
    sort: _sort_pb2.SortType
    granularity: _timeseries_granularity_pb2.TimeseriesGranularityRequest
    partition: str
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        ts_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ts_to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationRequest, _Mapping]] = ...,
        sort: _Optional[_Union[_sort_pb2.SortType, str]] = ...,
        granularity: _Optional[
            _Union[_timeseries_granularity_pb2.TimeseriesGranularityRequest, _Mapping]
        ] = ...,
        partition: _Optional[str] = ...,
    ) -> None: ...

class GetElementTelemetryResponse(_message.Message):
    __slots__ = ("element_id", "telemetry", "pagination")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    telemetry: _containers.RepeatedCompositeFieldContainer[SingleElementTelemetry]
    pagination: _pagination_pb2.PaginationResponse
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        telemetry: _Optional[_Iterable[_Union[SingleElementTelemetry, _Mapping]]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationResponse, _Mapping]] = ...,
    ) -> None: ...

class GetManyElementTelemetryRequest(_message.Message):
    __slots__ = (
        "element_ids",
        "ts_from",
        "ts_to",
        "pagination",
        "sort",
        "granularity",
        "partition",
    )
    ELEMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    TS_FROM_FIELD_NUMBER: _ClassVar[int]
    TS_TO_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    element_ids: _containers.RepeatedScalarFieldContainer[str]
    ts_from: _timestamp_pb2.Timestamp
    ts_to: _timestamp_pb2.Timestamp
    pagination: _pagination_pb2.PaginationRequest
    sort: _sort_pb2.SortType
    granularity: _timeseries_granularity_pb2.TimeseriesGranularityRequest
    partition: str
    def __init__(
        self,
        element_ids: _Optional[_Iterable[str]] = ...,
        ts_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ts_to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationRequest, _Mapping]] = ...,
        sort: _Optional[_Union[_sort_pb2.SortType, str]] = ...,
        granularity: _Optional[
            _Union[_timeseries_granularity_pb2.TimeseriesGranularityRequest, _Mapping]
        ] = ...,
        partition: _Optional[str] = ...,
    ) -> None: ...

class GetManyElementTelemetryResponse(_message.Message):
    __slots__ = ("element_ids", "telemetry", "pagination")
    ELEMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    element_ids: _containers.RepeatedScalarFieldContainer[str]
    telemetry: _containers.RepeatedCompositeFieldContainer[MultipleElementTelemetry]
    pagination: _pagination_pb2.PaginationResponse
    def __init__(
        self,
        element_ids: _Optional[_Iterable[str]] = ...,
        telemetry: _Optional[_Iterable[_Union[MultipleElementTelemetry, _Mapping]]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationResponse, _Mapping]] = ...,
    ) -> None: ...

class GetManyElementPartitionTelemetryRequest(_message.Message):
    __slots__ = ("elements_partitions", "ts_from", "ts_to", "pagination", "sort")
    ELEMENTS_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    TS_FROM_FIELD_NUMBER: _ClassVar[int]
    TS_TO_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    elements_partitions: _containers.RepeatedCompositeFieldContainer[ElementPartition]
    ts_from: _timestamp_pb2.Timestamp
    ts_to: _timestamp_pb2.Timestamp
    pagination: _pagination_pb2.PaginationRequest
    sort: _sort_pb2.SortType
    def __init__(
        self,
        elements_partitions: _Optional[_Iterable[_Union[ElementPartition, _Mapping]]] = ...,
        ts_from: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ts_to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationRequest, _Mapping]] = ...,
        sort: _Optional[_Union[_sort_pb2.SortType, str]] = ...,
    ) -> None: ...

class GetManyElementPartitionTelemetryResponse(_message.Message):
    __slots__ = ("telemetry", "pagination")
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    telemetry: _containers.RepeatedCompositeFieldContainer[MultipleElementPartitionTelemetry]
    pagination: _pagination_pb2.PaginationResponse
    def __init__(
        self,
        telemetry: _Optional[_Iterable[_Union[MultipleElementPartitionTelemetry, _Mapping]]] = ...,
        pagination: _Optional[_Union[_pagination_pb2.PaginationResponse, _Mapping]] = ...,
    ) -> None: ...

class GetLatestElementTelemetryRequest(_message.Message):
    __slots__ = ("element_id", "ts_upper_bound", "partition")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TS_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    ts_upper_bound: _timestamp_pb2.Timestamp
    partition: str
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        ts_upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        partition: _Optional[str] = ...,
    ) -> None: ...

class GetLatestElementTelemetryResponse(_message.Message):
    __slots__ = ("element_id", "telemetry")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    telemetry: SingleElementTelemetry
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        telemetry: _Optional[_Union[SingleElementTelemetry, _Mapping]] = ...,
    ) -> None: ...

class GetManyLatestElementTelemetryRequest(_message.Message):
    __slots__ = ("element_ids", "ts_upper_bound", "partition")
    ELEMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    TS_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    element_ids: _containers.RepeatedScalarFieldContainer[str]
    ts_upper_bound: _timestamp_pb2.Timestamp
    partition: str
    def __init__(
        self,
        element_ids: _Optional[_Iterable[str]] = ...,
        ts_upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        partition: _Optional[str] = ...,
    ) -> None: ...

class GetManyLatestElementTelemetryResponse(_message.Message):
    __slots__ = ("telemetry",)
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    telemetry: _containers.RepeatedCompositeFieldContainer[MultipleElementTelemetry]
    def __init__(
        self, telemetry: _Optional[_Iterable[_Union[MultipleElementTelemetry, _Mapping]]] = ...
    ) -> None: ...

class GetManyLatestElementPartitionTelemetryRequest(_message.Message):
    __slots__ = ("elements_partitions", "ts_upper_bound")
    ELEMENTS_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    TS_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    elements_partitions: _containers.RepeatedCompositeFieldContainer[ElementPartition]
    ts_upper_bound: _timestamp_pb2.Timestamp
    def __init__(
        self,
        elements_partitions: _Optional[_Iterable[_Union[ElementPartition, _Mapping]]] = ...,
        ts_upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetManyLatestElementPartitionTelemetryResponse(_message.Message):
    __slots__ = ("telemetry",)
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    telemetry: _containers.RepeatedCompositeFieldContainer[MultipleElementPartitionTelemetry]
    def __init__(
        self,
        telemetry: _Optional[_Iterable[_Union[MultipleElementPartitionTelemetry, _Mapping]]] = ...,
    ) -> None: ...

class PushElementTelemetryRequest(_message.Message):
    __slots__ = ("element_id", "telemetry", "partition", "event_type")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    telemetry: SingleElementTelemetry
    partition: str
    event_type: str
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        telemetry: _Optional[_Union[SingleElementTelemetry, _Mapping]] = ...,
        partition: _Optional[str] = ...,
        event_type: _Optional[str] = ...,
    ) -> None: ...

class PushElementTelemetryResponse(_message.Message):
    __slots__ = ("document_id",)
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    document_id: str
    def __init__(self, document_id: _Optional[str] = ...) -> None: ...

class PushManyElementTelemetryRequest(_message.Message):
    __slots__ = ("element_id", "telemetry", "partition")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    telemetry: _containers.RepeatedCompositeFieldContainer[SingleElementTelemetry]
    partition: str
    def __init__(
        self,
        element_id: _Optional[str] = ...,
        telemetry: _Optional[_Iterable[_Union[SingleElementTelemetry, _Mapping]]] = ...,
        partition: _Optional[str] = ...,
    ) -> None: ...

class GetAggregatedTelemetryRequest(_message.Message):
    __slots__ = ("pipeline",)
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    pipeline: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(
        self, pipeline: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...
    ) -> None: ...

class GetAggregatedTelemetryResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    def __init__(
        self, result: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ...
    ) -> None: ...
