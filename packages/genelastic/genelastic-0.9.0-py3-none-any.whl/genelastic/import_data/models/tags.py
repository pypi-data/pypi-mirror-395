import logging
import re
import typing
from collections import UserDict

from genelastic.common.exceptions import TagsDefinitionError
from genelastic.common.types import BundleDict
from genelastic.import_data.constants import (
    DEFAULT_TAG2FIELD,
    DEFAULT_TAG_DELIMITER_END,
    DEFAULT_TAG_DELIMITER_START,
)

logger = logging.getLogger("genelastic")


class Tags(UserDict[str, dict[str, str]]):
    """Represents a set of tags used to extract metadata from filenames.

    Each tag maps a name to a metadata field and a regex pattern, supporting
    custom delimiters. This class combines default tags (``DEFAULT_TAG2FIELD``)
    with optional user-defined tags, and provides utilities for searching,
    accessing, and resolving tags in filename patterns.
    """

    def __init__(
        self,
        delimiter_start: str | None = None,
        delimiter_end: str | None = None,
        match: dict[str, dict[str, str]] | None = None,
    ) -> None:
        """Initialize a Tags instance.

        :param delimiter_start: Optional character prepended to all tag names.
            Defaults to ``DEFAULT_TAG_DELIMITER_START``.
        :param delimiter_end: Optional character appended to all tag names.
            Defaults to ``DEFAULT_TAG_DELIMITER_END``.
        :param match: Optional dictionary of user-defined tags. Overrides
            ``DEFAULT_TAG2FIELD`` if keys overlap.
        """
        super().__init__()

        if delimiter_start is None:
            self._delimiter_start = DEFAULT_TAG_DELIMITER_START
        else:
            if not self.validate_tag_delimiter(delimiter_start):
                msg = (
                    "A tag delimiter start should contain only one special "
                    "character, excluding the following: (, ), ?, <, >."
                )
                raise TagsDefinitionError(msg)
            self._delimiter_start = delimiter_start

        if delimiter_end is None:
            self._delimiter_end = DEFAULT_TAG_DELIMITER_END
        else:
            if not self.validate_tag_delimiter(delimiter_end):
                msg = (
                    "A tag delimiter end should contain only one special "
                    "character, excluding the following: (, ), ?, <, >."
                )
                raise TagsDefinitionError(msg)
            self._delimiter_end = delimiter_end

        # Combine default tags with user-provided tags. User-defined ones takes
        # precedence.
        effective_match = DEFAULT_TAG2FIELD | (match or {})

        # Store each tag in the dictionary using the full name
        # (delimiter start + tag name + delimiter end).
        for tag_name, tag_attrs in effective_match.items():
            if not self.validate_tag_name(tag_name):
                msg = (
                    f"Invalid tag '{tag_name}': its name should contain at "
                    f"least one alphanumeric character: a-z, A-Z and 0-9."
                )
                raise TagsDefinitionError(msg)

            for mandatory_key in ("field", "regex"):
                if mandatory_key not in tag_attrs:
                    msg = (
                        f"Invalid tag '{tag_name}': mandatory key "
                        f"'{mandatory_key}' missing."
                    )
                    raise TagsDefinitionError(msg)

            tag = f"{self._delimiter_start}{tag_name}{self._delimiter_end}"
            self[tag] = tag_attrs

        logger.info(
            "The following tags will be used "
            "to extract metadata from filenames : %s",
            self,
        )

    @property
    def delimiter_start(self) -> str:
        """Return the tag delimiter start. Defaults to
        ``DEFAULT_TAG_DELIMITER_START``.
        """
        return self._delimiter_start

    @property
    def delimiter_end(self) -> str:
        """Return the tag delimiter end. Defaults to
        ``DEFAULT_TAG_DELIMITER_END``.
        """
        return self._delimiter_end

    @property
    def search_regex(self) -> str:
        """Return a regex pattern to search for tags inside a string.

        This regex matches any tag using the current start and end delimiters.
        Used for filename prefixes validation or resolving tags into regex
        patterns.
        """
        return (
            re.escape(self._delimiter_start)
            + r"[a-zA-Z0-9]+"
            + re.escape(self._delimiter_end)
        )

    @classmethod
    def from_dict(cls, bundle: BundleDict) -> typing.Self:
        """Create tags from a bundle dict."""
        delimiter_start, delimiter_end = None, None

        if "tags" not in bundle:
            msg = (
                "Could not create a Tags object: bundle does not define tags "
                "(root key 'tags' missing)."
            )
            raise TagsDefinitionError(msg)

        tags = bundle["tags"]
        match = tags.get("match")
        tag_delimiter = tags.get("delimiter")

        if tag_delimiter:
            delimiter_start = tag_delimiter.get("start")
            delimiter_end = tag_delimiter.get("end")

        return cls(
            delimiter_start=delimiter_start,
            delimiter_end=delimiter_end,
            match=match,
        )

    @staticmethod
    def validate_tag_delimiter(s: str) -> bool:
        """A tag delimiter should only contain one special character,
        excluding the following: (, ), ?, <, >.
        """
        if len(s) != 1:
            return False

        return not re.match(r"^[\w()<>?]$", s)

    @staticmethod
    def validate_tag_name(s: str) -> bool:
        """A tag name should contain at least one alphanumeric character:
        ``a-z``, ``A-Z`` and ``0-9``.

        :return: True if the tag name is valid, False otherwise.
        """
        if len(s) < 1:
            return False

        return bool(re.match(r"^[^_\W]+$", s))
