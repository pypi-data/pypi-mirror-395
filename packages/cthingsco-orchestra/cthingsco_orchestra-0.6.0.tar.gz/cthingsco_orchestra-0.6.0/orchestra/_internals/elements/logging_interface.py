from datetime import datetime
from typing import Dict, Generator, List, Optional, Tuple

import grpc
from pydantic import NonNegativeInt

import orchestra._internals.common.utils as utils
import orchestra._internals.rpc.orchestra.element_logs_pb2 as element_logs_pb2
import orchestra._internals.rpc.orchestra.pagination_pb2 as pagination_pb2
from orchestra._internals.common.models.basemodels import PydObjectId
import orchestra._internals.common.models.exceptions as exceptions
from orchestra._internals.common.models.pagination import Pagination
from orchestra._internals.common.models.sort import Sort
from orchestra._internals.rpc.orchestra import element_logs_pb2_grpc
from orchestra.elements.models.logging import Log
from orchestra.timeout import TIMEOUT, handle_deadline


class OrchestraLoggingInterface:
    def __init__(
        self, channel: grpc.Channel, compression: grpc.Compression = grpc.Compression.Gzip
    ):
        self.element_logs_stub = element_logs_pb2_grpc.ElementLogsServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    def push_logs(self, element_id: PydObjectId, logs: List[Log]) -> None:
        try:
            self.element_logs_stub.PushMany(
                element_logs_pb2.PushManyElementLogsRequest(
                    element_id=str(element_id),
                    logs=[log.to_protobuf_model() for log in logs],
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

    @handle_deadline
    def get_many_logs_paginated(
        self,
        element_id: PydObjectId,
        tags: Dict[str, str],
        ts_from: Optional[datetime] = None,
        ts_to: Optional[datetime] = None,
        limit: NonNegativeInt = 0,
        offset: NonNegativeInt = 0,
        ts_sort: Sort = Sort.ASCENDING,
    ) -> Tuple[List[Log], Pagination]:
        try:
            response: Generator[element_logs_pb2.GetManyElementLogsResponse, None, None] = (
                self.element_logs_stub.GetMany(
                    element_logs_pb2.GetManyElementLogsRequest(
                        element_id=str(element_id),
                        tags=[element_logs_pb2.LogTag(key=k, value=v) for k, v in tags.items()],
                        ts_from=(
                            utils._get_pb2_timestamp_from_datetime(ts_from) if ts_from else None
                        ),
                        ts_to=utils._get_pb2_timestamp_from_datetime(ts_to) if ts_to else None,
                        pagination=pagination_pb2.PaginationRequest(limit=limit, offset=offset),
                        sort=Sort.to_protobuf_model(ts_sort),
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            elif e.code() == grpc.StatusCode.UNAVAILABLE:
                raise exceptions.UnavailableError(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        result: Optional[element_logs_pb2.GetManyElementLogsResponse] = None

        for item in response:
            if result == None:
                result = element_logs_pb2.GetManyElementLogsResponse(
                    element_id=item.element_id,
                    logs=item.logs,
                    pagination=item.pagination,
                )
            else:
                result.logs.extend(item.logs)

        return (
            [Log.from_protobuf_model(proto=x, element_id=element_id) for x in result.logs],
            Pagination.from_protobuf_model(proto_model=result.pagination),
        )
