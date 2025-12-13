from typing import Callable

import google.protobuf.empty_pb2 as empty_pb2
import grpc

from orchestra.timeout import TIMEOUT, handle_deadline
from orchestra._internals.common.models.basemodels import PydObjectId
import orchestra._internals.common.models.exceptions as exceptions
import orchestra._internals.rpc.orchestra.elements_pb2 as elements_pb2
import orchestra._internals.rpc.orchestra.element_types_pb2 as element_types_pb2
from orchestra._internals.rpc.orchestra import element_types_pb2_grpc
from orchestra._internals.rpc.orchestra import elements_pb2_grpc
from orchestra._internals.watcher.watcher import Watcher

from orchestra.elements.models.element import Element
from orchestra.elements.models.element_type import ElementType


class OrchestraElementInterface:
    def __init__(
        self, channel: grpc.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ):
        self.elements_stub = elements_pb2_grpc.ElementsServiceStub(channel)
        self.element_types_stub = element_types_pb2_grpc.ElementTypesServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    def get_element(self, element_id: PydObjectId) -> Element:
        try:
            response: elements_pb2.Element = self.elements_stub.Get(
                elements_pb2.GetElementRequest(id=str(element_id)),
                timeout=TIMEOUT,
                compression=self.compression,
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
        return Element.from_protobuf_model(proto=response)

    @handle_deadline
    def get_element_type(self, element_type_id: PydObjectId) -> ElementType:
        try:
            response: element_types_pb2.ElementType = self.element_types_stub.Get(
                element_types_pb2.GetElementTypeRequest(
                    id=element_types_pb2.ElementTypeIdentifier(element_type_id=str(element_type_id))
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return ElementType.from_protobuf_model(proto=response)

    @handle_deadline
    def create_element(self, name: str, element_type_id: PydObjectId) -> Element:
        try:
            response: elements_pb2.Element = self.elements_stub.Create(
                elements_pb2.CreateElementRequest(name=name, element_type_id=str(element_type_id)),
                timeout=TIMEOUT,
                compression=self.compression,
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

        return Element.from_protobuf_model(proto=response)

    def get_element_type_by_element_id(self, element_id: PydObjectId) -> ElementType:
        try:
            element: Element = self.get_element(element_id=element_id)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return self.get_element_type(element_type_id=element.element_type_id)

    @handle_deadline
    def delete_element(self, element_id: PydObjectId) -> None:
        try:
            response: empty_pb2.Empty = self.elements_stub.Delete(
                elements_pb2.DeleteElementRequest(id=str(element_id)),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise exceptions.NotFoundError(e.details())
            elif (e.code() == grpc.StatusCode.UNAVAILABLE) and (
                "Etcd3 connection error" in e.details()
            ):
                raise exceptions.Etcd3ConnectionError(e.details())
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

    def make_element_watcher(
        self, element_id: PydObjectId, callback: Callable[[str, str], None]
    ) -> Callable[[], None]:

        def _callback(response: elements_pb2.WatchElementResponse) -> None:
            callback(response.twin_id, response.type)

        try:
            watcher: Watcher = Watcher(
                rpc=self.elements_stub.Watch,
                proto_request=elements_pb2.WatchElementRequest(id=str(element_id)),
                callback=_callback,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )
        return watcher.cancel
