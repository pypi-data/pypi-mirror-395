"""Database connection and management."""

import re
import sqlite3
from pathlib import Path
from typing import Optional, Any, List, Dict, Generator
from contextlib import contextmanager

from prompt_versioner.storage.schema import SCHEMA_DEFINITIONS, INDEXES


class DatabaseManager:
    """Manages SQLite database connection and operations."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database manager.

        Args:
            db_path: Path to SQLite database file. Defaults to .prompt_versions/db.sqlite
        """
        if db_path is None:
            db_path = Path.cwd() / ".prompt_versions" / "db.sqlite"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initialize database schema."""
        with self.get_connection() as conn:
            # Create tables
            for table_name, table_sql in SCHEMA_DEFINITIONS.items():
                conn.execute(table_sql)

            # Create indexes
            for index_sql in INDEXES:
                conn.execute(index_sql)

    def execute(self, query: str, params: tuple = (), fetch: str | None = None) -> Any:
        """Execute a query.

        Args:
            query: SQL query
            params: Query parameters
            fetch: 'one', 'all', or None

        Returns:
            Query results based on fetch parameter
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)

            if fetch == "one":
                return cursor.fetchone()
            elif fetch == "all":
                return cursor.fetchall()
            else:
                return cursor

    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """Execute a query multiple times with different parameters.

        Args:
            query: SQL query
            params_list: List of parameter tuples
        """
        with self.get_connection() as conn:
            conn.executemany(query, params_list)

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        self._validate_table_name(table_name)
        """Get information about a table.

        Args:
            table_name: Name of the table

        Returns:
            List of column information dicts
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                f"PRAGMA table_info({table_name})"
            )  # nosec: B608 -- table_name validated
            return [dict(row) for row in cursor.fetchall()]

    def get_tables(self) -> List[str]:
        """Get list of all tables.

        Returns:
            List of table names
        """
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            return [row["name"] for row in cursor.fetchall()]

    def vacuum(self) -> None:
        """Vacuum the database to reclaim space."""
        with self.get_connection() as conn:
            conn.execute("VACUUM")

    def get_db_size(self) -> int:
        """Get database file size in bytes.

        Returns:
            Size in bytes
        """
        return self.db_path.stat().st_size if self.db_path.exists() else 0

    def backup(self, backup_path: Path) -> None:
        """Backup database to another file.

        Args:
            backup_path: Path for backup file
        """
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        with self.get_connection() as source:
            dest = sqlite3.connect(backup_path)
            source.backup(dest)
            dest.close()

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics.

        Returns:
            Dict with database stats
        """
        with self.get_connection() as conn:
            stats: Dict[str, Any] = {
                "db_path": str(self.db_path),
                "db_size_bytes": self.get_db_size(),
                "tables": {},
            }

            for table in self.get_tables():
                self._validate_table_name(table)
                cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table}")  # nosec: B608
                count = cursor.fetchone()["count"]
                stats["tables"][table] = count

            return stats

    def _validate_table_name(self, table_name: str) -> None:
        """Validate table name to prevent SQL injection."""
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", table_name):
            raise ValueError(f"Invalid table name: {table_name}")
