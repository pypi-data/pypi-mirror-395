from typing import Protocol


class CheckerObserver(Protocol):
    """Protocol for classes observing Checker events."""

    def notify_missing(self, label: str, missing: list[str]) -> None:
        """Called when expected IDs are missing in Elasticsearch."""
        ...

    def notify_extra(self, label: str, extra: list[str]) -> None:
        """Called when unexpected IDs exist in Elasticsearch."""
        ...
