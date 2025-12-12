"""Module: constants

This module contains genelastic constants.
"""

import typing

import schema

ALLOWED_EXTENSIONS: typing.Final[list[str]] = [
    "vcf",
    "cov",
    "json",
    "yml",
    "yaml",
]

BUNDLE_CURRENT_VERSION = 3

DEFAULT_TAG_REGEX = "[^_]+"
DEFAULT_TAG_DELIMITER_START = "%"
DEFAULT_TAG_DELIMITER_END = ""

DEFAULT_TAG2FIELD: typing.Final[dict[str, dict[str, str]]] = {
    "S": {"field": "sample_name", "regex": DEFAULT_TAG_REGEX},
    "F": {"field": "source", "regex": DEFAULT_TAG_REGEX},
    "W": {"field": "wet_process", "regex": DEFAULT_TAG_REGEX},
    "B": {"field": "bi_process", "regex": DEFAULT_TAG_REGEX},
    "D": {"field": "cov_depth", "regex": DEFAULT_TAG_REGEX},
    "A": {"field": "barcode", "regex": DEFAULT_TAG_REGEX},
    "R": {"field": "reference_genome", "regex": DEFAULT_TAG_REGEX},
}

TOOLS_SUFFIX_RE = r"_(?P<tool>[a-zA-Z0-9]+)-(?P<version>\d+(?:-\d+){0,2})(?!-)"
"""
Regular expression to extract individual tool-version metadata pairs from a
validated ``.metrics`` suffix in filenames.

- Captures exactly one tool-version pair, where:

  - ``tool`` is an alphanumeric identifier (letters and digits),
  - ``version`` consists of 1 to 3 numeric components separated by hyphens
    (e.g., '1', '1-0', '1-0-0'),
- Uses named capture groups (``tool`` and ``version``) to extract data,
- The negative lookahead ``(?!-)`` ensures the version does not end with a
  hyphen,
- Intended for extracting all matching pairs after the ``.metrics`` prefix has
  been validated.
"""

_METRICS_SUFFIX_RE = r"(?:\.metrics(?:_[a-zA-Z0-9]+-\d+(?:-\d+){0,2}(?!-))*)?"
"""
Regular expression to match and validate the entire optional ``.metrics``
suffix in filenames.

- Matches zero or one occurrence of:

  - A literal ``.metrics`` prefix, which must be the first suffix in the
    filename,
  - Followed optionally by zero or more tool-version pairs, each starting with
    an underscore ``_`` and matching the same format as ``TOOLS_SUFFIX_RE``,
- Validates that the whole suffix structure is correct (including optional
  presence),
- Ensures that when present, the suffix starts with ``.metrics`` and is
  correctly formatted,
- Does not extract individual tool-version pairs; its role is to validate the
  suffix as a whole.
"""

_EXTENSIONS_SUFFIX_RE = rf"\.(?P<ext>{'|'.join(ALLOWED_EXTENSIONS)})(\.gz)?"
"""
Regular expression for matching allowed file extensions with optional gzip
compression.

This regex matches the file extension suffixes for files belonging to
a set of predefined allowed extensions, specified in the ``ALLOWED_EXTENSIONS``
list.

The pattern matches:

- a dot (``.``) followed by one of the allowed extensions,
- optionally, a second extension ``.gz`` indicating gzip compression.

Examples of matched suffixes: ``.vcf``, ``.cov``, ``.json``, ``.vcf.gz``,
``.json.gz``.
"""

FILE_SUFFIXES_RE = rf"{_METRICS_SUFFIX_RE}{_EXTENSIONS_SUFFIX_RE}"
"""Regex used to validate the suffix part of a filename.

It matches an optional metrics suffix (containing tool-version metadata),
immediately followed by a required allowed file extension suffix
(possibly compressed with .gz).

This regex is the combination of ``_METRICS_SUFFIX_RE`` and
``_EXTENSIONS_SUFFIX_RE``.
"""

QC_METRICS_SCHEMA = schema.Schema(
    {
        "id": str,
        "genome_coverage_size": float,
        "genome_coverage_percent": float,
        "n50": int,
        "larger_contig": int,
        "iqr": int,
        "outlier_percent": float,
        "mean_depth": float,
        "mean_duplicat_percent": float,
        "fold_regions_percents": {
            "5": float,
            "10": float,
            "20": float,
            "30": float,
            "40": float,
        },
    }
)


SV_METRICS_SCHEMA = schema.Schema(
    {
        "metadata_mandatory": [{str: schema.Or(str, int, float, bool)}],
        schema.Optional("metadata_optional"): [
            {str: schema.Or(str, int, float, bool)}
        ],
        "regions": [
            {
                "name": str,
                "bed": str,
                "results": [
                    {
                        "svtype": str,
                        "size": str,
                        "FP_query": int,
                        "TP_truth": int,
                        "TP_query": int,
                        "FN_truth": int,
                        "total_truth": int,
                        "total_query": int,
                        "precision": schema.Or(int, float),
                        "recall": schema.Or(int, float),
                        "f1": schema.Or(int, float),
                    }
                ],
            }
        ],
    }
)
