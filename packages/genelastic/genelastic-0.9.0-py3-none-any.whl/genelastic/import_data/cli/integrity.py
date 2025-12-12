import argparse
import logging
import typing

from elasticsearch import NotFoundError

from genelastic.common.cli import (
    add_es_connection_args,
    add_verbose_control_args,
    add_version_arg,
)
from genelastic.common.elastic import ElasticQueryConn
from genelastic.common.exceptions import DBIntegrityError
from genelastic.import_data.logger import configure_logging

if typing.TYPE_CHECKING:
    from genelastic.common.types import Bucket

logger = logging.getLogger("genelastic")
logging.getLogger("elastic_transport").setLevel(
    logging.WARNING
)  # Disable excessive logging


def read_args() -> argparse.Namespace:
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(
        description="Utility to check the integrity "
        "of the genelastic ElasticSearch database.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    add_version_arg(parser)
    add_verbose_control_args(parser)
    add_es_connection_args(parser)
    return parser.parse_args()


def check_for_undefined_file_indices(
    es_query_conn: ElasticQueryConn, analyses_index: str
) -> None:
    """Check for potentially undefined files indices in the analyses index.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :raises genelastic.common.DBIntegrityError:
        Some files indices are used in the analyses index but are undefined.
    """
    if not es_query_conn.client:
        logger.info(
            "[Dryrun] check_for_undefined_file_indices: "
            "no Elasticsearch client."
        )
        return

    logger.info(
        "Checking for references to undefined file indices in the index '%s'...",
        analyses_index,
    )

    undefined_indices = set()

    query = {
        "size": 0,
        "aggs": {
            "get_file_indices": {
                "composite": {
                    "sources": {
                        "file_index": {"terms": {"field": "file_index.keyword"}}
                    },
                    "size": 1000,
                }
            }
        },
    }

    buckets: list[Bucket] = es_query_conn.run_composite_aggregation(
        analyses_index, query
    )

    for bucket in buckets:
        file_index = bucket["key"]["file_index"]

        try:
            es_query_conn.client.indices.get(index=file_index)
            logger.debug(
                "File index %s used in index '%s' is defined.",
                file_index,
                analyses_index,
            )
        except NotFoundError:
            logger.debug(
                "File index %s used in '%s' is undefined.",
                file_index,
                analyses_index,
            )
            undefined_indices.add(file_index)

    if len(undefined_indices) > 0:
        msg = (
            f"Found the following undefined file indices defined in the index '{analyses_index}': "
            f"{', '.join(undefined_indices)}"
        )
        raise DBIntegrityError(msg)

    logger.info("All defined file indices are referenced.")


def get_undefined_processes(
    es_query_conn: ElasticQueryConn,
    analyses_index: str,
    process_index: str,
    field: str,
) -> set[str]:
    """Return a set of undefined processes IDs in an index.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param process_index: Name of the index to check for undefined processes.
    :param field: Field name used to retrieve the process ID.
    :returns: A set of undefined processes IDs.
    """
    query = {
        "size": 0,
        "aggs": {
            "get_analyses_processes": {
                "composite": {
                    "sources": {
                        "process": {"terms": {"field": f"{field}.keyword"}}
                    },
                    "size": 1000,
                }
            }
        },
    }

    buckets: list[Bucket] = es_query_conn.run_composite_aggregation(
        analyses_index, query
    )

    used_processes = {bucket["key"]["process"] for bucket in buckets}
    logger.debug(
        "Used values for field '%s' in index '%s': %s",
        field,
        analyses_index,
        used_processes,
    )

    defined_processes = es_query_conn.get_field_values(process_index, "proc_id")
    logger.debug(
        "Defined values in index '%s': %s", process_index, defined_processes
    )

    return used_processes.difference(defined_processes)


def check_for_undefined_wet_processes(
    es_query_conn: ElasticQueryConn, analyses_index: str, wet_process_index: str
) -> None:
    """Check that each wet process used in the analyses index is defined.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param wet_process_index: Name of the index where wet processes are stored.
    :raises genelastic.common.DBIntegrityError:
        Some wet processes used in the analyses index are undefined.
    """
    logger.info(
        "Checking for undefined wet processes used in index '%s'...",
        analyses_index,
    )
    undefined_wet_processes = get_undefined_processes(
        es_query_conn, analyses_index, wet_process_index, "metadata.wet_process"
    )

    if len(undefined_wet_processes) > 0:
        msg = (
            f"Index '{analyses_index}' uses the following undefined wet processes: "
            f"{', '.join(undefined_wet_processes)}."
        )
        raise DBIntegrityError(msg)

    logger.info(
        "All wet processes used in index '%s' are defined.", wet_process_index
    )


def check_for_undefined_bi_processes(
    es_query_conn: ElasticQueryConn, analyses_index: str, bi_process_index: str
) -> None:
    """Check that each bio info process used in the analyses index is defined.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param bi_process_index: Name of the index where bio info processes are stored.
    :raises genelastic.common.DBIntegrityError:
        Some bio info processes used in the analyses index are undefined.
    """
    logger.info(
        "Checking for undefined bio info processes used in index '%s'...",
        analyses_index,
    )
    undefined_bi_processes = get_undefined_processes(
        es_query_conn, analyses_index, bi_process_index, "metadata.bi_process"
    )

    if len(undefined_bi_processes) > 0:
        msg = (
            f"Index '{analyses_index}' uses the following undefined bio info processes: "
            f"{', '.join(undefined_bi_processes)}."
        )
        raise DBIntegrityError(msg)

    logger.info(
        "All bio info processes used in index '%s' are defined.",
        bi_process_index,
    )


def check_for_unused_file_indices(
    es_query_conn: ElasticQueryConn, analyses_index: str, index_prefix: str
) -> int:
    """Check that each of the file indices are used in at least one analysis.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param index_prefix: Prefix given to all the indices of the ElasticSearch database.
    :returns: 1 if some file indices exists but are unused in the analyses index,
        and 0 otherwise.
    """
    if not es_query_conn.client:
        logger.info(
            "[Dryrun] check_for_unused_file_indices: "
            "no Elasticsearch client."
        )
        return -1

    json_indices = es_query_conn.client.cat.indices(
        index=f"{index_prefix}-file-*", format="json"
    ).body

    found_file_indices = set()
    for x in json_indices:
        if isinstance(x, dict):
            found_file_indices.add(x["index"])

    query = {
        "size": 0,
        "aggs": {
            "get_file_indices": {
                "composite": {
                    "sources": {
                        "file_index": {"terms": {"field": "file_index.keyword"}}
                    },
                    "size": 1000,
                }
            }
        },
    }

    buckets: list[Bucket] = es_query_conn.run_composite_aggregation(
        analyses_index, query
    )

    used_files_indices = {bucket["key"]["file_index"] for bucket in buckets}
    unused_files_indices = found_file_indices.difference(used_files_indices)

    if len(unused_files_indices) > 0:
        logger.warning(
            "Found the following unused files indices: %s",
            ", ".join(unused_files_indices),
        )
        return 1

    logger.info("All files indices are used.")
    return 0


def check_for_unused_wet_processes(
    es_query_conn: ElasticQueryConn, analyses_index: str, wet_proc_index: str
) -> int:
    """Check for defined wet processes that are not used in the analyses index.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param wet_proc_index: Name of the index where wet processes are stored.
    :returns: 1 if some wet process are defined but unused in the analyses index,
        and 0 otherwise.
    """
    logger.info(
        "Checking for unused wet processes in the index '%s'...", wet_proc_index
    )

    defined_wet_procs = es_query_conn.get_field_values(
        wet_proc_index, "proc_id"
    )
    logger.debug(
        "Found the following defined wet processes: %s", defined_wet_procs
    )

    used_wet_procs = es_query_conn.get_field_values(
        analyses_index, "metadata.wet_process"
    )
    logger.debug(
        "Following processes are used in the index '%s': %s",
        analyses_index,
        used_wet_procs,
    )

    unused_wet_procs = defined_wet_procs - used_wet_procs
    if len(unused_wet_procs) > 0:
        logger.warning("Found unused wet processes: %s", unused_wet_procs)
        return 1

    logger.info("No unused wet processes found.")
    return 0


def check_for_unused_bi_processes(
    es_query_conn: ElasticQueryConn, analyses_index: str, bi_proc_index: str
) -> int:
    """Check for defined bio info processes that are not used in the analyses index.

    :param es_query_conn: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param bi_proc_index: Name of the index where bio info processes are stored.
    :returns: 1 if some wet process are defined but unused in the analyses index,
        and 0 otherwise.
    """
    logger.info(
        "Checking for unused bio info processes in the index '%s'...",
        bi_proc_index,
    )

    defined_bi_procs = es_query_conn.get_field_values(bi_proc_index, "proc_id")
    logger.debug(
        "Found the following defined bio info processes: %s", defined_bi_procs
    )

    used_bi_procs = es_query_conn.get_field_values(
        analyses_index, "metadata.bi_process"
    )
    logger.debug(
        "Following processes are used in the index '%s': %s",
        analyses_index,
        used_bi_procs,
    )

    unused_bi_procs = defined_bi_procs - used_bi_procs
    if len(unused_bi_procs) > 0:
        logger.warning("Found unused bio info processes: %s", unused_bi_procs)
        return 1

    logger.info("No unused bio info processes found.")
    return 0


def main() -> None:
    """Entry point of the integrity script."""
    args = read_args()

    configure_logging(args.verbose)
    logger.debug("Arguments: %s", args)

    analyses_index = f"{args.es_index_prefix}-analyses"
    wet_processes_index = f"{args.es_index_prefix}-wet_processes"
    bi_processes_index = f"{args.es_index_prefix}-bi_processes"

    addr = f"https://{args.es_host}:{args.es_port}"
    logger.info("Connecting to Elasticsearch at %s...", addr)
    es_query_conn = ElasticQueryConn(
        addr,
        args.es_cert_fp,
        args.es_index_prefix,
        args.dryrun,
        basic_auth=(args.es_usr, args.es_pwd),
    )

    # Fatal errors
    try:
        es_query_conn.ensure_unique(wet_processes_index, "proc_id")
        es_query_conn.ensure_unique(bi_processes_index, "proc_id")
        check_for_undefined_file_indices(es_query_conn, analyses_index)
        check_for_undefined_wet_processes(
            es_query_conn, analyses_index, wet_processes_index
        )
        check_for_undefined_bi_processes(
            es_query_conn, analyses_index, bi_processes_index
        )
    except DBIntegrityError as e:
        raise SystemExit(e) from e

    # Warnings
    check_for_unused_wet_processes(
        es_query_conn, analyses_index, wet_processes_index
    )
    check_for_unused_bi_processes(
        es_query_conn, analyses_index, bi_processes_index
    )
    check_for_unused_file_indices(
        es_query_conn, analyses_index, args.es_index_prefix
    )


if __name__ == "__main__":
    main()
