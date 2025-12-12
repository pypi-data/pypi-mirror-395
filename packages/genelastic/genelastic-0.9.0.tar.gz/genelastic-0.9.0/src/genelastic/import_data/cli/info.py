import argparse
import logging
from datetime import datetime

from genelastic.common.cli import (
    add_es_connection_args,
    add_verbose_control_args,
    add_version_arg,
)
from genelastic.common.elastic import ElasticQueryConn
from genelastic.import_data.logger import configure_logging

logger = logging.getLogger("genelastic")
logging.getLogger("elastic_transport").setLevel(
    logging.WARNING
)  # Disable excessive logging


def read_args() -> argparse.Namespace:
    """Read arguments from the command line."""
    parser = argparse.ArgumentParser(
        description="ElasticSearch database info.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    add_version_arg(parser)
    add_verbose_control_args(parser)
    add_es_connection_args(parser)
    parser.add_argument(
        "-a",
        "--list-analyses",
        action="store_true",
        help="List all imported analyses.",
    )
    parser.add_argument(
        "-w",
        "--list-wet-processes",
        action="store_true",
        help="List all imported wet processes.",
    )
    parser.add_argument(
        "-b",
        "--list-bi-processes",
        action="store_true",
        help="List all imported bio info processes.",
    )
    parser.add_argument(
        "-B",
        "--list-bundles",
        action="store_true",
        help="List YAML bundles and associated analyses.",
    )

    return parser.parse_args()


def list_processes(es_query_conn: ElasticQueryConn, index: str) -> None:
    """List all processes."""
    process_ids = es_query_conn.get_field_values(index, "proc_id")

    if len(process_ids) == 0:
        logger.info("Empty response.")
        return

    for process_id in process_ids:
        logger.info("- %s", process_id)


def list_wet_processes(es_query_conn: ElasticQueryConn) -> None:
    """List all wet processes."""
    logger.info("Imported wet processes")
    logger.info("======================")
    list_processes(es_query_conn, es_query_conn.wet_processes_index)


def list_bi_processes(es_query_conn: ElasticQueryConn) -> None:
    """List all bio info processes."""
    logger.info("Imported bi processes")
    logger.info("=====================")
    list_processes(es_query_conn, es_query_conn.bi_processes_index)


def list_analyses(es_query_conn: ElasticQueryConn) -> None:
    """List all imported analyses and their associated data files."""
    query = {
        "size": 0,
        "aggs": {
            "by_analysis": {
                "composite": {
                    "size": 1000,
                    "sources": [
                        {
                            "analysis_id": {
                                "terms": {"field": "analysis_id.keyword"}
                            }
                        }
                    ],
                },
                "aggs": {
                    "data_files": {
                        "top_hits": {
                            "size": 100,
                        }
                    }
                },
            }
        },
    }

    buckets = es_query_conn.run_composite_aggregation(
        es_query_conn.data_files_index, query
    )

    if not buckets:
        logger.info("No data files found.")
        return

    logger.info("Data files per YAML bundle")
    logger.info("=" * 80)

    for i, bucket in enumerate(buckets):
        analysis_id = bucket["key"]["analysis_id"]
        hits = bucket["data_files"]["hits"]["hits"]
        doc_count = len(hits)

        logger.info(
            "[%d] Analysis ID: %s (%d file%s)",
            i + 1,
            analysis_id,
            doc_count,
            "s" if doc_count > 1 else "",
        )
        logger.info("-" * 80)

        for j, hit in enumerate(hits):
            source = hit["_source"]

            created_at = datetime.fromisoformat(source["created_at"])
            created_at_formatted = created_at.strftime("%Y-%m-%d")

            logger.info(" File %d of %d:", j + 1, doc_count)
            logger.info(" created_at : %s", created_at_formatted)
            logger.info(" bundle_file : %s", source["bundle_file"])
            logger.info(" path : %s", source["path"])


def list_bundles(es_query_conn: ElasticQueryConn) -> None:
    """List bundle_file → associated analysis_id (clean visual CLI output)."""
    query = {
        "size": 0,
        "aggs": {
            "by_bundle": {
                "composite": {
                    "size": 2000,
                    "sources": [
                        {
                            "bundle_file": {
                                "terms": {"field": "bundle_file.keyword"}
                            }
                        }
                    ],
                },
                "aggs": {
                    "analyses": {
                        "terms": {
                            "field": "analysis_id.keyword",
                            "size": 2000,
                        }
                    }
                },
            }
        },
    }

    buckets = es_query_conn.run_composite_aggregation(
        es_query_conn.data_files_index, query
    )

    if not buckets:
        logger.info("No bundles found.")
        return

    # Sort bundles by bundle_file path
    buckets = sorted(buckets, key=lambda b: b["key"]["bundle_file"])

    logger.info("========================================")
    logger.info(" BUNDLES AND ASSOCIATED ANALYSES")
    logger.info("========================================")
    logger.info("")

    for idx, bucket in enumerate(buckets, start=1):
        bundle = bucket["key"]["bundle_file"]
        analyses = bucket["analyses"]["buckets"]

        logger.info("#%d %s", idx, bundle)
        if not analyses:
            logger.info("   (no analyses)")
        else:
            for a in analyses:
                logger.info("   • %s", a["key"])

        logger.info("----------------------------------------")


def main() -> None:
    """Entry point of the info script."""
    args = read_args()

    configure_logging(args.verbose)
    logger.debug("Arguments: %s", args)

    addr = f"https://{args.es_host}:{args.es_port}"
    logger.info("Connecting to Elasticsearch at %s...", addr)
    es_query_conn = ElasticQueryConn(
        addr,
        args.es_cert_fp,
        args.es_index_prefix,
        basic_auth=(args.es_usr, args.es_pwd),
    )

    list_call_count = 0

    if args.list_bundles:
        list_bundles(es_query_conn)
        list_call_count += 1

    if args.list_analyses:
        list_analyses(es_query_conn)
        list_call_count += 1

    if args.list_wet_processes:
        list_wet_processes(es_query_conn)
        list_call_count += 1

    if args.list_bi_processes:
        list_bi_processes(es_query_conn)
        list_call_count += 1

    if list_call_count == 0:
        logger.debug("No list option specified, listing everything.")
        list_analyses(es_query_conn)
        list_wet_processes(es_query_conn)
        list_bi_processes(es_query_conn)


if __name__ == "__main__":
    main()
