"""Git integration for prompt versioning."""

import subprocess  # nosec: B404
from pathlib import Path
from typing import Optional


class GitTracker:
    """Handles Git integration for prompt versioning."""

    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize Git tracker.

        Args:
            repo_path: Path to Git repository. Defaults to current directory.
        """
        self.repo_path = repo_path or Path.cwd()
        self._check_git_repo()

    def _check_git_repo(self) -> None:
        """Check if we're in a Git repository."""
        try:
            self._run_git_command(["rev-parse", "--git-dir"])
        except subprocess.CalledProcessError:
            raise RuntimeError(f"Not a git repository: {self.repo_path}")

    def _run_git_command(self, args: list[str]) -> str:
        """Run a git command and return output.

        Args:
            args: Git command arguments

        Returns:
            Command output as string

        Raises:
            subprocess.CalledProcessError: If git command fails
        """
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True,
        )  # nosec: B603 -- only trusted git commands executed
        return result.stdout.strip()

    def get_current_commit(self) -> str:
        """Get current Git commit hash.

        Returns:
            Short commit hash (7 characters)
        """
        return self._run_git_command(["rev-parse", "--short", "HEAD"])

    def get_current_branch(self) -> str:
        """Get current Git branch name.

        Returns:
            Branch name
        """
        return self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

    def get_commit_message(self, commit_hash: Optional[str] = None) -> str:
        """Get commit message.

        Args:
            commit_hash: Specific commit hash, or HEAD if None

        Returns:
            Commit message
        """
        ref = commit_hash or "HEAD"
        return self._run_git_command(["log", "-1", "--pretty=%B", ref])

    def get_author_info(self, commit_hash: Optional[str] = None) -> dict:
        """Get commit author information.

        Args:
            commit_hash: Specific commit hash, or HEAD if None

        Returns:
            Dict with 'name' and 'email'
        """
        ref = commit_hash or "HEAD"
        name = self._run_git_command(["log", "-1", "--pretty=%an", ref])
        email = self._run_git_command(["log", "-1", "--pretty=%ae", ref])
        return {"name": name, "email": email}

    def is_dirty(self) -> bool:
        """Check if there are uncommitted changes.

        Returns:
            True if there are uncommitted changes
        """
        try:
            output = self._run_git_command(["status", "--porcelain"])
            return bool(output)
        except subprocess.CalledProcessError:
            return False

    def get_changed_files(self) -> list[str]:
        """Get list of changed files.

        Returns:
            List of changed file paths
        """
        try:
            output = self._run_git_command(["status", "--porcelain"])
            if not output:
                return []

            files = []
            for line in output.splitlines():
                # Parse status line format: "XY filename"
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    files.append(parts[1])
            return files
        except subprocess.CalledProcessError:
            return []

    def get_version_string(self) -> str:
        """Generate version string based on Git state.

        Returns:
            Version string in format: branch-commit[-dirty]
        """
        branch = self.get_current_branch()
        commit = self.get_current_commit()
        dirty = "-dirty" if self.is_dirty() else ""
        return f"{branch}-{commit}{dirty}"

    def get_full_metadata(self) -> dict:
        """Get comprehensive Git metadata.

        Returns:
            Dict with branch, commit, author, message, dirty status
        """
        try:
            return {
                "branch": self.get_current_branch(),
                "commit": self.get_current_commit(),
                "author": self.get_author_info(),
                "message": self.get_commit_message(),
                "dirty": self.is_dirty(),
                "changed_files": self.get_changed_files() if self.is_dirty() else [],
            }
        except Exception as e:
            # Return minimal metadata if Git operations fail
            return {
                "error": str(e),
                "dirty": False,
            }

    def install_hooks(self) -> None:
        """Install Git hooks for automatic prompt versioning.

        Raises:
            RuntimeError: If hooks directory doesn't exist
        """
        hooks_dir = self.repo_path / ".git" / "hooks"

        if not hooks_dir.parent.exists():
            raise RuntimeError("Not a git repository (no .git directory)")

        hooks_dir.mkdir(exist_ok=True)

        # Pre-commit hook
        pre_commit_hook = hooks_dir / "pre-commit"
        pre_commit_content = """#!/bin/bash
# Auto-generated by prompt-versioner
# This hook automatically versions prompts before commits

prompt-versioner auto-version --pre-commit

exit 0
"""

        pre_commit_hook.write_text(pre_commit_content)
        pre_commit_hook.chmod(0o755)

        # Post-commit hook
        post_commit_hook = hooks_dir / "post-commit"
        post_commit_content = """#!/bin/bash
# Auto-generated by prompt-versioner
# This hook automatically versions prompts after commits

prompt-versioner auto-version --post-commit

exit 0
"""

        post_commit_hook.write_text(post_commit_content)
        post_commit_hook.chmod(0o755)

    def uninstall_hooks(self) -> None:
        """Remove Git hooks installed by prompt-versioner."""
        hooks_dir = self.repo_path / ".git" / "hooks"

        for hook_name in ["pre-commit", "post-commit"]:
            hook_path = hooks_dir / hook_name
            if hook_path.exists():
                content = hook_path.read_text()
                if "prompt-versioner" in content:
                    hook_path.unlink()

    def get_remote_url(self) -> Optional[str]:
        """Get remote origin URL.

        Returns:
            Remote URL or None if not configured
        """
        try:
            return self._run_git_command(["config", "--get", "remote.origin.url"])
        except subprocess.CalledProcessError:
            return None

    def get_tags_at_commit(self, commit_hash: Optional[str] = None) -> list[str]:
        """Get tags pointing to a commit.

        Args:
            commit_hash: Specific commit hash, or HEAD if None

        Returns:
            List of tag names
        """
        try:
            ref = commit_hash or "HEAD"
            output = self._run_git_command(["tag", "--points-at", ref])
            return output.splitlines() if output else []
        except subprocess.CalledProcessError:
            return []
