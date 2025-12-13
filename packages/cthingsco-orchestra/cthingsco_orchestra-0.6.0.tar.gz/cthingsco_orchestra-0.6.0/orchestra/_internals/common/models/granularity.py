from enum import IntEnum

from orchestra._internals.common.models.basemodels import RWModel
import orchestra._internals.rpc.orchestra.timeseries_granularity_pb2 as timeseries_granularity_pb2


class TimeseriesGranularityUnit(IntEnum):
    MINUTE = 0
    HOUR = 1
    DAY = 2


class TimeseriesGranularity(RWModel):
    unit: TimeseriesGranularityUnit
    value: int

    @classmethod
    def from_protobuf_model(
        cls, proto_model: timeseries_granularity_pb2.TimeseriesGranularityRequest
    ):
        return cls(
            unit=TimeseriesGranularityUnit(proto_model.unit),
            value=int(proto_model.value),
        )

    def to_protobuf_model(
        self,
    ) -> timeseries_granularity_pb2.TimeseriesGranularityRequest:
        return timeseries_granularity_pb2.TimeseriesGranularityRequest(
            unit=int(self.unit),
            value=int(self.value),
        )
