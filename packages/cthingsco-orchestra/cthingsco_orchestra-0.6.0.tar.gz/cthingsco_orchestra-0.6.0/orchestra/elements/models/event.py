from datetime import datetime
from typing import Any, Optional, Dict, List
from google.protobuf import json_format
from orchestra._internals.common import utils

import orchestra._internals.rpc.orchestra.events_pb2 as events_pb2
from orchestra._internals.common.models.basemodels import RWModel


class Event(RWModel):
    event_tag: str
    data: Dict[str, Any]


class EventResponse(Event):
    event_id: str
    created_at: datetime

    @classmethod
    def from_protobuf_model(
        cls,
        proto: events_pb2.EventResponse,
    ):
        return cls(
            event_id=proto.event_id,
            event_tag=proto.event_tag,
            data=json_format.MessageToDict(proto.data),
            created_at=utils._get_datetime_from_pb2_timestamp(proto.created_at),
        )


class DeclareSubscriberResponse(RWModel):
    consumer_name: str
    event_tags: Optional[List[str]] = None

    @classmethod
    def from_protobuf_model(
        cls,
        proto: events_pb2.DeclareSubscriberResponse,
    ):
        return cls(
            consumer_name=proto.consumer_name,
            event_tags=list(proto.event_tags),
        )


class UnsubscribeResponse(RWModel):
    consumer_name: str
    unsubscribed_event_tags: Optional[List[str]] = None

    @classmethod
    def from_protobuf_model(
        cls,
        proto: events_pb2.UnsubscribeResponse,
    ):
        return cls(
            consumer_name=proto.consumer_name,
            unsubscribed_event_tags=list(proto.unsubscribed_event_tags),
        )
