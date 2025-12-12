# vi: se tw=80

# Elasticsearch Python API:
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
# https://elasticsearch-py.readthedocs.io/en/latest/api.html

import argparse
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

from genelastic.common.cli import (
    add_es_connection_args,
    add_verbose_control_args,
    add_version_arg,
    log_item,
    log_section,
    log_subsection,
    positive_int,
)
from genelastic.common.elastic import ElasticImportConn
from genelastic.import_data.import_bundle_factory import (
    make_import_bundle_from_files,
)
from genelastic.import_data.importers.importer_base import ImporterError
from genelastic.import_data.importers.importer_factory import ImporterFactory
from genelastic.import_data.logger import configure_logging
from genelastic.import_data.models.analysis import Analysis
from genelastic.import_data.models.data_file import DataFile
from genelastic.import_data.models.processes import Processes

logger = logging.getLogger("genelastic")
logging.getLogger("elastic_transport").setLevel(
    logging.WARNING
)  # Disable excessive logging
logging.getLogger("urllib3").setLevel(
    logging.WARNING
)  # Disable excessive logging


def read_args() -> argparse.Namespace:
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(
        description="Genetics data importer.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    add_version_arg(parser)
    add_verbose_control_args(parser)
    add_es_connection_args(parser)
    parser.add_argument(
        "-D",
        "--dry-run",
        dest="dryrun",
        action="count",
        default=0,
        help=(
            "Dry-run level. -D for data files loading (VCF, coverage, etc) "
            "without connecting or importing to database. "
            "-DD for metadata YAML files loading only (no loading of data files)."
        ),
    )
    parser.add_argument(
        "--log-file", dest="log_file", help="Path to a log file."
    )
    parser.add_argument(
        "--no-list",
        dest="no_list",
        action="store_true",
        help="Do not print list of files to be imported.",
    )
    parser.add_argument(
        "--no-confirm",
        dest="no_confirm",
        action="store_true",
        help="Do not ask confirmation before importing.",
    )
    parser.add_argument(
        "-t",
        "--threads",
        dest="thread_count",
        type=positive_int,
        default=4,
        help="Number of threads to use for parallel data files import.",
    )
    parser.add_argument(
        "--multi-match",
        dest="multi_match",
        action="store_true",
        help=(
            "Enable grouping of files from the same 'data_path' into multiple "
            "analyses by extracting variable metadata fields directly from "
            "filenames using the file prefix. If some metadata fields (e.g., "
            "sample_name, wet_process, bi_process) are not defined in the YAML "
            "bundle, the importer detects all analyses sharing the same "
            "defined metadata, but differing by the undefined fields. This "
            "allows importing and filtering several analyses at once from a "
            "single directory, based on the metadata present in filenames. "
            "When disabled (default), only files matching the fixed filename "
            "pattern (where all metadata fields are defined in the YAML) are "
            "grouped into a single analysis; other files are ignored."
        ),
    )
    parser.add_argument(
        "files",
        type=Path,
        nargs="+",
        default=None,
        help="Data files that describe what to import.",
    )
    return parser.parse_args()


def import_analysis(
    es_import_conn: ElasticImportConn,
    analysis: Analysis,
) -> None:
    """Import analysis into a dedicated index."""
    logger.info(
        " -> Importing analysis '%s' metadata into index '%s'...",
        analysis.id,
        es_import_conn.analyses_index,
    )

    documents = [
        {
            "_index": es_import_conn.analyses_index,
            "_source": {
                "created_at": datetime.now(UTC).isoformat(),
                "analysis_id": analysis.id,
                "bundle_file": str(analysis.bundle_file),
                "data_path": str(analysis.data_path),
                "metadata": analysis.metadata,
            },
        }
    ]

    es_import_conn.bulk_import(documents)


def import_data_file(
    es_import_conn: ElasticImportConn,
    data_file: DataFile,
) -> None:
    """Import data files into a dedicated index."""
    logger.info(
        " -> Importing metadata into index '%s'...",
        es_import_conn.data_files_index,
    )

    documents = [
        {
            "_index": es_import_conn.data_files_index,
            "_source": {
                "created_at": datetime.now(UTC).isoformat(),
                "analysis_id": data_file.analysis_id,
                "path": str(data_file.path),
                "bundle_file": str(data_file.bundle_file),
                "metadata": data_file.metadata,
                "metrics": data_file.metrics,
            },
        }
    ]

    es_import_conn.bulk_import(documents)


def import_data_file_content(
    es_import_conn: ElasticImportConn,
    data_file: DataFile,
    thread_count: int,
    dry_run: int,
) -> None:
    """Import data file content into a dedicated index,
    based on their extension and type.
    """
    # -DD: no file processing, no import.
    if dry_run > 1:
        logger.info("[Dryrun] Data file neither processed nor imported.")
        return

    try:
        logger.info(
            " -> Processing file content for import...",
        )
        importer = ImporterFactory.get_importer(
            data_file, es_import_conn, thread_count
        )

        # -D: only process files, no import.
        if dry_run == 1:
            logger.info("[Dryrun] Data file processed but not imported.")
            return

        logger.info(
            " -> Importing file content into index '%s'...",
            importer.target_index,
        )
        importer.import_docs()
    except ImporterError as e:
        logger.error(e)


def import_processes(
    es_import_conn: ElasticImportConn,
    index: str,
    processes: Processes,
) -> None:
    """Import processes into a dedicated index, based on their type."""
    documents = [
        {
            "_index": index,
            "_source": {
                "proc_id": process.id,
                "type": process.type,
                "metadata": process.data,
            },
        }
        for process in processes.values()
    ]

    es_import_conn.bulk_import(documents)


def main() -> None:
    """Entry point of the import script."""
    # Read command line arguments
    args = read_args()

    # Configure logging
    configure_logging(args.verbose, log_file=args.log_file)
    logger.debug("Arguments: %s", args)
    logger.debug("LOGGERS: %s", logging.root.manager.loggerDict)

    # Open connection to ES
    addr = f"https://{args.es_host}:{args.es_port}"
    logger.info("Connecting to Elasticsearch at %s...", addr)
    es_import_conn = ElasticImportConn(
        addr,
        args.es_cert_fp,
        args.es_index_prefix,
        args.dryrun,
        basic_auth=(args.es_usr, args.es_pwd),
    )

    log_section("LOAD DATA")
    logger.info("")
    import_bundle = make_import_bundle_from_files(
        args.files, multi_match=args.multi_match, check=True
    )
    all_bundled_files = import_bundle.analyses.get_data_files()

    if not all_bundled_files:
        logger.warning("No matching data files found from import bundle(s) !")

    log_section("IMPORT DATA")
    # List files before importing.
    if not args.no_list:
        logger.info("")
        logger.info(
            "The following %s file(s) will be imported:", len(all_bundled_files)
        )

        for data_file in all_bundled_files:
            logger.info("- '%s'", data_file.path)
    else:
        logger.debug(
            "'--no-list' argument provided: "
            "not listing files about to be imported."
        )

    # Ask confirmation for importing
    if not args.no_confirm:
        answer: str = "maybe"
        while answer not in ["", "n", "y"]:
            answer = input("Import (y/N)? ").lower()
        if answer != "y":
            logger.info("Import canceled.")
            sys.exit(0)
    else:
        logger.debug(
            "'--no-confirm' argument provided: "
            "not asking for confirmation before importing files."
        )

    # Start import.
    log_subsection("Importing wet processes...")
    logger.info(
        "-> Importing %s wet process(es) into index '%s': %s.",
        len(import_bundle.wet_processes),
        es_import_conn.wet_processes_index,
        ", ".join(import_bundle.wet_processes.keys()),
    )
    import_processes(
        es_import_conn,
        es_import_conn.wet_processes_index,
        import_bundle.wet_processes,
    )
    log_subsection("Importing bioinformatics processes...")
    logger.info(
        "-> Importing %s bioinformatics process(es) into index '%s': %s.",
        len(import_bundle.bi_processes),
        es_import_conn.bi_processes_index,
        ", ".join(import_bundle.bi_processes.keys()),
    )
    import_processes(
        es_import_conn,
        es_import_conn.bi_processes_index,
        import_bundle.bi_processes,
    )

    log_subsection("Importing analysis metadata...")
    for i, analysis in enumerate(sorted(import_bundle.analyses)):
        log_item(
            "Analysis",
            i + 1,
            len(import_bundle.analyses),
        )
        import_analysis(es_import_conn, analysis)

    log_subsection("Importing data files...")
    counter = 1
    for ext in sorted(import_bundle.analyses.extensions):
        data_files = import_bundle.analyses.get_data_files(ext)
        logger.info("[ %s data files ]", ext.upper())

        for data_file in data_files:
            logger.info(
                " -> Processing data file #%s/%s: '%s'...",
                counter,
                len(import_bundle.analyses.get_data_files()),
                data_file.path.name,
            )
            import_data_file(es_import_conn, data_file)
            import_data_file_content(
                es_import_conn, data_file, args.thread_count, args.dryrun
            )
            logger.info("")
            counter += 1

    logger.info("=> Done.")


if __name__ == "__main__":
    main()
