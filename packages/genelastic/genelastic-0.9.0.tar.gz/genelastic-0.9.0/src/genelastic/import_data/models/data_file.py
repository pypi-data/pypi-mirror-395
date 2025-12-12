"""This module defines the DataFile class, which handles the representation,
management, and extraction of metadata for a data file within a data bundle.

It includes functionality to construct DataFile instances from paths and
optional filename patterns, retrieve file paths and metadata, and support
for extracting metadata from filenames using specified patterns.
"""

import logging
from pathlib import Path
from types import NotImplementedType

from genelastic.common.types import Metadata
from genelastic.import_data.patterns import MetricsPattern

logger = logging.getLogger("genelastic")


class DataFile:
    """Class for handling a data file and its metadata."""

    def __init__(
        self,
        analysis_id: str,
        path: Path,
        bundle_file: Path,
        metadata: Metadata,
    ) -> None:
        self._analysis_id = analysis_id
        self._path = path
        self._bundle_file = bundle_file
        self._metadata = metadata
        self._metrics = MetricsPattern.extract_metadata(path)
        self._validate_params()

        self._ext = str(self._metadata["ext"]).lower()

        key = "type" if self._metrics is not None else "ext"
        self._type = str(self._metadata[key]).lower()

    def __eq__(self, other: object) -> bool | NotImplementedType:
        """Defines equality comparison for DataFile instances based on their
        file path.
        """
        if isinstance(other, DataFile):
            return self._path == other._path
        return NotImplemented

    def __hash__(self) -> int:
        """Defines hash behavior for DataFile to allow use in sets and as dict keys."""
        return hash(self._path)

    def _validate_params(self) -> None:
        """Validate values of some ``DataFile`` constructor parameters.

        :raises RuntimeError: One of the parameters value is invalid.
        """
        if "ext" not in self._metadata:
            msg = (
                f"Data file '{self._path}' "
                f"is missing the required metadata key 'ext'."
            )
            raise RuntimeError(msg)

        if self._metrics is not None and "type" not in self._metadata:
            msg = (
                f"Metrics data file '{self._path}' "
                f"is missing the required metadata key 'type'."
            )
            raise RuntimeError(msg)

    @property
    def analysis_id(self) -> str:
        """Get the analysis ID."""
        return self._analysis_id

    @property
    def path(self) -> Path:
        """Retrieve the data file path."""
        return self._path

    @property
    def ext(self) -> str:
        """Retrieve the data file extension."""
        return self._ext

    @property
    def type(self) -> str:
        """Retrieve the data file type.

        Normally, the type is the file's extension.
        If the file is a metrics file, its type is taken from the metadata key
        'type'.
        """
        return self._type

    @property
    def bundle_file(self) -> Path:
        """Retrieve the path to the associated data bundle file."""
        return self._bundle_file

    @property
    def metadata(self) -> Metadata:
        """Retrieve a copy of the metadata associated with the data file."""
        return self._metadata.copy()

    @property
    def metrics(self) -> list[dict[str, str]] | None:
        """Retrieve a copy of the metrics associated with the data file."""
        return self._metrics
