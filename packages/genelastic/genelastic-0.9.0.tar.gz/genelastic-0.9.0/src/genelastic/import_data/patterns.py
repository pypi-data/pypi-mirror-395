import re
from pathlib import Path

from genelastic.common.types import Metadata
from genelastic.import_data.constants import TOOLS_SUFFIX_RE


class FilenamePattern:
    """Utility class to extract metadata from filenames based on a regex
    pattern.
    """

    def __init__(self, pattern: str) -> None:
        """Initializes a FilenamePattern instance.

        :param pattern: The regex pattern used to extract metadata from
        filenames.
        """
        self._re = re.compile(pattern)

    def extract_metadata(self, filename: str) -> Metadata:
        """Extracts metadata from the given filename using the defined pattern.

        :param filename: The filename from which metadata should be extracted.
        :raises RuntimeError: If the filename does not match the pattern.
        :returns: A dictionary containing the extracted metadata.
        """
        m = self._re.search(filename)
        if not m:
            msg = (
                f"Failed parsing filename '{filename}' with pattern "
                f"'{self._re.pattern}'."
            )
            raise RuntimeError(msg)

        # Convert necessary values.
        metadata = m.groupdict()
        if "cov_depth" in metadata:
            metadata["cov_depth"] = int(metadata["cov_depth"])

        return metadata

    def matches_pattern(self, filename: str) -> bool:
        """Checks whether the given filename matches the defined pattern.

        :param filename: The filename to check.
        :returns: True if the filename matches the pattern, False otherwise.
        """
        return bool(self._re.fullmatch(filename))


class MetricsPattern:
    """Utility class to extract tool/version metadata from filenames with a
    ``.metrics`` suffix.
    """

    @staticmethod
    def extract_metadata(file: Path) -> list[dict[str, str]] | None:
        """Extracts metadata from a filename based on the ``.metrics`` suffix.

        :param file: The path to the file to be analyzed.
        :raises RuntimeError: If the suffix is malformed or cannot be parsed.
        :returns:
            - None if the file does not have a ``.metrics`` prefix,
            - An empty list if the prefix is present but no metadata is found,
            - A list of dictionaries with ``tool`` and ``version`` keys if
                metadata is extracted.
        """
        if not file.suffixes or not file.suffixes[0].startswith(".metrics"):
            return None

        tools_str = file.suffixes[0].replace(".metrics", "")
        matches = list(re.finditer(TOOLS_SUFFIX_RE, tools_str))
        matched_str = "".join(m.group(0) for m in matches)

        if matched_str != tools_str:
            msg = (
                f"Failed extracting metrics from filename '{file}': "
                f"'{tools_str}' does not fully match pattern "
                f"'{TOOLS_SUFFIX_RE}'."
            )
            raise RuntimeError(msg)

        return [
            {
                "tool": m.group("tool"),
                "version": m.group("version").replace("-", "."),
            }
            for m in matches
        ]
