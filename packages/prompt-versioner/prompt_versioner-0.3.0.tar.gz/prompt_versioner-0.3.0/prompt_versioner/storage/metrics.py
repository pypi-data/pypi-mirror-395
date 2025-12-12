"""Metrics storage operations."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
from prompt_versioner.storage.database import DatabaseManager


class MetricsStorage:
    # Allowed metric columns for time series queries
    ALLOWED_METRIC_COLUMNS = {
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cost_eur",
        "latency_ms",
        "quality_score",
        "accuracy",
        "temperature",
        "top_p",
        "max_tokens",
        "success",
        "error_message",
        # Add more if needed
    }

    """Handles metrics CRUD operations."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize metrics storage.

        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager

    def save(
        self,
        version_id: int,
        model_name: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        cost_eur: Optional[float] = None,
        latency_ms: Optional[float] = None,
        quality_score: Optional[float] = None,
        accuracy: Optional[float] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Save metrics for a prompt version.

        Args:
            version_id: ID of the prompt version
            model_name: Name of the LLM model used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            total_tokens: Total tokens
            cost_eur: Cost in EUR
            latency_ms: Response latency in milliseconds
            quality_score: Quality score (0-1)
            accuracy: Accuracy score (0-1)
            temperature: Model temperature
            top_p: Model top_p
            max_tokens: Max tokens parameter
            success: Whether the call succeeded
            error_message: Error message if failed
            metadata: Additional metadata

        Returns:
            Metrics ID
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        metadata_json = json.dumps(metadata) if metadata else None

        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO prompt_metrics
                (version_id, model_name, input_tokens, output_tokens, total_tokens,
                 cost_eur, latency_ms, quality_score, accuracy, temperature, top_p,
                 max_tokens, success, error_message, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version_id,
                    model_name,
                    input_tokens,
                    output_tokens,
                    total_tokens,
                    cost_eur,
                    latency_ms,
                    quality_score,
                    accuracy,
                    temperature,
                    top_p,
                    max_tokens,
                    success,
                    error_message,
                    timestamp,
                    metadata_json,
                ),
            )
            return cursor.rowcount if cursor.rowcount is not None else 0

    def get(self, version_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all metrics for a version.

        Args:
            version_id: ID of the prompt version
            limit: Optional limit on results

        Returns:
            List of metric dicts
        """
        query = """
            SELECT * FROM prompt_metrics
            WHERE version_id = ?
            ORDER BY timestamp DESC
        """

        if limit:
            query += f" LIMIT {limit}"

        rows = self.db.execute(query, (version_id,), fetch="all")

        metrics = []
        for row in rows:
            metric = dict(row)
            if metric.get("metadata"):
                try:
                    metric["metadata"] = json.loads(metric["metadata"])
                except json.JSONDecodeError:
                    metric["metadata"] = {}
            metrics.append(metric)

        return metrics

    def get_summary(self, version_id: int) -> Dict[str, Any]:
        """Get summary statistics of metrics for a version.

        Args:
            version_id: ID of the prompt version

        Returns:
            Dict with summary statistics
        """
        row = self.db.execute(
            """
            SELECT
                COUNT(*) as call_count,
                AVG(input_tokens) as avg_input_tokens,
                AVG(output_tokens) as avg_output_tokens,
                AVG(total_tokens) as avg_total_tokens,
                SUM(total_tokens) as total_tokens_used,
                AVG(cost_eur) as avg_cost,
                SUM(cost_eur) as total_cost,
                AVG(latency_ms) as avg_latency,
                MIN(latency_ms) as min_latency,
                MAX(latency_ms) as max_latency,
                AVG(quality_score) as avg_quality,
                AVG(accuracy) as avg_accuracy,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as error_count
            FROM prompt_metrics
            WHERE version_id = ?
            """,
            (version_id,),
            fetch="one",
        )

        if row:
            summary = dict(row)
            summary["success_rate"] = (
                summary["success_count"] / summary["call_count"] if summary["call_count"] > 0 else 0
            )
            return summary
        return {}

    def get_by_model(self, version_id: int) -> Dict[str, Dict[str, Any]]:
        """Get metrics grouped by model.

        Args:
            version_id: Version ID

        Returns:
            Dict of model_name -> summary stats
        """
        rows = self.db.execute(
            """
            SELECT
                model_name,
                COUNT(*) as call_count,
                AVG(total_tokens) as avg_tokens,
                SUM(cost_eur) as total_cost,
                AVG(latency_ms) as avg_latency,
                AVG(quality_score) as avg_quality
            FROM prompt_metrics
            WHERE version_id = ? AND model_name IS NOT NULL
            GROUP BY model_name
            """,
            (version_id,),
            fetch="all",
        )

        return {row["model_name"]: dict(row) for row in rows}

    def get_latest(self, version_id: int, n: int = 10) -> List[Dict[str, Any]]:
        """Get latest N metrics for a version.

        Args:
            version_id: Version ID
            n: Number of metrics to return

        Returns:
            List of metric dicts
        """
        return self.get(version_id, limit=n)

    def delete_old(self, version_id: int, keep_latest: int = 100) -> int:
        """Delete old metrics, keeping only the latest N.

        Args:
            version_id: Version ID
            keep_latest: Number of latest metrics to keep

        Returns:
            Number of deleted metrics
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                DELETE FROM prompt_metrics
                WHERE version_id = ?
                AND id NOT IN (
                    SELECT id FROM prompt_metrics
                    WHERE version_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                )
                """,
                (version_id, version_id, keep_latest),
            )
            return cursor.rowcount if cursor.rowcount is not None else 0

    def get_failures(self, version_id: int) -> List[Dict[str, Any]]:
        """Get all failed metrics for a version.

        Args:
            version_id: Version ID

        Returns:
            List of failed metric dicts
        """
        rows = self.db.execute(
            """
            SELECT * FROM prompt_metrics
            WHERE version_id = ? AND success = 0
            ORDER BY timestamp DESC
            """,
            (version_id,),
            fetch="all",
        )

        return [dict(row) for row in rows]

    def get_time_series(
        self, version_id: int, metric_name: str, interval: str = "hour"
    ) -> List[Dict[str, Any]]:
        """Get time series data for a metric.

        Args:
            version_id: Version ID
            metric_name: Name of metric column
            interval: Time interval ('hour', 'day', 'week')

        Returns:
            List of time-series data points
        """
        # Validate metric_name to prevent SQL injection
        self._validate_metric_name(metric_name)

        # SQLite date functions
        if interval == "hour":
            group_by = "strftime('%Y-%m-%d %H:00:00', timestamp)"
        elif interval == "day":
            group_by = "strftime('%Y-%m-%d', timestamp)"
        else:  # week
            group_by = "strftime('%Y-%W', timestamp)"

        query = f"""
            SELECT
                {group_by} as time_bucket,
                COUNT(*) as count,
                AVG({metric_name}) as avg_value,
                MIN({metric_name}) as min_value,
                MAX({metric_name}) as max_value
            FROM prompt_metrics
            WHERE version_id = ? AND {metric_name} IS NOT NULL
            GROUP BY time_bucket
            ORDER BY time_bucket
        """  # nosec: B608 -- metric_name validated
        rows = self.db.execute(query, (version_id,), fetch="all")
        return [dict(row) for row in rows]

    def _validate_metric_name(self, metric_name: str) -> None:
        """Validate metric name to prevent SQL injection."""
        if metric_name not in MetricsStorage.ALLOWED_METRIC_COLUMNS:
            raise ValueError(f"Invalid metric name: {metric_name}")

    def get_summary_by_model(self, version_id: int) -> Dict[str, Dict[str, Any]]:
        """Get metrics summary grouped by model for a specific version.

        Args:
            version_id: Version ID

        Returns:
            Dict mapping model_name to its summary stats
        """
        rows = self.db.execute(
            """
            SELECT
                model_name,
                COUNT(*) as call_count,
                AVG(input_tokens) as avg_input_tokens,
                AVG(output_tokens) as avg_output_tokens,
                AVG(total_tokens) as avg_total_tokens,
                SUM(total_tokens) as total_tokens_used,
                AVG(cost_eur) as avg_cost,
                SUM(cost_eur) as total_cost,
                AVG(latency_ms) as avg_latency,
                MIN(latency_ms) as min_latency,
                MAX(latency_ms) as max_latency,
                AVG(quality_score) as avg_quality,
                AVG(accuracy) as avg_accuracy,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                COUNT(*) - SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as failure_count
            FROM prompt_metrics
            WHERE version_id = ? AND model_name IS NOT NULL
            GROUP BY model_name
            ORDER BY call_count DESC
            """,
            (version_id,),
            fetch="all",
        )

        result = {}
        for row in rows:
            model_name = row["model_name"]
            result[model_name] = {
                "call_count": row["call_count"],
                "avg_input_tokens": round(row["avg_input_tokens"] or 0, 2),
                "avg_output_tokens": round(row["avg_output_tokens"] or 0, 2),
                "avg_total_tokens": round(row["avg_total_tokens"] or 0, 2),
                "total_tokens_used": row["total_tokens_used"] or 0,
                "avg_cost": round(row["avg_cost"] or 0, 6),
                "total_cost": round(row["total_cost"] or 0, 6),
                "avg_latency": round(row["avg_latency"] or 0, 2),
                "min_latency": round(row["min_latency"] or 0, 2),
                "max_latency": round(row["max_latency"] or 0, 2),
                "avg_quality": (round(row["avg_quality"], 3) if row["avg_quality"] else None),
                "avg_accuracy": (round(row["avg_accuracy"], 3) if row["avg_accuracy"] else None),
                "success_count": row["success_count"],
                "failure_count": row["failure_count"],
                "success_rate": round((row["success_count"] / row["call_count"]) * 100, 2),
            }

        return result
