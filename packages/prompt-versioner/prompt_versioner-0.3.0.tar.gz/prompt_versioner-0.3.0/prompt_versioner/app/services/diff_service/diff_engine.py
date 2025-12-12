"""Semantic diff engine for prompts."""

import difflib
from typing import List
from prompt_versioner.app.models import PromptDiff, PromptChange, ChangeType


class DiffEngine:
    """Engine for computing semantic diffs between prompts."""

    @staticmethod
    def compute_diff(
        old_system: str,
        old_user: str,
        new_system: str,
        new_user: str,
    ) -> PromptDiff:
        """Compute comprehensive diff between two prompt versions.

        Args:
            old_system: Original system prompt
            old_user: Original user prompt
            new_system: New system prompt
            new_user: New user prompt

        Returns:
            PromptDiff object with detailed changes
        """
        # Compute changes for each prompt type
        system_changes = DiffEngine._compute_line_changes(old_system, new_system)
        user_changes = DiffEngine._compute_line_changes(old_user, new_user)

        # Compute similarity scores
        system_similarity = DiffEngine._compute_similarity(old_system, new_system)
        user_similarity = DiffEngine._compute_similarity(old_user, new_user)

        # Weighted total similarity (can adjust weights as needed)
        total_similarity = (system_similarity + user_similarity) / 2

        # Generate summary
        summary = DiffEngine._generate_summary(
            system_changes, user_changes, system_similarity, user_similarity
        )

        return PromptDiff(
            system_changes=system_changes,
            user_changes=user_changes,
            system_similarity=system_similarity,
            user_similarity=user_similarity,
            total_similarity=total_similarity,
            summary=summary,
        )

    @staticmethod
    def _compute_line_changes(old_text: str, new_text: str) -> List[PromptChange]:
        """Compute line-by-line changes between two texts.

        Args:
            old_text: Original text
            new_text: New text

        Returns:
            List of PromptChange objects
        """
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()

        changes: List[PromptChange] = []
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for idx, line in enumerate(old_lines[i1:i2]):
                    changes.append(
                        PromptChange(
                            change_type=ChangeType.UNCHANGED,
                            old_line=line,
                            new_line=line,
                            line_number=i1 + idx,
                        )
                    )
            elif tag == "delete":
                for idx, line in enumerate(old_lines[i1:i2]):
                    changes.append(
                        PromptChange(
                            change_type=ChangeType.REMOVED,
                            old_line=line,
                            new_line="",
                            line_number=i1 + idx,
                        )
                    )
            elif tag == "insert":
                for idx, line in enumerate(new_lines[j1:j2]):
                    changes.append(
                        PromptChange(
                            change_type=ChangeType.ADDED,
                            old_line="",
                            new_line=line,
                            line_number=j1 + idx,
                        )
                    )
            elif tag == "replace":
                # Handle replacements
                for idx in range(max(i2 - i1, j2 - j1)):
                    old_line = old_lines[i1 + idx] if i1 + idx < i2 else ""
                    new_line = new_lines[j1 + idx] if j1 + idx < j2 else ""
                    changes.append(
                        PromptChange(
                            change_type=ChangeType.MODIFIED,
                            old_line=old_line,
                            new_line=new_line,
                            line_number=i1 + idx,
                        )
                    )

        return changes

    @staticmethod
    def _compute_similarity(old_text: str, new_text: str) -> float:
        """Compute similarity ratio between two texts.

        Args:
            old_text: Original text
            new_text: New text

        Returns:
            Similarity ratio (0.0 to 1.0)
        """
        return difflib.SequenceMatcher(None, old_text, new_text).ratio()

    @staticmethod
    def _generate_summary(
        system_changes: List[PromptChange],
        user_changes: List[PromptChange],
        system_similarity: float,
        user_similarity: float,
    ) -> str:
        """Generate human-readable summary of changes.

        Args:
            system_changes: List of system prompt changes
            user_changes: List of user prompt changes
            system_similarity: System prompt similarity score
            user_similarity: User prompt similarity score

        Returns:
            Summary string
        """
        system_added = sum(1 for c in system_changes if c.change_type == ChangeType.ADDED)
        system_removed = sum(1 for c in system_changes if c.change_type == ChangeType.REMOVED)
        system_modified = sum(1 for c in system_changes if c.change_type == ChangeType.MODIFIED)

        user_added = sum(1 for c in user_changes if c.change_type == ChangeType.ADDED)
        user_removed = sum(1 for c in user_changes if c.change_type == ChangeType.REMOVED)
        user_modified = sum(1 for c in user_changes if c.change_type == ChangeType.MODIFIED)

        parts = []

        # System prompt summary
        if system_added or system_removed or system_modified:
            sys_parts = []
            if system_added:
                sys_parts.append(f"+{system_added} lines")
            if system_removed:
                sys_parts.append(f"-{system_removed} lines")
            if system_modified:
                sys_parts.append(f"~{system_modified} lines")
            parts.append(f"System: {', '.join(sys_parts)} ({system_similarity:.1%} similar)")
        else:
            parts.append("System: unchanged")

        # User prompt summary
        if user_added or user_removed or user_modified:
            usr_parts = []
            if user_added:
                usr_parts.append(f"+{user_added} lines")
            if user_removed:
                usr_parts.append(f"-{user_removed} lines")
            if user_modified:
                usr_parts.append(f"~{user_modified} lines")
            parts.append(f"User: {', '.join(usr_parts)} ({user_similarity:.1%} similar)")
        else:
            parts.append("User: unchanged")

        return " | ".join(parts)

    @staticmethod
    def format_diff_text(diff: PromptDiff, context_lines: int = 3) -> str:
        """Format diff as colored text output (Unix diff style).

        Args:
            diff: PromptDiff object
            context_lines: Number of context lines to show around changes

        Returns:
            Formatted diff string
        """
        output = []

        output.append("=" * 80)
        output.append(f"DIFF SUMMARY: {diff.summary}")
        output.append(f"Total Similarity: {diff.total_similarity:.1%}")
        output.append("=" * 80)

        # System prompt diff
        if diff.system_changes:
            output.append("\n--- SYSTEM PROMPT ---")
            output.append(DiffEngine._format_changes(diff.system_changes, context_lines))

        # User prompt diff
        if diff.user_changes:
            output.append("\n--- USER PROMPT ---")
            output.append(DiffEngine._format_changes(diff.user_changes, context_lines))

        return "\n".join(output)

    @staticmethod
    def _format_changes(changes: List[PromptChange], context_lines: int) -> str:
        """Format a list of changes with context.

        Args:
            changes: List of PromptChange objects
            context_lines: Number of context lines to show

        Returns:
            Formatted string
        """
        output = []

        for i, change in enumerate(changes):
            # Show context or changed lines
            if change.change_type == ChangeType.UNCHANGED:
                # Only show if near a change
                show = False
                for j in range(max(0, i - context_lines), min(len(changes), i + context_lines + 1)):
                    if changes[j].change_type != ChangeType.UNCHANGED:
                        show = True
                        break

                if show:
                    output.append(f"  {change.old_line}")
            elif change.change_type == ChangeType.ADDED:
                output.append(f"+ {change.new_line}")
            elif change.change_type == ChangeType.REMOVED:
                output.append(f"- {change.old_line}")
            elif change.change_type == ChangeType.MODIFIED:
                output.append(f"- {change.old_line}")
                output.append(f"+ {change.new_line}")

        return "\n".join(output)
