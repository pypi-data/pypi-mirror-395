from datetime import datetime, timezone
from typing import Any

import sys
import futurist

import google.protobuf.json_format as json_format
import google.protobuf.struct_pb2 as struct_pb2
import google.protobuf.timestamp_pb2 as timestamp_pb2


def _get_pb2_struct(prop: dict) -> struct_pb2.Struct:
    struct_prop: struct_pb2.Struct = struct_pb2.Struct()
    for k, v in prop.items():
        if isinstance(v, dict):
            struct_prop.update({k: _get_pb2_struct(prop=v)})
        else:
            struct_prop.update({k: v})
    return struct_prop


def _get_dict_from_pb2_struct_(struct: struct_pb2.Struct) -> dict:
    return json_format.MessageToDict(struct)


def _get_datetime_from_pb2_timestamp(
    timestamp: timestamp_pb2.Timestamp,
) -> datetime:
    return datetime.fromtimestamp(timestamp.seconds + timestamp.nanos / 1e9, tz=timezone.utc)


def _get_pb2_timestamp_from_datetime(dt: datetime) -> timestamp_pb2.Timestamp:
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp


def _get_pb2_value(value: Any) -> struct_pb2.Value:
    if isinstance(value, str):
        return struct_pb2.Value(string_value=value)
    elif isinstance(value, (float, int)):
        return struct_pb2.Value(number_value=value)
    elif isinstance(value, bool):
        return struct_pb2.Value(bool_value=value)
    elif isinstance(value, dict):
        return struct_pb2.Value(struct_value=_get_pb2_struct(value))
    elif isinstance(value, list):
        return struct_pb2.Value(
            list_value=struct_pb2.ListValue(values=[_get_pb2_value(val) for val in value])
        )
    elif isinstance(value, None):
        return struct_pb2.Value(null_value=value)
    else:
        # todo something nicer?
        raise RuntimeError()


def _import_module(import_str):
    """Import a module."""
    __import__(import_str)
    return sys.modules[import_str]


def _try_import(import_str, default=None):
    """Try to import a module and if it fails return default."""
    try:
        return _import_module(import_str)
    except ImportError:
        return default


# These may or may not exist; so carefully import them if we can...
_eventlet = _try_import("eventlet")
_patcher = _try_import("eventlet.patcher")


def _get_threadpool_executor() -> type:
    if all((_eventlet, _patcher)) and _patcher.is_monkey_patched("thread"):
        return futurist.GreenThreadPoolExecutor
    return futurist.ThreadPoolExecutor
