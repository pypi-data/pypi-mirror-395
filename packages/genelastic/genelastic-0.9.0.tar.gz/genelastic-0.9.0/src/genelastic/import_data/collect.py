import logging
from dataclasses import dataclass
from pathlib import Path

from genelastic.common.exceptions import DataFileCollectorError
from genelastic.common.types import Metadata
from genelastic.import_data.models.data_file import DataFile
from genelastic.import_data.models.tags import Tags
from genelastic.import_data.patterns import FilenamePattern
from genelastic.import_data.resolve import resolve_analysis_id

logger = logging.getLogger("genelastic")


def collect_files(data_path: Path) -> set[Path]:
    """Collect files for a given analysis.
    All files directly under ``data_path`` are returned.

    :param data_path: Directory containing the files.
    :raises DataFileCollectorError: If ``data_path`` is not an existing
        directory.
    :return: Set of absolute paths to collected files.
    """
    try:
        collected_files = {x for x in data_path.iterdir() if x.is_file()}
    except OSError as e:
        msg = f"Error collecting files: data directory is invalid. {e}."
        raise DataFileCollectorError(msg) from e
    return collected_files


def match_files(
    files: set[Path],
    filename_pattern: FilenamePattern,
) -> tuple[set[Path], set[Path]]:
    """Splits a set of files into those that match a given filename pattern and
    those that don't.

    This function applies the provided ``filename_pattern`` to each file name
    in ``files``, and returns two sets: one containing files that match the
    pattern, and one containing those that do not.

    :param files: A set of file paths to check.
    :param filename_pattern: The filename pattern used for matching.

    :returns: A tuple containing in first position a set of files that match
      the pattern, and in second position a set of files that do not match the
      pattern.
    """
    matched_files = {
        f for f in files if filename_pattern.matches_pattern(f.name)
    }
    return matched_files, files - matched_files


def extract_analysis_metadata(
    data_path: Path,
    file_prefix: str,
    tags: Tags,
    filename_pattern: FilenamePattern,
) -> dict[str, Metadata]:
    analysis = {}

    for file in collect_files(data_path):
        if not filename_pattern.matches_pattern(file.name):
            logger.debug("File '%s' was not matched.", file.name)
            continue

        filename_metadata = filename_pattern.extract_metadata(file.name)
        analysis_id = resolve_analysis_id(file_prefix, tags, filename_metadata)
        analysis[analysis_id] = filename_metadata

    return analysis


def init_data_files(
    analysis_id: str,
    files: set[Path],
    filename_pattern: FilenamePattern,
    bundle_file: Path,
) -> set[DataFile]:
    """Instantiate ``DataFile`` objects from a set of file paths associated
    with an analysis.

    :param analysis_id: ID of the analysis, shared by all created ``DataFile``
      instances.
    :param files: Set of file paths associated with the analysis.
    :param filename_pattern: Pattern used to extract metadata from filenames.
      The extracted metadata is included in each ``DataFile``.
    :param bundle_file: Path to the YAML bundle file from which the analysis is
      defined.
    :raises DataFileCollectorError: If metadata extraction or instantiation
        of a data file objet fails for a given file.
    :return: A set of successfully instantiated ``DataFile`` objects.
    """
    data_files = set()
    for file in files:
        try:
            metadata = filename_pattern.extract_metadata(file.name)
            data_file = DataFile(
                analysis_id=analysis_id,
                path=file,
                bundle_file=bundle_file,
                metadata=metadata,
            )
            data_files.add(data_file)
        except RuntimeError as e:
            msg = f"Error instantiating data files: {e}"
            raise DataFileCollectorError(msg) from None
    return data_files


@dataclass(frozen=True)
class DataFileCollectorResult:
    """Result of a data file collection."""

    matched_files: set[Path]
    unmatched_files: set[Path]
    data_files: set[DataFile]


class DataFileCollector:
    """Collect all data files belonging to an analysis."""

    def __init__(
        self,
        analysis_id: str,
        bundle_file: Path,
        data_path: Path,
        filename_pattern: FilenamePattern,
        *,
        multi_match: bool = False,
    ) -> None:
        self._analysis_id = analysis_id
        self._bundle_file = bundle_file
        self._data_path = data_path
        self._filename_pattern = filename_pattern
        self._multi_match = multi_match

    def run(self) -> DataFileCollectorResult:
        """Collects files from the analysis data path, matches them against the
        analysis filename pattern, and instantiates ``DataFile`` objects for
        each matched file.

        :raises DataFileCollectorError: If the ``data_path`` is not an existing
            directory or if metadata extraction or instantiation of a data file
            objet fails for a given file.
        :return: A ``DataFileCollectorResult`` containing the sets of matched
            and unmatched files, as well as a set of instantiated ``DataFile``
            objects.
        """
        files = collect_files(self._data_path)
        logger.debug(
            " -> Collected %s file(s):",
            len(files),
        )
        for path in sorted(files):
            logger.debug("  - '%s'", path.name)

        matched_files, unmatched_files = match_files(
            files, self._filename_pattern
        )
        logger.info(" -> Found %s matching file(s):", len(matched_files))
        for path in sorted(matched_files):
            logger.info("  - '%s'", path.name)

        logger.info(
            " -> Found %s non-matching file(s):",
            len(unmatched_files),
        )
        for path in sorted(unmatched_files):
            logger.info("  - '%s'", path.name)

        data_files = init_data_files(
            self._analysis_id,
            matched_files,
            self._filename_pattern,
            self._bundle_file,
        )

        return DataFileCollectorResult(
            matched_files=matched_files,
            unmatched_files=unmatched_files,
            data_files=data_files,
        )
