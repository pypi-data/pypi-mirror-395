from datetime import datetime
from typing import Any, Iterable, Optional, Tuple, List, Dict
from typing import Union

import grpc
from pydantic import NonNegativeInt, UUID4

from orchestra._internals.common.models.basemodels import PydObjectId
from orchestra._internals.common.models.granularity import TimeseriesGranularity
from orchestra._internals.common.models.pagination import Pagination
from orchestra._internals.common.models.sort import Sort
from orchestra._internals.elements.element_interface import OrchestraElementInterface
from orchestra._internals.elements.element_type_interface import OrchestraElementTypeInterface
from orchestra._internals.elements.events_interface import OrchestraEventsInterface
from orchestra._internals.elements.logging_interface import OrchestraLoggingInterface
from orchestra._internals.elements.telemetry_interface import OrchestraTelemetryInterface
from orchestra._internals.elements.twin_interface import OrchestraTwinInterface

from orchestra.elements.credentials import OrchestraCredentials

from orchestra.elements.models.element import Element
from orchestra.elements.models.element_twin import ElementTwin, ElementTwinObservables
from orchestra.elements.models.element_type import ElementType
from orchestra.elements.models.event import DeclareSubscriberResponse, EventResponse
from orchestra.elements.models.logging import Log


class OrchestraControllerClient:
    """Provides support for interaction with Orchestra Elements
    from the perspective of the controller
    """

    def __init__(
        self,
        credentials: OrchestraCredentials,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ) -> None:
        self.channel = credentials.channel
        self.element_iface = OrchestraElementInterface(
            channel=self.channel, compression=compression
        )
        self.element_type_iface = OrchestraElementTypeInterface(
            channel=self.channel, compression=compression
        )
        self.events_iface = OrchestraEventsInterface(channel=self.channel, compression=compression)
        self.logging_iface = OrchestraLoggingInterface(
            channel=self.channel, compression=compression
        )
        self.telemetry_iface = OrchestraTelemetryInterface(
            channel=self.channel, compression=compression
        )
        self.twin_iface = OrchestraTwinInterface(channel=self.channel, compression=compression)

    def get_telemetry(
        self,
        element_id: PydObjectId,
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> List[Tuple[datetime, dict]]:
        return self.telemetry_iface.get_telemetry(
            element_id=element_id,
            ts_from=ts_from,
            ts_to=ts_to,
            ts_sort=ts_sort,
            granularity=granularity,
            partition=partition,
        )

    def get_telemetry_paginated(
        self,
        element_id: PydObjectId,
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> Tuple[List[Tuple[datetime, dict]], Pagination]:
        return self.telemetry_iface.get_telemetry_paginated(
            element_id=element_id,
            ts_from=ts_from,
            ts_to=ts_to,
            limit=limit,
            offset=offset,
            ts_sort=ts_sort,
            granularity=granularity,
            partition=partition,
        )

    def get_many_telemetry(
        self,
        element_ids: Iterable[PydObjectId],
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> Dict[PydObjectId, List[Tuple[datetime, dict]]]:
        return self.telemetry_iface.get_many_telemetry(
            element_ids=element_ids,
            ts_from=ts_from,
            ts_to=ts_to,
            ts_sort=ts_sort,
            granularity=granularity,
            partition=partition,
        )

    def get_many_telemetry_paginated(
        self,
        element_ids: Iterable[PydObjectId],
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> Tuple[List[Tuple[PydObjectId, datetime, dict]], Pagination]:
        return self.telemetry_iface.get_many_telemetry_paginated(
            element_ids=element_ids,
            ts_from=ts_from,
            ts_to=ts_to,
            limit=limit,
            offset=offset,
            ts_sort=ts_sort,
            granularity=granularity,
            partition=partition,
        )

    def get_many_telemetry_partitions(
        self,
        elements_partitions: List[Tuple[Union[PydObjectId, str], str]],
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
    ) -> List[Tuple[str, str, datetime, dict]]:
        return self.telemetry_iface.get_many_telemetry_partitions(
            elements_partitions=elements_partitions,
            ts_from=ts_from,
            ts_to=ts_to,
            ts_sort=ts_sort,
        )

    def get_many_telemetry_partitions_paginated(
        self,
        elements_partitions: List[Tuple[Union[PydObjectId, str], str]],
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
    ) -> Tuple[List[Tuple[PydObjectId, str, datetime, dict]], Pagination]:
        return self.telemetry_iface.get_many_telemetry_partitions_paginated(
            elements_partitions=elements_partitions,
            ts_from=ts_from,
            ts_to=ts_to,
            limit=limit,
            offset=offset,
            ts_sort=ts_sort,
        )

    def get_latest_telemetry(
        self,
        element_id: PydObjectId,
        ts_upper_bound: Optional[datetime] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> Tuple[datetime, dict]:
        return self.telemetry_iface.get_latest_telemetry_by_element_id(
            element_id=element_id,
            ts_upper_bound=ts_upper_bound,
            partition=partition,
        )

    def get_many_latest_telemetry(
        self,
        element_ids: Iterable[PydObjectId],
        ts_upper_bound: Optional[datetime] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> Dict[PydObjectId, Tuple[datetime, dict]]:
        return self.telemetry_iface.get_many_latest_telemetry_by_element_ids(
            element_ids=element_ids,
            ts_upper_bound=ts_upper_bound,
            partition=partition,
        )

    def get_many_latest_telemetry_partitions(
        self,
        elements_partitions: List[Tuple[Union[PydObjectId, str], str]],
        ts_upper_bound: Optional[datetime] = None,
    ) -> List[Tuple[PydObjectId, str, datetime, dict]]:
        return self.telemetry_iface.get_many_latest_telemetry_partitions_by_element_ids(
            elements_partitions=elements_partitions,
            ts_upper_bound=ts_upper_bound,
        )

    # is this method really required for the controller?
    def push_telemetry(
        self,
        element_id: PydObjectId,
        data: dict,
        ts: Optional[datetime] = None,
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
        event_type: Optional[str] = None,
    ) -> PydObjectId:
        return self.telemetry_iface.push_telemetry(
            element_id=element_id,
            data=data,
            ts=ts,
            partition=partition,
            event_type=event_type,
        )

    # is this method really required for the controller?
    def push_batch_telemetry(
        self,
        element_id: PydObjectId,
        data: Iterable[Tuple[datetime, dict]],
        partition: Optional[str] = OrchestraTelemetryInterface.DEFAULT_PARTITION,
    ) -> None:
        self.telemetry_iface.push_batch_telemetry(
            element_id=element_id,
            data=data,
            partition=partition,
        )

    def create_element_twin(self, element_id: PydObjectId) -> ElementTwin:
        return self.twin_iface.create_element_twin(element_id=element_id)

    def get_element_twin(self, twin_id: UUID4) -> ElementTwin:
        return self.twin_iface.get_element_twin(twin_id=twin_id)

    def request_set_element_twin_property(
        self, twin_id: UUID4, key: str, value: Any
    ) -> ElementTwin:
        return self.twin_iface.request_set_element_twin_property(
            twin_id=twin_id, key=key, value=value
        )

    def request_set_element_twin_properties(
        self, twin_id: UUID4, delta: Dict[str, Any]
    ) -> ElementTwin:
        return self.twin_iface.request_set_element_twin_properties(twin_id=twin_id, delta=delta)

    def get_element(self, element_id: PydObjectId) -> Element:
        return self.element_iface.get_element(element_id=element_id)

    def get_element_type(self, element_type_id: PydObjectId) -> ElementType:
        return self.element_iface.get_element_type(element_type_id=element_type_id)

    def get_element_type_by_element_id(self, element_id: PydObjectId) -> ElementType:
        return self.element_iface.get_element_type_by_element_id(element_id=element_id)

    def get_element_type_by_name(self, element_type_name: str) -> ElementType:
        return self.element_type_iface.get_element_type_by_name(name=element_type_name)

    def request_set_element_twin_observable(
        self, twin_id: UUID4, key: str, value: Any, event_type: Optional[str] = None
    ):
        return self.twin_iface.set_element_twin_observable(
            twin_id, key=key, value=value, event_type=event_type
        )

    def get_element_twin_observable(self, twin_id: UUID4) -> ElementTwinObservables:
        return self.twin_iface.get_element_twin_observables(twin_id)

    def declare_events_consumer(
        self, consumer_name: str, event_tags: Optional[List[str]] = None
    ) -> DeclareSubscriberResponse:
        return self.events_iface.declare_consumer(
            consumer_name=consumer_name, event_tags=event_tags
        )

    def push_event(
        self,
        event_tag: str,
        data: Dict[str, Any],
    ) -> EventResponse:
        return self.events_iface.push_event(event_tag=event_tag, data=data)

    def get_many_logs_paginated(
        self,
        element_id: PydObjectId,
        tags: Dict[str, str],
        ts_from: Optional[datetime] = None,
        ts_to: Optional[datetime] = None,
        limit: NonNegativeInt = 0,
        offset: NonNegativeInt = 0,
        ts_sort: Sort = Sort.ASCENDING,
    ) -> Tuple[List[Log], Pagination]:
        return self.logging_iface.get_many_logs_paginated(
            element_id=element_id,
            tags=tags,
            ts_from=ts_from,
            ts_to=ts_to,
            limit=limit,
            offset=offset,
            ts_sort=ts_sort,
        )

    def aggregate(self, pipeline: List[Dict]) -> List[Dict[str, Any]]:
        res = self.telemetry_iface.aggregate(pipeline=pipeline)
        return res.result
