"""Web dashboard for prompt versioner - Flask application factory."""

from flask import Flask, render_template
from typing import Any
import os

from prompt_versioner.app.config import config
from prompt_versioner.app.services import MetricsService, DiffService, AlertService
from prompt_versioner.app.controllers import prompts_bp, versions_bp, alerts_bp, export_import_bp


def create_app(versioner: Any, config_name: str | None = None) -> Flask:
    """Create and configure Flask application.

    Args:
        versioner: PromptVersioner instance
        config_name: Configuration name ('development', 'production', or 'default')

    Returns:
        Configured Flask app
    """
    # Determine config
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    config_class = config.get(config_name, config["default"])

    # Create Flask app
    app = Flask(
        __name__,
        template_folder=config_class.TEMPLATE_FOLDER,
        static_folder=config_class.STATIC_FOLDER,
    )

    # Load configuration
    app.config.from_object(config_class)

    # Store versioner
    app.versioner = versioner  # type: ignore[attr-defined]

    # Initialize services
    app.metrics_service = MetricsService(versioner)  # type: ignore[attr-defined]
    app.diff_service = DiffService(versioner)  # type: ignore[attr-defined]
    app.alert_service = AlertService(versioner, app.config)  # type: ignore[attr-defined]

    # Register blueprints
    app.register_blueprint(prompts_bp)
    app.register_blueprint(versions_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(export_import_bp)

    # Main route
    @app.route("/")
    def index() -> str:
        """Render dashboard."""
        return render_template("dashboard.html")

    # Error handlers

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple[dict[str, str], int]:
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error: Exception) -> tuple[dict[str, str], int]:
        return {"error": "Internal server error"}, 500

    return app
