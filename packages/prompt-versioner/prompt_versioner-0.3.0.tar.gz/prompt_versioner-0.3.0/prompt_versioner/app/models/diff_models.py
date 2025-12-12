from dataclasses import dataclass
from enum import Enum
from typing import List


class ChangeType(Enum):
    """Type of change in a prompt."""

    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


@dataclass
class PromptChange:
    """Represents a change in a prompt."""

    change_type: ChangeType
    old_line: str
    new_line: str
    line_number: int


@dataclass
class PromptDiff:
    """Complete diff between two prompt versions."""

    system_changes: List[PromptChange]
    user_changes: List[PromptChange]
    system_similarity: float
    user_similarity: float
    total_similarity: float
    summary: str
