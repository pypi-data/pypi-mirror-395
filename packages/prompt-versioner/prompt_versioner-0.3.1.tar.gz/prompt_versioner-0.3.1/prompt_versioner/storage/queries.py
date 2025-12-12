"""Common queries and query builder utilities."""

from typing import List, Dict, Any
from prompt_versioner.storage.database import DatabaseManager


class QueryBuilder:
    @staticmethod
    def _validate_table_name(table_name: str) -> None:
        import re

        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", table_name):
            raise ValueError(f"Invalid table name: {table_name}")

    @staticmethod
    def _validate_column_names(columns: list[str]) -> None:
        import re

        for col in columns:
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", col):
                raise ValueError(f"Invalid column name: {col}")

    """Utility class for building SQL queries."""

    @staticmethod
    def build_where_clause(conditions: Dict[str, Any]) -> tuple[str, List[Any]]:
        """Build WHERE clause from conditions dict.

        Args:
            conditions: Dict of column -> value

        Returns:
            Tuple of (where_clause, params)
        """
        if not conditions:
            return "", []

        clauses = []
        params: List[Any] = []

        for column, value in conditions.items():
            if value is None:
                clauses.append(f"{column} IS NULL")
            elif isinstance(value, (list, tuple)):
                placeholders = ",".join("?" * len(value))
                clauses.append(f"{column} IN ({placeholders})")
                params.extend(value)
            else:
                clauses.append(f"{column} = ?")
                params.append(value)

        where_clause = " AND ".join(clauses)
        return f"WHERE {where_clause}", params

    @staticmethod
    def build_select(
        table: str,
        columns: list[str] | None = None,
        where: Dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ) -> tuple[str, List[Any]]:
        """Build SELECT query.

        Args:
            table: Table name
            columns: List of columns (or None for *)
            where: Where conditions
            order_by: Order by clause
            limit: Limit number

        Returns:
            Tuple of (query, params)
        """
        # Validate table and columns to prevent SQL injection
        QueryBuilder._validate_table_name(table)
        if columns:
            QueryBuilder._validate_column_names(columns)
            cols = ", ".join(columns)
        else:
            cols = "*"
        query = f"SELECT {cols} FROM {table}"  # nosec: B608 -- validated
        params = []

        if where:
            where_clause, where_params = QueryBuilder.build_where_clause(where)
            query += f" {where_clause}"
            params.extend(where_params)

        if order_by:
            query += f" ORDER BY {order_by}"

        if limit:
            query += f" LIMIT {limit}"

        return query, params


class CommonQueries:
    """Collection of common queries."""

    @staticmethod
    def get_version_stats(db_manager: DatabaseManager) -> Dict[str, Any]:
        """Get overall version statistics.

        Args:
            db_manager: DatabaseManager instance

        Returns:
            Dict with stats
        """
        stats = {}

        # Total versions
        row = db_manager.execute("SELECT COUNT(*) as count FROM prompt_versions", fetch="one")
        stats["total_versions"] = row["count"]

        # Total prompts
        row = db_manager.execute(
            "SELECT COUNT(DISTINCT name) as count FROM prompt_versions", fetch="one"
        )
        stats["total_prompts"] = row["count"]

        # Total metrics
        row = db_manager.execute("SELECT COUNT(*) as count FROM prompt_metrics", fetch="one")
        stats["total_metrics"] = row["count"]

        # Total annotations
        row = db_manager.execute("SELECT COUNT(*) as count FROM annotations", fetch="one")
        stats["total_annotations"] = row["count"]

        return stats

    @staticmethod
    def get_most_used_models(db_manager: DatabaseManager, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most frequently used models.

        Args:
            db_manager: DatabaseManager instance
            limit: Max results

        Returns:
            List of model usage stats
        """
        rows = db_manager.execute(
            f"""
            SELECT
                model_name,
                COUNT(*) as usage_count,
                AVG(cost_eur) as avg_cost,
                AVG(latency_ms) as avg_latency
            FROM prompt_metrics
            WHERE model_name IS NOT NULL
            GROUP BY model_name
            ORDER BY usage_count DESC
            LIMIT {limit}
            """,  # nosec: B608 -- limit is int and safe
            fetch="all",
        )

        return [dict(row) for row in rows]

    @staticmethod
    def get_recent_activity(db_manager: DatabaseManager, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent version activity.

        Args:
            db_manager: DatabaseManager instance
            days: Number of days to look back

        Returns:
            List of recent versions
        """
        rows = db_manager.execute(
            f"""
            SELECT *
            FROM prompt_versions
            WHERE datetime(timestamp) >= datetime('now', '-{days} days')
            ORDER BY timestamp DESC
            """,  # nosec: B608 -- days is int and safe
            fetch="all",
        )

        return [dict(row) for row in rows]
