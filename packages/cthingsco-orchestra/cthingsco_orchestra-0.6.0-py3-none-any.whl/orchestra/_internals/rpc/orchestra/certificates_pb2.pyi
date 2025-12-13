from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateRevokeRequest(_message.Message):
    __slots__ = ("certificate_pem",)
    CERTIFICATE_PEM_FIELD_NUMBER: _ClassVar[int]
    certificate_pem: str
    def __init__(self, certificate_pem: _Optional[str] = ...) -> None: ...
