from enum import Enum
from typing import List

from pydantic import UUID4, BaseModel

from orchestra._internals.common.models.basemodels import PydObjectId, RWModel
import orchestra._internals.rpc.orchestra.elements_pb2 as elements_pb2


class Element(RWModel):
    id: PydObjectId
    twin_ids: List[UUID4]
    name: str
    element_type_id: PydObjectId

    def to_protobuf_model(self) -> elements_pb2.Element:
        return elements_pb2.Element(
            id=str(self.id),
            twin_ids=[str(twin_id) for twin_id in self.twin_ids],
            name=self.name,
            element_type_id=str(self.element_type_id),
        )

    @classmethod
    def from_protobuf_model(cls, proto: elements_pb2.Element):
        return cls(
            id=proto.id,
            twin_ids=[twin_id for twin_id in proto.twin_ids],
            name=proto.name,
            element_type_id=proto.element_type_id,
        )


class ElementEventType(str, Enum):
    twin_created = "twin_created"
    twin_updated = "twin_updated"
    twin_deleted = "twin_deleted"


class ElementInWatchResponse(BaseModel):
    id: PydObjectId
    twin_id: UUID4
    type: ElementEventType

    def to_protobuf_model(self) -> elements_pb2.WatchElementResponse:
        return elements_pb2.WatchElementResponse(
            id=str(self.id), twin_id=str(self.twin_id), type=self.type.value
        )

    @classmethod
    def from_protobuf_model(cls, proto: elements_pb2.WatchElementResponse):
        return cls(id=proto.id, twin_id=proto.twin_id, type=ElementEventType(proto.type))
