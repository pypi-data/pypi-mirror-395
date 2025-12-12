"""Controller for alert-related routes."""

from flask import Blueprint, jsonify, current_app
from typing import Any


alerts_bp = Blueprint("alerts", __name__, url_prefix="/api")


@alerts_bp.route("/alerts", methods=["GET"])
def get_all_alerts() -> Any:
    """Get all performance alerts across all prompts."""
    try:
        alert_service = current_app.alert_service  # type: ignore[attr-defined]
        alerts = alert_service.get_all_alerts()
        return jsonify(alerts)
    except Exception as e:
        print(f"Error in get_all_alerts: {e}")
        import traceback

        traceback.print_exc()
        # Return empty array instead of error to not break UI
        return jsonify([])


@alerts_bp.route("/prompts/<n>/alerts", methods=["GET"])
def get_prompt_alerts(name: str) -> Any:
    """Get performance alerts for a specific prompt."""
    try:
        alert_service = current_app.alert_service  # type: ignore[attr-defined]
        alerts = alert_service.get_prompt_alerts(name)
        return jsonify(alerts)
    except Exception as e:
        print(f"Error in get_prompt_alerts: {e}")
        import traceback

        traceback.print_exc()
        # Return empty array instead of error
        return jsonify([])
