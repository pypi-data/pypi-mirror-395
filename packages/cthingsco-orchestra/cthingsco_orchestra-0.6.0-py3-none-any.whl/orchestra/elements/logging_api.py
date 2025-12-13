import contextlib
import queue
import threading
from datetime import datetime, timezone
from typing import List, Optional

import grpc
from pydantic import UUID4

from orchestra._internals.common.models.basemodels import PydObjectId
from orchestra._internals.elements.logging_interface import OrchestraLoggingInterface
from orchestra.elements.credentials import OrchestraCredentials
from orchestra.elements.models.logging import Log


class OrchestraLoggingClient:
    """Provides support for logging with Orchestra"""

    def __init__(
        self,
        credentials: OrchestraCredentials,
        element_id: PydObjectId,
        transmit_interval: int,
        max_logs: int,
        num_workers: int = 2,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ) -> None:
        self.channel: grpc.Channel = credentials.channel
        self.logging_iface: OrchestraLoggingInterface = OrchestraLoggingInterface(
            channel=self.channel,
            compression=compression,
        )
        self.element_id = element_id

        self.num_workers: int = num_workers
        self.max_logs = max_logs
        self.transmit_interval = transmit_interval

        self.logs_queue: queue.Queue[Log] = queue.Queue()
        self.worker_threads: List[threading.Thread] = []

        self._stop_event: threading.Event = threading.Event()
        self._worker_lock: threading.Condition = threading.Condition()
        self._queue_lock: threading.Lock = threading.Lock()

    def start(self) -> None:
        if self.worker_threads:
            return

        with self._worker_lock:
            for _ in range(self.num_workers):
                worker = threading.Thread(target=self._worker, daemon=True)
                self.worker_threads.append(worker)
                worker.start()

    def _worker(self) -> None:
        while not self._stop_event.is_set():
            with self._worker_lock:
                self._worker_lock.wait(timeout=self.transmit_interval)

            logs: List[Log] = []
            while True:
                try:
                    logs.append(self.logs_queue.get_nowait())
                except queue.Empty:
                    break

            if logs:
                try:
                    self.logging_iface.push_logs(element_id=self.element_id, logs=logs)
                except Exception as e:
                    print(f"Exception in OrchestraLoggingClient worker - push_logs: {e}")

    def push_log(
        self,
        log: str,
        element_id: PydObjectId,
        twin_id: UUID4,
        tenant_id: Optional[PydObjectId] = None,
        ts: datetime = datetime.now(timezone.utc),
    ) -> PydObjectId:
        with self._queue_lock:
            if self.logs_queue.qsize() >= self.max_logs:
                try:
                    self.logs_queue.get_nowait()  # removing the oldest item
                except queue.Empty:  # should never happen
                    pass

            self.logs_queue.put(
                item=Log(
                    element_id=element_id, twin_id=twin_id, log=log, tenant_id=tenant_id, ts=ts
                )
            )

    def stop(self) -> None:
        self._stop_event.set()

        with self._worker_lock:
            self._worker_lock.notify_all()

        with contextlib.suppress(AttributeError):
            with self._worker_lock:
                for thread in self.worker_threads:
                    with contextlib.suppress(RuntimeError):
                        thread.join()
                self.worker_threads.clear()
