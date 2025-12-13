from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateSignRequest(_message.Message):
    __slots__ = ("csr_pem", "token")
    CSR_PEM_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    csr_pem: str
    token: str
    def __init__(self, csr_pem: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class CertificateSignResponse(_message.Message):
    __slots__ = ("certificate_pem", "certificate_chain_pem", "ca_pem", "issuing_ca_pem")
    CERTIFICATE_PEM_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_CHAIN_PEM_FIELD_NUMBER: _ClassVar[int]
    CA_PEM_FIELD_NUMBER: _ClassVar[int]
    ISSUING_CA_PEM_FIELD_NUMBER: _ClassVar[int]
    certificate_pem: str
    certificate_chain_pem: str
    ca_pem: str
    issuing_ca_pem: str
    def __init__(
        self,
        certificate_pem: _Optional[str] = ...,
        certificate_chain_pem: _Optional[str] = ...,
        ca_pem: _Optional[str] = ...,
        issuing_ca_pem: _Optional[str] = ...,
    ) -> None: ...
