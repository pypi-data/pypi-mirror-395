"""Module: import_bundle

This module provides functionality for importing data bundles.
"""

import logging
import sys
import typing
from pathlib import Path

from genelastic.common.cli import log_subsection
from genelastic.common.types import BundleDict
from genelastic.import_data.models.analyses import Analyses
from genelastic.import_data.models.process import BioInfoProcess, WetProcess
from genelastic.import_data.models.processes import Processes
from genelastic.import_data.models.tags import Tags

logger = logging.getLogger("genelastic")


def resolve_data_path(bundle_file: Path, data_path: Path | None) -> Path:
    """Resolves the data path relative to the given bundle file if necessary.

    If ``data_path`` is:

    - Absolute: it is returned as-is,
    - Relative: it is resolved relative to the parent of ``bundle_file``,
    - None: considered as the current directory (``.``) and resolved
      accordingly.

    :param bundle_file: Path to the bundle file used for resolution context.
    :param data_path: Optional path to the data directory or file.
    :return: An absolute Path object pointing to the resolved data location.
    """
    resolved_data_path = data_path if data_path else Path()
    if not resolved_data_path.is_absolute():
        resolved_data_path = Path(
            bundle_file.parent / resolved_data_path
        ).resolve()
    return resolved_data_path


class ImportBundle:
    """Class for handling an import bundle description."""

    def __init__(
        self,
        x: typing.Sequence[BundleDict],
        *,
        multi_match: bool = False,
        check: bool = False,
    ) -> None:
        self._documents = x
        self._custom_tags_doc: (
            dict[str, dict[str, str | dict[str, str]]] | None
        ) = None

        analyses: list[BundleDict] = []
        wet_processes: list[BundleDict] = []
        bi_processes: list[BundleDict] = []

        self._search_custom_tags()
        tags = (
            Tags.from_dict(self._custom_tags_doc)
            if self._custom_tags_doc
            else Tags()
        )

        # Loop on dicts
        for d in x:
            # Gather all analyses
            if "analyses" in d and d["analyses"] is not None:
                # Copy some bundle properties into each analysis
                for analysis in d["analyses"]:
                    bundle_file = d["bundle_file"]

                    analysis["bundle_file"] = bundle_file
                    analysis["tags"] = tags
                    analysis["multi_match"] = multi_match

                    # Resolve data path
                    data_path = (
                        Path(analysis["data_path"])
                        if "data_path" in analysis
                        else None
                    )
                    analysis["data_path"] = resolve_data_path(
                        bundle_file, data_path
                    )
                analyses.extend(d["analyses"])

            # If some wet processes are defined, copy the bundle file path into each of them.
            if "wet_processes" in d and d["wet_processes"] is not None:
                for wet_process in d["wet_processes"]:
                    wet_process["bundle_file"] = d["bundle_file"]
                wet_processes.extend(d["wet_processes"])

            # If some bio processes are defined, copy the bundle file path into each of them.
            if "bi_processes" in d and d["bi_processes"] is not None:
                for bi_process in d["bi_processes"]:
                    bi_process["bundle_file"] = d["bundle_file"]
                bi_processes.extend(d["bi_processes"])

        # Instantiate all objects
        log_subsection("Loading wet processes...")
        self._wet_processes = Processes.from_dicts(wet_processes, WetProcess)
        logger.info(
            "=> %s wet process(es) loaded from bundle(s).",
            len(self._wet_processes),
        )

        log_subsection("Loading bioinformatics processes...")
        self._bi_processes = Processes.from_dicts(bi_processes, BioInfoProcess)
        logger.info(
            "=> %s bioinformatics process(es) loaded from bundle(s).",
            len(self._bi_processes),
        )

        log_subsection("Loading analyses...")
        self._analyses = Analyses.from_dicts(analyses)

        logger.info(
            "=> %s analysis(es) loaded from bundle(s).", len(self._analyses)
        )
        logger.info("")

        if check:
            self._check_referenced_processes()

    def _check_referenced_processes(self) -> None:
        """Check if wet and bi processes referenced inside each analysis are defined.
        If one of the processes is not defined, the program exits.
        """
        for index, analysis in enumerate(self._analyses):
            analysis_wet_process = analysis.metadata.get("wet_process")

            if (
                analysis_wet_process
                and analysis_wet_process not in self._wet_processes
            ):
                sys.exit(
                    f"Analysis at index {index} in file {analysis.bundle_file} "
                    f"is referencing an undefined wet process: {analysis_wet_process}"
                )

            analysis_bi_process = analysis.metadata.get("bi_process")

            if (
                analysis_bi_process
                and analysis_bi_process not in self._bi_processes
            ):
                sys.exit(
                    f"Analysis at index {index} in file {analysis.bundle_file} "
                    f"is referencing an undefined bi process: {analysis_bi_process}"
                )

    def _search_custom_tags(self) -> None:
        docs_with_custom_tags = [d for d in self._documents if "tags" in d]

        # Only one 'tags' redefinition is allowed across all the documents.
        if len(docs_with_custom_tags) > 1:
            bundle_files = sorted(
                [str(d["bundle_file"]) for d in docs_with_custom_tags]
            )
            msg = (
                f"Only one 'tags' key should be defined across all documents, "
                f"but multiple were found : {', '.join(bundle_files)}"
            )
            raise RuntimeError(msg)

        if len(docs_with_custom_tags) == 1:
            self._custom_tags_doc = docs_with_custom_tags[0]

    @property
    def analyses(self) -> Analyses:
        """The analyses."""
        return self._analyses

    @property
    def wet_processes(self) -> Processes:
        """The wet processes."""
        return self._wet_processes

    @property
    def bi_processes(self) -> Processes:
        """The bi processes."""
        return self._bi_processes
