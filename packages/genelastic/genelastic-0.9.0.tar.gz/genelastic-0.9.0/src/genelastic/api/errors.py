import elasticsearch
from flask import Flask, Response, jsonify


def register_error_handlers(app: Flask) -> None:
    """Register handlers for elasticsearch ApiError and TransportError
    exceptions.
    """

    @app.errorhandler(elasticsearch.ApiError)
    def handle_api_error(e: elasticsearch.ApiError) -> tuple[Response, int]:
        # See https://elasticsearch-py.readthedocs.io/en/latest/exceptions.html#api-errors
        app.logger.error("Elasticsearch ApiError: %s", e, exc_info=True)

        return (
            jsonify(
                {
                    "error": {
                        "message": str(e),
                        "type": e.__class__.__name__,
                    }
                }
            ),
            e.status_code,
        )

    @app.errorhandler(elasticsearch.TransportError)
    def handle_transport_error(
        e: elasticsearch.TransportError,
    ) -> tuple[Response, int]:
        # See https://elasticsearch-py.readthedocs.io/en/latest/exceptions.html#transport-and-connection-errors
        app.logger.error("Elasticsearch TransportError: %s", e, exc_info=True)

        status_code = 502
        if (
            e.errors
            and hasattr(e.errors[0], "status")
            and e.errors[0].status is not None
        ):
            status_code = e.errors[0].status

        return (
            jsonify(
                {
                    "error": {
                        "message": str(e),
                        "type": e.__class__.__name__,
                    }
                }
            ),
            status_code,
        )
