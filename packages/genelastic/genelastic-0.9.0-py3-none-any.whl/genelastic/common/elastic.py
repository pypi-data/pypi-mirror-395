import datetime
import logging
import time
from collections.abc import Iterable
from typing import Any

import elastic_transport
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from tqdm import tqdm

from .exceptions import DBIntegrityError
from .types import Bucket

logger = logging.getLogger("genelastic")


class ElasticConn:
    """Base class for Elasticsearch connectors.

    This class provides common functionality for managing index names and
    establishing a connection to an Elasticsearch server. It is not
    intended to be instantiated directly. Instead, use one of its
    subclasses:

    - ``ElasticQueryConn`` for performing search and query operations,
    - ``ElasticImportConn`` for importing and indexing data.

    :param url: URL of the Elasticsearch host.
    :param fingerprint: SHA256 certificate fingerprint for secure HTTPS
        connection.
    :param index_prefix: Prefix to prepend to all index names.
    :param dry_run: Dry run mode; 0 = execute queries, >=1 = skip queries,
        no Elasticsearch client is created.
    :param kwargs: Additional keyword arguments passed to the Elasticsearch
        client.
    :raises SystemExit: If connection or authentication to Elasticsearch
        fails.
    """

    def __init__(
        self,
        url: str,
        fingerprint: str,
        index_prefix: str,
        dry_run: int = 0,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        self._index_prefix = index_prefix
        self._dry_run = dry_run
        self._init_indices()
        self._client = None

        if self._dry_run > 0:
            msg = (
                f"[Dryrun] {self.__class__.__name__} "
                f"instantiated without an Elasticsearch client."
            )
            logger.info(msg)
            return

        try:
            self._client = Elasticsearch(
                url,
                ssl_assert_fingerprint=fingerprint,
                # Verify cert only when the fingerprint is not None.
                verify_certs=bool(fingerprint),
                **kwargs,
            )
            self._client.info()
        except (
            elastic_transport.TransportError,
            elasticsearch.AuthenticationException,
        ) as e:
            raise SystemExit(e) from e

    def _init_indices(self) -> None:
        # Core indices.
        self._analyses_index = f"{self._index_prefix}_analyses"
        self._data_files_index = f"{self._index_prefix}_data_files"
        # Content indices.
        self._vcf_variants_index = f"{self._index_prefix}_vcf_variants"
        self._coverage_index = f"{self._index_prefix}_coverage"
        # Metrics indices.
        self._qc_metrics_index = f"{self._index_prefix}_qc_metrics"
        self._sv_metrics_index = f"{self._index_prefix}_sv_metrics"
        self._smallvar_metrics_index = f"{self._index_prefix}_smallvar_metrics"
        # Processes indices.
        self._bi_processes_index = f"{self._index_prefix}_bi_processes"
        self._wet_processes_index = f"{self._index_prefix}_wet_processes"

    @property
    def client(self) -> Elasticsearch | None:
        """Elasticsearch client."""
        return self._client

    @property
    def analyses_index(self) -> str:
        """Index for analyses."""
        return self._analyses_index

    @property
    def data_files_index(self) -> str:
        """Index for data files."""
        return self._data_files_index

    @property
    def vcf_variants_index(self) -> str:
        """Index for VCF variants."""
        return self._vcf_variants_index

    @property
    def coverage_index(self) -> str:
        """Index for coverage data."""
        return self._coverage_index

    @property
    def qc_metrics_index(self) -> str:
        """Index for quality control metrics."""
        return self._qc_metrics_index

    @property
    def sv_metrics_index(self) -> str:
        """Index for structural variant (SV) metrics."""
        return self._sv_metrics_index

    @property
    def smallvar_metrics_index(self) -> str:
        """Index for small variant (SNV/indel) metrics."""
        return self._smallvar_metrics_index

    @property
    def bi_processes_index(self) -> str:
        """Index for bioinformatics processes."""
        return self._bi_processes_index

    @property
    def wet_processes_index(self) -> str:
        """Index for wet lab processes."""
        return self._wet_processes_index


class ElasticImportConn(ElasticConn):
    """Connector to import data into an Elasticsearch database."""

    @staticmethod
    def _handle_bulk_response(response: Iterable[tuple[bool, Any]]) -> None:
        success_count = 0
        failure_count = 0
        total_items = 0

        start_time = time.perf_counter()

        for success, info in tqdm(
            response,
            desc="Import progress",
            unit=" documents",
            unit_scale=True,  # Scale large counts for easier readability (e.g., 1200 => 1.2k).
            leave=False,  # Hide finished bars to keep console clean.
        ):
            total_items += 1
            if success:
                success_count += 1
                logger.trace(info)  # type: ignore[attr-defined]
            else:
                failure_count += 1
                logger.error("Failed to import item: %s", info)

        elapsed = time.perf_counter() - start_time
        logger.info(
            "  - Imported %d document(s) (ok: %d, failed: %d) in %s (%f docs/s).",
            total_items,
            success_count,
            failure_count,
            datetime.timedelta(seconds=elapsed),
            total_items / elapsed if elapsed > 0 else 0,
        )

    def bulk_import(self, documents: Iterable[dict[str, Any]]) -> None:
        """Import documents in streaming mode, suitable for low to medium
        document volumes.

        :param documents: documents to index.
        """
        if not self.client:
            logger.info("[Dryrun] bulk_import: no Elasticsearch client.")
            return

        self._handle_bulk_response(
            elasticsearch.helpers.streaming_bulk(
                self.client,
                actions=documents,
                raise_on_error=False,
            )
        )

    def parallel_bulk_import(
        self,
        documents: Iterable[dict[str, Any]],
        thread_count: int = 4,
    ) -> None:
        """Import documents in parallel mode, suitable for large document
        volumes.

        :param documents: documents to index.
        :param thread_count: Number of threads to use for parallel bulk import.
        """
        if not self.client:
            logger.info(
                "[Dryrun] parallel_bulk_import: no Elasticsearch client."
            )
            return

        logger.debug("parallel_bulk_import: using %s thread(s).", thread_count)

        self._handle_bulk_response(
            elasticsearch.helpers.parallel_bulk(
                self.client,
                actions=documents,
                raise_on_error=False,
                thread_count=thread_count,
            )
        )


class ElasticQueryConn(ElasticConn):
    """Connector to query data from an Elasticsearch database."""

    def get_indices(self) -> Any | str:  # noqa: ANN401
        """Return all indices."""
        if not self.client:
            logger.info("[Dryrun] get_indices: no Elasticsearch client.")
            return []

        return self.client.cat.indices(format="json").body

    def get_document_by_id(self, index: str, document_id: str) -> Any | str:  # noqa: ANN401
        """Return a document by its ID."""
        if not self.client:
            logger.info("[Dryrun] get_document_by_id: no Elasticsearch client.")
            return {}

        return self.client.get(index=index, id=document_id).body

    def run_composite_aggregation(
        self, index: str, query: dict[str, Any]
    ) -> list[Bucket]:
        """Executes a composite aggregation on an Elasticsearch index and
        returns all paginated results.

        :param index: Name of the index to query.
        :param query: Aggregation query to run.
        :return: List of aggregation results.
        """
        if not self.client:
            logger.info(
                "[Dryrun] run_composite_aggregation: "
                "no Elasticsearch client."
            )
            return []

        # Extract the aggregation name from the query dict.
        agg_name = next(iter(query["aggs"]))
        all_buckets: list[Bucket] = []

        response = self.client.search(index=index, body=query)

        while True:
            # Extract buckets from the response.
            buckets: list[Bucket] = response["aggregations"][agg_name][
                "buckets"
            ]
            all_buckets.extend(buckets)

            # Check if there are more results to fetch.
            if "after_key" in response["aggregations"][agg_name]:
                after_key = response["aggregations"][agg_name]["after_key"]
                query["aggs"][agg_name]["composite"]["after"] = after_key

                # Fetch the next page of results.
                logger.debug("Running query %s on index '%s'.", query, index)
                response = self.client.search(index=index, body=query)
            else:
                break

        return all_buckets

    def get_field_values(self, index: str, field_name: str) -> set[str]:
        """Return a set of values for a given field."""
        if not self.client:
            logger.info("[Dryrun] get_field_values: no Elasticsearch client.")
            return set()

        values = set()

        query = {
            "size": 0,
            "aggs": {
                "get_field_values": {
                    "composite": {
                        "sources": {
                            "values": {
                                "terms": {"field": f"{field_name}.keyword"}
                            }
                        },
                        "size": 1000,
                    }
                }
            },
        }

        buckets: list[Bucket] = self.run_composite_aggregation(index, query)

        for bucket in buckets:
            values.add(bucket["key"]["values"])

        return values

    def search_by_field_value(
        self, index: str, field: str, value: str
    ) -> dict[str, Any] | None:
        """Search a document by a value for a certain field."""
        if not self.client:
            logger.info(
                "[Dryrun] search_by_field_value: no Elasticsearch client."
            )
            return {}

        logger.info(
            "Searching for field '%s' with value '%s' inside index '%s'.",
            field,
            value,
            index,
        )
        search_query = {
            "query": {
                "term": {
                    f"{field}.keyword": value,
                }
            }
        }

        response = self.client.search(index=index, body=search_query)

        try:
            return response["hits"]["hits"][0]["_source"]  # type: ignore[no-any-return]
        except KeyError:
            return None

    def ensure_unique(self, index: str, field: str) -> None:
        """Ensure that all values of a field in an index are all unique.

        :param index: Name of the index.
        :param field: Field name to check for value uniqueness.
        :raises genelastic.common.DBIntegrityError:
            Some values of the given field are duplicated in the index.
        """
        if not self.client:
            logger.info("[Dryrun] ensure_unique: no Elasticsearch client.")
            return

        logger.info(
            "Ensuring that the field '%s' in the index '%s' only contains unique values...",
            field,
            index,
        )
        query = {
            "size": 0,
            "aggs": {
                "duplicate_proc_ids": {
                    "terms": {
                        "field": f"{field}.keyword",
                        "size": 10000,
                        "min_doc_count": 2,
                    }
                }
            },
        }
        buckets: list[Bucket] = self.run_composite_aggregation(index, query)
        duplicated_processes: set[str] = {
            str(bucket["key"]) for bucket in buckets
        }

        if len(duplicated_processes) > 0:
            msg = f"Found non-unique value for field {field} in index '{index}': {', '.join(duplicated_processes)}."
            raise DBIntegrityError(msg)

        logger.info(
            "All values of field '%s' in index '%s' are unique.", field, index
        )

    def get_all_documents_kv(self, index: str) -> list[dict[str, Any]]:
        """Return all key-value pairs from all documents in an index."""
        if not self.client:
            logger.info(
                "[Dryrun] get_all_documents_kv: no Elasticsearch client."
            )
            return []

        def flatten(
            d: dict[str, Any], parent_key: str = "", sep: str = "."
        ) -> dict[str, Any]:
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(flatten(v, new_key, sep=sep))
                else:
                    items[new_key] = v
            return items

        results = []
        for doc in scan(
            self.client, index=index, query={"query": {"match_all": {}}}
        ):
            source = doc.get("_source", {})
            flattened = flatten(source)
            results.append(flattened)

        return results

    def get_all_documents_kv_count(
        self, index: str, field: str, size: int = 10000
    ) -> dict[str, int]:
        """Return a dictionary with the count of each unique value for an index field."""
        if not self.client:
            logger.info(
                "[Dryrun] get_all_documents_kv_count: no Elasticsearch client."
            )
            return {}

        query = {
            "size": 0,
            "aggs": {
                "value_counts": {
                    "terms": {
                        "field": f"{field}.keyword",
                        "size": size,
                    }
                }
            },
        }

        response = self.client.search(index=index, body=query)
        buckets = response["aggregations"]["value_counts"]["buckets"]
        return {bucket["key"]: bucket["doc_count"] for bucket in buckets}

    def get_process(self, index: str, proc_id: str) -> dict[str, Any] | None:
        """Get details about a specific process."""
        if not self.client:
            logger.info("[Dryrun] get_process: no Elasticsearch client.")
            return {}

        query = {
            "query": {"term": {"proc_id.keyword": {"value": proc_id}}},
            "size": 1,
        }

        response = self.client.search(index=index, body=query)

        result = response["hits"]["hits"]
        return result[0]["_source"] if result else None

    def list_analyses_by_process(self, term: str, proc_id: str) -> list[str]:
        """Route to list analyses that contain the specified process."""
        if not self.client:
            logger.info(
                "[Dryrun] list_analyses_by_process: " "no Elasticsearch client."
            )
            return []

        search_query = {
            "query": {
                "term": {
                    f"metadata.{term}.keyword": proc_id,
                }
            }
        }
        response = self.client.search(
            index=self.analyses_index, body=search_query
        )
        return [
            hit["_source"]["analysis_id"] for hit in response["hits"]["hits"]
        ]

    def list_analyses_by_process_esql(
        self,
        term: str,
        proc_id: str,
    ) -> list[dict[str, str]]:
        """ES|QL route to list analyses that contain the specified process."""
        if not self.client:
            logger.info(
                "[Dryrun] list_analyses_by_process_esql: no Elasticsearch client."
            )
            return []

        query = (
            f"FROM {self.analyses_index} | "
            f"WHERE metadata.{term} == ? | "
            f"KEEP analysis_id"
        )

        response = self.client.esql.query(
            body={"query": query, "params": [proc_id]},
        )

        columns_name = [column["name"] for column in response["columns"]]
        return [
            dict(zip(columns_name, value, strict=False))
            for value in response["values"]
        ]

    def list_analyses_by_process_sql(
        self,
        term: str,
        proc_id: str,
    ) -> list[dict[str, str]]:
        """SQL route to list analyses that contain the specified process."""
        if not self.client:
            logger.info(
                "[Dryrun] list_analyses_by_process_sql: no Elasticsearch client."
            )
            return []

        # ruff: noqa: S608
        query = (
            f"SELECT analysis_id "
            f"FROM {self.analyses_index} "
            f"WHERE metadata.{term} = ?"
        )

        response = self.client.sql.query(
            body={"query": query, "params": [proc_id]}
        )

        columns_name = [column["name"] for column in response["columns"]]
        return [
            dict(zip(columns_name, row, strict=False))
            for row in response["rows"]
        ]
