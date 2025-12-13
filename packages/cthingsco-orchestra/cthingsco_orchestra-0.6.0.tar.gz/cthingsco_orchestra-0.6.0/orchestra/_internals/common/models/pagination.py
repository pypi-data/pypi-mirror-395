from pydantic import BaseModel, NonNegativeInt, PositiveInt

import orchestra._internals.rpc.orchestra.pagination_pb2 as pagination_pb2


class Pagination(BaseModel):
    limit: NonNegativeInt
    offset: NonNegativeInt
    page_number: PositiveInt
    total_items: NonNegativeInt
    total_pages: NonNegativeInt

    @classmethod
    def from_protobuf_model(cls, proto_model: pagination_pb2.PaginationResponse):
        return cls(
            limit=proto_model.limit,
            offset=proto_model.offset,
            page_number=proto_model.page_number,
            total_items=proto_model.total_items,
            total_pages=proto_model.total_pages,
        )

    def to_protobuf_model(self) -> pagination_pb2.PaginationResponse:
        return pagination_pb2.PaginationResponse(**self.dict())
