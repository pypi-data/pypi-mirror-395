from datetime import datetime
from typing import Any, Dict, Optional, Union, List

from google.protobuf import json_format, struct_pb2
import orjson
from pydantic import UUID4

from orchestra._internals.common.models.basemodels import PydObjectId, RWModel
import orchestra._internals.common.utils as utils
import orchestra._internals.rpc.orchestra.element_twins_pb2 as element_twins_pb2


class ElementTwin(RWModel):
    class TwinState(RWModel):
        class State(RWModel):
            version: int
            properties: dict

            def to_protobuf_model(
                self,
            ) -> element_twins_pb2.ElementTwin.TwinState.State:
                return element_twins_pb2.ElementTwin.TwinState.State(
                    version=self.version,
                    properties=utils._get_pb2_struct(prop=self.properties),
                )

        current: State
        desired: State

        def to_protobuf_model(self) -> element_twins_pb2.ElementTwin.TwinState:
            return element_twins_pb2.ElementTwin.TwinState(
                current=self.current.to_protobuf_model(),
                desired=self.desired.to_protobuf_model(),
            )

    id: UUID4
    element_type_id: PydObjectId
    state: TwinState

    def to_protobuf_model(self) -> element_twins_pb2.ElementTwin:
        return element_twins_pb2.ElementTwin(
            id=str(self.id),
            element_type_id=str(self.element_type_id),
            state=self.state.to_protobuf_model(),
        )

    @classmethod
    def from_protobuf_model(cls, proto_twin: element_twins_pb2.ElementTwin):
        d: dict = json_format.MessageToDict(proto_twin)
        # json_format.MessageToDict removes underscores in non-Struct keys
        # and converts them to camelCase, resulting in a ValidationError
        # from Pydantic
        return cls(element_type_id=d["elementTypeId"], **d)

    def serialise(self) -> bytes:
        return orjson.dumps(
            {
                "id": str(self.id),
                "element_type_id": str(self.element_type_id),
                "state": self.state.dict(),
            }
        )

    @classmethod
    def deserialise(cls, data: bytes):
        return cls(**orjson.loads(data))


class ElementTwinObservables(RWModel):
    class Observable(RWModel):
        ts: datetime
        value: Any

        @classmethod
        def from_protobuf_model(cls, proto_observable: element_twins_pb2.Observable):
            return cls(
                ts=utils._get_datetime_from_pb2_timestamp(proto_observable.ts),
                value=proto_observable.value,
            )

    id: str
    observables: Dict[str, Observable]

    @classmethod
    def make_new_from_element_twin(cls, element_twin: ElementTwin):
        return cls(
            id=str(element_twin.id) + "_observables",
            observables={},
        )

    def to_protobuf_model(self) -> element_twins_pb2.ElementTwinObservables:
        observables: List[element_twins_pb2.Observable] = []
        for key, val in self.observables.items():
            observable: element_twins_pb2.Observable = element_twins_pb2.Observable(
                key=str(key),
                value=utils._get_pb2_value(val.value),
                ts=utils._get_pb2_timestamp_from_datetime(val.ts),
            )
            observables.append(observable)

        protobuf_model: element_twins_pb2.ElementTwinObservables = (
            element_twins_pb2.ElementTwinObservables(id=str(self.id), observables=())
        )
        protobuf_model.observables.extend(observables)

        return protobuf_model

    @classmethod
    def from_protobuf_model(
        cls,
        proto_observables: Optional[
            Union[
                element_twins_pb2.ElementTwinObservables,
                element_twins_pb2.SetElementTwinObservablesResponse,
            ]
        ],
    ):
        return cls(
            id=proto_observables.id,
            observables={
                o.key: cls.Observable(
                    ts=utils._get_datetime_from_pb2_timestamp(o.ts),
                    value=json_format.MessageToDict(o.value),
                )
                for o in proto_observables.observables
            },
        )

    def serialize(self) -> bytes:
        return orjson.dumps(self.dict())

    @classmethod
    def deserialise(cls, data: bytes):
        return cls(**orjson.loads(data))

    def _update_with_protobuf_observables(self, pb2struct_observables: struct_pb2.Struct) -> bool:
        changed: bool = False
        pb2props: dict = json_format.MessageToDict(pb2struct_observables)
        # add validation to check if pb2props can be transformed into Dict[str, Observable]?
        if self.observables == pb2props:
            return changed

        for key in pb2props.keys():
            if key in self.observables.keys() and self.observables.get(key) == pb2props.get(key):
                continue
            observable: ElementTwinObservables.Observable = ElementTwinObservables.Observable(
                ts=datetime.utcnow(), value=pb2props[key]
            )
            self.observables[key] = observable
            changed = True
        return changed
