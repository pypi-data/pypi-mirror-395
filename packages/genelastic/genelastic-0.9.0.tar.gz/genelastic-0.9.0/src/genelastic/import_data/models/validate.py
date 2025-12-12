from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationIssue:
    """Contains context about a bundle validation issue."""

    exc_type: str
    file_path: Path
    file_index: int
    file_count: int
    doc_index: int | None = None
    doc_count: int | None = None

    def __str__(self) -> str:
        if not self.doc_index:
            return (
                f"[{self.exc_type}] "
                f"File {self.file_index}/{self.file_count}: {self.file_path}"
            )
        return (
            f"[{self.exc_type}] "
            f"File {self.file_index}/{self.file_count}: {self.file_path} "
            f"(in doc #{self.doc_index}/{self.doc_count})"
        )
