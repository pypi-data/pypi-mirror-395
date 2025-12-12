import logging
import typing
from collections import UserDict
from typing import Self

from genelastic.common.types import BundleDict
from genelastic.import_data.models.process import (
    Process,
)

logger = logging.getLogger("genelastic")


class Processes(UserDict[str, Process]):
    """Container for homogeneous Process objects.

    Unlike a standard dict:
      - Only subclasses of ``Process`` are allowed as values.
      - All items must be of the same concrete subclass of ``Process``.
      - Duplicate keys are not allowed and will raise an exception.

    :ivar _item_type: Internal attribute storing the concrete subclass
        of ``Process`` enforced in this container.
    """

    _item_type: type | None = None

    def __setitem__(self, key: str, value: Process) -> None:
        if not isinstance(value, Process):
            msg = (
                "Object type not supported. "
                "Container only supports 'Process' subclasses as items."
            )
            raise TypeError(msg)

        if self._item_type is None:
            self._item_type = type(value)
        elif not isinstance(value, self._item_type):
            msg = (
                f"Cannot mix types. Container already holds "
                f"{self._item_type.__name__} items."
            )
            raise TypeError(msg)

        if key in self:
            msg = (
                f"Duplicate key. "
                f"Container already holds an item with key '{key}'."
            )
            raise ValueError(msg)

        super().__setitem__(key, value)

    def add(self, item: Process) -> None:
        """Add one process item to the container.

        :raises TypeError: If ``item`` is not a subclass of ``Process``,
            or if it does not match the subclass type of items already in the
            container.
        :raises ValueError: If an item with the same key (``item.id``) already
            exists in the container.
        """
        self[item.id] = item

    @classmethod
    def from_dicts(
        cls, arr: typing.Sequence[BundleDict], process_cls: type[Process]
    ) -> Self:
        """Build a Processes container instance from a sequence of dictionaries.

        :param arr: Sequence of dictionaries representing process data.
        :param process_cls: The subclass of ``Process`` to instantiate for each
            dict.
        :raises TypeError: If instantiating ``process_cls`` fails due to invalid
                dictionary arguments, or if the resulting object type does not
                match the container's enforced type.
        :raises ValueError: If two or more dictionaries yield items with the
            same key (``id``), leading to duplicate entries in the container.
        :return: A Processes container instance populated with process objects.
        """
        instance = cls()
        for d in arr:
            instance.add(process_cls(**d))
        return instance
