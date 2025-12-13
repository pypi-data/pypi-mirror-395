import grpc

import orchestra._internals.common.models.exceptions as exceptions
from orchestra.timeout import TIMEOUT, handle_deadline
import orchestra._internals.rpc.orchestra.element_types_pb2 as element_types_pb2
from orchestra._internals.rpc.orchestra import element_types_pb2_grpc

from orchestra.elements.models.element_type import ElementType


class OrchestraElementTypeInterface:

    def __init__(
        self, channel: grpc.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ):
        self.element_types_stub = element_types_pb2_grpc.ElementTypesServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    def create_element_type(self, name: str) -> ElementType:
        try:
            response: element_types_pb2.ElementType = self.element_types_stub.Create(
                element_types_pb2.CreateElementTypeRequest(name=name),
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
        return ElementType.from_protobuf_model(proto=response)

    @handle_deadline
    def get_element_type_by_name(self, name: str) -> ElementType:
        try:
            response: element_types_pb2.ElementType = self.element_types_stub.GetByName(
                element_types_pb2.GetElementTypeByNameRequest(name=name),
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
