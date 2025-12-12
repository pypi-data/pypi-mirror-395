"""Controller for export/import routes."""

from flask import Blueprint, jsonify, send_file, request, current_app
import zipfile
from typing import Any


export_import_bp = Blueprint("export_import", __name__, url_prefix="/api")


@export_import_bp.route("/prompts/<name>/export", methods=["GET"])
def export_prompt(name: str) -> Any:
    """Export a prompt to JSON file."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        config = current_app.config

        temp_file = config["EXPORT_TEMP_DIR"] / f"{name}.json"
        versioner.export_prompt(name, temp_file, format="json", include_metrics=True)

        return send_file(
            temp_file,
            as_attachment=True,
            download_name=f"{name}_export.json",
            mimetype="application/json",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@export_import_bp.route("/prompts/<name>/versions/<version>/export", methods=["GET"])
def export_version(name: str, version: str) -> Any:
    """Export a specific version of a prompt to JSON file."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        config = current_app.config

        # Get the specific version
        version_data = versioner.get_version(name, version)
        if not version_data:
            return jsonify({"error": f"Version '{version}' not found for prompt '{name}'"}), 404

        # Create export data for this specific version
        export_data = {
            "prompt_name": name,
            "version": version,
            "data": version_data,
            "export_timestamp": version_data.get("timestamp"),
            "export_type": "single_version",
        }

        temp_file = config["EXPORT_TEMP_DIR"] / f"{name}_v{version}.json"

        import json

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return send_file(
            temp_file,
            as_attachment=True,
            download_name=f"{name}_v{version}_export.json",
            mimetype="application/json",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@export_import_bp.route("/prompts/import", methods=["POST"])
def import_prompt() -> Any:
    """Import a prompt from uploaded JSON file."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        versioner = current_app.versioner  # type: ignore[attr-defined]
        config = current_app.config

        temp_file = config["EXPORT_TEMP_DIR"] / file.filename
        file.save(temp_file)

        result = versioner.import_prompt(temp_file, overwrite=False)

        temp_file.unlink()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@export_import_bp.route("/export-all", methods=["GET"])
def export_all() -> Any:
    """Export all prompts as ZIP."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        config = current_app.config

        temp_dir = config["EXPORT_TEMP_DIR"] / "prompt_export"
        temp_dir.mkdir(exist_ok=True)

        versioner.export_all(temp_dir, format="json")

        zip_path = config["EXPORT_TEMP_DIR"] / "all_prompts.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for json_file in temp_dir.glob("*.json"):
                zipf.write(json_file, json_file.name)

        # Cleanup
        for json_file in temp_dir.glob("*.json"):
            json_file.unlink()
        temp_dir.rmdir()

        return send_file(
            zip_path,
            as_attachment=True,
            download_name="all_prompts.zip",
            mimetype="application/zip",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
