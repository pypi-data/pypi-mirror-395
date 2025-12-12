"""Enums for versioning."""

from enum import Enum


class VersionBump(Enum):
    """Type of version bump following SemVer 2.0.0."""

    MAJOR = "major"  # Breaking changes (non retrocompatibile)
    MINOR = "minor"  # New features (retrocompatibile)
    PATCH = "patch"  # Bug fixes (retrocompatibile)


class PreReleaseLabel(Enum):
    """Pre-release labels for versioning."""

    SNAPSHOT = "SNAPSHOT"  # Development version
    MILESTONE = "M"  # Milestone version
    RC = "RC"  # Release Candidate
    STABLE = None  # Stable release (no label)
