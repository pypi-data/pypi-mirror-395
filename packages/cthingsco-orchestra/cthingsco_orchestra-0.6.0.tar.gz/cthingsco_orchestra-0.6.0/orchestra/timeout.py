from functools import wraps
import logging

from grpc import RpcError, StatusCode

logger = logging.getLogger(__name__)

TIMEOUT = 600


def handle_deadline(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except RpcError as error:
            logger.exception(f"ORC SDK Deadline exceeded exception: {error.details()}")
            if error.details().lower() == StatusCode.DEADLINE_EXCEEDED.value[1]:
                raise TimeoutError(error.details()) from error
            else:
                raise error(error.details())

    return inner
