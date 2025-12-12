import logging
import typing
from typing import ClassVar, TypedDict

from genelastic.common.elastic import ElasticImportConn
from genelastic.import_data.importers.importer_base import (
    BaseImporter,
    ImporterError,
)
from genelastic.import_data.importers.importer_types import (
    CoverageImporter,
    QCImporter,
    SmallvarImporter,
    SVImporter,
    VCFImporter,
)
from genelastic.import_data.models.data_file import DataFile

logger = logging.getLogger("genelastic")


class _ImporterConfig(TypedDict):
    """Internal configuration mapping an importer class to its supported file
    extensions.
    """

    cls: type[BaseImporter[typing.Any]]
    extensions: set[str]


class ImporterFactory:
    """Factory to create a BaseImporter instance based on the file's
    extension and type.
    """

    _importers: ClassVar[dict[str, _ImporterConfig]] = {
        "vcf": _ImporterConfig(cls=VCFImporter, extensions={"vcf"}),
        "cov": _ImporterConfig(cls=CoverageImporter, extensions={"cov"}),
        "qc": _ImporterConfig(cls=QCImporter, extensions={"yaml", "yml"}),
        "smallvar": _ImporterConfig(cls=SmallvarImporter, extensions={"json"}),
        "sv": _ImporterConfig(cls=SVImporter, extensions={"json"}),
    }

    @staticmethod
    def get_importer(
        data_file: DataFile,
        es_import_conn: ElasticImportConn,
        thread_count: int = 4,
    ) -> BaseImporter[typing.Any]:
        """Create an appropriate BaseImporter instance based on the data
        file's extension and type.

        :param data_file: Data file to process and import.
        :param es_import_conn: Elasticsearch import connector instance.
        :param thread_count: Number of threads to use for parallel data file
            import.
        :return: An instance of the appropriate BaseImporter subclass.
        :raises ImporterError: If the data file extension or type is invalid.
        """
        try:
            importer = ImporterFactory._importers[data_file.type]
        except KeyError:
            supported_types = sorted(
                [f"'{i_type}'" for i_type in ImporterFactory._importers]
            )
            msg = (
                f"Data file '{data_file.path.name}': no importer for type "
                f"'{data_file.type}'. Supported types are: "
                f"{', '.join(supported_types)}."
            )
            raise ImporterError(msg) from None

        if data_file.ext not in importer["extensions"]:
            supported_exts = sorted(
                [f"'{ext}'" for ext in importer["extensions"]]
            )
            msg = (
                f"Data file '{data_file.path.name}': extension "
                f"'{data_file.ext}' not supported by importer "
                f"{importer['cls'].__name__}. Supported extensions are: "
                f"{', '.join(supported_exts)}."
            )
            raise ImporterError(msg)

        return importer["cls"](data_file, es_import_conn, thread_count)
