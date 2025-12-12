class DBIntegrityError(Exception):
    """Exception raised when the database content does not match the expected
    data schema.
    """


class DataFileCollectorError(Exception):
    """Exception raised when an error occur while collecting analysis data
    files.
    """


class InvalidFilePrefixError(Exception):
    """Exception raised when a file prefix is invalid."""


class FilenamePatternResolveError(Exception):
    """Exception raised when a filename pattern could not be resolved."""


class UniqueListDuplicateError(Exception):
    """Exception raised when trying to add an item that already exist in the
    list.
    """


class TagsDefinitionError(Exception):
    """Exception raised when the tags definition is invalid."""


class YAMLFileReadError(Exception):
    """Exception raised when a YAML file cannot be opened or parsed."""


class ValidationError(Exception):
    """Exception raised when a YAML document fails schema validation."""
