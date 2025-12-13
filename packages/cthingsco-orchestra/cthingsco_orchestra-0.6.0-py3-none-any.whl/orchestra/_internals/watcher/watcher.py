import logging
import queue
import time
import threading
from typing import Callable, Iterable, Optional

from google.protobuf.message import Message
import grpc

import orchestra._internals.common.utils as utils


logger = logging.getLogger(__name__)


class Watcher:
    def __init__(self, rpc: Callable, proto_request: Message, callback: Callable) -> None:
        self._rpc = rpc
        self._proto_request = proto_request
        self._callback = callback

        self._event_queue = queue.Queue()
        self._cancelled = threading.Event()

        self._response_iterator: Iterable = self._rpc(self._proto_request)

        self._executor = utils._get_threadpool_executor()(max_workers=4)
        self._executor.submit(self._response_watcher)
        self._executor.submit(self._process_callbacks)

    def cancel(self) -> None:
        self._cancelled.set()
        self._event_queue.put(None)
        self._response_iterator.cancel()
        self._executor.shutdown()  # wait=False?

    def _process_callbacks(self) -> None:
        while not self._cancelled.is_set():
            event: Optional[Message] = self._event_queue.get()
            if event is None:
                self._cancelled.set()
            if not self._cancelled.is_set():
                self._callback(event)

    def _response_watcher(self) -> None:
        while not self._cancelled.is_set():
            try:
                for response in self._response_iterator:
                    self._event_queue.put(response)
            except grpc.RpcError:
                logger.exception("Connection error with RPC server; will attempt reconnect")
                time.sleep(10)
                self._response_iterator: Iterable = self._rpc(self._proto_request)
                continue
            except:
                logger.exception("Something unexpected occurred")
                # TODO: handle this
                time.sleep(10)
                continue
