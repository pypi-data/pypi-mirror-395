from orchestra._internals.common.models.basemodels import RWModel
from orchestra._internals.rpc.orchestra import certificates_public_pb2


class CertificateSigned(RWModel):
    certificate_pem: str
    certificate_chain_pem: str
    ca_pem: str
    issuing_ca_pem: str

    @classmethod
    def from_protobuf_model(cls, proto: certificates_public_pb2.CertificateSignResponse):
        return cls(
            certificate_pem=proto.certificate_pem,
            certificate_chain_pem=proto.certificate_chain_pem,
            ca_pem=proto.ca_pem,
            issuing_ca_pem=proto.issuing_ca_pem,
        )
