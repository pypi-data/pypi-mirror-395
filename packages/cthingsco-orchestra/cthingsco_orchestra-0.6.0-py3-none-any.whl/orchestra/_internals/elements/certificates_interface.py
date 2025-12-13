from typing import Optional

import grpc
from google.protobuf import empty_pb2

import orchestra._internals.common.models.exceptions as exceptions
from orchestra._internals.rpc.orchestra import certificates_pb2
from orchestra._internals.rpc.orchestra import certificates_pb2_grpc
from orchestra._internals.rpc.orchestra import certificates_public_pb2
from orchestra._internals.rpc.orchestra import certificates_public_pb2_grpc
from orchestra.timeout import TIMEOUT, handle_deadline


class OrchestraCertificatesInterface:

    def __init__(
        self,
        channel: grpc.Channel,
        public_channel: grpc.Channel,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ):
        self.certificates_public_stub = certificates_public_pb2_grpc.CertificatesPublicServiceStub(
            public_channel
        )
        self.certificates_stub: Optional[certificates_pb2_grpc.CertificatesServiceStub] = None
        if channel:
            self.certificates_stub = certificates_pb2_grpc.CertificatesServiceStub(channel)
        self.compression: grpc.Compression = compression

    @handle_deadline
    def sign(self, csr_pem: str, token: str) -> certificates_public_pb2.CertificateSignResponse:
        try:
            response: certificates_public_pb2.CertificateSignResponse = (
                self.certificates_public_stub.Sign(
                    certificates_public_pb2.CertificateSignRequest(
                        csr_pem=csr_pem,
                        token=token,
                    ),
                    timeout=TIMEOUT,
                    compression=self.compression,
                )
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            elif e.code() == grpc.StatusCode.INTERNAL:
                raise exceptions.InternalError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return response

    @handle_deadline
    def revoke(self, certificate_pem: str) -> empty_pb2.Empty():
        try:
            certificates_pb2.CertificateRevokeRequest = self.certificates_stub.Revoke(
                certificates_pb2.CertificateRevokeRequest(
                    certificate_pem=certificate_pem,
                ),
                timeout=TIMEOUT,
                compression=self.compression,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise exceptions.InvalidData(e.details())
            elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError(e.details())
            else:
                raise exceptions.UnavailableError(
                    f"Orchestra Communications Server unavailable: {e}"
                )

        return empty_pb2.Empty()
