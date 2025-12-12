import typing
from collections import UserList
from typing import SupportsIndex

from genelastic.common.exceptions import UniqueListDuplicateError

T = typing.TypeVar("T")


class UniqueList(UserList[T]):
    """A list that only allows unique elements.

    :param init_list: Optional iterable to initialize the list.
    """

    def __init__(self, init_list: typing.Iterable[T] | None = None) -> None:
        super().__init__()

        if init_list:
            for item in init_list:
                self._ensure_unique(item)
                super().append(item)

    def __setitem__(
        self, i: SupportsIndex | slice, item: T | typing.Iterable[T]
    ) -> None:
        if isinstance(i, slice):
            if not isinstance(item, typing.Iterable):
                msg = "Expected iterable for slice assignment."
                raise TypeError(msg)

            slice_dupes = self._find_dupes(item)
            if slice_dupes:
                formatted_dupes = [str(dupe) for dupe in slice_dupes]
                msg = (
                    f"Duplicate item(s) in slice assignment: "
                    f"{', '.join(formatted_dupes)}."
                )
                raise UniqueListDuplicateError(msg)
            for x in item:
                if x in self and x not in self[i]:
                    msg = f"Duplicate item: {x}."
                    raise UniqueListDuplicateError(msg)
            super().__setitem__(i, item)
        else:
            self._ensure_unique(typing.cast(T, item))
            super().__setitem__(i, typing.cast(T, item))

    def __add__(self, other: typing.Iterable[T]) -> "UniqueList[T]":
        for item in other:
            self._ensure_unique(item)
        return UniqueList(super().__add__(other))

    def __iadd__(self, other: typing.Iterable[T]) -> typing.Self:
        for item in other:
            self._ensure_unique(item)
        return super().__iadd__(other)

    def __mul__(self, n: int) -> typing.Self:
        raise NotImplementedError

    def __imul__(self, n: int) -> typing.Self:
        raise NotImplementedError

    @staticmethod
    def _find_dupes(a: typing.Iterable[T]) -> list[T]:
        seen = set()
        dupes = []
        for x in a:
            if x in seen:
                dupes.append(x)
            else:
                seen.add(x)
        return dupes

    def _ensure_unique(self, item: T) -> None:
        if item in self:
            msg = f"Duplicate item: {item}."
            raise UniqueListDuplicateError(msg)

    def append(self, item: T) -> None:
        """Appends a unique item to the end of the list.

        :param item: Element to append.
        :raises UniqueListError: If the item already exists in the list.
        """
        self._ensure_unique(item)
        super().append(item)

    def insert(self, i: int, item: T) -> None:
        """Inserts a unique item at a specified position.

        :param i: Index where the item should be inserted.
        :param item: Element to insert.
        :raises UniqueListError: If the item already exists in the list.
        """
        self._ensure_unique(item)
        super().insert(i, item)

    def extend(self, other: typing.Iterable[T]) -> None:
        """Extends the list with unique elements from another iterable.

        :param other: Iterable of elements to add.
        :raises UniqueListError: If any element in the iterable already exists in
            the list.
        """
        for item in other:
            self._ensure_unique(item)
        super().extend(other)
