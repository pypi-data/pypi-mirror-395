from datetime import datetime
from typing import Optional
from typing import Tuple, List, Dict

from google.protobuf import json_format

from orchestra._internals.common.models.basemodels import PydObjectId, RWModel
import orchestra._internals.common.utils as utils
import orchestra._internals.rpc.orchestra.element_telemetry_pb2 as element_telemetry_pb2


def _element_telemetry_to_protobuf_model(
    ts: datetime, data: dict
) -> element_telemetry_pb2.SingleElementTelemetry:
    return element_telemetry_pb2.SingleElementTelemetry(
        ts=utils._get_pb2_timestamp_from_datetime(ts),
        data=utils._get_pb2_struct(data),
    )


class SingleElementTelemetry(RWModel):
    ts: datetime
    data: dict

    @classmethod
    def from_protobuf_model(cls, proto_model: element_telemetry_pb2.SingleElementTelemetry):
        return cls(
            ts=utils._get_datetime_from_pb2_timestamp(proto_model.ts),
            data=json_format.MessageToDict(proto_model.data),
        )

    @classmethod
    def to_tuple(
        cls, proto_model: element_telemetry_pb2.SingleElementTelemetry
    ) -> Tuple[datetime, dict]:
        return (
            utils._get_datetime_from_pb2_timestamp(proto_model.ts),
            json_format.MessageToDict(proto_model.data),
        )

    def to_protobuf_model(self) -> element_telemetry_pb2.SingleElementTelemetry:
        return _element_telemetry_to_protobuf_model(ts=self.ts, data=self.data)


class ElementTelemetryPartition(RWModel):
    element_id: str
    data: dict
    ts: datetime
    partition: str

    @classmethod
    def to_tuple(
        cls, proto_model: element_telemetry_pb2.MultipleElementPartitionTelemetry
    ) -> Tuple[PydObjectId, str, datetime, dict]:
        return (
            PydObjectId(proto_model.element_partition.element_id),
            proto_model.element_partition.partition,
            utils._get_datetime_from_pb2_timestamp(proto_model.telemetry.ts),
            json_format.MessageToDict(proto_model.telemetry.data),
        )


class MultipleElementTelemetry(RWModel):
    element_id: PydObjectId
    telemetry: SingleElementTelemetry

    @classmethod
    def from_protobuf_model(cls, proto_model: element_telemetry_pb2.MultipleElementTelemetry):
        return cls(
            element_id=PydObjectId(proto_model.element_id),
            telemetry=SingleElementTelemetry.from_protobuf_model(proto_model=proto_model.telemetry),
        )

    @classmethod
    def to_tuple(
        cls, proto_model: element_telemetry_pb2.MultipleElementTelemetry
    ) -> Tuple[PydObjectId, datetime, dict]:
        telemetry: SingleElementTelemetry = SingleElementTelemetry.from_protobuf_model(
            proto_model=proto_model.telemetry
        )
        return (
            PydObjectId(proto_model.element_id),
            telemetry.ts,
            telemetry.data,
        )


class ElementPartition(RWModel):
    element_id: PydObjectId
    partition: str

    @classmethod
    def from_protobuf_model(cls, proto_model: element_telemetry_pb2.ElementPartition):
        return cls(
            element_id=PydObjectId(proto_model.element_id),
            partiton=str(proto_model.partition),
        )

    @classmethod
    def to_tuple(
        cls, proto_model: element_telemetry_pb2.ElementPartition
    ) -> Tuple[PydObjectId, str]:
        return (
            PydObjectId(proto_model.element_id),
            proto_model.partition,
        )


class MultipleElementPartitionTelemetry(RWModel):
    element_partition: ElementPartition
    telemetry: SingleElementTelemetry

    @classmethod
    def from_protobuf_model(
        cls, proto_model: element_telemetry_pb2.MultipleElementPartitionTelemetry
    ):
        return cls(
            element_partition=ElementPartition.from_protobuf_model(
                proto_model=proto_model.element_partition
            ),
            telemetry=SingleElementTelemetry.from_protobuf_model(proto_model=proto_model.telemetry),
        )

    @classmethod
    def to_tuple(
        cls, proto_model: element_telemetry_pb2.MultipleElementPartitionTelemetry
    ) -> Tuple[PydObjectId, str, datetime, dict]:
        telemetry: SingleElementTelemetry = SingleElementTelemetry.from_protobuf_model(
            proto_model=proto_model.telemetry
        )
        return (
            PydObjectId(proto_model.element_partition.element_id),
            proto_model.element_partition.partition,
            telemetry.ts,
            telemetry.data,
        )


class ElementTelemetry(SingleElementTelemetry, RWModel):
    element_id: PydObjectId

    @classmethod
    def from_protobuf_model_single_element(
        cls,
        element_id: PydObjectId,
        proto_model: element_telemetry_pb2.SingleElementTelemetry,
    ):
        telemetry = SingleElementTelemetry.from_protobuf_model(proto_model=proto_model)
        return cls(element_id=element_id, ts=telemetry.ts, data=telemetry.data)

    def to_protobuf_model_push_request(
        self,
        partition: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> element_telemetry_pb2.PushElementTelemetryRequest:
        return element_telemetry_pb2.PushElementTelemetryRequest(
            element_id=str(self.element_id),
            telemetry=_element_telemetry_to_protobuf_model(ts=self.ts, data=self.data),
            partition=partition,
            event_type=event_type,
        )

    def to_protobuf_model_single_element(
        self,
    ) -> element_telemetry_pb2.SingleElementTelemetry:
        return _element_telemetry_to_protobuf_model(ts=self.ts, data=self.data)


class AggregateTelemetryResult(RWModel):
    result: List[Dict]

    @classmethod
    def from_protobuf_model(cls, proto_model: element_telemetry_pb2.GetAggregatedTelemetryResponse):
        return cls(
            result=[utils._get_dict_from_pb2_struct_(r) for r in proto_model.result],
        )
