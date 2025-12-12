from typing import Any

import requests
from flask import Blueprint, current_app, render_template, request

routes_bp = Blueprint("routes", __name__)


def clean_field_name(field: str) -> str:
    return field.replace("metadata.", "").replace("_", " ").title()


@routes_bp.route("/")
def home() -> str:
    api_url = current_app.config["GENUI_API_URL"]

    response = requests.get(
        f"{api_url}analyses/count_key_value_analyses_index", timeout=20
    ).json()
    analyse_count = response.get("result", {})

    response = requests.get(
        f"{api_url}wet_processes/count_key_value_wet_processes_index",
        timeout=20,
    ).json()
    wet_count = response.get("result", {})

    response = requests.get(
        f"{api_url}bi_processes/count_key_value_bi_processes_index", timeout=20
    ).json()
    bi_count = response.get("result", {})

    total_analyses = (
        sum(sum(values.values()) for values in analyse_count.values())
        if analyse_count
        else 0
    )
    total_wet = (
        sum(sum(values.values()) for values in wet_count.values())
        if wet_count
        else 0
    )
    total_bi = (
        sum(sum(values.values()) for values in bi_count.values())
        if bi_count
        else 0
    )

    total_analyses_per_key = {}
    if analyse_count:
        for key, values in analyse_count.items():
            total_analyses_per_key[key] = sum(values.values())

    return render_template(
        "home.html",
        analyse_count=analyse_count,
        wet_count=wet_count,
        bi_count=bi_count,
        total_analyses=total_analyses,
        total_wet=total_wet,
        total_bi=total_bi,
        total_analyses_per_key=total_analyses_per_key,
    )


@routes_bp.route("/analyses")
def show_analyses() -> str:
    api_url = current_app.config["GENUI_API_URL"]
    try:
        response = requests.get(f"{api_url}analyses", timeout=20)
        analyses = response.json()["result"]
    except requests.exceptions.RequestException:
        analyses = ["Error fetching data."]

    return render_template("analyses.html", analyses=analyses)


@routes_bp.route("/analysis/<analysis_id>")
def show_analysis_detail(analysis_id: str) -> str:
    api_url = current_app.config["GENUI_API_URL"]
    source = request.args.get(
        "source"
    )  # récupère ?source=wet ou ?source=bi si présent

    try:
        wet_response = requests.get(f"{api_url}wet_processes", timeout=20)
        bi_response = requests.get(f"{api_url}bi_processes", timeout=20)
        wet_processes = wet_response.json()["result"]
        bi_processes = bi_response.json()["result"]
    except requests.exceptions.RequestException:
        wet_processes = []
        bi_processes = []

    matched_wet = [wp for wp in wet_processes if wp in analysis_id]
    matched_bi = [bp for bp in bi_processes if bp in analysis_id]

    return render_template(
        "analysis_detail.html",
        analysis_id=analysis_id,
        wet_processes=matched_wet,
        bi_processes=matched_bi,
        source=source,
    )


@routes_bp.route("/bi_processes", methods=["GET"])
def show_bi_processes() -> str:
    api_url = current_app.config["GENUI_API_URL"]
    selected_bi_processes = request.args.getlist("bi_processes")

    try:
        bi_processes, analyses = get_processes_and_analyses(
            api_url, "bi_processes", selected_bi_processes
        )
    except requests.exceptions.RequestException:
        bi_processes = []
        analyses = []

    return render_template(
        "bi_processes.html",
        bi_processes=bi_processes,
        selected_bi_processes=selected_bi_processes,
        analyses=analyses,
    )


@routes_bp.route("/wet_processes", methods=["GET"])
def show_wet_processes() -> str:
    api_url = current_app.config["GENUI_API_URL"]
    selected_wet_processes = request.args.getlist("wet_processes")

    try:
        wet_processes, analyses = get_processes_and_analyses(
            api_url, "wet_processes", selected_wet_processes
        )
    except requests.exceptions.RequestException:
        wet_processes = []
        analyses = []

    return render_template(
        "wet_processes.html",
        wet_processes=wet_processes,
        selected_wet_processes=selected_wet_processes,
        analyses=analyses,
    )


def get_processes_and_analyses(
    api_url: str, process_type: str, selected_processes: list[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    analyses = []

    try:
        processes_response = requests.get(
            f"{api_url}{process_type}", timeout=20
        )
        processes = processes_response.json()["result"]

        if selected_processes:
            analyses_response = requests.get(f"{api_url}analyses", timeout=20)
            all_analyses = analyses_response.json()["result"]
            analyses = [
                analysis
                for analysis in all_analyses
                if any(process in analysis for process in selected_processes)
            ]
    except requests.exceptions.RequestException:
        processes = []
        analyses = []

    return processes, analyses


@routes_bp.route("/wet_process/details/<wet_process_id>")
def wet_process_detail(wet_process_id: str) -> str:
    api_url = current_app.config["GENUI_API_URL"]

    try:
        wet_response = requests.get(
            f"{api_url}wet_processes/{wet_process_id}", timeout=20
        )
        wet_response.raise_for_status()
        wet_process = wet_response.json()["result"]
    except requests.exceptions.HTTPError as e:
        return render_template(
            "wet_process_detail.html",
            proc_id=wet_process_id,
            error=e.response.json(),
        )

    # Récupérer tous les bi-processus pour la sélection
    try:
        bi_list_response = requests.get(f"{api_url}bi_processes", timeout=20)
        bi_processes = bi_list_response.json()["result"]
    except requests.exceptions.RequestException:
        bi_processes = []

    # Si un bi_process_id est présent en paramètre GET, on le charge pour comparaison
    bi_process_id = request.args.get("compare_with")
    bi_process_data = None
    if bi_process_id:
        try:
            bi_response = requests.get(
                f"{api_url}bi_processes/{bi_process_id}", timeout=20
            )
            bi_response.raise_for_status()
            bi_process_data = bi_response.json()["result"]
        except requests.exceptions.RequestException:
            bi_process_data = {"error": "Could not fetch bi process"}

    return render_template(
        "wet_process_detail.html",
        proc_id=wet_process_id,
        wet_process=wet_process,
        bi_processes=bi_processes,
        selected_bi=bi_process_id,
        bi_process_data=bi_process_data,
    )


@routes_bp.route("/bi_process/details/<bi_process_id>")
def bi_process_detail(bi_process_id: str) -> str:
    api_url = current_app.config["GENUI_API_URL"]

    # Récupérer les données du bi process principal
    try:
        response = requests.get(
            f"{api_url}bi_processes/{bi_process_id}", timeout=20
        )
        response.raise_for_status()
        bi_process = response.json()["result"]
    except requests.exceptions.HTTPError as e:
        return render_template(
            "bi_process_detail.html",
            proc_id=bi_process_id,
            error=e.response.json(),
        )

    # Charger tous les wet processes pour le menu déroulant
    try:
        wet_list_response = requests.get(f"{api_url}wet_processes", timeout=20)
        wet_processes = wet_list_response.json()["result"]
    except requests.exceptions.RequestException:
        wet_processes = []

    # Récupérer le wet process sélectionné pour la comparaison
    wet_process_id = request.args.get("compare_with")
    wet_process_data = None
    if wet_process_id:
        try:
            wet_response = requests.get(
                f"{api_url}wet_processes/{wet_process_id}", timeout=20
            )
            wet_response.raise_for_status()
            wet_process_data = wet_response.json()["result"]
        except requests.exceptions.RequestException:
            wet_process_data = {"error": "Could not fetch wet process"}

    return render_template(
        "bi_process_detail.html",
        proc_id=bi_process_id,
        bi_process=bi_process,
        wet_processes=wet_processes,
        selected_wet=wet_process_id,
        wet_process_data=wet_process_data,
    )


@routes_bp.route("/version")
def version() -> str:
    api_url = current_app.config["GENUI_API_URL"]
    try:
        response = requests.get(f"{api_url}version", timeout=20)
        vers = response.json()["result"].get("version", "Version not found")
    except requests.exceptions.RequestException:
        vers = "Error fetching version."

    return render_template("version.html", version=vers)


@routes_bp.route("/search_analyses")
def search_analyses() -> dict[str, list[str]]:
    api_url = current_app.config["GENUI_API_URL"]
    query = request.args.get("q", "").lower()

    try:
        analyses_response = requests.get(f"{api_url}analyses", timeout=20)
        analyses = analyses_response.json()["result"]
    except requests.exceptions.RequestException:
        return {"results": []}

    filtered = [a for a in analyses if query in a.lower()]

    filtered = filtered[:10]

    return {"results": filtered}


@routes_bp.route("/explorer")
def explorer() -> str:
    api_url = current_app.config["GENUI_API_URL"]

    try:
        wet_count = requests.get(
            f"{api_url}wet_processes/count_key_value_wet_processes_index",
            timeout=20,
        ).json()["result"]
    except requests.exceptions.RequestException:
        wet_count = {}

    try:
        bi_count = requests.get(
            f"{api_url}bi_processes/count_key_value_bi_processes_index",
            timeout=20,
        ).json()["result"]
    except requests.exceptions.RequestException:
        bi_count = {}

    # Fusionner les deux dictionnaires et exclure les champs contenant "index"
    metadata_counts: dict[str, dict[str | None, int]] = {}

    for dataset in [wet_count, bi_count]:
        for key, values in dataset.items():
            if "index" in key:
                continue  # on saute les champs techniques
            if key not in metadata_counts:
                metadata_counts[key] = {}
            for val, count in values.items():
                metadata_counts[key][val] = (
                    metadata_counts[key].get(val, 0) + count
                )

    return render_template("explorer.html", metadata_counts=metadata_counts)
