import typing
from importlib.metadata import version as get_version

from flask import Response, current_app, jsonify

if typing.TYPE_CHECKING:
    from genelastic.common.elastic import ElasticQueryConn


def indexes() -> tuple[Response, int]:
    """List all Elasticsearch indexes."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    return jsonify({"result": es_query_conn.get_indices()}), 200


def retrieve_document_by_index_and_id(
    index_id: str, document_id: str
) -> tuple[Response, int]:
    """Retrieve a document by its index name and ID."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.get_document_by_id(index_id, document_id)
    return jsonify({"result": result}), 200


def wet_processes() -> tuple[Response, int]:
    """List wet processes."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]

    result = es_query_conn.get_field_values(
        es_query_conn.wet_processes_index,
        "proc_id",
    )
    return jsonify({"result": list(result)}), 200


def get_wet_process(proc_id: str) -> tuple[Response, int]:
    """Retrieve details of a specific wet process by its ID."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.get_process(
        es_query_conn.wet_processes_index, proc_id
    )

    if not result:
        return jsonify(
            {
                "error": {
                    "message": f"Wet process with proc_id "
                    f"'{proc_id}' not found.",
                    "type": "NotFoundError",
                }
            }
        ), 404

    return jsonify({"result": result}), 200


def list_analyses_by_wet_process(proc_id: str) -> tuple[Response, int]:
    """List analyses that contain the specified wet process."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.list_analyses_by_process("wet_process", proc_id)
    return jsonify({"result": result}), 200


def bi_processes() -> tuple[Response, int]:
    """List bioinformatics processes."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.get_field_values(
        es_query_conn.bi_processes_index, "proc_id"
    )
    return jsonify({"result": list(result)}), 200


def get_bi_process(proc_id: str) -> tuple[Response, int]:
    """Retrieve details of a specific bioinformatics process by its ID."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.get_process(
        es_query_conn.bi_processes_index, proc_id
    )

    if not result:
        return jsonify(
            {
                "error": {
                    "message": f"Bioinformatics process with proc_id "
                    f"'{proc_id}' not found.",
                    "type": "NotFoundError",
                }
            }
        ), 404

    return jsonify({"result": result}), 200


def list_analyses_by_bi_process(proc_id: str) -> tuple[Response, int]:
    """List analyses that contain the specified bioinformatics process"""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.list_analyses_by_process("bi_process", proc_id)
    return jsonify({"result": result}), 200


def list_analyses_by_bi_process_esql(
    proc_id: str,
) -> tuple[Response, int]:
    """List analyses that contain the specified bioinformatics process using
    an ES|QL query.
    """
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.list_analyses_by_process_esql("bi_process", proc_id)
    return jsonify({"result": result}), 200


def list_analyses_by_bi_process_sql(
    proc_id: str,
) -> tuple[Response, int]:
    """List analyses that contain the specified bioinformatics process using
    an SQL query.
    """
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.list_analyses_by_process_sql("bi_process", proc_id)
    return jsonify({"result": result}), 200


def analyses() -> tuple[Response, int]:
    """List analyses."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]

    result = es_query_conn.get_field_values(
        es_query_conn.analyses_index, "analysis_id"
    )
    return jsonify({"result": list(result)}), 200


# TODO(?): All the following functions are commented because it is currently
# unclear what they do and if they are still needed.

# def list_snv_documents() -> Response:
#     """Route to list all documents containing a mutation at a single position (SNV)."""
#     es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
#     index_pattern = "genelastic-file-*"
#     target_value = "SNV"
#
#     search_query = {
#         "aggs": {
#             "snv_docs": {
#                 "composite": {
#                     "sources": [
#                         {"alt_value": {"terms": {"field": "alt.keyword"}}}
#                     ],
#                     "size": 1000,
#                 }
#             }
#         },
#         "query": {"term": {"alt.keyword": target_value}},
#         "size": 0,
#     }
#
#     all_documents = []
#     buckets = es_query_conn.run_composite_aggregation(
#         index_pattern, search_query
#     )
#
#     for bucket in buckets:
#         alt_value = bucket["key"]["alt_value"]
#
#         search_query_docs = {
#             "query": {"term": {"alt.keyword": alt_value}},
#             "size": 1000,
#         }
#
#         response = es_query_conn.client.search(
#             index=index_pattern, body=search_query_docs
#         )
#
#         all_documents.extend(response["hits"]["hits"])
#
#     return jsonify(all_documents)
#
#
# def build_snv_search_query(
#     target_alt: str, target_svtype: str
# ) -> dict[str, Any]:
#     """Helper function to build the search query for SNV documents with specified alt and SVTYPE."""
#     return {
#         "query": {
#             "bool": {
#                 "must": [
#                     {"term": {"alt.keyword": target_alt}},
#                     {"term": {"info.SVTYPE.keyword": target_svtype}},
#                 ]
#             }
#         },
#         "size": 1000,
#     }
#
#
# def build_snv_mutation_search_query(
#     target_svtypes: list[str],
# ) -> dict[str, Any]:
#     """Helper function to build the search query for SNV mutations with specified SVTYPE values."""
#     return {
#         "query": {
#             "bool": {
#                 "must": [
#                     {"term": {"alt.keyword": "SNV"}},
#                     {"terms": {"info.SVTYPE.keyword": target_svtypes}},
#                 ]
#             }
#         },
#         "size": 1000,
#     }
#
#
# def list_snv_insertion_documents() -> Response:
#     """Route to list all documents containing an insertion (INS) at a single position (SNV)."""
#     es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
#
#     index_pattern = "genelastic-file-*"
#     search_query = build_snv_search_query(target_alt="SNV", target_svtype="INS")
#
#     response = es_query_conn.client.search(
#         index=index_pattern, body=search_query
#     )
#
#     all_documents = [hit["_source"] for hit in response["hits"]["hits"]]
#
#     return jsonify(all_documents)
#
#
# def list_snv_deletion_documents() -> Response:
#     """Route to list all documents containing a deletion (DEL) at a single position (SNV)."""
#     es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
#     index_pattern = "genelastic-file-*"
#     search_query = build_snv_search_query(target_alt="SNV", target_svtype="DEL")
#
#     response = es_query_conn.client.search(
#         index=index_pattern, body=search_query
#     )
#
#     all_documents = [hit["_source"] for hit in response["hits"]["hits"]]
#
#     return jsonify(all_documents)
#
#
# def list_snv_mutation_documents() -> Response:
#     """Route to list all documents containing a mutation at a single position (SNV)."""
#     es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
#     index_pattern = "genelastic-file-*"
#     target_svtypes = ["INS", "DEL"]
#
#     search_query = build_snv_mutation_search_query(
#         target_svtypes=target_svtypes
#     )
#
#     response = es_query_conn.client.search(
#         index=index_pattern, body=search_query
#     )
#
#     all_documents = [hit["_source"] for hit in response["hits"]["hits"]]
#
#     return jsonify(all_documents)


def version() -> tuple[Response, int]:
    """Obtain genelastic package version used by the server."""
    top_level_package = __package__.split(".")[0]
    return jsonify({"result": {"version": get_version(top_level_package)}}), 200


def key_value_analyses_index() -> tuple[Response, int]:
    """Route to return all key-values in an index."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    result = es_query_conn.get_all_documents_kv(es_query_conn.analyses_index)
    return jsonify({"result": result}), 200


def count_key_value_analyses_index() -> tuple[Response, int]:
    """Route to return the key-value counts for fields in an index."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    fields = [
        "metadata.barcode",
        "metadata.reference_genome",
        "metadata.sample_name",
        "metadata.source",
    ]

    result: dict[str, dict[str, int]] = {}
    for field in fields:
        result[field] = es_query_conn.get_all_documents_kv_count(
            es_query_conn.analyses_index, field
        )

    return jsonify({"result": result}), 200


def count_wet_process_fields() -> tuple[Response, int]:
    """Return key-value counts for each field in wet_process documents."""
    # BUG: this does not work for numeric values.
    # error_rate_expected, fragmentation, reads_size will always return an
    # empty dict.
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    wet_fields = [
        "metadata.amplification",
        "metadata.error_rate_expected",
        "metadata.flowcell_type",
        "metadata.fragmentation",
        "metadata.generic_kit",
        "metadata.input_type",
        "metadata.library_kit",
        "metadata.manufacturer",
        "metadata.reads_size",
        "metadata.sequencer",
        "metadata.sequencing_kit",
        "metadata.sequencing_type",
        "proc_id",
        "type",
    ]

    result: dict[str, dict[str, int]] = {}
    for field in wet_fields:
        result[field] = es_query_conn.get_all_documents_kv_count(
            es_query_conn.wet_processes_index, field
        )

    return jsonify({"result": result}), 200


def count_bi_process_fields() -> tuple[Response, int]:
    """Return key-value counts for each field in bi_process documents, including steps."""
    es_query_conn: ElasticQueryConn = current_app.elastic_query_conn  # type: ignore[attr-defined]
    # Champs de niveau racine
    bi_fields = [
        "metadata.name",
        "metadata.pipeline_version",
        "metadata.sequencing_type",
        "proc_id",
        "type",
    ]

    # Champs des steps (dans la liste steps[])
    step_fields = [
        "metadata.steps.name",
        "metadata.steps.cmd",
        "metadata.steps.version",
        "metadata.steps.output",  # optionnel
    ]

    result: dict[str, dict[str, int]] = {}
    for field in bi_fields + step_fields:
        result[field] = es_query_conn.get_all_documents_kv_count(
            es_query_conn.bi_processes_index, field
        )

    return jsonify({"result": result}), 200
