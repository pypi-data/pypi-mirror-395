import argparse
import logging
from pathlib import Path

from biophony import DEFAULT_RATE, MutSimParams

from genelastic.common.cli import add_verbose_control_args, add_version_arg
from genelastic.import_data.logger import configure_logging
from genelastic.import_data.random_bundle import (
    RandomBundle,
)

logger = logging.getLogger("genelastic")


def read_args() -> argparse.Namespace:
    """Read arguments from the command line."""
    parser = argparse.ArgumentParser(
        description="Random bundle generator. "
        "A bundle is a YAML file format used to import genetic data into an Elasticsearch database. "
        "It can contain one or more analyses; "
        "each analysis including metadata, references to "
        "a wet lab and bioinformatics process "
        "and paths to a VCF file and optionally to a coverage file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    add_version_arg(parser)
    add_verbose_control_args(parser)
    parser.add_argument(
        "output_dir",
        help="Path where analyses VCF and coverage files will be generated.",
        type=Path,
    )
    parser.add_argument("--log-file", help="Path to a log file.")
    parser.add_argument(
        "-n",
        "--chrom-nb",
        type=int,
        default=5,
        help="Number of chromosomes to include in the generated VCF file.",
    )
    parser.add_argument(
        "-o",
        "--output-bundle",
        default=None,
        help="Path where the YAML bundle file will be written. "
        "If no path is provided, the bundle is written to stdout.",
        type=Path,
    )
    parser.add_argument(
        "-l",
        "--sequence-length",
        type=int,
        default=2000,
        help="Sequence length (number of nucleotides) generated for each chromosome.",
    )
    parser.add_argument(
        "-c",
        "--coverage",
        action="store_true",
        help="Generate a coverage file for each analysis.",
    )
    parser.add_argument(
        "-a",
        "--analyses",
        help="Number of analyses to generate. "
        "Each analysis will reference a wet lab and bioinformatics process, "
        "a VCF file and optionally a coverage file.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--processes",
        help="Number of wet lab and bioinformatics processes to generate.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--snp-rate",
        help="Generated VCF SNP rate.",
        type=float,
        default=DEFAULT_RATE,
    )
    parser.add_argument(
        "-i",
        "--ins-rate",
        help="Generated VCF insertion rate.",
        type=float,
        default=DEFAULT_RATE,
    )
    parser.add_argument(
        "-d",
        "--del-rate",
        help="Generated VCF deletion rate.",
        type=float,
        default=DEFAULT_RATE,
    )
    return parser.parse_args()


def main() -> None:
    """Entry point of the gen-data script."""
    # Read command line arguments
    args = read_args()
    output_dir = args.output_dir.resolve()

    if not output_dir.is_dir():
        msg = f"ERROR: '{output_dir}' does not exist or is not a directory."
        raise SystemExit(msg)

    if args.analyses < 1:
        msg = "Analyses count must be at least 1."
        raise SystemExit(msg)

    if args.processes < 1:
        msg = "Processes count must be at least 1."
        raise SystemExit(msg)

    # Configure logging
    configure_logging(args.verbose, log_file=args.log_file)
    logger.debug("Arguments: %s", args)

    # Write to stdout or file
    RandomBundle(
        output_dir,
        args.analyses,
        args.processes,
        args.chrom_nb,
        args.sequence_length,
        MutSimParams(
            snp_rate=args.snp_rate,
            ins_rate=args.ins_rate,
            del_rate=args.del_rate,
        ),
        do_gen_coverage=args.coverage,
    ).to_yaml(args.output_bundle)


if __name__ == "__main__":
    main()
