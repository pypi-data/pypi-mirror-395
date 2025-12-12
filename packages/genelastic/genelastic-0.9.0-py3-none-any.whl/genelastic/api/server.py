from pathlib import Path
from typing import Any

import connexion
import yaml
from connexion import FlaskApp

from genelastic.api.errors import register_error_handlers
from genelastic.common.elastic import ElasticQueryConn


def load_yaml(file_path: Path) -> Any:  # noqa: ANN401
    """Load a YAML file and return its content."""
    content = None
    with file_path.open(encoding="utf-8") as f:
        try:
            content = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise SystemExit(exc) from exc
    return content


def aggregate_openapi_specs(
    main_spec_file: Path, additional_spec_path: Path
) -> Any:  # noqa: ANN401
    """Aggregate OpenAPI specifications from a main file and a directory
    of additional specifications.
    """
    main_spec = load_yaml(main_spec_file)
    try:
        entries = additional_spec_path.iterdir()
    except OSError as exc:
        raise SystemExit(exc) from exc

    if "paths" not in main_spec:
        main_spec["paths"] = []

    for entry in entries:
        if not entry.is_file():
            continue

        if entry.suffix not in [".yml", ".yaml"]:
            continue

        content = load_yaml(entry)

        if content and "paths" in content:
            main_spec["paths"].update(content["paths"])

    return main_spec


def create_app() -> FlaskApp:
    # Initialiser l'application Connexion
    connexion_app = connexion.FlaskApp(__name__)
    connexion_app.app.config.from_object("genelastic.api.settings")

    # Initialiser le client Elasticsearch
    es_url = connexion_app.app.config["GENAPI_ES_URL"]
    es_cert_fp = connexion_app.app.config["GENAPI_ES_CERT_FP"]
    es_api_key = connexion_app.app.config["GENAPI_ES_ENCODED_API_KEY"]
    index_prefix = connexion_app.app.config["GENAPI_ES_INDEX_PREFIX"]

    connexion_app.app.elastic_query_conn = ElasticQueryConn(
        es_url, es_cert_fp, index_prefix, api_key=es_api_key
    )

    connexion_app.app.logger.debug(
        "Successfully connected to Elasticsearch server: %s",
        connexion_app.app.elastic_query_conn.client.info(),
    )

    # Chemins des fichiers YAML
    main_yaml_file = Path(__file__).parents[0] / "specification.yml"
    additional_yaml_dir = Path(__file__).parents[0] / "extends"

    # Charger et combiner les fichiers YAML
    yaml_spec = aggregate_openapi_specs(main_yaml_file, additional_yaml_dir)

    # Ajouter la spécification vers OpenAPI
    connexion_app.add_api(yaml_spec)

    register_error_handlers(connexion_app.app)

    return connexion_app


app = create_app()
