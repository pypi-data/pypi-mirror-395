import contextlib
import copy
import logging
from collections import defaultdict
from pathlib import Path
from types import NotImplementedType

from genelastic.common.types import Metadata
from genelastic.import_data.collect import (
    DataFileCollector,
)
from genelastic.import_data.constants import (
    ALLOWED_EXTENSIONS,
)
from genelastic.import_data.models.data_file import DataFile
from genelastic.import_data.patterns import FilenamePattern

logger = logging.getLogger("genelastic")


class Analysis:
    """Class Analysis that represents an analysis."""

    METADATA_INTERNAL_KEYS = frozenset(
        ["tags", "multi_match", "ext", "file_prefix"]
    )

    def __init__(
        self,
        analysis_id: str,
        bundle_file: Path,
        data_path: Path,
        filename_pattern: FilenamePattern,
        **metadata: str | int,
    ) -> None:
        self._analysis_id = analysis_id
        self._bundle_file = bundle_file
        self._data_path = data_path
        self._metadata = self._remove_internal_keys(metadata)
        self._data_files_by_ext: dict[str, set[DataFile]] = defaultdict(set)

        logger.info("")
        logger.info("[ Analysis ID %s ]", self._analysis_id)

        self._collected_files = DataFileCollector(
            analysis_id,
            bundle_file,
            data_path,
            filename_pattern,
        ).run()

        for data_file in self._collected_files.data_files:
            self._data_files_by_ext[data_file.ext].add(data_file)

        logger.info(
            " -> Extracted %s file extension(s): %s.",
            len(self._data_files_by_ext.keys()),
            ", ".join(ext.upper() for ext in self._data_files_by_ext),
        )

    def __eq__(self, other: object) -> bool | NotImplementedType:
        """Defines equality comparison for Analysis instances based on their
        ID.
        """
        if isinstance(other, Analysis):
            return self._analysis_id == other._analysis_id
        return NotImplemented

    def __lt__(self, other: object) -> bool | NotImplementedType:
        """Defines sort order for Analysis instances based on their ID."""
        if isinstance(other, Analysis):
            return self._analysis_id < other._analysis_id
        return NotImplemented

    def __str__(self) -> str:
        return (
            f"Analysis(id='{self._analysis_id}', "
            f"bundle_file='{self._bundle_file}', "
            f"data_path='{self._data_path}', "
            f"metadata={self._metadata})"
        )

    @staticmethod
    def _remove_internal_keys(
        metadata: Metadata,
    ) -> Metadata:
        updated_metadata = metadata.copy()

        for key in Analysis.METADATA_INTERNAL_KEYS:
            with contextlib.suppress(KeyError):
                del updated_metadata[key]

        return updated_metadata

    @property
    def metadata(self) -> Metadata:
        """Get metadata."""
        return copy.deepcopy(self._metadata)

    @property
    def bundle_file(self) -> Path:
        """Get the bundle file."""
        return self._bundle_file

    @property
    def data_path(self) -> Path:
        """Get the data path specified in the bundle file."""
        return self._data_path

    @property
    def id(self) -> str:
        """Get the analysis ID."""
        return self._analysis_id

    @property
    def matched_files(self) -> set[Path]:
        """Returns the list of files that matched the filename pattern."""
        return self._collected_files.matched_files

    @property
    def unmatched_files(self) -> set[Path]:
        """Returns the list of files that did not match the filename pattern."""
        return self._collected_files.unmatched_files

    @property
    def extensions(self) -> set[str]:
        """Returns all the matched files extensions."""
        return set(self._data_files_by_ext.keys())

    def get_data_files(self, ext: str | None = None) -> set[DataFile]:
        """Returns the list of matched files as DataFile objects.

        :param ext: Filter the list of matched files by their extension
            (case-sensitive).
        """
        if ext:
            if ext not in ALLOWED_EXTENSIONS:
                msg = f"Unsupported extension {ext}."
                raise ValueError(msg)

            if ext in self._data_files_by_ext:
                return self._data_files_by_ext[ext]
            return set()
        return {f for value in self._data_files_by_ext.values() for f in value}
