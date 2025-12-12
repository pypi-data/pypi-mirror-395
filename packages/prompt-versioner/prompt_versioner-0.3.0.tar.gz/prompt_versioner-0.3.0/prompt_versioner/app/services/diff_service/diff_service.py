"""Service for handling diff operations."""

from typing import Any, Dict, List
from prompt_versioner.web.utils.diff_utils import create_inline_diff
from prompt_versioner.app.services.diff_service.diff_engine import DiffEngine


class DiffService:
    """Service for computing diffs between versions."""

    def __init__(self, versioner: Any):
        """Initialize service.

        Args:
            versioner: PromptVersioner instance
        """
        self.versioner = versioner

    def enrich_with_diffs(self, versions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich versions with diff information from previous version.

        Args:
            versions: List of version dictionaries (newest first)

        Returns:
            Enriched versions with diff data
        """
        for i, v in enumerate(versions):
            if i < len(versions) - 1:
                # Compare with previous version
                prev_version = versions[i + 1]

                diff = DiffEngine.compute_diff(
                    old_system=prev_version["system_prompt"],
                    old_user=prev_version["user_prompt"],
                    new_system=v["system_prompt"],
                    new_user=v["user_prompt"],
                )

                v["has_changes"] = diff.total_similarity < 1.0
                v["diff_summary"] = diff.summary
                v["system_similarity"] = diff.system_similarity
                v["user_similarity"] = diff.user_similarity

                v["system_diff"] = create_inline_diff(
                    prev_version["system_prompt"], v["system_prompt"]
                )
                v["user_diff"] = create_inline_diff(prev_version["user_prompt"], v["user_prompt"])
            else:
                # Initial version - no diff
                v["has_changes"] = False
                v["diff_summary"] = "Initial version"
                v["system_diff"] = [{"type": "unchanged", "text": v["system_prompt"]}]
                v["user_diff"] = [{"type": "unchanged", "text": v["user_prompt"]}]

        return versions

    def compare_versions(self, name: str, version_a: str, version_b: str) -> Dict[str, Any]:
        """Get diff between two specific versions.

        Args:
            name: Prompt name
            version_a: First version
            version_b: Second version

        Returns:
            Diff information
        """
        v1 = self.versioner.get_version(name, version_a)
        v2 = self.versioner.get_version(name, version_b)

        if not v1 or not v2:
            raise ValueError("Version not found")

        diff = self.versioner.diff(name, version_a, version_b)

        return {
            "summary": diff.summary,
            "system_similarity": diff.system_similarity,
            "user_similarity": diff.user_similarity,
            "total_similarity": diff.total_similarity,
        }
