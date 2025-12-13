from typing import Optional

import grpc

from orchestra._internals.elements.grpc import GRPC_HTTP2_MAX_PINGS_WITHOUT_DATA
from orchestra._internals.elements.grpc import GRPC_KEEPALIVE_PERMIT_WITHOUT_CALLS
from orchestra._internals.elements.grpc import GRPC_KEEPALIVE_TIME_MS
from orchestra._internals.elements.grpc import GRPC_KEEPALIVE_TIMEOUT_MS
from orchestra._internals.elements.grpc import GRPC_MAX_MESSAGE_LENGTH

GRPC_OPTIONS = [
    ("grpc.max_send_message_length", GRPC_MAX_MESSAGE_LENGTH),
    ("grpc.max_receive_message_length", GRPC_MAX_MESSAGE_LENGTH),
    ("grpc.keepalive_time_ms", GRPC_KEEPALIVE_TIME_MS),
    ("grpc.keepalive_timeout_ms", GRPC_KEEPALIVE_TIMEOUT_MS),
    ("grpc.keepalive_permit_without_calls", GRPC_KEEPALIVE_PERMIT_WITHOUT_CALLS),
    ("grpc.http2.max_pings_without_data", GRPC_HTTP2_MAX_PINGS_WITHOUT_DATA),
]


class OrchestraCredentials:
    def __init__(
        self,
        url: str,
        public_url: str,
        root_certificate: bytes,
        certificate_key: Optional[bytes] = None,
        certificate: Optional[bytes] = None,
    ):
        self.channel: Optional[grpc.Channel] = None
        if certificate_key and certificate:
            self.channel: grpc.Channel = grpc.secure_channel(
                url,
                grpc.ssl_channel_credentials(
                    root_certificates=root_certificate,
                    private_key=certificate_key,
                    certificate_chain=certificate,
                ),
                options=GRPC_OPTIONS,
            )
        self.public_channel: grpc.Channel = grpc.secure_channel(
            public_url,
            grpc.ssl_channel_credentials(root_certificates=root_certificate),
            options=GRPC_OPTIONS,
        )

    @staticmethod
    def from_files(
        url: str,
        public_url: str,
        root_certificate_path: str,
        certificate_key_path: Optional[str] = None,
        certificate_path: Optional[str] = None,
    ):
        with open(root_certificate_path, "rb") as f:
            root_certificate = f.read()
        certificate_key = None
        if certificate_key_path:
            with open(certificate_key_path, "rb") as f:
                certificate_key = f.read()
        certificate = None
        if certificate_path:
            with open(certificate_path, "rb") as f:
                certificate = f.read()
        return OrchestraCredentials(
            url=url,
            public_url=public_url,
            root_certificate=root_certificate,
            certificate_key=certificate_key,
            certificate=certificate,
        )


class AsyncOrchestraCredentials(OrchestraCredentials):
    def __init__(
        self,
        url: str,
        public_url: str,
        root_certificate: bytes,
        certificate_key: Optional[bytes] = None,
        certificate: Optional[bytes] = None,
    ):
        self.channel: Optional[grpc.aio.Channel] = None
        if certificate_key and certificate:
            self.channel: grpc.aio.Channel = grpc.aio.secure_channel(
                url,
                grpc.ssl_channel_credentials(
                    root_certificates=root_certificate,
                    private_key=certificate_key,
                    certificate_chain=certificate,
                ),
                options=GRPC_OPTIONS,
            )
        self.public_channel: grpc.aio.Channel = grpc.aio.secure_channel(
            public_url,
            grpc.ssl_channel_credentials(root_certificates=root_certificate),
            options=GRPC_OPTIONS,
        )

    @staticmethod
    def from_files(
        url: str,
        public_url: str,
        root_certificate_path: str,
        certificate_key_path: Optional[str] = None,
        certificate_path: Optional[str] = None,
    ):
        with open(root_certificate_path, "rb") as f:
            root_certificate = f.read()
        certificate_key = None
        if certificate_key_path:
            with open(certificate_key_path, "rb") as f:
                certificate_key = f.read()
        certificate = None
        if certificate_path:
            with open(certificate_path, "rb") as f:
                certificate = f.read()
        return AsyncOrchestraCredentials(
            url=url,
            public_url=public_url,
            root_certificate=root_certificate,
            certificate_key=certificate_key,
            certificate=certificate,
        )
