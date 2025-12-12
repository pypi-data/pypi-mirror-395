"""Storage module for prompt versions using SQLite."""

from typing import Any, Dict, List, Optional
from pathlib import Path
from prompt_versioner.storage.database import DatabaseManager
from prompt_versioner.storage.versions import VersionStorage
from prompt_versioner.storage.metrics import MetricsStorage
from prompt_versioner.storage.annotations import AnnotationStorage
from prompt_versioner.storage.queries import QueryBuilder


# Main storage class that combines all operations
class PromptStorage:
    """Unified storage interface for prompt versions."""

    def __init__(self, db_path: Path | None = None) -> None:
        """Initialize storage with SQLite database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.db = DatabaseManager(self.db_path)
        self.versions = VersionStorage(self.db)
        self.metrics = MetricsStorage(self.db)
        self.annotations = AnnotationStorage(self.db)

    # Delegate version operations
    def save_version(self, *args: Any, **kwargs: Any) -> int:
        return self.versions.save(*args, **kwargs)

    def get_version(self, *args: Any, **kwargs: Any) -> Optional[Dict[str, Any]]:
        return self.versions.get(*args, **kwargs)

    def get_latest_version(self, *args: Any, **kwargs: Any) -> Optional[Dict[str, Any]]:
        return self.versions.get_latest(*args, **kwargs)

    def list_versions(self, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        return self.versions.list(*args, **kwargs)

    def list_all_prompts(self, *args: Any, **kwargs: Any) -> List[str]:
        return self.versions.list_all_prompts(*args, **kwargs)

    def delete_version(self, *args: Any, **kwargs: Any) -> bool:
        return self.versions.delete(*args, **kwargs)

    def delete_prompt(self, *args: Any, **kwargs: Any) -> bool:
        return self.versions.delete_prompt(*args, **kwargs)

    # Delegate metrics operations
    def save_metrics(self, *args: Any, **kwargs: Any) -> int:
        return self.metrics.save(*args, **kwargs)

    def get_metrics(self, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        return self.metrics.get(*args, **kwargs)

    def get_metrics_summary(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return self.metrics.get_summary(*args, **kwargs)

    # Delegate annotation operations
    def add_annotation(self, *args: Any, **kwargs: Any) -> int:
        return self.annotations.add(*args, **kwargs)

    def get_annotations(self, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        return self.annotations.get(*args, **kwargs)


__all__ = [
    "PromptStorage",
    "DatabaseManager",
    "VersionStorage",
    "MetricsStorage",
    "AnnotationStorage",
    "QueryBuilder",
]
