from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimeseriesGranularityUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MINUTE: _ClassVar[TimeseriesGranularityUnit]
    HOUR: _ClassVar[TimeseriesGranularityUnit]
    DAY: _ClassVar[TimeseriesGranularityUnit]

MINUTE: TimeseriesGranularityUnit
HOUR: TimeseriesGranularityUnit
DAY: TimeseriesGranularityUnit

class TimeseriesGranularityRequest(_message.Message):
    __slots__ = ("unit", "value")
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    unit: TimeseriesGranularityUnit
    value: int
    def __init__(
        self,
        unit: _Optional[_Union[TimeseriesGranularityUnit, str]] = ...,
        value: _Optional[int] = ...,
    ) -> None: ...
