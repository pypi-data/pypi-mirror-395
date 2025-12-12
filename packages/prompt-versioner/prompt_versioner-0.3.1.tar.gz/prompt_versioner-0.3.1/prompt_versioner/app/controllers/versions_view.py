"""Controller for version-related routes."""

from flask import Blueprint, jsonify, request, current_app
from typing import Any


versions_bp = Blueprint("versions", __name__, url_prefix="/api/prompts/<name>")


@versions_bp.route("/versions", methods=["GET"])
def get_versions(name: str) -> Any:
    """Get all versions of a prompt with metrics."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        metrics_service = current_app.metrics_service  # type: ignore[attr-defined]

        versions = versioner.list_versions(name)
        versions = metrics_service.enrich_versions_with_metrics(versions)

        return jsonify(versions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@versions_bp.route("/versions/with-diffs", methods=["GET"])
def get_versions_with_diffs(name: str) -> Any:
    """Get all versions with diffs from previous version."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        metrics_service = current_app.metrics_service  # type: ignore[attr-defined]
        diff_service = current_app.diff_service  # type: ignore[attr-defined]

        versions = versioner.list_versions(name)

        if not versions:
            return jsonify([])

        # Enrich with metrics
        versions = metrics_service.enrich_versions_with_metrics(versions)

        # Add diffs
        versions = diff_service.enrich_with_diffs(versions)

        return jsonify(versions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@versions_bp.route("/versions/<version>", methods=["GET"])
def get_version_detail(name: str, version: str) -> Any:
    """Get a specific version with metrics summary."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]

        v = versioner.get_version(name, version)
        if not v:
            return jsonify({"error": "Version not found"}), 404

        metrics_summary = versioner.storage.get_metrics_summary(v["id"])
        metrics_list = versioner.storage.get_metrics(v["id"])

        # Get model name from metrics
        model_name = None
        if metrics_list:
            model_names = [m.get("model_name") for m in metrics_list if m.get("model_name")]
            if model_names:
                # Use the most recent model or the most common one
                model_name = model_names[-1]  # Get the last (most recent) model

        v["metrics_summary"] = metrics_summary
        v["metrics_history"] = metrics_list
        v["model_name"] = model_name

        return jsonify(v)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@versions_bp.route("/compare", methods=["GET"])
def compare_versions(name: str) -> Any:
    """Compare two versions with A/B test style analysis."""
    try:
        version_a = request.args.get("version_a")
        version_b = request.args.get("version_b")
        metric = request.args.get("metric", "quality_score")

        if not version_a or not version_b:
            return jsonify({"error": "Missing version_a or version_b"}), 400

        versioner = current_app.versioner  # type: ignore[attr-defined]

        v_a = versioner.get_version(name, version_a)
        v_b = versioner.get_version(name, version_b)

        if not v_a or not v_b:
            return jsonify({"error": "Version not found"}), 404

        summary_a = versioner.storage.get_metrics_summary(v_a["id"])
        summary_b = versioner.storage.get_metrics_summary(v_b["id"])

        metric_map = {
            "quality_score": "avg_quality",
            "cost": "avg_cost",
            "latency": "avg_latency",
            "accuracy": "avg_accuracy",
        }

        summary_metric = metric_map.get(metric, "avg_quality")

        value_a = summary_a.get(summary_metric, 0) if summary_a else 0
        value_b = summary_b.get(summary_metric, 0) if summary_b else 0

        # Determine winner
        if metric in ["cost", "latency"]:
            winner = "a" if value_a < value_b else "b"
            improvement = abs(value_b - value_a) / value_a * 100 if value_a > 0 else 0
        else:
            winner = "a" if value_a > value_b else "b"
            improvement = abs(value_b - value_a) / value_a * 100 if value_a > 0 else 0

        return jsonify(
            {
                "version_a": version_a,
                "version_b": version_b,
                "metric": metric,
                "summary_a": summary_a,
                "summary_b": summary_b,
                "value_a": value_a,
                "value_b": value_b,
                "winner": version_b if winner == "b" else version_a,
                "improvement_percent": improvement,
                "call_count_a": summary_a.get("call_count", 0) if summary_a else 0,
                "call_count_b": summary_b.get("call_count", 0) if summary_b else 0,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@versions_bp.route("/diff", methods=["GET"])
def get_diff(name: str) -> Any:
    """Get diff between two versions."""
    try:
        version1 = request.args.get("version1")
        version2 = request.args.get("version2")

        if not all([name, version1, version2]):
            return jsonify({"error": "Missing parameters"}), 400

        diff_service = current_app.diff_service  # type: ignore[attr-defined]
        diff_info = diff_service.compare_versions(name, version1, version2)

        return jsonify(diff_info)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@versions_bp.route("/versions/<version>", methods=["DELETE"])
def delete_version(name: str, version: str) -> Any:
    """Delete a specific version of a prompt (and related data)."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        deleted = versioner.delete_version(name, version)
        if deleted:
            return jsonify({"success": True, "message": f"Version {version} deleted."})
        else:
            return jsonify({"success": False, "error": "Version not found."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
