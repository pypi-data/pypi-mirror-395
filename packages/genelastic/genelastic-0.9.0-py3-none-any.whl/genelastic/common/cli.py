"""Utility functions for CLI scripts."""

import argparse
import logging
from importlib.metadata import version

logger = logging.getLogger("genelastic")


BASE_LOG_LEVEL = ["critical", "error", "warning", "info", "debug"]


def positive_int(value: str) -> int:
    """Argparse type: require a positive integer."""
    try:
        number = int(value)
    except ValueError:
        msg = f"expected a valid integer, got '{value}'."
        raise argparse.ArgumentTypeError(msg) from None
    if number <= 0:
        msg = f"expected a positive integer, got {value}."
        raise argparse.ArgumentTypeError(msg) from None
    return number


def add_version_arg(parser: argparse.ArgumentParser) -> None:
    """Add a version argument to query the current Genelastic version.
    Argument is added to the parser by using its reference.
    """
    top_level_package = __package__.split(".")[0]
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {version(top_level_package)}",
    )


def add_verbose_control_args(parser: argparse.ArgumentParser) -> None:
    """Add verbose control arguments to the parser.
    Arguments are added to the parser by using its reference.
    """
    parser.add_argument(
        "-q",
        "--quiet",
        dest="verbose",
        action="store_const",
        const=0,
        default=1,
        help="Set verbosity to 0 (quiet mode).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        default=1,
        help=(
            "Verbose level. -v for information, -vv for debug, -vvv for trace."
        ),
    )


def add_es_connection_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to the parser needed to gather ElasticSearch server connection parameters.
    Arguments are added to the parser by using its reference.
    """
    parser.add_argument(
        "--es-host",
        dest="es_host",
        default="localhost",
        help="Address of Elasticsearch host.",
    )
    parser.add_argument(
        "--es-port",
        type=int,
        default=9200,
        dest="es_port",
        help="Elasticsearch port.",
    )
    parser.add_argument(
        "--es-usr", dest="es_usr", default="elastic", help="Elasticsearch user."
    )
    parser.add_argument(
        "--es-pwd", dest="es_pwd", required=True, help="Elasticsearch password."
    )
    parser.add_argument(
        "--es-cert-fp",
        dest="es_cert_fp",
        help="Elasticsearch sha256 certificate fingerprint.",
    )
    parser.add_argument(
        "--es-index-prefix",
        dest="es_index_prefix",
        help="Add the given prefix to each index created during import.",
    )


def parse_server_launch_args(
    parser_desc: str, default_port: int
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=parser_desc,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=default_port,
    )

    env_subparsers = parser.add_subparsers(dest="env", required=True)
    dev_parser = env_subparsers.add_parser(
        "dev",
        help="Use development environment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    dev_parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=[*BASE_LOG_LEVEL, "trace"],
    )

    prod_parser = env_subparsers.add_parser(
        "prod",
        help="Use production environment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    prod_parser.add_argument(
        "--log-level", type=str, default="info", choices=BASE_LOG_LEVEL
    )
    prod_parser.add_argument(
        "-w", "--workers", type=int, default=1, help="Number of workers."
    )

    prod_parser.add_argument("--access-logfile", type=str, default=None)
    prod_parser.add_argument("--log-file", type=str, default=None)

    return parser.parse_args()


def log_section(title: str) -> None:
    msg = f">>  {title}  <<"
    logger.info("*" * len(msg))
    logger.info(msg)
    logger.info("*" * len(msg))


def log_subsection(title: str) -> None:
    logger.info("")
    logger.info("<%s>", title)


def log_item(name: str, index: int, count: int) -> None:
    msg = f"[ {name} #{index}/{count} ]"
    logger.info(msg)
