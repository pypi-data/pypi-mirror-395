import argparse
import logging
from pathlib import Path

from genelastic.common.cli import add_verbose_control_args, add_version_arg
from genelastic.common.exceptions import (
    ValidationError,
    YAMLFileReadError,
)
from genelastic.import_data.import_bundle_factory import (
    load_yaml_file,
    validate_doc,
)
from genelastic.import_data.logger import configure_logging
from genelastic.import_data.models.validate import ValidationIssue

logger = logging.getLogger("genelastic")


def read_args() -> argparse.Namespace:
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(
        description="Statically validates YAML bundles: "
        "ensure they comply to the bundle schema.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    add_version_arg(parser)
    add_verbose_control_args(parser)
    parser.add_argument(
        "files",
        type=Path,
        nargs="+",
        default=None,
        help="Paths to YAML files containing bundles to validate.",
    )
    parser.add_argument(
        "-x",
        "--fail-fast",
        dest="fail_fast",
        action="store_true",
        help="Stop validating files after the first error is encountered.",
    )
    return parser.parse_args()


def main() -> int:
    """Entry point of the validate script."""
    args = read_args()
    configure_logging(args.verbose)

    validation_issues = []
    file_count = len(args.files)

    for file_index, file_path in enumerate(args.files):
        resolved_file_path = file_path.resolve()

        logger.info(
            "[%s/%s] Validating bundle(s) from file '%s'.",
            file_index + 1,
            file_count,
            resolved_file_path,
        )
        logger.info("Loading YAML file...")

        try:
            docs = load_yaml_file(resolved_file_path)
        except YAMLFileReadError as e:
            logger.error(e)

            if args.fail_fast:
                raise SystemExit(1) from None

            validation_issues.append(
                ValidationIssue(
                    exc_type=type(e).__name__,
                    file_path=resolved_file_path,
                    file_index=file_index + 1,
                    file_count=file_count,
                )
            )
            continue

        logger.info("-> YAML file successfully loaded.")

        doc_count = len(docs)
        logger.info("Found %s document(s) in the YAML file.", doc_count)

        for doc_index, doc in enumerate(docs):
            logger.info(
                "  Validating bundle format for document #%s/%s...",
                doc_index + 1,
                doc_count,
            )

            try:
                validate_doc(doc)
            except ValidationError as e:
                logger.error(e)

                if args.fail_fast:
                    raise SystemExit(1) from None

                validation_issues.append(
                    ValidationIssue(
                        exc_type=type(e).__name__,
                        file_path=resolved_file_path,
                        file_index=file_index + 1,
                        file_count=file_count,
                        doc_index=doc_index + 1,
                        doc_count=doc_count,
                    )
                )
                continue

            logger.info("  -> Bundle format is valid.")

        logger.info("")

    if len(validation_issues) > 0:
        logger.error("Some files raised exceptions:")
        for issue in validation_issues:
            logger.error("  - %s", issue)

        ret_code = 1
    else:
        logger.info("All bundles respect the genelastic YAML bundle format.")
        ret_code = 0

    files_failing_validation = len(
        {issue.file_path for issue in validation_issues}
    )
    files_passing_validation = file_count - files_failing_validation

    logger.info(
        "Out of %s file(s), validation passed for %s and failed for %s.",
        file_count,
        files_passing_validation,
        files_failing_validation,
    )

    return ret_code


if __name__ == "__main__":
    raise SystemExit(main())
