from typing import AsyncIterable

import grpc

from orchestra.elements.credentials import AsyncOrchestraCredentials
from typing import Any, Callable, List

import orchestra._internals.elements.events_interface as events_iface
from orchestra.elements.credentials import OrchestraCredentials
from orchestra.elements.models.event import (
    DeclareSubscriberResponse,
    EventResponse,
    UnsubscribeResponse,
)


class OrchestraEventsConsumerClient:
    """Provides a client for interacting with the Orchestra Events System"""

    def __init__(
        self,
        credentials: OrchestraCredentials,
        consumer_name: str,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ) -> None:
        self.channel = credentials.channel
        self.events_iface = events_iface.OrchestraEventsInterface(
            channel=self.channel,
            compression=compression,
        )
        self.consumer_name = consumer_name
        self._watcher_cancel = None
        self.events_iface.declare_consumer(consumer_name=self.consumer_name)

    def bind(self, event_tags: List[str]) -> DeclareSubscriberResponse:
        return self.events_iface.declare_consumer(
            consumer_name=self.consumer_name,
            event_tags=event_tags,
        )

    def unbind(self, event_tags: List[str]) -> UnsubscribeResponse:
        return self.events_iface.unsubscribe_consumer(
            consumer_name=self.consumer_name,
            event_tags=event_tags,
        )

    def consume(self, callback: Callable[[EventResponse], Any]) -> Callable[..., None]:
        self._watcher_cancel = self.events_iface.consume_events(
            consumer_name=self.consumer_name,
            callback=callback,
        )
        return self._watcher_cancel

    def stop_consuming(self) -> None:
        if self._watcher_cancel is not None:
            self._watcher_cancel()


class AsyncOrchestraEventsConsumerClient:
    """Provides a client for interacting with the Orchestra Events System"""

    def __init__(
        self,
        credentials: AsyncOrchestraCredentials,
        consumer_name: str,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ) -> None:
        self.channel = credentials.channel
        self.events_iface = events_iface.AsyncOrchestraEventsInterface(
            channel=self.channel,
            compression=compression,
        )
        self.consumer_name = consumer_name

    async def bind(self, event_tags: List[str]) -> DeclareSubscriberResponse:
        return await self.events_iface.declare_consumer(
            consumer_name=self.consumer_name,
            event_tags=event_tags,
        )

    async def unbind(self, event_tags: List[str]) -> UnsubscribeResponse:
        return await self.events_iface.unsubscribe_consumer(
            consumer_name=self.consumer_name,
            event_tags=event_tags,
        )

    async def consume(self) -> AsyncIterable[EventResponse]:
        await self.events_iface.declare_consumer(consumer_name=self.consumer_name)
        async for event in self.events_iface.consume_events(consumer_name=self.consumer_name):
            yield event
