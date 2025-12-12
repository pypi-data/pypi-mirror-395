"""Semantic version management."""

import re
from typing import Optional, Dict
from prompt_versioner.core.enums import VersionBump, PreReleaseLabel


class VersionManager:
    """Manager for semantic versioning operations."""

    @staticmethod
    def parse_bump_type(bump_type: VersionBump | str | None) -> Optional[VersionBump]:
        """Parse bump type from string or enum.

        Args:
            bump_type: VersionBump enum or string ("major", "minor", "patch")

        Returns:
            VersionBump enum or None

        Examples:
            >>> parse_bump_type("patch")
            VersionBump.PATCH
            >>> parse_bump_type("MAJOR")
            VersionBump.MAJOR
            >>> parse_bump_type(VersionBump.MINOR)
            VersionBump.MINOR
        """
        if bump_type is None:
            return None

        if isinstance(bump_type, VersionBump):
            return bump_type

        if isinstance(bump_type, str):
            bump_map = {
                "major": VersionBump.MAJOR,
                "minor": VersionBump.MINOR,
                "patch": VersionBump.PATCH,
            }
            return bump_map.get(bump_type.lower())

        return None

    @staticmethod
    def parse_pre_label(pre_label: PreReleaseLabel | str | None) -> Optional[PreReleaseLabel]:
        """Parse pre-release label from string or enum.

        Args:
            pre_label: PreReleaseLabel enum or string

        Returns:
            PreReleaseLabel enum or None

        Examples:
            >>> parse_pre_label("snapshot")
            PreReleaseLabel.SNAPSHOT
            >>> parse_pre_label("RC")
            PreReleaseLabel.RC
            >>> parse_pre_label("m")
            PreReleaseLabel.MILESTONE
            >>> parse_pre_label("stable")
            PreReleaseLabel.STABLE
        """
        if pre_label is None:
            return None

        if isinstance(pre_label, PreReleaseLabel):
            return pre_label

        if isinstance(pre_label, str):
            label_map = {
                "snapshot": PreReleaseLabel.SNAPSHOT,
                "milestone": PreReleaseLabel.MILESTONE,
                "m": PreReleaseLabel.MILESTONE,
                "rc": PreReleaseLabel.RC,
                "release_candidate": PreReleaseLabel.RC,
                "stable": PreReleaseLabel.STABLE,
                "": PreReleaseLabel.STABLE,
            }
            return label_map.get(pre_label.lower())

        return None

    @staticmethod
    def parse_version(version_string: str) -> Optional[Dict]:
        """Parse a semantic version string.

        Args:
            version_string: Version string (e.g., "1.2.3-RC.1")

        Returns:
            Dict with parsed components or None if invalid
        """
        # Pattern: MAJOR.MINOR.PATCH[-PRERELEASE]
        pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([A-Za-z]+)(?:\.(\d+))?)?$"
        match = re.match(pattern, version_string)

        if not match:
            return None

        major, minor, patch, pre_label, pre_number = match.groups()

        return {
            "major": int(major),
            "minor": int(minor),
            "patch": int(patch),
            "pre_label": pre_label,
            "pre_number": int(pre_number) if pre_number else None,
        }

    @staticmethod
    def format_version(
        major: int,
        minor: int,
        patch: int,
        pre_label: Optional[PreReleaseLabel] = None,
        pre_number: Optional[int] = None,
    ) -> str:
        """Format version components into string.

        Args:
            major: Major version
            minor: Minor version
            patch: Patch version
            pre_label: Pre-release label (optional)
            pre_number: Pre-release number (optional)

        Returns:
            Formatted version string
        """
        base = f"{major}.{minor}.{patch}"

        if pre_label and pre_label != PreReleaseLabel.STABLE:
            if pre_number is not None:
                return f"{base}-{pre_label.value}.{pre_number}"
            else:
                return f"{base}-{pre_label.value}"

        return base

    @staticmethod
    def calculate_next_version(
        current_version: Optional[str],
        bump_type: VersionBump,
        pre_label: Optional[PreReleaseLabel] = None,
        pre_number: Optional[int] = None,
    ) -> str:
        """Calculate next semantic version following SemVer 2.0.0.

        Args:
            current_version: Current version string (e.g., "1.2.3-RC.1") or None
            bump_type: Type of version bump (MAJOR, MINOR, PATCH)
            pre_label: Pre-release label (SNAPSHOT, M, RC, or STABLE)
            pre_number: Pre-release number (for M.X or RC.X)

        Returns:
            Next version string

        Examples:
            >>> calculate_next_version(None, VersionBump.PATCH)
            "1.0.0"

            >>> calculate_next_version("1.0.0", VersionBump.PATCH, PreReleaseLabel.SNAPSHOT)
            "1.0.1-SNAPSHOT"

            >>> calculate_next_version("1.0.0", VersionBump.MINOR, PreReleaseLabel.MILESTONE, 1)
            "1.1.0-M.1"

            >>> calculate_next_version("1.0.0-RC.1", VersionBump.PATCH, PreReleaseLabel.RC, 2)
            "1.0.0-RC.2"

            >>> calculate_next_version("1.0.0-RC.2", VersionBump.PATCH, PreReleaseLabel.STABLE)
            "1.0.0"
        """
        # First version
        if current_version is None:
            major, minor, patch = 1, 0, 0
        else:
            # Parse current version
            parsed = VersionManager.parse_version(current_version)
            if not parsed:
                # Invalid format, start fresh
                major, minor, patch = 1, 0, 0
            else:
                major = parsed["major"]
                minor = parsed["minor"]
                patch = parsed["patch"]

                # If current is pre-release and new is stable with same version, keep numbers
                if (
                    pre_label == PreReleaseLabel.STABLE
                    and parsed["pre_label"] is not None
                    and bump_type == VersionBump.PATCH
                ):
                    # Releasing stable from pre-release, keep version
                    pass
                # Otherwise bump version
                elif bump_type == VersionBump.MAJOR:
                    major += 1
                    minor = 0
                    patch = 0
                elif bump_type == VersionBump.MINOR:
                    minor += 1
                    patch = 0
                elif bump_type == VersionBump.PATCH:
                    patch += 1

        return VersionManager.format_version(major, minor, patch, pre_label, pre_number)

    @staticmethod
    def is_valid_semver(version_string: str) -> bool:
        """Check if version string is valid SemVer.

        Args:
            version_string: Version string to validate

        Returns:
            True if valid
        """
        return VersionManager.parse_version(version_string) is not None

    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        """Compare two semantic versions.

        Args:
            version1: First version
            version2: Second version

        Returns:
            -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        v1 = VersionManager.parse_version(version1)
        v2 = VersionManager.parse_version(version2)

        if not v1 or not v2:
            # Fallback to string comparison
            return -1 if version1 < version2 else (1 if version1 > version2 else 0)

        # Compare major.minor.patch
        for key in ["major", "minor", "patch"]:
            if v1[key] < v2[key]:
                return -1
            elif v1[key] > v2[key]:
                return 1

        # If base versions equal, compare pre-release
        # Stable > pre-release
        if v1["pre_label"] is None and v2["pre_label"] is not None:
            return 1
        if v1["pre_label"] is not None and v2["pre_label"] is None:
            return -1

        # Both have pre-release, compare
        if v1["pre_label"] and v2["pre_label"]:
            if v1["pre_label"] != v2["pre_label"]:
                # SNAPSHOT < M < RC
                order = {"SNAPSHOT": 1, "M": 2, "RC": 3}
                return -1 if order.get(v1["pre_label"], 0) < order.get(v2["pre_label"], 0) else 1

            # Same pre-label, compare numbers
            num1 = v1["pre_number"] or 0
            num2 = v2["pre_number"] or 0
            return -1 if num1 < num2 else (1 if num1 > num2 else 0)

        return 0
