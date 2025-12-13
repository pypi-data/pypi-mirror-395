import grpc

from orchestra._internals.elements.certificates_interface import OrchestraCertificatesInterface
from orchestra.elements.credentials import OrchestraCredentials
from orchestra.elements.models.certificate import CertificateSigned


class OrchestraCertificateClient:
    """
    Provides support for signing and revoking certificates
    """

    def __init__(
        self,
        credentials: OrchestraCredentials,
        compression: grpc.Compression = grpc.Compression.Gzip,
    ) -> None:
        self.channel = credentials.channel
        self.public_channel = credentials.public_channel
        self.certificates_iface = OrchestraCertificatesInterface(
            channel=self.channel,
            public_channel=self.public_channel,
            compression=compression,
        )

    def sign(self, csr_pem: str, token: str) -> CertificateSigned:
        return CertificateSigned.from_protobuf_model(
            self.certificates_iface.sign(
                csr_pem=csr_pem,
                token=token,
            )
        )

    def revoke(self, certificate_pem: str) -> None:
        self.certificates_iface.revoke(
            certificate_pem=certificate_pem,
        )
