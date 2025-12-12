import copy
from abc import ABC
from typing import Any


class Process(ABC):  # noqa: B024
    """Abstract base class for a Process.

    It is not intended to be instantiated directly. Instead, use one of its
    subclasses, ``WetProcess`` or ``BioInfoProcess``.
    """

    def __init__(
        self,
        proc_id: str,
        bundle_file: str | None = None,
        **data: Any,  # noqa: ANN401
    ) -> None:
        self._proc_id = proc_id
        self._bundle_file = bundle_file
        self._data = data
        self._type = self.__class__.__name__

    @property
    def id(self) -> str:
        """Unique identifier of the process."""
        return self._proc_id

    @property
    def data(self) -> dict[str, Any]:
        """Return a copy of the associated data."""
        return copy.deepcopy(self._data)

    @property
    def type(self) -> str:
        """Type of the process."""
        return self._type


class WetProcess(Process):
    """Concrete wet lab process."""


class BioInfoProcess(Process):
    """Concrete bioinformatics process."""
