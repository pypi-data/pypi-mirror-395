import csv
import logging
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

import schema
import vcf
from vcf.model import _Record

from genelastic.import_data.constants import (
    QC_METRICS_SCHEMA,
    SV_METRICS_SCHEMA,
)
from genelastic.import_data.importers.importer_base import (
    BaseImporter,
    ImporterError,
    JSONBaseImporter,
    YAMLBaseImporter,
)

logger = logging.getLogger("genelastic")


class CoverageImporter(BaseImporter[Iterable[list[str]]]):
    """Importer for coverage files."""

    @property
    def target_index(self) -> str:
        """Returns the import target index name."""
        return self._es_import_conn.coverage_index

    def _load(self) -> Iterable[list[str]]:
        """Load a TSV formatted coverage file.
        :raises ImporterError: If the file could not be opened or decoded.
        """
        try:
            with self._data_file.path.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter="\t")
                try:
                    first_row = next(reader)
                except StopIteration:
                    msg = f"Coverage file '{self._data_file.path}' is empty."
                    raise ImporterError(msg) from None
                yield first_row
                yield from reader
        except (OSError, UnicodeDecodeError) as e:
            raise ImporterError(e) from None

    def _transform(self, data: Iterable[list[str]]) -> Iterable[dict[str, Any]]:
        """Transform each coverage file row into a JSON document."""
        for row in data:
            yield {
                "_index": self.target_index,
                "_source": {
                    "analysis_id": self._data_file.analysis_id,
                    "created_at": datetime.now(UTC).isoformat(),
                    "row": {
                        "chr": row[0],
                        "pos": int(row[1]) + 1,
                        "depth": int(row[2]),
                    },
                },
            }


class VCFImporter(BaseImporter[Iterable[_Record]]):
    """Importer for VCF files."""

    @property
    def target_index(self) -> str:
        """Returns the import target index name."""
        return self._es_import_conn.vcf_variants_index

    def _load(self) -> Iterable[_Record]:
        """Load a VCF file. GZ compressed VCF files are supported.
        :raises ImporterError: If the file could not be opened, decoded or is empty.
        """
        try:
            yield from vcf.Reader(
                filename=str(self._data_file.path), encoding="utf-8"
            )
        except StopIteration:
            msg = f"VCF file '{self._data_file.path}' is empty."
            raise ImporterError(msg) from None
        except (OSError, UnicodeDecodeError) as e:
            raise ImporterError(e) from None

    def _transform(self, data: Iterable[_Record]) -> Iterable[dict[str, Any]]:
        """Transform each VCF file record into a JSON document."""
        for record in data:
            # Fix values
            if not record.CHROM.startswith("chr"):
                if record.CHROM.lower().startswith("chr"):
                    record.CHROM = "chr" + record.CHROM[3:]
                else:
                    record.CHROM = "chr" + record.CHROM

            # Build document
            alt = [x if x is None else x.type for x in record.ALT]

            yield {
                "_index": self.target_index,
                "_source": {
                    "created_at": datetime.now(UTC).isoformat(),
                    "analysis_id": self._data_file.analysis_id,
                    "record": {
                        "type": "vcf",
                        "chr": record.CHROM,
                        "pos": record.POS,
                        "alt": alt,
                        "info": record.INFO,
                    },
                },
            }


class QCImporter(YAMLBaseImporter):
    """Importer for QC YAML metrics files."""

    @property
    def target_index(self) -> str:
        """Returns the import target index name."""
        return self._es_import_conn.qc_metrics_index

    def _validate(self, data: dict[str, Any]) -> None:
        """Validate the YAML document against the expected schema.

        :raises ImporterError: If the file format is invalid.
        """
        try:
            QC_METRICS_SCHEMA.validate(data)
        except schema.SchemaError as e:
            raise ImporterError(e) from None

    def _transform(self, data: dict[str, Any]) -> Iterable[dict[str, Any]]:
        """Transform a QC YAML metrics file into a JSON document."""
        yield {
            "_index": self.target_index,
            "_source": {
                "created_at": datetime.now(UTC).isoformat(),
                "analysis_id": self._data_file.analysis_id,
                "metrics": data,
            },
        }


class SmallvarImporter(JSONBaseImporter):
    """Importer for SmallVar JSON metrics files."""

    @property
    def target_index(self) -> str:
        """Returns the import target index name."""
        return self._es_import_conn.smallvar_metrics_index

    def _transform(self, data: dict[str, Any]) -> Iterable[dict[str, Any]]:
        """Transform a SmallVar metrics file into JSON documents."""
        try:
            for metric in data["metrics"]:
                values_count = len(metric["data"][0]["values"])

                metric_id = metric["id"].replace(".", "_").lower()

                for i in range(values_count):
                    doc = {}
                    for item in metric["data"]:
                        # Attribute name should not use '.' as it refers
                        # to nested objects.
                        label = item["label"].replace(".", "_")
                        doc[label] = item["values"][i]

                    yield {
                        "_index": self.target_index,
                        "_source": {
                            "created_at": datetime.now(UTC).isoformat(),
                            "analysis_id": self._data_file.analysis_id,
                            "metric_id": metric_id,
                            "metrics": doc,
                        },
                    }
        except KeyError as e:
            msg = (
                f"Smallvar metrics file '{self._data_file.path}' "
                f"is invalid: missing key {e}."
            )
            raise ImporterError(msg) from None


class SVImporter(JSONBaseImporter):
    """Importer for SV JSON metrics files."""

    @property
    def target_index(self) -> str:
        """Returns the import target index name."""
        return self._es_import_conn.sv_metrics_index

    def _validate(self, data: dict[str, Any]) -> None:
        """Validate the YAML document against the expected schema.

        :raises ImporterError: If the file format is invalid.
        """
        try:
            SV_METRICS_SCHEMA.validate(data)
        except schema.SchemaError as e:
            raise ImporterError(e) from None

    def _transform(self, data: dict[str, Any]) -> Iterable[dict[str, Any]]:
        """Transform a SV metrics file into a JSON document."""
        for region in data["regions"]:
            for result in region["results"]:
                # Convert all values to float to avoid mapping issues.
                result["precision"] = float(result["precision"])
                result["recall"] = float(result["recall"])
                result["f1"] = float(result["f1"])

        yield {
            "_index": self.target_index,
            "_source": {
                "created_at": datetime.now(UTC).isoformat(),
                "analysis_id": self._data_file.analysis_id,
                "metrics": data,
            },
        }
