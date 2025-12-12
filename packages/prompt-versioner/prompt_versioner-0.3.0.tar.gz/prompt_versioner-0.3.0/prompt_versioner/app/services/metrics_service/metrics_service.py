"""Service for handling metrics operations."""

from typing import Any, Dict, List


class MetricsService:
    """Service for metrics aggregation and retrieval."""

    def __init__(self, versioner: Any):
        """Initialize service.

        Args:
            versioner: PromptVersioner instance
        """
        self.versioner = versioner

    def get_global_stats(self) -> Dict[str, Any]:
        """Get global statistics across all prompts.

        Returns:
            Dictionary with global stats
        """
        prompts = self.versioner.list_prompts()

        prompt_data = []
        total_versions = 0
        total_cost = 0.0
        total_tokens = 0
        total_calls = 0

        for name in prompts:
            versions = self.versioner.list_versions(name)
            total_versions += len(versions)

            for v in versions:
                summary = self.versioner.storage.get_metrics_summary(v["id"])
                if summary:
                    total_cost += summary.get("total_cost", 0) or 0
                    total_tokens += summary.get("total_tokens_used", 0) or 0
                    total_calls += summary.get("call_count", 0) or 0

            latest = versions[0] if versions else None
            prompt_data.append(
                {
                    "name": name,
                    "version_count": len(versions),
                    "latest_version": latest["version"] if latest else "N/A",
                    "latest_timestamp": latest["timestamp"] if latest else None,
                }
            )

        return {
            "prompts": prompt_data,
            "total_versions": total_versions,
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "total_calls": total_calls,
        }

    def get_prompt_stats(self, name: str) -> Dict[str, Any]:
        """Get aggregated stats for a specific prompt.

        Args:
            name: Prompt name

        Returns:
            Dictionary with prompt stats
        """
        versions = self.versioner.list_versions(name)

        if not versions:
            raise ValueError(f"Prompt '{name}' not found")

        total_calls = 0
        total_cost = 0.0
        total_tokens = 0
        all_latencies = []
        all_quality_scores = []
        models_used = set()
        version_stats = []

        for v in versions:
            summary = self.versioner.storage.get_metrics_summary(v["id"])
            if summary and summary.get("call_count", 0) > 0:
                total_calls += summary.get("call_count", 0)
                total_cost += summary.get("total_cost", 0)
                total_tokens += summary.get("total_tokens_used", 0)

                if summary.get("avg_latency"):
                    all_latencies.append(summary["avg_latency"])
                if summary.get("avg_quality"):
                    all_quality_scores.append(summary["avg_quality"])

                metrics = self.versioner.storage.get_metrics(v["id"])
                for m in metrics:
                    if m.get("model_name"):
                        models_used.add(m["model_name"])

                version_stats.append(
                    {
                        "version": v["version"],
                        "timestamp": v["timestamp"],
                        "summary": summary,
                    }
                )

        return {
            "name": name,
            "total_versions": len(versions),
            "total_calls": total_calls,
            "total_cost_eur": round(total_cost, 4),
            "total_tokens": total_tokens,
            "avg_latency_ms": (
                round(sum(all_latencies) / len(all_latencies), 2) if all_latencies else 0
            ),
            "avg_quality_score": (
                round(sum(all_quality_scores) / len(all_quality_scores), 2)
                if all_quality_scores
                else 0
            ),
            "models_used": list(models_used),
            "version_stats": version_stats,
        }

    def enrich_versions_with_metrics(self, versions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich versions with metrics summaries.

        Args:
            versions: List of version dictionaries

        Returns:
            Enriched versions list
        """
        for v in versions:
            v["metrics_summary"] = self.versioner.storage.get_metrics_summary(v["id"])

            # Get model name from metrics
            metrics_list = self.versioner.storage.get_metrics(v["id"])
            model_name = None
            if metrics_list:
                model_names = [m.get("model_name") for m in metrics_list if m.get("model_name")]
                if model_names:
                    # Take the last (most recent) model name instead of the first
                    model_name = model_names[-1]
            v["model_name"] = model_name

            # Get annotations
            annotations = self.versioner.storage.get_annotations(v["id"])
            v["annotations"] = annotations

        return versions
