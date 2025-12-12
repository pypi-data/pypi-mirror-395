from asgiref.wsgi import WsgiToAsgi
from flask import Flask

from .routes import routes_bp


def create_app() -> WsgiToAsgi:
    flask_app = Flask(__name__)
    flask_app.config.from_object("genelastic.ui.settings")
    flask_app.register_blueprint(routes_bp)
    return WsgiToAsgi(flask_app)  # type: ignore[no-untyped-call]


app = create_app()
