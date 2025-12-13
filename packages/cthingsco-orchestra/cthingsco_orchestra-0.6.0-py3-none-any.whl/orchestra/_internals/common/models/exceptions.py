class NotFoundError(Exception):
    pass


class TwinAtomicSetError(Exception):
    pass


class TwinRequestNoLongerValid(Exception):
    pass


class Etcd3ConnectionError(Exception):
    pass


class UnavailableError(Exception):
    pass


class InvalidData(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


class InternalError(Exception):
    pass
