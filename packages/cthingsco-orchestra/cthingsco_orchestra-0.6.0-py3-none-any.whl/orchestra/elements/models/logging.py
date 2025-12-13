from datetime import datetime
from typing import Optional

from pydantic import UUID4

import orchestra._internals.rpc.orchestra.element_logs_pb2 as element_logs_pb2
from orchestra._internals.common import utils
from orchestra._internals.common.models.basemodels import PydObjectId, RWModel


class Log(RWModel):
    element_id: PydObjectId
    twin_id: UUID4
    log: str
    tenant_id: Optional[PydObjectId] = None
    ts: datetime

    @classmethod
    def from_protobuf_model(cls, proto: element_logs_pb2.SingleElementLog, element_id: str):
        twin_id = None
        tenant_id = None
        for t in proto.tags:
            if t.key == "twin_id":
                twin_id = t.value
            if t.key == "tenant_id":
                tenant_id = t.value

        return cls(
            ts=utils._get_datetime_from_pb2_timestamp(proto.ts),
            element_id=element_id,
            twin_id=twin_id,
            tenant_id=tenant_id,
            log=proto.log,
        )

    def to_protobuf_model(self) -> element_logs_pb2.SingleElementLog:
        return element_logs_pb2.SingleElementLog(
            ts=utils._get_pb2_timestamp_from_datetime(self.ts),
            log=self.log,
            tags=[
                element_logs_pb2.LogTag(key=k, value=v)
                for k, v in {
                    "tenant_id": str(self.tenant_id),
                    "twin_id": str(self.twin_id),
                    "element_id": str(self.element_id),
                }.items()
            ],
        )
