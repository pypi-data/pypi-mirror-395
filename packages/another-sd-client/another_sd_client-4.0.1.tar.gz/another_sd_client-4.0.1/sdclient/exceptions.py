from types import MappingProxyType
from typing import Any


class SDCallError(Exception):
    def __init__(self, message: str, error: dict[str, Any] | None = None) -> None:
        super().__init__()
        self._message = message
        self.error = MappingProxyType(error) if error is not None else None

    def __str__(self) -> str:
        return self._message

    @property
    def message(self) -> str:
        return self._message


class SDParseResponseError(SDCallError):
    pass


class SDRootElementNotFound(SDCallError):
    pass


class SDParentNotFound(Exception):
    pass


class SDEmploymentNotFound(Exception):
    pass
