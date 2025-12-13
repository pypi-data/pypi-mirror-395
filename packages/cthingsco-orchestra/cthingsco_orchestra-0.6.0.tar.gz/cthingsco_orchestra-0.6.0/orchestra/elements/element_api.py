from datetime import datetime
from typing import Any, Callable, Optional, Dict, List, Tuple

import grpc
from pydantic import UUID4

from orchestra._internals.common.models.basemodels import PydObjectId
from orchestra._internals.elements.element_interface import OrchestraElementInterface
from orchestra._internals.elements.telemetry_interface import OrchestraTelemetryInterface
from orchestra._internals.elements.twin_interface import OrchestraTwinInterface
from orchestra.elements.credentials import OrchestraCredentials

from orchestra.elements.models.element import Element
from orchestra.elements.models.element_twin import ElementTwin
from orchestra.elements.models.element_type import ElementType


class OrchestraElementClient:
    """Provides support for interaction with Orchestra Elements
    from the perspective of the element
    """

    def __init__(
        self,
        credentials: OrchestraCredentials,
        element_id: PydObjectId,
        twin_id: UUID4,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ) -> None:
        self.channel = credentials.channel
        self.element_iface = OrchestraElementInterface(
            channel=self.channel, compression=compression
        )
        self.telemetry_iface = OrchestraTelemetryInterface(
            channel=self.channel, compression=compression
        )
        self.twin_iface = OrchestraTwinInterface(channel=self.channel, compression=compression)
        self.element_id: PydObjectId = element_id

        self._element: Element = self.element_iface.get_element(
            element_id=self.element_id,
        )

        self._twin_id: UUID4 = twin_id
        self._type_id: PydObjectId = self._element.element_type_id

        self._twin_type: ElementType = self.element_iface.get_element_type(
            element_type_id=self._type_id,
        )

        self._twin: ElementTwin = self.twin_iface.get_element_twin(twin_id=self._twin_id)
        # TODO: close watcher channel gracefully on program exit
        self._twin_state_watch_cancel: Callable = self.twin_iface.make_twin_state_watch(
            twin_id=self._twin_id,
            callback=self._twin_state_watcher,
            suppress_current_changes=True,
        )

        self._callbacks: Dict[str, List[Callable]] = {"twin_state_change_request": []}

    def get_twin_property_keys(self) -> List[str]:
        return [x.key for x in self._twin_type.properties]

    def get_twin_properties(self) -> dict:
        return self._twin.state.current.properties

    def get_twin_state_version(self) -> int:
        return self._twin.state.current.version

    def get_property(self, key: str) -> Any:
        # TODO: cast properties correctly based on schema definition
        return self._twin.state.current.properties.get(key)

    def set_property(self, key: str, value: Any) -> ElementTwin:
        # TODO: cast properties correctly based on schema definition
        self._twin = self.twin_iface.set_element_twin_property(
            twin_id=self._twin_id,
            key=key,
            value=value,
        )
        return self._twin

    def set_properties(self, delta: Dict[str, Any]) -> ElementTwin:
        self._twin = self.twin_iface.set_element_twin_properties(
            twin_id=self._twin_id,
            delta=delta,
        )
        return self._twin

    def get_desired_twin_state(self) -> Tuple[int, dict]:
        return (self._twin.state.desired.version, self._twin.state.desired.properties)

    def register_twin_state_change_request_callback(
        self, callback: Callable[[int, int, ElementTwin], None]
    ) -> None:
        self._callbacks["twin_state_change_request"].append(callback)

    def accept_twin_state_change_request(self, accept_version: int) -> ElementTwin:
        self._twin = self.twin_iface.accept_twin_state_change_request(
            twin_id=self._twin_id,
            accept_version=accept_version,
        )
        return self._twin

    def push_telemetry(self, data: dict, ts: Optional[datetime] = None) -> PydObjectId:
        return self.telemetry_iface.push_telemetry(element_id=self.element_id, data=data, ts=ts)

    def set_observables(self, event_type: Optional[str] = None, **observables):
        return self.twin_iface.set_element_twin_observables(
            self._twin_id, observables=observables, event_type=event_type
        )

    def _twin_state_watcher(self, old_version: int, new_version: int, twin: ElementTwin) -> None:
        # TODO: This code is unfortunately worrysome as _twin_state_watcher
        # is called in a different thread than the running application's main
        # thread
        self._twin = twin
        for cb in self._callbacks["twin_state_change_request"]:
            cb(old_version, new_version, twin)
