import gzip
import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable
from json import JSONDecodeError
from typing import Any, Generic, TypeVar

import yaml

from genelastic.common.elastic import ElasticImportConn
from genelastic.import_data.models.data_file import DataFile

logger = logging.getLogger("genelastic")

T = TypeVar("T")


class ImporterError(Exception):
    """An error occurred while loading, validating or transforming a data file
    into JSON documents.
    """


class BaseImporter(ABC, Generic[T]):
    """Abstract base class for all importers."""

    def __init__(
        self,
        data_file: DataFile,
        es_import_conn: ElasticImportConn,
        thread_count: int = 4,
    ) -> None:
        self._data_file = data_file
        self._es_import_conn = es_import_conn
        self._thread_count = thread_count

        self._cls_name = self.__class__.__name__
        self._process_file()

    def _process_file(self) -> None:
        """Process the file before import: load, validate and transform the
        data into JSON documents.
        :raises ImporterError: If an error occurs while processing the file.
        """
        logger.debug("%s: Loading data...", self._cls_name)
        data = self._load()
        logger.debug("%s: Validating data...", self._cls_name)
        self._validate(data)
        logger.debug("%s: Transforming data...", self._cls_name)
        self._documents = self._transform(data)

    def import_docs(self) -> None:
        """Import the JSON documents into Elasticsearch."""
        logger.debug("%s: Indexing documents...", self._cls_name)
        self._es_import_conn.parallel_bulk_import(
            self._documents, self._thread_count
        )

    @property
    @abstractmethod
    def target_index(self) -> str:
        """Returns the import target index name."""

    @property
    def documents(self) -> Iterable[dict[str, Any]]:
        """Return the documents about to be indexed."""
        return self._documents

    @abstractmethod
    def _load(self) -> T:
        """Load and parse raw data from the file."""

    def _validate(self, data: T) -> None:
        """Validate the data structure (optional)."""

    @abstractmethod
    def _transform(self, data: T) -> Iterable[dict[str, Any]]:
        """Transform raw data into Elasticsearch-ready documents."""


class JSONBaseImporter(BaseImporter[Any], ABC):
    """Base importer to load JSON and gzipped JSON data files."""

    def _load(self) -> Any:  # noqa: ANN401
        try:
            if self._data_file.path.suffix == ".gz":
                logger.debug(
                    "Opening gzip-compressed file in text mode and "
                    "reading content...",
                )
                with gzip.open(
                    self._data_file.path, "rt", encoding="utf-8"
                ) as f:
                    content = f.read()
            else:
                logger.debug(
                    "Opening uncompressed file in text mode and "
                    "reading content...",
                )
                content = self._data_file.path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            raise ImporterError(e) from None

        if not content.strip():
            msg = f"JSON file '{self._data_file.path}' is empty."
            raise ImporterError(msg) from None

        try:
            data = json.loads(content)
        except JSONDecodeError as e:
            raise ImporterError(e) from None

        return data


class YAMLBaseImporter(BaseImporter[Any], ABC):
    """Base importer to load YAML data files."""

    def _load(self) -> dict[str, Any]:
        try:
            with self._data_file.path.open(encoding="utf-8") as f:
                doc: dict[str, Any] = yaml.safe_load(f)
        except (yaml.YAMLError, OSError, UnicodeDecodeError) as e:
            raise ImporterError(e) from None

        if doc is None:
            msg = f"YAML file '{self._data_file.path}' is empty."
            raise ImporterError(msg) from None

        return doc
