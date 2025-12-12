import logging
import typing
from pathlib import Path

from genelastic.common.types import BundleDict
from genelastic.import_data.collect import (
    extract_analysis_metadata,
)
from genelastic.import_data.models.analysis import Analysis
from genelastic.import_data.models.data_file import DataFile
from genelastic.import_data.models.unique_list import UniqueList
from genelastic.import_data.resolve import (
    resolve_filename_pattern,
    validate_file_prefix,
)

logger = logging.getLogger("genelastic")


class Analyses(UniqueList[Analysis]):
    """Container of Analysis objects."""

    def get_data_files(self, ext: str | None = None) -> list[DataFile]:
        """Returns matched files as DataFile objects across all analyses.

        :param ext: Filter the list of matched files by their extension
            (case-sensitive).
        """
        return [df for a in self for df in a.get_data_files(ext=ext)]

    @property
    def extensions(self) -> set[str]:
        """Returns all matched files extensions across all analyses."""
        return {ext for a in self for ext in a.extensions}

    @property
    def matched_files(self) -> set[Path]:
        """Returns the number of files that matched the pattern across all
        analyses.
        """
        return {f for a in self for f in a.matched_files}

    @property
    def unmatched_files(self) -> set[Path]:
        """Return the set of files that were not matched by any analysis.

        The behavior differs depending on whether analyses share the same
        ``data_path``:

        - Within the same directory: a file is considered unmatched only if
            **all** analyses in that directory failed to match it. This is
            computed as the intersection of their respective ``unmatched_files``
            sets.

        - Across different directories: unmatched files are simply aggregated
            (union of sets), since each directory is independent.

        :return: A set of paths corresponding to unmatched files across all
            analyses.
        """
        unmatched_per_dir: dict[Path, set[Path]] = {}

        for a in self:
            try:
                unmatched_per_dir[a.data_path] = set.intersection(
                    unmatched_per_dir[a.data_path], a.unmatched_files
                )
            except KeyError:
                unmatched_per_dir[a.data_path] = a.unmatched_files

        if not unmatched_per_dir.values():
            return set()
        return set.union(*unmatched_per_dir.values())

    @classmethod
    def from_dict(cls, bundle: BundleDict) -> typing.Self:
        """Initialize an ``Analyses`` container from a single bundle dictionary.

        Expected bundle keys:

        - Mandatory: ``file_prefix``, ``tags``, ``bundle_file``, ``data_path``.
        - Optional: ``multi_match`` (default: ``False``), ``suffix`` (default: ``None``).

        :param bundle: A dictionary describing one analysis configuration.
        :raises InvalidFilePrefixError: If the ``file_prefix`` is invalid.
        :raises FilenamePatternResolveError: If ``multi_match=False`` and some
            tag fields are missing from the bundle metadata.
        :raises UniqueListDuplicateError: If two ``Analysis`` objects happens
            to share the same ID inside the ``Analyses`` instance.
        :raises DataFileCollectorError: If the ``data_path`` is not an existing
            directory or if metadata extraction or instantiation of a data file
            objet fails for a given file.
        :return: An ``Analyses`` instance containing one or several
            ``Analysis`` objects.
        """
        analyses = cls()

        # Validate file prefix structure.
        logger.info("- Validating file prefix '%s'...", bundle["file_prefix"])
        validate_file_prefix(
            file_prefix=bundle["file_prefix"], tags=bundle["tags"]
        )

        # Resolve the filename pattern. In multi-match mode, tags without
        # metadata values are accepted. They will be resolved later from
        # filename-extracted metadata. In single-match mode, a
        # FilenamePatternResolveError exception will be raised.
        strict_mode = not bool(bundle.get("multi_match"))
        logger.info(
            "- Resolving filename pattern in %s mode...",
            "strict" if strict_mode else "non-strict",
        )
        filename_pattern = resolve_filename_pattern(
            file_prefix=bundle["file_prefix"],
            tags=bundle["tags"],
            metadata=bundle,
            suffix=bundle.get("suffix"),
            strict=strict_mode,
        )

        # Scan the data path to extract metadata from filenames.
        logger.info(
            "- Collecting files to extract metadata from using the resolved "
            "filename pattern."
        )
        extracted_metadata = extract_analysis_metadata(
            data_path=bundle["data_path"],
            file_prefix=bundle["file_prefix"],
            tags=bundle["tags"],
            filename_pattern=filename_pattern,
        )

        logger.info(
            "- Extracted metadata from %d analysis(es): %s",
            len(extracted_metadata.keys()),
            ", ".join(extracted_metadata.keys()),
        )

        for analysis_id, metadata in extracted_metadata.items():
            # For each file match, merge filename-extracted metadata with the
            # original bundle to describe one analysis.
            full_metadata = {**bundle, **metadata}
            full_metadata["analysis_id"] = analysis_id

            # Re-resolve filename pattern in strict mode to let the analysis
            # collect its own files (all tags should now be defined).
            full_metadata["filename_pattern"] = resolve_filename_pattern(
                file_prefix=full_metadata["file_prefix"],
                tags=full_metadata["tags"],
                metadata=full_metadata,
                suffix=full_metadata.get("suffix"),
                strict=True,
            )

            # Instantiate the Analysis and add it to the container.
            analyses.append(Analysis(**full_metadata))
            logger.info("")

        return analyses

    @classmethod
    def from_dicts(cls, arr: typing.Sequence[BundleDict]) -> typing.Self:
        """Initialize an ``Analyses`` container from multiple bundle
        dictionaries.

        This is a convenience wrapper that calls ``from_dict`` for each
        bundle in the sequence and concatenates the results.

        :param arr: A sequence of bundle dictionaries.
        :return: An ``Analyses`` instance containing all analyses from the
            input bundles.
        """
        analyses = cls()

        for bundle in arr:
            analyses.extend(analyses.from_dict(bundle))

        return analyses
