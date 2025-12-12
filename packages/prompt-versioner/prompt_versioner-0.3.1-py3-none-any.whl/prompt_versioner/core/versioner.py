"""Core PromptVersioner class - main interface for the library."""

from pathlib import Path
import json
import yaml
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Literal
from functools import wraps

from prompt_versioner.storage import PromptStorage
from prompt_versioner.app.services.diff_service.diff_engine import DiffEngine, PromptDiff
from prompt_versioner.tracker import GitTracker, AutoTracker, PromptHasher
from prompt_versioner.metrics import MetricsTracker, MetricsCalculator, PricingManager

from prompt_versioner.core.enums import VersionBump, PreReleaseLabel
from prompt_versioner.core.version_manager import VersionManager
from prompt_versioner.core.test_context import TestContext

F = TypeVar("F", bound=Callable[..., Any])


class PromptVersioner:
    """Main interface for prompt versioning system."""

    def __init__(
        self,
        project_name: str,
        db_path: Optional[Path] = None,
        enable_git: bool = True,
        auto_track: bool = False,
    ):
        """Initialize PromptVersioner.

        Args:
            project_name: Name of your project
            db_path: Optional custom database path
            enable_git: Enable Git integration
            auto_track: Enable automatic tracking on prompt changes
        """
        self.project_name = project_name
        self.storage = PromptStorage(db_path)
        self.version_manager = VersionManager()
        self.pricing_manager = PricingManager()
        self.metrics_calculator = MetricsCalculator(self.pricing_manager)

        # Git integration
        self.git_tracker: Optional[GitTracker] = None
        if enable_git:
            try:
                self.git_tracker = GitTracker()
            except RuntimeError:
                # Not in a Git repo, continue without Git features
                pass

        # Auto tracking
        self.auto_tracker = AutoTracker(self.storage, self.git_tracker)
        self.auto_track_enabled = auto_track

        # Metrics
        self.metrics_tracker = MetricsTracker()

    def track(
        self,
        name: str,
        auto_commit: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Callable[[F], F]:
        """Decorator to track prompt functions.

        Args:
            name: Name/identifier for the prompt
            auto_commit: Automatically version on each call
            metadata: Additional metadata to store

        Returns:
            Decorated function

        Example:
            @pv.track(name="code_reviewer", auto_commit=True)
            def get_prompts(code: str):
                return {
                    "system": "You are a code reviewer...",
                    "user": f"Review: {code}"
                }
        """

        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)

                # Extract prompts from result
                system_prompt, user_prompt = self._extract_prompts(result)

                # Auto-version if enabled
                if auto_commit or self.auto_track_enabled:
                    self.auto_tracker.auto_version(
                        name=name,
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        metadata=metadata,
                    )

                return result

            return cast(F, wrapper)

        return decorator

    def save_version(
        self,
        name: str,
        system_prompt: str,
        user_prompt: str,
        version: Optional[str] = None,
        bump_type: Optional[VersionBump | str] = None,
        pre_label: Optional[PreReleaseLabel | str] = None,
        pre_number: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        overwrite: bool = False,
    ) -> int:
        """Manually save a prompt version following SemVer 2.0.0.

        Args:
            name: Name/identifier for the prompt
            system_prompt: System prompt content
            user_prompt: User prompt content
            version: Optional explicit version string (overrides bump_type)
            bump_type: Type of version bump (MAJOR/MINOR/PATCH or "major"/"minor"/"patch")
            pre_label: Pre-release label (SNAPSHOT/M/RC/STABLE or "snapshot"/"m"/"rc"/"stable")
            pre_number: Pre-release number (for M.X or RC.X)
            metadata: Additional metadata
            overwrite: Overwrite existing version

        Returns:
            Version ID
        """
        parsed_bump = self.version_manager.parse_bump_type(bump_type)
        parsed_label = self.version_manager.parse_pre_label(pre_label)

        # Generate version if not provided
        version_str, git_commit = self._generate_version(
            name, version, parsed_bump, parsed_label, pre_number, system_prompt, user_prompt
        )

        # Check for existing version
        self._handle_existing_version(name, version_str, overwrite)

        return self.storage.save_version(
            name=name,
            version=version_str,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata=metadata,
            git_commit=git_commit,
        )

    def get_version(self, name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get a specific prompt version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            Version data or None
        """
        return self.storage.get_version(name, version)

    def get_latest(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the latest version of a prompt.

        Args:
            name: Prompt name

        Returns:
            Latest version data or None
        """
        return self.storage.get_latest_version(name)

    def list_versions(self, name: str) -> List[Dict[str, Any]]:
        """List all versions of a prompt.

        Args:
            name: Prompt name

        Returns:
            List of versions (newest first)
        """
        return self.storage.list_versions(name)

    def list_prompts(self) -> List[str]:
        """List all tracked prompt names.

        Returns:
            List of prompt names
        """
        return self.storage.list_all_prompts()

    def diff(
        self,
        name: str,
        version1: str,
        version2: str,
        format_output: bool = False,
    ) -> PromptDiff:
        """Compare two versions of a prompt.

        Args:
            name: Prompt name
            version1: First version
            version2: Second version
            format_output: If True, print formatted diff

        Returns:
            PromptDiff object
        """
        v1 = self.storage.get_version(name, version1)
        v2 = self.storage.get_version(name, version2)

        if not v1:
            raise ValueError(f"Version {version1} not found for prompt {name}")
        if not v2:
            raise ValueError(f"Version {version2} not found for prompt {name}")

        diff = DiffEngine.compute_diff(
            old_system=v1["system_prompt"],
            old_user=v1["user_prompt"],
            new_system=v2["system_prompt"],
            new_user=v2["user_prompt"],
        )

        if format_output:
            print(DiffEngine.format_diff_text(diff))

        return diff

    def rollback(self, name: str, to_version: str) -> int:
        """Rollback to a previous version (creates new version with old content).

        Args:
            name: Prompt name
            to_version: Version to rollback to

        Returns:
            New version ID
        """
        old_version = self.storage.get_version(name, to_version)

        if not old_version:
            raise ValueError(f"Version {to_version} not found for prompt {name}")

        return self.save_version(
            name=name,
            system_prompt=old_version["system_prompt"],
            user_prompt=old_version["user_prompt"],
            metadata={"rollback_from": to_version},
        )

    def compare_versions(
        self,
        name: str,
        versions: List[str],
    ) -> Dict[str, Any]:
        """Compare multiple versions with metrics.

        Args:
            name: Prompt name
            versions: List of version strings to compare

        Returns:
            Comparison data with metrics
        """
        comparison: Dict[str, Any] = {
            "versions": [],
            "metrics": {},
        }

        for version in versions:
            v = self.storage.get_version(name, version)
            if v:
                metrics = self.storage.get_metrics(v["id"])

                versions_list = cast(List[Dict[str, Any]], comparison["versions"])
                versions_list.append(
                    {
                        "version": version,
                        "timestamp": v["timestamp"],
                        "git_commit": v.get("git_commit"),
                        "metrics": metrics,
                    }
                )

        return comparison

    def log_metrics(
        self,
        name: str,
        version: str,
        model_name: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
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
    ) -> None:
        """Log metrics for a specific version.

        Args:
            name: Prompt name
            version: Version string
            model_name: Name of the LLM model
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_eur: Cost in EUR (auto-calculated if not provided)
            latency_ms: Response latency in ms
            quality_score: Quality score (0-1)
            accuracy: Accuracy score (0-1)
            temperature: Model temperature
            top_p: Model top_p parameter
            max_tokens: Max tokens parameter
            success: Whether call succeeded
            error_message: Error message if failed
            metadata: Additional metadata
        """
        v = self.storage.get_version(name, version)
        if not v:
            raise ValueError(f"Version {version} not found for prompt {name}")

        # Auto-calculate cost if not provided
        if cost_eur is None and model_name and input_tokens and output_tokens:
            cost_eur = self.metrics_calculator.calculate_cost(
                model_name, input_tokens, output_tokens
            )

        # Calculate total tokens
        total_tokens = None
        if input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens

        self.storage.save_metrics(
            version_id=v["id"],
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_eur=cost_eur,
            latency_ms=latency_ms,
            quality_score=quality_score,
            accuracy=accuracy,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            success=success,
            error_message=error_message,
            metadata=metadata,
        )

    def test_version(
        self,
        name: str,
        version: str,
    ) -> TestContext:
        """Context manager for testing a prompt version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            TestContext for logging metrics

        Example:
            with pv.test_version("my_prompt", "v1.0.0") as test:
                result = call_llm(prompt)
                test.log(tokens=150, cost=0.002)
        """
        return TestContext(self, name, version)

    def install_git_hooks(self) -> None:
        """Install Git hooks for automatic versioning."""
        if not self.git_tracker:
            raise RuntimeError("Git integration not enabled")

        self.git_tracker.install_hooks()

    def uninstall_git_hooks(self) -> None:
        """Remove Git hooks."""
        if not self.git_tracker:
            raise RuntimeError("Git integration not enabled")

        self.git_tracker.uninstall_hooks()

    def export_prompt(
        self,
        name: str,
        output_file: Path,
        format: Literal["json", "yaml"] = "json",
        include_metrics: bool = True,
    ) -> None:
        """Export all versions of a prompt to file.

        Args:
            name: Prompt name to export
            output_file: Output file path
            format: Export format (json or yaml)
            include_metrics: Whether to include metrics data
        """
        versions = self.list_versions(name)

        if not versions:
            raise ValueError(f"No versions found for prompt '{name}'")

        versions_list: List[Dict[str, Any]] = []
        export_data = {
            "prompt_name": name,
            "export_date": datetime.now(timezone.utc).isoformat(),
            "versions": versions_list,
        }

        for v in versions:
            version_data = {
                "version": v["version"],
                "system_prompt": v["system_prompt"],
                "user_prompt": v["user_prompt"],
                "metadata": v.get("metadata"),
                "git_commit": v.get("git_commit"),
                "timestamp": v["timestamp"],
            }

            if include_metrics:
                metrics_summary = self.storage.get_metrics_summary(v["id"])
                metrics_list = self.storage.get_metrics(v["id"])
                version_data["metrics_summary"] = metrics_summary
                version_data["metrics_count"] = len(metrics_list)

            versions_list.append(version_data)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            output_file.write_text(json.dumps(export_data, indent=2, ensure_ascii=False))
        elif format == "yaml":
            output_file.write_text(yaml.dump(export_data, allow_unicode=True))

        print(f"Exported {len(versions)} versions of '{name}' to {output_file}")

    def import_prompt(
        self, input_file: Path, overwrite: bool = False, bump_type: Optional[VersionBump] = None
    ) -> dict:
        """Import prompt versions from file.

        Args:
            input_file: Input file path
            overwrite: If True, overwrite existing versions
            bump_type: If specified, renumber versions with semantic versioning

        Returns:
            Dict with import statistics
        """
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {input_file}")

        content = input_file.read_text()

        if input_file.suffix == ".json":
            import_data = json.loads(content)
        elif input_file.suffix in [".yaml", ".yml"]:
            import_data = yaml.safe_load(content)
        else:
            raise ValueError(f"Unsupported format: {input_file.suffix}")

        prompt_name = import_data["prompt_name"]
        versions = import_data["versions"]

        imported = 0
        skipped = 0

        for v in versions:
            existing = self.get_version(prompt_name, v["version"])

            if existing and not overwrite:
                skipped += 1
                continue

            version_str = v["version"]
            if bump_type:
                latest = self.get_latest(prompt_name)
                current_version = latest["version"] if latest else None
                version_str = self.version_manager.calculate_next_version(
                    current_version, bump_type
                )

            self.save_version(
                name=prompt_name,
                system_prompt=v["system_prompt"],
                user_prompt=v["user_prompt"],
                version=version_str,
                metadata=v.get("metadata"),
                overwrite=overwrite,
            )
            imported += 1

        result = {
            "prompt_name": prompt_name,
            "imported": imported,
            "skipped": skipped,
            "total": len(versions),
        }

        print(f"Import completed: {imported} imported, {skipped} skipped")

        return result

    def export_all(self, output_dir: Path, format: Literal["json", "yaml"] = "json") -> None:
        """Export all prompts to directory.

        Args:
            output_dir: Output directory
            format: Export format
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        prompts = self.list_prompts()

        for prompt_name in prompts:
            safe_name = prompt_name.replace("/", "_").replace("\\", "_")
            output_file = output_dir / f"{safe_name}.{format}"
            self.export_prompt(prompt_name, output_file, format)

        print(f"Exported {len(prompts)} prompts to {output_dir}")

    def add_annotation(self, name: str, version: str, text: str, author: str = "unknown") -> None:
        """Add annotation to a prompt version.

        Args:
            name: Prompt name
            version: Version string
            text: Annotation text
            author: Author name/email
        """
        v = self.get_version(name, version)
        if not v:
            raise ValueError(f"Version {version} not found for prompt {name}")

        self.storage.add_annotation(v["id"], author, text)
        print(f"Added annotation to {name} v{version} by {author}")

    def get_annotations(self, name: str, version: str) -> List[Dict[str, Any]]:
        """Get annotations for a version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            List of annotations
        """
        v = self.get_version(name, version)
        if not v:
            return []

        return self.storage.get_annotations(v["id"])

    def delete_version(self, name: str, version: str) -> bool:
        """Delete a specific version of a prompt (and related data).

        Args:
            name: Prompt name
            version: Version string

        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete_version(name, version)

    def delete_prompt(self, name: str) -> bool:
        """Delete a prompt and all its versions (and related data).

        Args:
            name: Prompt name

        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete_prompt(name)

    # Private helper methods

    def _extract_prompts(self, result: Any) -> tuple[str, str]:
        """Extract system and user prompts from function result.

        Args:
            result: Function return value

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        if isinstance(result, dict):
            system_prompt = result.get("system", "")
            user_prompt = result.get("user", "")
        elif isinstance(result, tuple) and len(result) == 2:
            system_prompt, user_prompt = result
        else:
            raise ValueError(
                "Tracked function must return dict with 'system' and 'user' keys, "
                "or tuple of (system, user)"
            )

        return system_prompt, user_prompt

    def _generate_version(
        self,
        name: str,
        version: Optional[str],
        bump_type: Optional[VersionBump],
        pre_label: Optional[PreReleaseLabel],
        pre_number: Optional[int],
        system_prompt: str,
        user_prompt: str,
    ) -> tuple[str, Optional[str]]:
        """Generate version string and git commit.

        Args:
            name: Prompt name
            version: Explicit version or None
            bump_type: Version bump type
            pre_label: Pre-release label
            pre_number: Pre-release number
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Tuple of (version_string, git_commit)
        """
        if version is None:
            if bump_type is not None:
                # Semantic versioning
                latest = self.get_latest(name)
                current_version = latest["version"] if latest else None
                version = self.version_manager.calculate_next_version(
                    current_version, bump_type, pre_label, pre_number
                )
                git_commit = self.git_tracker.get_current_commit() if self.git_tracker else None
            elif self.git_tracker:
                # Git-based versioning (fallback)
                version = self.git_tracker.get_version_string()
                git_commit = self.git_tracker.get_current_commit()
            else:
                # Hash-based versioning (fallback)
                version = PromptHasher.compute_hash(system_prompt, user_prompt)
                git_commit = None
        else:
            git_commit = self.git_tracker.get_current_commit() if self.git_tracker else None

        return version, git_commit

    def _handle_existing_version(self, name: str, version: str, overwrite: bool) -> None:
        """Handle existing version conflict.

        Args:
            name: Prompt name
            version: Version string
            overwrite: Whether to overwrite existing

        Raises:
            ValueError: If version exists and overwrite is False
        """
        existing = self.get_version(name, version)
        if existing:
            if overwrite:
                self.storage.delete_version(name, version)
                print(f"Overwriting existing version {version} for {name}")
            else:
                raise ValueError(
                    f"Version {version} already exists for prompt '{name}'. "
                    f"Use overwrite=True to replace it or use a different bump_type."
                )
