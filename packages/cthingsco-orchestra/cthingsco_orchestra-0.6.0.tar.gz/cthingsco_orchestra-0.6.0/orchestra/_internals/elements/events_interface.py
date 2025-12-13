from typing import Any, AsyncIterable, Callable, Optional, Dict, List
import grpc

from orchestra.timeout import TIMEOUT, handle_deadline
from orchestra._internals.common import utils
import orchestra._internals.common.models.exceptions as exceptions
from orchestra._internals.rpc.orchestra import events_pb2_grpc
import orchestra._internals.rpc.orchestra.events_pb2 as events_pb2
from orchestra._internals.watcher.watcher import Watcher

from orchestra.elements.models.event import (
    DeclareSubscriberResponse,
    EventResponse,
    UnsubscribeResponse,
)


class OrchestraEventsInterface:
    """
    This interface is used to interact with the Orchestra Events service.

    Following API calls are available:
    - push_event:
        - Proto: `Push`
        - This method is used to push an event to the Orchestra Communication Service.
    - consume_events:
        - Proto: `Watch`
        - This method is used to consume events from the consumer in the Orchestra Communication Service.
    - declare_consumer:
        - Proto: `DeclareSubscriber`
        - This method is used to declare a consumer to the Orchestra Communication Service. Could be used to bind a consumer to a set of event tags.
    - unsubscribe_consumer:
        - Proto: `Unsubscribe`
        - This method is used to unsubscribe a consumer from a set of event tags in the Orchestra Communication Service.
    """

    def __init__(
        self, channel: grpc.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ) -> None:
        self._stub = events_pb2_grpc.EventsServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    def push_event(
        self,
        event_tag: str,
        data: Dict[str, Any],
    ) -> EventResponse:
        try:
            response: events_pb2.EventResponse = self._stub.Push(
                events_pb2.PushEventRequest(
                    event_tag=event_tag,
                    data=utils._get_pb2_struct(data),
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return EventResponse.from_protobuf_model(response)

    @handle_deadline
    def consume_events(
        self,
        consumer_name: str,
        callback: Callable[[EventResponse], Any],
    ) -> Callable[..., None]:
        try:
            watcher = Watcher(
                rpc=self._stub.Watch,
                proto_request=events_pb2.WatchEventsRequest(
                    consumer_name=consumer_name,
                ),
                callback=callback,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return watcher.cancel

    @handle_deadline
    def declare_consumer(
        self,
        consumer_name: str,
        event_tags: Optional[List[str]] = None,
    ) -> DeclareSubscriberResponse:
        try:
            response: events_pb2.DeclareSubscriberResponse = self._stub.DeclareSubscriber(
                events_pb2.DeclareSubscriberRequest(
                    consumer_name=consumer_name,
                    event_tags=event_tags,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return DeclareSubscriberResponse.from_protobuf_model(response)

    @handle_deadline
    def unsubscribe_consumer(
        self,
        consumer_name: str,
        event_tags: Optional[List[str]] = None,
    ) -> UnsubscribeResponse:
        try:
            response: events_pb2.UnsubscribeResponse = self._stub.Unsubscribe(
                events_pb2.UnsubscribeRequest(
                    consumer_name=consumer_name,
                    event_tags=event_tags,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return UnsubscribeResponse.from_protobuf_model(response)


class AsyncOrchestraEventsInterface:
    """
    This interface is used to interact with the Orchestra Events service.

    Following API calls are available:
    - push_event:
        - Proto: `Push`
        - This method is used to push an event to the Orchestra Communication Service.
    - consume_events:
        - Proto: `Watch`
        - This method is used to consume events from the consumer in the Orchestra Communication Service.
    - declare_consumer:
        - Proto: `DeclareSubscriber`
        - This method is used to declare a consumer to the Orchestra Communication Service. Could be used to bind a consumer to a set of event tags.
    - unsubscribe_consumer:
        - Proto: `Unsubscribe`
        - This method is used to unsubscribe a consumer from a set of event tags in the Orchestra Communication Service.
    """

    def __init__(
        self, channel: grpc.aio.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ) -> None:
        self._stub = events_pb2_grpc.EventsServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    async def push_event(
        self,
        event_tag: str,
        data: Dict[str, Any],
    ) -> EventResponse:
        try:
            response: events_pb2.EventResponse = await self._stub.Push(
                events_pb2.PushEventRequest(
                    event_tag=event_tag,
                    data=utils._get_pb2_struct(data),
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return EventResponse.from_protobuf_model(response)

    @handle_deadline
    async def consume_events(
        self,
        consumer_name: str,
    ) -> AsyncIterable[EventResponse]:
        try:
            async for response in self._stub.Watch(
                events_pb2.WatchEventsRequest(
                    consumer_name=consumer_name,
                ),
            ):
                yield EventResponse.from_protobuf_model(response)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

    @handle_deadline
    async def declare_consumer(
        self,
        consumer_name: str,
        event_tags: Optional[List[str]] = None,
    ) -> DeclareSubscriberResponse:
        try:
            response: events_pb2.DeclareSubscriberResponse = await self._stub.DeclareSubscriber(
                events_pb2.DeclareSubscriberRequest(
                    consumer_name=consumer_name,
                    event_tags=event_tags,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return DeclareSubscriberResponse.from_protobuf_model(response)

    @handle_deadline
    async def unsubscribe_consumer(
        self,
        consumer_name: str,
        event_tags: Optional[List[str]] = None,
    ) -> UnsubscribeResponse:
        try:
            response: events_pb2.UnsubscribeResponse = await self._stub.Unsubscribe(
                events_pb2.UnsubscribeRequest(
                    consumer_name=consumer_name,
                    event_tags=event_tags,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return UnsubscribeResponse.from_protobuf_model(response)
