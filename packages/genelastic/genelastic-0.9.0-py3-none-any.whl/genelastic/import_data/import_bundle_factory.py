"""ImportBundle factory module."""

import logging
from pathlib import Path
from typing import Any

import schema
import yaml
from yaml import YAMLError

from genelastic.common.exceptions import (
    ValidationError,
    YAMLFileReadError,
)
from genelastic.common.types import BundleDict

from .constants import BUNDLE_CURRENT_VERSION
from .import_bundle import ImportBundle
from .models.tags import Tags

logger = logging.getLogger("genelastic")


_SCHEMA_V3 = schema.Schema(
    {
        "version": 3,
        schema.Optional("analyses"): schema.Or(
            None,
            [
                {
                    "file_prefix": str,
                    schema.Optional("suffix"): str,
                    schema.Optional("sample_name"): str,
                    schema.Optional("source"): str,
                    schema.Optional("barcode"): str,
                    schema.Optional("wet_process"): str,
                    schema.Optional("bi_process"): str,
                    schema.Optional("reference_genome"): str,
                    schema.Optional("flowcell"): str,
                    schema.Optional("lanes"): [int],
                    schema.Optional("seq_indices"): [str],
                    schema.Optional("cov_depth"): int,
                    schema.Optional("qc_comment"): str,
                    schema.Optional("data_path"): str,
                }
            ],
        ),
        schema.Optional("wet_processes"): schema.Or(
            None,
            [
                {
                    "proc_id": str,
                    "manufacturer": str,
                    "sequencer": str,
                    "generic_kit": str,
                    "fragmentation": int,
                    "reads_size": int,
                    "input_type": str,
                    "amplification": str,
                    "flowcell_type": str,
                    "sequencing_type": str,
                    schema.Optional("desc"): str,
                    schema.Optional("library_kit"): str,
                    schema.Optional("sequencing_kit"): str,
                    schema.Optional("error_rate_expected"): float,
                }
            ],
        ),
        schema.Optional("bi_processes"): schema.Or(
            None,
            [
                {
                    "proc_id": str,
                    "name": str,
                    "pipeline_version": str,
                    schema.Optional("steps"): [
                        {
                            "name": str,
                            "cmd": str,
                            schema.Optional("version"): str,
                            schema.Optional("output"): str,
                        }
                    ],
                    "sequencing_type": str,
                    schema.Optional("desc"): str,
                }
            ],
        ),
        schema.Optional("tags"): {
            schema.Optional("delimiter"): {
                schema.Optional("start"): schema.And(
                    str,
                    Tags.validate_tag_delimiter,
                    error="Key 'delimiter.start' should only contain one special character, "
                    "excluding the following : (, ), ?, <, >.",
                ),
                schema.Optional("end"): schema.And(
                    str,
                    Tags.validate_tag_delimiter,
                    error="Key 'delimiter.end' should only contain one special character, "
                    "excluding the following : (, ), ?, <, >.",
                ),
            },
            schema.Optional("match"): {
                schema.And(
                    str,
                    Tags.validate_tag_name,
                    error="Tags listed under the 'match' key should only contain "
                    "word characters. A word character is a character "
                    "a-z, A-Z, 0-9, including _ (underscore).",
                ): {"field": str, "regex": str}
            },
        },
    }
)


def make_import_bundle_from_files(
    files: list[Path], *, multi_match: bool = False, check: bool = False
) -> ImportBundle:
    """Create an ImportBundle instance from a list of YAML files.

    :raises YAMLFileReadError: If a YAML file cannot be read.
    :raises ValidationError: If an import bundle is invalid.
    :return: An ImportBundle instance.
    """
    all_docs = []
    for file in files:
        # Load documents stored in each file.
        docs = load_yaml_file(file)

        for doc in docs:
            # Let schema handle structure/type/version validation.
            validate_doc(doc)

            # Set the original bundle YAML file path in each new document.
            doc["bundle_file"] = Path(file).resolve()

        all_docs.extend(docs)

    # Create bundle instance.
    return ImportBundle(all_docs, multi_match=multi_match, check=check)


def validate_doc(doc: Any) -> None:  # noqa: ANN401
    """Validate a single YAML document against its versioned bundle schema.

    :param doc: Dictionary with a 'version' key indicating the schema to use.
    :raises ValidationError: If validation fails.
    """
    bundle_version = None

    if isinstance(doc, dict):
        # If the document is a dict but lacks a version,
        # assume current version.
        if "version" not in doc:
            doc["version"] = BUNDLE_CURRENT_VERSION

        bundle_version = doc["version"]

    # Get schema
    bundle_schema = globals().get(f"_SCHEMA_V{bundle_version}")
    if not bundle_schema:
        msg = (
            f"Failed to validate import bundle. "
            f"Reason: unsupported version found ({bundle_version})."
        )
        raise ValidationError(msg)

    # Validate
    try:
        bundle_schema.validate(doc)
    except schema.SchemaError as e:
        msg = f"Failed to validate import bundle. Reason: {e}"
        raise ValidationError(msg) from None


def load_yaml_file(file_path: Path) -> list[Any]:
    """Load a YAML file.

    :param file_path: Path to the file to load.
    :raises YAMLFileError: If the file cannot be opened, decoded or
        parsed as valid YAML.
    :returns: A list of documents loaded from the YAML file.
    """
    try:
        with file_path.open(encoding="utf-8") as f:
            documents = list(yaml.safe_load_all(f))
    except (OSError, YAMLError, UnicodeDecodeError) as e:
        msg = f"Failed to read YAML file '{file_path}'. Reason: {e}"
        raise YAMLFileReadError(msg) from None

    return documents


def upgrade_bundle_version(x: BundleDict, to_version: int) -> BundleDict:
    """Upgrade a loaded import bundle dictionary.

    :raises ValueError: Raised if the input bundle lacks a version key or if the target version is invalid.
    :raises TypeError: Raised if the version value in the input bundle is not an integer.
    """
    # Check version
    if "version" not in x:
        msg = "No version in input bundle dictionary."
        raise ValueError(msg)
    if not isinstance(x["version"], int):
        msg = "Version of input bundle is not an integer."
        raise TypeError(msg)
    if x["version"] >= to_version:
        msg = f"Original version ({x['version']}) is greater or equal to target version ({to_version})."
        raise ValueError(msg)

    # Loop on upgrades to run
    y = x.copy()
    for v in range(x["version"], to_version):
        upgrade_fct = globals().get(f"_upgrade_from_v{v}_to_v{v + 1}")
        y = upgrade_fct(y)  # type: ignore[misc]

    return y
