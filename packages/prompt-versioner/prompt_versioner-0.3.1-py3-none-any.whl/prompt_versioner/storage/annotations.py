"""Annotations storage operations."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from prompt_versioner.storage.database import DatabaseManager


class AnnotationStorage:
    """Handles annotation CRUD operations."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize annotation storage.

        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager

    def add(self, version_id: int, author: str, text: str, annotation_type: str = "comment") -> int:
        """Add annotation to a version.

        Args:
            version_id: Version ID
            author: Author name/email
            text: Annotation text
            annotation_type: Type of annotation

        Returns:
            Annotation ID
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO annotations (version_id, author, text, timestamp, annotation_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (version_id, author, text, timestamp, annotation_type),
            )
            return cursor.rowcount if cursor.rowcount is not None else 0

    def get(self, version_id: int, include_resolved: bool = True) -> List[Dict[str, Any]]:
        """Get all annotations for a version.

        Args:
            version_id: Version ID
            include_resolved: Whether to include resolved annotations

        Returns:
            List of annotations
        """
        query = """
            SELECT * FROM annotations
            WHERE version_id = ?
        """

        if not include_resolved:
            query += " AND resolved = 0"

        query += " ORDER BY timestamp DESC"

        rows = self.db.execute(query, (version_id,), fetch="all")
        return [dict(row) for row in rows]

    def get_by_author(self, author: str) -> List[Dict[str, Any]]:
        """Get all annotations by an author.

        Args:
            author: Author name/email

        Returns:
            List of annotations
        """
        rows = self.db.execute(
            """
            SELECT a.*, v.name, v.version
            FROM annotations a
            JOIN prompt_versions v ON a.version_id = v.id
            WHERE a.author = ?
            ORDER BY a.timestamp DESC
            """,
            (author,),
            fetch="all",
        )
        return [dict(row) for row in rows]

    def update(self, annotation_id: int, text: str) -> bool:
        """Update annotation text.

        Args:
            annotation_id: Annotation ID
            text: New text

        Returns:
            True if updated, False if not found
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE annotations SET text = ? WHERE id = ?", (text, annotation_id)
            )
            return cursor.rowcount > 0

    def resolve(self, annotation_id: int) -> bool:
        """Mark annotation as resolved.

        Args:
            annotation_id: Annotation ID

        Returns:
            True if updated, False if not found
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE annotations SET resolved = 1 WHERE id = ?", (annotation_id,)
            )
            return cursor.rowcount > 0

    def unresolve(self, annotation_id: int) -> bool:
        """Mark annotation as unresolved.

        Args:
            annotation_id: Annotation ID

        Returns:
            True if updated, False if not found
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE annotations SET resolved = 0 WHERE id = ?", (annotation_id,)
            )
            return cursor.rowcount > 0

    def delete(self, annotation_id: int) -> bool:
        """Delete an annotation.

        Args:
            annotation_id: Annotation ID

        Returns:
            True if deleted, False if not found
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM annotations WHERE id = ?", (annotation_id,))
            return cursor.rowcount > 0

    def count(self, version_id: int, resolved: Optional[bool] = None) -> int:
        """Count annotations for a version.

        Args:
            version_id: Version ID
            resolved: Filter by resolved status (None for all)

        Returns:
            Number of annotations
        """
        if resolved is None:
            row = self.db.execute(
                "SELECT COUNT(*) as count FROM annotations WHERE version_id = ?",
                (version_id,),
                fetch="one",
            )
        else:
            row = self.db.execute(
                "SELECT COUNT(*) as count FROM annotations WHERE version_id = ? AND resolved = ?",
                (version_id, 1 if resolved else 0),
                fetch="one",
            )

        return row["count"] if row else 0

    def get_by_type(self, version_id: int, annotation_type: str) -> List[Dict[str, Any]]:
        """Get annotations by type.

        Args:
            version_id: Version ID
            annotation_type: Type of annotation

        Returns:
            List of annotations
        """
        rows = self.db.execute(
            """
            SELECT * FROM annotations
            WHERE version_id = ? AND annotation_type = ?
            ORDER BY timestamp DESC
            """,
            (version_id, annotation_type),
            fetch="all",
        )
        return [dict(row) for row in rows]
