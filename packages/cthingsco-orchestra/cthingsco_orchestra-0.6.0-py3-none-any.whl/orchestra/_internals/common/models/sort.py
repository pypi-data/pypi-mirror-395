from enum import IntEnum

import orchestra._internals.rpc.orchestra.sort_pb2 as sort_pb2


class Sort(IntEnum):
    ASCENDING = 1
    DESCENDING = -1

    @classmethod
    def to_protobuf_model(cls, value: int) -> int:
        if value == Sort.DESCENDING:
            return 1
        return 0
