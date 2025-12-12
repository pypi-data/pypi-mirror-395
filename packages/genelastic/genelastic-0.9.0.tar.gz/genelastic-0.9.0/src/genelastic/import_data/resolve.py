import logging
import re

from genelastic.common.exceptions import (
    FilenamePatternResolveError,
    InvalidFilePrefixError,
)
from genelastic.common.types import Metadata
from genelastic.import_data.constants import (
    FILE_SUFFIXES_RE,
)
from genelastic.import_data.models.tags import Tags
from genelastic.import_data.patterns import FilenamePattern

logger = logging.getLogger("genelastic")


def validate_file_prefix(file_prefix: str, tags: Tags) -> None:
    """Validate a filename prefix for correctness.

    The file prefix must be non-empty and contain only defined tags,
    with no duplicates. If any of these rules are violated, an
    `InvalidFilePrefixError`` is raised.

    :param file_prefix: The filename prefix containing tags to validate
        (e.g. ``%S_%F_%W_%B_%D_%R_rep-1``).
    :param tags: The tag definitions used to verify whether tags are defined.
    :raises InvalidFilePrefixError: If the file prefix is invalid.
    """
    seen_tags = set()

    if not file_prefix:
        msg = "File prefix is empty."
        raise InvalidFilePrefixError(msg)

    # Check all tags in the file prefix:
    # they must be defined and appear only once.
    for match in re.finditer(tags.search_regex, file_prefix):
        tag_name = match.group()
        start = match.start() + 1
        end = match.end()

        if tag_name not in tags:
            msg = (
                f"File prefix '{file_prefix}' has an unknown tag "
                f"'{tag_name}' at position {start}-{end}."
            )
            raise InvalidFilePrefixError(msg)

        if tag_name in seen_tags:
            msg = (
                f"File prefix '{file_prefix}' has a duplicated tag "
                f"'{tag_name}' at position {start}-{end}."
            )
            raise InvalidFilePrefixError(msg)
        seen_tags.add(tag_name)


def resolve_analysis_id(
    file_prefix: str, tags: Tags, metadata: Metadata
) -> str:
    """Resolve an analysis identifier from a filename prefix and metadata.

    Each tag in the file prefix is replaced with its corresponding value from
    ``metadata``.

    :param file_prefix: A filename prefix containing tags
        (e.g. ``%S_%F_%W_%B_%D_%R_rep-1``).
    :param tags: The tag definitions used to map tags to metadata fields.
    :param metadata: A dictionary mapping metadata fields to their values.
    :return: The resolved analysis identifier string where all tags have been
        replaced by their metadata values.
    """
    analysis_id = file_prefix
    for match in re.finditer(tags.search_regex, file_prefix):
        tag_name = match.group()
        tag_field = tags[tag_name]["field"]
        analysis_id = analysis_id.replace(tag_name, str(metadata[tag_field]))
    return analysis_id


def resolve_filename_pattern(
    file_prefix: str,
    tags: Tags,
    metadata: Metadata,
    suffix: str | None = None,
    *,
    strict: bool = False,
) -> FilenamePattern:
    """Build a regex pattern from a filename prefix containing tags.

    Each tag in the file prefix is replaced with a named capturing group.
    The group name corresponds to the metadata field associated with the tag,
    and the group regex is chosen as follows:

    - If the field has a value in ``metadata``, the tag becomes a group that
        matches exactly this value (e.g. ``(?P<sample_name>HG0003)``).
    - Otherwise, the tag becomes a group that matches the tag's default regex
        (e.g. ``(?P<sample_name>[^_]+)``), unless ``strict=True``,
        in which case a ``FilenamePatternResolveError`` is raised.

    The resulting pattern is anchored at the start and end of the string,
    includes the optional ``suffix`` if provided, and always appends
    ``FILE_SUFFIXES_RE`` at the end.

    :param file_prefix: A string containing tags that describe the expected
        structure of filenames (e.g. ``%S_%F_%W_%B_%D_%R_rep-1``).
    :param tags: The tag definitions that map tag names to metadata fields
        and default regexes.
    :param metadata: Known metadata values used to restrict tag matches when
        available.
    :param suffix: Optional suffix to append to the regex after replacing tags.
    :param strict: If True, all tags must have a corresponding value in
        ``metadata``; otherwise a ``FilenamePatternResolveError`` exception is
        raised.
    :raises FilenamePatternResolveError: If ``strict=True`` and some tag fields
        are missing from ``metadata``.
    :return: A ``FilenamePattern`` object encapsulating the compiled regex.
    """
    filename_re = file_prefix
    undefined_fields = []

    # Expand each tag in the file prefix into a named capturing group.
    # If a metadata value is provided, the group matches it exactly.
    # Otherwise, fall back to the tag's default regex (or record it as
    # undefined if strict).
    for match in re.finditer(tags.search_regex, file_prefix):
        tag_name = match.group()
        tag_field = tags[tag_name]["field"]
        tag_regex = tags[tag_name]["regex"]

        tag_field_value = metadata.get(tag_field)
        if not tag_field_value and strict:
            undefined_fields.append(tag_field)

        tag_field_regex = f"(?P<{tag_field}>{tag_field_value or tag_regex})"
        filename_re = filename_re.replace(tag_name, tag_field_regex)

    if undefined_fields:
        formatted_fields = ", ".join(sorted(undefined_fields))
        msg = (
            f"In file prefix '{file_prefix}': "
            f"no value in metadata found for field(s): {formatted_fields}. "
            f"In single-match mode, "
            f"all fields must have a corresponding value defined."
        )
        raise FilenamePatternResolveError(msg)

    # Finalize the regex: append the optional suffix, enforce start (^) and end
    # ($) anchors, and include FILE_SUFFIXES_RE to capture allowed file
    # extensions.
    parts = [f"^{filename_re}"]
    if suffix:
        # Avoid double anchors if suffix already ends with '$'.
        parts.append(suffix.rstrip("$"))
    parts.append(f"{FILE_SUFFIXES_RE}$")
    return FilenamePattern("".join(parts))
