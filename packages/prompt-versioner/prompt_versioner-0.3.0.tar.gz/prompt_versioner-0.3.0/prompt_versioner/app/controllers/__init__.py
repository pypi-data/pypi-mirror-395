"""Controllers for web dashboard."""

from prompt_versioner.app.controllers.prompts_view import prompts_bp
from prompt_versioner.app.controllers.versions_view import versions_bp
from prompt_versioner.app.controllers.alerts_view import alerts_bp
from prompt_versioner.app.controllers.export_import_view import export_import_bp

__all__ = ["prompts_bp", "versions_bp", "alerts_bp", "export_import_bp"]
