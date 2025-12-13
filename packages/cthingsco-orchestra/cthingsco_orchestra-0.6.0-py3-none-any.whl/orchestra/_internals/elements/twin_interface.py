from typing import Any, Callable, Dict, Optional

import grpc
from pydantic import UUID4

from orchestra.timeout import TIMEOUT, handle_deadline
from orchestra._internals.common.models.basemodels import PydObjectId
import orchestra._internals.common.models.exceptions as exceptions
import orchestra._internals.common.utils as utils
import orchestra._internals.rpc.orchestra.element_twins_pb2 as element_twins_pb2
from orchestra._internals.rpc.orchestra import element_twins_pb2_grpc
from orchestra._internals.watcher.watcher import Watcher

from orchestra.elements.models.element_twin import ElementTwin, ElementTwinObservables


class OrchestraTwinInterface:

    def __init__(
        self, channel: grpc.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ):
        self.element_twins_stub = element_twins_pb2_grpc.ElementTwinsServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    def create_element_twin(self, element_id: PydObjectId) -> ElementTwin:
        try:
            response: element_twins_pb2.ElementTwin = self.element_twins_stub.Create(
                element_twins_pb2.CreateElementTwinRequest(element_id=str(element_id)),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwin.from_protobuf_model(proto_twin=response)

    @handle_deadline
    def get_element_twin(self, twin_id: UUID4) -> ElementTwin:
        try:
            response: element_twins_pb2.ElementTwin = self.element_twins_stub.Get(
                element_twins_pb2.GetElementTwinRequest(
                    id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id))
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwin.from_protobuf_model(proto_twin=response)

    @handle_deadline
    def get_element_twin_observables(self, twin_id: UUID4) -> ElementTwinObservables:
        try:
            response: element_twins_pb2.ElementTwinObservables = (
                self.element_twins_stub.GetObservables(
                    element_twins_pb2.GetElementTwinObservablesRequest(
                        id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id))
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwinObservables.from_protobuf_model(proto_observables=response)

    @handle_deadline
    def set_element_twin_properties(self, twin_id: UUID4, delta: Dict[str, Any]) -> ElementTwin:
        try:
            response: element_twins_pb2.SetElementTwinPropertiesResponse = (
                self.element_twins_stub.Set(
                    element_twins_pb2.SetElementTwinPropertiesRequest(
                        id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id)),
                        properties=utils._get_pb2_struct(prop=delta),
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.FAILED_PRECONDITION:
                raise exceptions.TwinAtomicSetError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwin.from_protobuf_model(proto_twin=response.twin)

    def set_element_twin_property(self, twin_id: UUID4, key: str, value: Any) -> ElementTwin:
        return self.set_element_twin_properties(twin_id=twin_id, delta={key: value})

    @handle_deadline
    def set_element_twin_observables(
        self, twin_id: UUID4, observables: Dict[str, Any], event_type: Optional[str] = None
    ) -> ElementTwinObservables:
        try:
            response: element_twins_pb2.SetElementTwinObservablesResponse = (
                self.element_twins_stub.SetObservables(
                    element_twins_pb2.SetElementTwinObservablesRequest(
                        id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id)),
                        observables=utils._get_pb2_struct(prop=observables),
                        event_type=event_type,
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwinObservables.from_protobuf_model(proto_observables=response)

    def set_element_twin_observable(
        self, twin_id: UUID4, key: str, value: Any, event_type: Optional[str] = None
    ) -> ElementTwinObservables:
        return self.set_element_twin_observables(
            twin_id=twin_id, observables={key: value}, event_type=event_type
        )

    @handle_deadline
    def request_set_element_twin_properties(
        self, twin_id: UUID4, delta: Dict[str, Any]
    ) -> ElementTwin:
        try:
            response: element_twins_pb2.RequestSetElementTwinPropertiesResponse = (
                self.element_twins_stub.RequestSet(
                    element_twins_pb2.RequestSetElementTwinPropertiesRequest(
                        id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id)),
                        properties=utils._get_pb2_struct(prop=delta),
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.FAILED_PRECONDITION:
                raise exceptions.TwinAtomicSetError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwin.from_protobuf_model(proto_twin=response.twin)

    def request_set_element_twin_property(
        self, twin_id: UUID4, key: str, value: Any
    ) -> ElementTwin:
        return self.request_set_element_twin_properties(twin_id=twin_id, delta={key: value})

    @handle_deadline
    def accept_twin_state_change_request(self, twin_id: UUID4, accept_version: int) -> ElementTwin:
        try:
            response: element_twins_pb2.ValidateTwinStateChangeResponse = (
                self.element_twins_stub.ValidateTwinStateChange(
                    element_twins_pb2.ValidateTwinStateChangeRequest(
                        id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id)),
                        version=accept_version,
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif (e.code() == grpc.StatusCode.FAILED_PRECONDITION) and (
                "with version match" in e.details()
            ):
                raise exceptions.TwinAtomicSetError(e.details())
            elif (e.code() == grpc.StatusCode.FAILED_PRECONDITION) and (
                "requested version" in e.details()
            ):
                raise exceptions.TwinRequestNoLongerValid(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementTwin.from_protobuf_model(proto_twin=response.twin)

    def make_twin_state_watch(
        self, twin_id: UUID4, callback: Callable, suppress_current_changes: bool = True
    ) -> Callable:

        def _callback(event: element_twins_pb2.WatchElementTwinResponse) -> None:
            callback(
                int(event.old_version),
                int(event.new_version),
                ElementTwin.from_protobuf_model(event.twin),
            )

        try:
            watcher: Watcher = Watcher(
                rpc=self.element_twins_stub.Watch,
                proto_request=element_twins_pb2.WatchElementTwinRequest(
                    id=element_twins_pb2.TwinIdentifier(twin_id=str(twin_id)),
                    suppress_current_changes=suppress_current_changes,
                ),
                callback=_callback,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return watcher.cancel
