"""Utilities for creating inline diffs."""

import difflib
from typing import List, Dict


def create_inline_diff(old_text: str, new_text: str) -> List[Dict[str, str]]:
    """Create word-level inline diff for highlighting.

    Args:
        old_text: Previous text
        new_text: New text

    Returns:
        List of dicts with 'type' and 'text' for each segment
    """
    old_words = old_text.split()
    new_words = new_text.split()

    diff_result = []
    matcher = difflib.SequenceMatcher(None, old_words, new_words)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            diff_result.append({"type": "unchanged", "text": " ".join(new_words[j1:j2])})
        elif tag == "delete":
            diff_result.append({"type": "removed", "text": " ".join(old_words[i1:i2])})
        elif tag == "insert":
            diff_result.append({"type": "added", "text": " ".join(new_words[j1:j2])})
        elif tag == "replace":
            diff_result.append({"type": "removed", "text": " ".join(old_words[i1:i2])})
            diff_result.append({"type": "added", "text": " ".join(new_words[j1:j2])})

    return diff_result
