"""Automatic tracking of prompt changes."""

from typing import Optional, Any
from prompt_versioner.tracker.git import GitTracker
from prompt_versioner.tracker.hasher import PromptHasher
from prompt_versioner.storage import PromptStorage


class AutoTracker:
    """Automatic tracking of prompt changes."""

    def __init__(self, storage: PromptStorage, git_tracker: Optional[GitTracker] = None) -> None:
        """Initialize auto tracker.

        Args:
            storage: PromptStorage instance
            git_tracker: Optional GitTracker instance
        """
        self.storage = storage
        self.git_tracker = git_tracker

    def should_auto_version(
        self,
        name: str,
        system_prompt: str,
        user_prompt: str,
    ) -> bool:
        """Check if prompts should be auto-versioned.

        Args:
            name: Prompt name
            system_prompt: System prompt content
            user_prompt: User prompt content

        Returns:
            True if prompts have changed since last version
        """
        latest = self.storage.get_latest_version(name)

        if latest is None:
            return True

        return PromptHasher.has_changed(
            latest["system_prompt"],
            latest["user_prompt"],
            system_prompt,
            user_prompt,
        )

    def get_change_summary(
        self,
        name: str,
        system_prompt: str,
        user_prompt: str,
    ) -> Optional[dict]:
        """Get summary of what changed.

        Args:
            name: Prompt name
            system_prompt: System prompt content
            user_prompt: User prompt content

        Returns:
            Dict with change details or None if no previous version
        """
        latest = self.storage.get_latest_version(name)

        if latest is None:
            return None

        changes = PromptHasher.detect_changes(
            latest["system_prompt"],
            latest["user_prompt"],
            system_prompt,
            user_prompt,
        )

        changes["previous_version"] = latest["version"]
        changes["previous_hash"] = PromptHasher.compute_hash(
            latest["system_prompt"], latest["user_prompt"]
        )
        changes["new_hash"] = PromptHasher.compute_hash(system_prompt, user_prompt)

        return changes

    def auto_version(
        self,
        name: str,
        system_prompt: str,
        user_prompt: str,
        metadata: Optional[dict] = None,
    ) -> Optional[int]:
        """Automatically version prompts if changed.

        Args:
            name: Prompt name
            system_prompt: System prompt content
            user_prompt: User prompt content
            metadata: Optional metadata

        Returns:
            Version ID if saved, None if unchanged
        """
        if not self.should_auto_version(name, system_prompt, user_prompt):
            return None

        # Generate version string and metadata
        version_metadata = self._generate_version_metadata(system_prompt, user_prompt, metadata)

        # Save version
        return self.storage.save_version(
            name=name,
            version=version_metadata["version"],
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata=version_metadata.get("metadata"),
            git_commit=version_metadata.get("git_commit"),
        )

    def _generate_version_metadata(
        self,
        system_prompt: str,
        user_prompt: str,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Generate version string and metadata.

        Args:
            system_prompt: System prompt content
            user_prompt: User prompt content
            metadata: Optional user metadata

        Returns:
            Dict with 'version', 'git_commit', and 'metadata'
        """

        # Ensure metadata is always a dict[str, Any]
        meta_dict: dict[str, Any]
        if isinstance(metadata, dict):
            meta_dict = dict(metadata)
        elif metadata is None:
            meta_dict = {}
        else:
            raise TypeError("metadata must be a dict or None")

        result: dict[str, Any] = {"metadata": meta_dict, "version": "", "git_commit": None}

        if self.git_tracker:
            try:
                # Try to get Git version
                result["version"] = self.git_tracker.get_version_string()
                result["git_commit"] = self.git_tracker.get_current_commit()

                # Add full Git metadata
                git_metadata = self.git_tracker.get_full_metadata()
                result["metadata"]["git"] = git_metadata

            except Exception as e:
                # Fallback if Git operations fail
                result["version"] = PromptHasher.compute_hash(system_prompt, user_prompt)
                result["git_commit"] = None
                result["metadata"]["git_error"] = str(e)
        else:
            # No Git tracker, use hash
            result["version"] = PromptHasher.compute_hash(system_prompt, user_prompt)
            result["git_commit"] = None

        return result

    def force_version(
        self,
        name: str,
        system_prompt: str,
        user_prompt: str,
        version: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> int:
        """Force create a new version even if unchanged.

        Args:
            name: Prompt name
            system_prompt: System prompt content
            user_prompt: User prompt content
            version: Optional custom version string
            metadata: Optional metadata

        Returns:
            Version ID
        """
        if version is None:
            version_metadata = self._generate_version_metadata(system_prompt, user_prompt, metadata)
            version_str = version_metadata["version"]
            git_commit = version_metadata.get("git_commit")
        else:
            version_str = version
            git_commit = None

        return self.storage.save_version(
            name=name,
            version=version_str,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata=metadata,
            git_commit=git_commit,
        )

    def get_versioning_config(self) -> dict:
        """Get current versioning configuration.

        Returns:
            Dict with tracker configuration
        """
        config = {
            "has_git": self.git_tracker is not None,
            "hash_algorithm": PromptHasher.HASH_ALGORITHM,
            "hash_length": PromptHasher.HASH_LENGTH,
        }

        if self.git_tracker:
            try:
                config["git_branch"] = self.git_tracker.get_current_branch()
                config["git_commit"] = self.git_tracker.get_current_commit()
                config["git_dirty"] = self.git_tracker.is_dirty()
                config["git_remote"] = self.git_tracker.get_remote_url()
            except Exception as e:
                config["git_error"] = str(e)

        return config
