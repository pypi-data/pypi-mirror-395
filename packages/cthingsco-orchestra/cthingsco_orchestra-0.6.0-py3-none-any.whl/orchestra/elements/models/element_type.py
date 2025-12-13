from enum import IntEnum
from typing import List

from pydantic import Field

from orchestra._internals.common.models.basemodels import PydObjectId, RWModel
import orchestra._internals.rpc.orchestra.element_types_pb2 as element_types_pb2


class ElementType(RWModel):
    """ElementType"""

    class Property(RWModel):
        """Property"""

        class PropertyType(IntEnum):
            # TODO: potentially make this recursive in the future
            # to support hierarchical schema definition
            # and validation
            ANY = 0
            STRING = 1
            INTEGER = 2
            FLOAT = 3
            BOOLEAN = 4
            MAP = 5

        key: str
        kind: PropertyType  # type of value (data type)
        # default: None | str | int | float | bool
        optional: bool = False  # whether the value may be null
        read_only: bool = (
            False  # whether the value is read-only (i.e. only the element may write to it)
        )

        # @root_validator
        # def validate_default(cls, values) -> dict:
        #     default = values.get("default")
        #     optional = values.get("optional")
        #     if not optional:
        #         assert default is not None
        #     return values

    id: PydObjectId = Field(..., title="id", description="ID of the element type")
    name: str = Field(..., title="name", description="Pretty name for the element type")

    def to_protobuf_model(self) -> element_types_pb2.ElementType:
        return element_types_pb2.ElementType(
            id=str(self.id),
            name=self.name,
        )

    @classmethod
    def from_protobuf_model(cls, proto: element_types_pb2.ElementType):
        return cls(
            id=proto.id,
            name=proto.name,
        )
