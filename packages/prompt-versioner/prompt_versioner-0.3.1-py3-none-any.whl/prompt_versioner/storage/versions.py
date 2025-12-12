"""Version storage operations."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import sqlite3
import json

from prompt_versioner.storage.queries import QueryBuilder
from prompt_versioner.storage.database import DatabaseManager


class VersionStorage:
    """Handles version CRUD operations."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize version storage.

        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager
        self.query = QueryBuilder()

    def save(
        self,
        name: str,
        version: str,
        system_prompt: str,
        user_prompt: str,
        metadata: Optional[Dict[str, Any]] = None,
        git_commit: Optional[str] = None,
        created_by: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> int:
        """Save a new prompt version.

        Args:
            name: Name/identifier for the prompt
            version: Version string
            system_prompt: System prompt content
            user_prompt: User prompt content
            metadata: Additional metadata as dict
            git_commit: Git commit hash
            created_by: Creator name/email
            tags: List of tags

        Returns:
            ID of the saved version
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        tags_json = json.dumps(tags) if tags else None

        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO prompt_versions
                (name, version, system_prompt, user_prompt, metadata,
                 git_commit, timestamp, created_by, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    version,
                    system_prompt,
                    user_prompt,
                    metadata_json,
                    git_commit,
                    timestamp,
                    created_by,
                    tags_json,
                ),
            )
            version_id = cursor.lastrowid

            # Save tags separately if provided
            if tags:
                for tag in tags:
                    conn.execute(
                        "INSERT OR IGNORE INTO version_tags (version_id, tag) VALUES (?, ?)",
                        (version_id, tag),
                    )

            return version_id if version_id is not None else 0

    def get(self, name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get a specific prompt version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            Dict with version data or None if not found
        """
        row = self.db.execute(
            "SELECT * FROM prompt_versions WHERE name = ? AND version = ?",
            (name, version),
            fetch="one",
        )

        if row:
            return self._row_to_dict(row)
        return None

    def get_by_id(self, version_id: int) -> Optional[Dict[str, Any]]:
        """Get version by ID.

        Args:
            version_id: Version ID

        Returns:
            Dict with version data or None if not found
        """
        row = self.db.execute(
            "SELECT * FROM prompt_versions WHERE id = ?", (version_id,), fetch="one"
        )

        if row:
            return self._row_to_dict(row)
        return None

    def get_latest(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the most recent version of a prompt.

        Args:
            name: Prompt name

        Returns:
            Dict with version data or None if not found
        """
        row = self.db.execute(
            """
            SELECT * FROM prompt_versions
            WHERE name = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (name,),
            fetch="one",
        )

        if row:
            return self._row_to_dict(row)
        return None

    def list(self, name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all versions of a prompt.

        Args:
            name: Prompt name
            limit: Optional limit on number of results

        Returns:
            List of version dicts ordered by timestamp (newest first)
        """
        query = """
            SELECT * FROM prompt_versions
            WHERE name = ?
            ORDER BY timestamp DESC
        """

        if limit:
            query += f" LIMIT {limit}"

        rows = self.db.execute(query, (name,), fetch="all")
        return [self._row_to_dict(row) for row in rows]

    def list_all_prompts(self) -> List[str]:
        """List all unique prompt names.

        Returns:
            List of prompt names
        """
        rows = self.db.execute(
            "SELECT DISTINCT name FROM prompt_versions ORDER BY name", fetch="all"
        )
        return [row["name"] for row in rows]

    def search(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_by: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search for versions.

        Args:
            query: Search query (searches in name and prompts)
            tags: Filter by tags
            created_by: Filter by creator
            limit: Max results

        Returns:
            List of matching versions
        """
        sql = "SELECT DISTINCT v.* FROM prompt_versions v"
        conditions = []
        params = []

        if tags:
            sql += " JOIN version_tags t ON v.id = t.version_id"
            tag_placeholders = ",".join("?" * len(tags))
            conditions.append(f"t.tag IN ({tag_placeholders})")
            params.extend(tags)

        if query:
            conditions.append("(v.name LIKE ? OR v.system_prompt LIKE ? OR v.user_prompt LIKE ?)")
            search_param = f"%{query}%"
            params.extend([search_param, search_param, search_param])

        if created_by:
            conditions.append("v.created_by = ?")
            params.append(created_by)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += f" ORDER BY v.timestamp DESC LIMIT {limit}"

        rows = self.db.execute(sql, tuple(params), fetch="all")
        return [self._row_to_dict(row) for row in rows]

    def delete(self, name: str, version: str) -> bool:
        """Delete a specific version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            True if deleted, False if not found
        """
        with self.db.get_connection() as conn:
            # Get version_id first
            cursor = conn.execute(
                "SELECT id FROM prompt_versions WHERE name = ? AND version = ?",
                (name, version),
            )
            row = cursor.fetchone()

            if not row:
                return False

            version_id = row["id"]

            # Delete related data (CASCADE should handle this, but explicit is better)
            conn.execute("DELETE FROM prompt_metrics WHERE version_id = ?", (version_id,))
            conn.execute("DELETE FROM annotations WHERE version_id = ?", (version_id,))
            conn.execute("DELETE FROM version_tags WHERE version_id = ?", (version_id,))

            # Delete version
            conn.execute("DELETE FROM prompt_versions WHERE id = ?", (version_id,))

            return True

    def delete_prompt(self, name: str) -> bool:
        """Delete a prompt and all its versions (and related data).

        Args:
            name: Prompt name

        Returns:
            True if deleted, False if not found
        """
        with self.db.get_connection() as conn:
            # Get all version_ids for this prompt
            cursor = conn.execute("SELECT id FROM prompt_versions WHERE name = ?", (name,))
            version_ids = [row["id"] for row in cursor.fetchall()]

            if not version_ids:
                return False

            # Delete all related data for all versions
            for version_id in version_ids:
                conn.execute("DELETE FROM prompt_metrics WHERE version_id = ?", (version_id,))
                conn.execute("DELETE FROM annotations WHERE version_id = ?", (version_id,))
                conn.execute("DELETE FROM version_tags WHERE version_id = ?", (version_id,))

            # Delete all versions for this prompt
            conn.execute("DELETE FROM prompt_versions WHERE name = ?", (name,))

            return True

    def update_metadata(self, name: str, version: str, metadata: Dict[str, Any]) -> bool:
        """Update metadata for a version.

        Args:
            name: Prompt name
            version: Version string
            metadata: New metadata dict

        Returns:
            True if updated, False if not found
        """
        metadata_json = json.dumps(metadata)

        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE prompt_versions SET metadata = ? WHERE name = ? AND version = ?",
                (metadata_json, name, version),
            )
            return cursor.rowcount > 0

    def add_tags(self, version_id: int, tags: List[str]) -> None:
        """Add tags to a version.

        Args:
            version_id: Version ID
            tags: List of tags to add
        """
        with self.db.get_connection() as conn:
            for tag in tags:
                conn.execute(
                    "INSERT OR IGNORE INTO version_tags (version_id, tag) VALUES (?, ?)",
                    (version_id, tag),
                )

    def remove_tags(self, version_id: int, tags: List[str]) -> None:
        """Remove tags from a version.

        Args:
            version_id: Version ID
            tags: List of tags to remove
        """
        with self.db.get_connection() as conn:
            placeholders = ",".join("?" * len(tags))
            conn.execute(
                f"DELETE FROM version_tags WHERE version_id = ? AND tag IN ({placeholders})",  # nosec: B608 -- placeholders safe, tags parameterized
                (version_id, *tags),
            )

    def get_tags(self, version_id: int) -> List[str]:
        """Get tags for a version.

        Args:
            version_id: Version ID

        Returns:
            List of tags
        """
        rows = self.db.execute(
            "SELECT tag FROM version_tags WHERE version_id = ? ORDER BY tag",
            (version_id,),
            fetch="all",
        )
        return [row["tag"] for row in rows]

    def count_versions(self, name: Optional[str] = None) -> int:
        """Count versions.

        Args:
            name: Optional prompt name to filter by

        Returns:
            Number of versions
        """
        if name:
            row = self.db.execute(
                "SELECT COUNT(*) as count FROM prompt_versions WHERE name = ?", (name,), fetch="one"
            )
        else:
            row = self.db.execute("SELECT COUNT(*) as count FROM prompt_versions", fetch="one")

        return row["count"] if row else 0

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to dict.

        Args:
            row: SQLite row object

        Returns:
            Dict representation
        """
        data = dict(row)

        # Parse JSON fields
        if data.get("metadata"):
            try:
                data["metadata"] = json.loads(data["metadata"])
            except json.JSONDecodeError:
                data["metadata"] = {}

        if data.get("tags"):
            try:
                data["tags"] = json.loads(data["tags"])
            except json.JSONDecodeError:
                data["tags"] = []

        return data
