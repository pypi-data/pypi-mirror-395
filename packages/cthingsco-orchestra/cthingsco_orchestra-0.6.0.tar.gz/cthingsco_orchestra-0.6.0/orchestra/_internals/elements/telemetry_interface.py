from collections import defaultdict
from datetime import datetime, timezone
from typing import Generator, Iterable, Optional, Tuple, List, Dict, Union

import google.protobuf.empty_pb2 as empty_pb2
import grpc
from pydantic import NonNegativeInt

from orchestra.elements.models.element_telemetry import ElementTelemetryPartition
from orchestra.elements.models.element_telemetry import MultipleElementPartitionTelemetry
from orchestra.timeout import TIMEOUT, handle_deadline
from orchestra._internals.common.models.basemodels import PydObjectId
import orchestra._internals.common.models.exceptions as exceptions
from orchestra._internals.common.models.granularity import TimeseriesGranularity
from orchestra._internals.common.models.pagination import Pagination
from orchestra._internals.common.models.sort import Sort
import orchestra._internals.common.utils as utils
import orchestra._internals.rpc.orchestra.element_telemetry_pb2 as element_telemetry_pb2
import orchestra._internals.rpc.orchestra.pagination_pb2 as pagination_pb2
from orchestra._internals.rpc.orchestra import element_telemetry_pb2_grpc

from orchestra.elements.models.element_telemetry import (
    AggregateTelemetryResult,
    ElementTelemetry,
    MultipleElementTelemetry,
    SingleElementTelemetry,
)


class OrchestraTelemetryInterface:
    DEFAULT_PARTITION: str = "default"

    def __init__(
        self, channel: grpc.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ):
        self.element_telemetry_stub = element_telemetry_pb2_grpc.ElementTelemetryServiceStub(
            channel
        )
        self.compression: grpc.Compression = compression

    @handle_deadline
    def get_telemetry(
        self,
        element_id: PydObjectId,
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: str = DEFAULT_PARTITION,
    ) -> List[Tuple[datetime, dict]]:
        try:
            response: Generator[element_telemetry_pb2.GetElementTelemetryResponse, None, None] = (
                self.element_telemetry_stub.Get(
                    element_telemetry_pb2.GetElementTelemetryRequest(
                        element_id=str(element_id),
                        ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                        ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                        sort=Sort.to_protobuf_model(ts_sort),
                        granularity=granularity.to_protobuf_model() if granularity else None,
                        partition=partition,
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return [SingleElementTelemetry.to_tuple(x) for item in response for x in item.telemetry]

    @handle_deadline
    def get_telemetry_paginated(
        self,
        element_id: PydObjectId,
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: str = DEFAULT_PARTITION,
    ) -> Tuple[List[Tuple[datetime, dict]], Pagination]:
        try:
            response: Generator[element_telemetry_pb2.GetElementTelemetryResponse, None, None] = (
                self.element_telemetry_stub.Get(
                    element_telemetry_pb2.GetElementTelemetryRequest(
                        element_id=str(element_id),
                        ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                        ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                        pagination=pagination_pb2.PaginationRequest(limit=limit, offset=offset),
                        sort=Sort.to_protobuf_model(ts_sort),
                        granularity=granularity.to_protobuf_model() if granularity else None,
                        partition=partition,
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        response_items = list(response)
        if not response_items:
            return [], Pagination(limit=limit, offset=offset, total=0)

        telemetry_data = [
            SingleElementTelemetry.to_tuple(x) for item in response_items for x in item.telemetry
        ]
        return (
            telemetry_data,
            Pagination.from_protobuf_model(proto_model=response_items[0].pagination),
        )

    def get_many_telemetry(
        self,
        element_ids: Iterable[PydObjectId],
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: str = DEFAULT_PARTITION,
    ) -> Dict[PydObjectId, List[Tuple[datetime, dict]]]:
        try:
            response: Generator[
                element_telemetry_pb2.GetManyElementTelemetryResponse, None, None
            ] = self.element_telemetry_stub.GetMany(
                element_telemetry_pb2.GetManyElementTelemetryRequest(
                    element_ids=[str(id) for id in element_ids],
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    sort=Sort.to_protobuf_model(ts_sort),
                    granularity=granularity.to_protobuf_model() if granularity else None,
                    partition=partition,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        temp_ret: Dict[str, list] = defaultdict(list)

        for item in response:
            for doc in item.telemetry:
                temp_ret[doc.element_id].append(doc)

        return {
            PydObjectId(k): [MultipleElementTelemetry.to_tuple(doc) for doc in v]
            for k, v in temp_ret.items()
        }

    def get_many_telemetry_partitions(
        self,
        elements_partitions: List[Tuple[Union[PydObjectId, str], str]],
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
    ) -> List[Tuple[PydObjectId, str, datetime, dict]]:
        try:
            response: Generator[
                element_telemetry_pb2.GetManyElementPartitionTelemetryResponse, None, None
            ] = self.element_telemetry_stub.GetManyPartition(
                element_telemetry_pb2.GetManyElementPartitionTelemetryRequest(
                    elements_partitions=self._get_element_partition_items(elements_partitions),
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    sort=Sort.to_protobuf_model(ts_sort),
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return [
            ElementTelemetryPartition.to_tuple(doc) for item in response for doc in item.telemetry
        ]

    @handle_deadline
    def get_many_telemetry_paginated(
        self,
        element_ids: Iterable[PydObjectId],
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: str = DEFAULT_PARTITION,
    ) -> Tuple[List[Tuple[PydObjectId, datetime, dict]], Pagination]:
        try:
            response: Generator[
                element_telemetry_pb2.GetManyElementTelemetryResponse, None, None
            ] = self.element_telemetry_stub.GetMany(
                element_telemetry_pb2.GetManyElementTelemetryRequest(
                    element_ids=[str(id) for id in element_ids],
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    pagination=pagination_pb2.PaginationRequest(limit=limit, offset=offset),
                    sort=Sort.to_protobuf_model(ts_sort),
                    granularity=granularity.to_protobuf_model() if granularity else None,
                    partition=partition,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        response_items = list(response)
        if not response_items:
            return [], Pagination(limit=limit, offset=offset, total=0)

        telemetry_data = [
            MultipleElementTelemetry.to_tuple(x) for item in response_items for x in item.telemetry
        ]
        return (
            telemetry_data,
            Pagination.from_protobuf_model(proto_model=response_items[0].pagination),
        )

    @handle_deadline
    def get_many_telemetry_partitions_paginated(
        self,
        elements_partitions: List[Tuple[Union[PydObjectId, str], str]],
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
    ) -> Tuple[List[Tuple[PydObjectId, str, datetime, dict]], Pagination]:
        try:
            response: Generator[
                element_telemetry_pb2.GetManyElementPartitionTelemetryResponse, None, None
            ] = self.element_telemetry_stub.GetManyPartition(
                element_telemetry_pb2.GetManyElementPartitionTelemetryRequest(
                    elements_partitions=self._get_element_partition_items(elements_partitions),
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    pagination=pagination_pb2.PaginationRequest(limit=limit, offset=offset),
                    sort=Sort.to_protobuf_model(ts_sort),
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        response_items = list(response)
        if not response_items:
            return [], Pagination(limit=limit, offset=offset, total=0)

        telemetry_data = [
            MultipleElementPartitionTelemetry.to_tuple(x)
            for item in response_items
            for x in item.telemetry
        ]
        return (
            telemetry_data,
            Pagination.from_protobuf_model(proto_model=response_items[0].pagination),
        )

    def _get_element_partition_items(self, elements_partitions):
        elements_partitions_items: List[element_telemetry_pb2.ElementPartition] = []
        for element_id, partition in elements_partitions:
            elements_partitions_items.append(
                element_telemetry_pb2.ElementPartition(
                    element_id=str(element_id), partition=partition
                )
            )
        return elements_partitions_items

    @handle_deadline
    def get_latest_telemetry_by_element_id(
        self,
        element_id: PydObjectId,
        ts_upper_bound: Optional[datetime] = None,
        partition: str = DEFAULT_PARTITION,
    ) -> Tuple[datetime, dict]:
        if ts_upper_bound:
            request = element_telemetry_pb2.GetLatestElementTelemetryRequest(
                ts_upper_bound=utils._get_pb2_timestamp_from_datetime(ts_upper_bound)
            )
        else:
            request = element_telemetry_pb2.GetLatestElementTelemetryRequest()
        request.element_id = str(element_id)
        request.partition = partition
        try:
            response: element_telemetry_pb2.GetLatestElementTelemetryResponse = (
                self.element_telemetry_stub.GetLatest(
                    request, timeout=TIMEOUT, compression=self.compression
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return SingleElementTelemetry.to_tuple(response.telemetry)

    @handle_deadline
    def get_many_latest_telemetry_by_element_ids(
        self,
        element_ids: Iterable[PydObjectId],
        ts_upper_bound: Optional[datetime] = None,
        partition: str = DEFAULT_PARTITION,
    ) -> Dict[PydObjectId, Tuple[datetime, dict]]:
        request = element_telemetry_pb2.GetManyLatestElementTelemetryRequest(
            element_ids=[str(id) for id in element_ids]
        )
        if ts_upper_bound:
            request.ts_upper_bound = utils._get_pb2_timestamp_from_datetime(ts_upper_bound)
        request.partition = partition

        try:
            response: Generator[
                element_telemetry_pb2.GetManyLatestElementTelemetryResponse, None, None
            ] = self.element_telemetry_stub.GetManyLatest(
                request, timeout=TIMEOUT, compression=self.compression
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        temp_results = {x.element_id: x.telemetry for item in response for x in item.telemetry}

        return {PydObjectId(k): SingleElementTelemetry.to_tuple(v) for k, v in temp_results.items()}

    @handle_deadline
    def get_many_latest_telemetry_partitions_by_element_ids(
        self,
        elements_partitions: List[Tuple[Union[PydObjectId, str], str]],
        ts_upper_bound: Optional[datetime] = None,
    ) -> List[Tuple[PydObjectId, str, datetime, dict]]:
        request = element_telemetry_pb2.GetManyLatestElementPartitionTelemetryRequest(
            elements_partitions=self._get_element_partition_items(elements_partitions)
        )
        if ts_upper_bound:
            request.ts_upper_bound = utils._get_pb2_timestamp_from_datetime(ts_upper_bound)

        try:
            response: Generator[
                element_telemetry_pb2.GetManyLatestElementPartitionTelemetryResponse, None, None
            ] = self.element_telemetry_stub.GetManyPartitionLatest(
                request, timeout=TIMEOUT, compression=self.compression
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return [
            MultipleElementPartitionTelemetry.to_tuple(x)
            for item in response
            for x in item.telemetry
        ]

    @handle_deadline
    def push_telemetry(
        self,
        element_id: PydObjectId,
        data: dict,
        ts: Optional[datetime] = None,
        partition: str = DEFAULT_PARTITION,
        event_type: Optional[str] = None,
    ) -> PydObjectId:
        try:
            response: element_telemetry_pb2.PushElementTelemetryResponse = (
                self.element_telemetry_stub.Push(
                    ElementTelemetry(
                        element_id=element_id,
                        ts=ts if ts else datetime.now(timezone.utc),
                        data=data,
                    ).to_protobuf_model_push_request(
                        partition=partition or self.DEFAULT_PARTITION,
                        event_type=event_type,
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return PydObjectId(response.document_id)

    @handle_deadline
    def push_batch_telemetry(
        self,
        element_id: PydObjectId,
        data: Iterable[Tuple[datetime, dict]],
        partition: str = DEFAULT_PARTITION,
    ) -> None:
        data: List[Tuple[datetime, dict]] = list(data)
        data.sort(key=lambda x: x[0])
        try:
            response: empty_pb2.Empty = self.element_telemetry_stub.PushMany(
                element_telemetry_pb2.PushManyElementTelemetryRequest(
                    element_id=str(element_id),
                    telemetry=[
                        ElementTelemetry(
                            element_id=element_id, ts=x, data=y
                        ).to_protobuf_model_single_element()
                        for x, y in data
                    ],
                    partition=partition or self.DEFAULT_PARTITION,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

    @handle_deadline
    def aggregate(self, pipeline: List[Dict]) -> AggregateTelemetryResult:
        try:
            response: Generator[
                element_telemetry_pb2.GetAggregatedTelemetryResponse, None, None
            ] = self.element_telemetry_stub.Aggregate(
                element_telemetry_pb2.GetAggregatedTelemetryRequest(
                    pipeline=[utils._get_pb2_struct(prop=p) for p in pipeline]
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        result: Optional[element_telemetry_pb2.GetAggregatedTelemetryResponse] = None
        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetAggregatedTelemetryResponse(result=item.result)
            else:
                result.result.extend(item.result)

        return AggregateTelemetryResult.from_protobuf_model(result)
