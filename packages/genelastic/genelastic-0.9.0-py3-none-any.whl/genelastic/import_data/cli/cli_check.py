import argparse
import logging
import sys
from pathlib import Path

from genelastic.common.cli import (
    add_es_connection_args,
    add_verbose_control_args,
    add_version_arg,
)
from genelastic.common.elastic import ElasticQueryConn
from genelastic.import_data.checker import Checker
from genelastic.import_data.import_bundle_factory import (
    make_import_bundle_from_files,
)
from genelastic.import_data.logger import configure_logging

logger = logging.getLogger("genelastic")
logging.getLogger("elastic_transport").setLevel(logging.WARNING)


class CLICheckObserver:
    """Observer used by the CLI to log Checker errors."""

    def __init__(self) -> None:
        self._logger = logger

    def notify_missing(self, label: str, missing: list[str]) -> None:
        """Handle missing IDs by logging an error."""
        self._logger.error("[CHECKER] Missing %s in ES: %s", label, missing)

    def notify_extra(self, label: str, extra: list[str]) -> None:
        """Handle extra IDs by logging an error."""
        self._logger.error("[CHECKER] Extra %s in ES: %s", label, extra)


def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check database coherency against one or more YAML bundles.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    add_version_arg(parser)
    add_verbose_control_args(parser)
    add_es_connection_args(parser)

    parser.add_argument(
        "files",
        type=Path,
        nargs="+",
        help="Paths to YAML bundle files to validate.",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Enable strict mode: also report entries present in Elasticsearch "
            "but missing from YAML bundles."
        ),
    )

    parser.add_argument(
        "-A",
        "--check-analyses",
        action="store_true",
        help="Check only analyses coherence.",
    )

    parser.add_argument(
        "-W",
        "--check-wet",
        action="store_true",
        help="Check only wet processes coherence.",
    )

    parser.add_argument(
        "-B",
        "--check-bi",
        action="store_true",
        help="Check only biological processes coherence.",
    )

    parser.add_argument(
        "-X",
        "--all",
        action="store_true",
        help="Check all entities (analyses, wet processes and bi processes).",
    )

    return parser.parse_args()


def main() -> None:
    args = read_args()
    configure_logging(args.verbose)

    logger.info(
        "Connecting to Elasticsearch at https://%s:%s ...",
        args.es_host,
        args.es_port,
    )

    es = ElasticQueryConn(
        f"https://{args.es_host}:{args.es_port}",
        args.es_cert_fp,
        args.es_index_prefix,
        basic_auth=(args.es_usr, args.es_pwd),
    )

    import_bundle = make_import_bundle_from_files(args.files)

    checker = Checker(es, strict=args.strict)
    checker.attach(CLICheckObserver())

    run_all = args.all or not (
        args.check_analyses or args.check_wet or args.check_bi
    )

    if args.check_analyses or run_all:
        checker.check_analyses(import_bundle.analyses)

    if args.check_wet or run_all:
        checker.check_wet_processes(import_bundle.wet_processes)

    if args.check_bi or run_all:
        checker.check_bi_processes(import_bundle.bi_processes)

    if checker.errors_detected:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
