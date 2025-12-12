"""Exceptions for Vemmio."""


class VemmioError(Exception):
    """Generic Vemmio exception."""


class VemmioEmptyResponseError(Exception):
    """Vemmio empty API response exception."""


class VemmioConnectionError(VemmioError):
    """Vemmio connection exception."""


class VemmioConnectionTimeoutError(VemmioConnectionError):
    """Vemmio connection Timeout exception."""


class VemmioConnectionClosedError(VemmioConnectionError):
    """Vemmio WebSocket connection has been closed."""


class VemmioUnsupportedVersionError(VemmioError):
    """Vemmio version is unsupported."""


class VemmioUpgradeError(VemmioError):
    """Vemmio upgrade exception."""