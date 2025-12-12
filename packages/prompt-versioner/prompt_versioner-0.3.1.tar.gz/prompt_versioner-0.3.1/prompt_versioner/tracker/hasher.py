"""Hashing and change detection for prompts."""

import hashlib
from typing import Tuple


class PromptHasher:
    """Handles hashing and change detection for prompts."""

    # Hash algorithm to use
    HASH_ALGORITHM = "sha256"

    # Number of characters to use from hash
    HASH_LENGTH = 16

    @staticmethod
    def compute_hash(system_prompt: str, user_prompt: str) -> str:
        """Compute hash of prompt pair.

        Args:
            system_prompt: System prompt content
            user_prompt: User prompt content

        Returns:
            SHA256 hash of concatenated prompts (truncated)
        """
        combined = f"{system_prompt}\n---\n{user_prompt}"
        hash_obj = hashlib.new(PromptHasher.HASH_ALGORITHM)
        hash_obj.update(combined.encode("utf-8"))
        return hash_obj.hexdigest()[: PromptHasher.HASH_LENGTH]

    @staticmethod
    def compute_hash_full(system_prompt: str, user_prompt: str) -> str:
        """Compute full hash of prompt pair.

        Args:
            system_prompt: System prompt content
            user_prompt: User prompt content

        Returns:
            Full SHA256 hash
        """
        combined = f"{system_prompt}\n---\n{user_prompt}"
        hash_obj = hashlib.new(PromptHasher.HASH_ALGORITHM)
        hash_obj.update(combined.encode("utf-8"))
        return hash_obj.hexdigest()

    @staticmethod
    def compute_individual_hashes(system_prompt: str, user_prompt: str) -> Tuple[str, str]:
        """Compute separate hashes for system and user prompts.

        Args:
            system_prompt: System prompt content
            user_prompt: User prompt content

        Returns:
            Tuple of (system_hash, user_hash)
        """
        system_hash = hashlib.new(PromptHasher.HASH_ALGORITHM)
        system_hash.update(system_prompt.encode("utf-8"))

        user_hash = hashlib.new(PromptHasher.HASH_ALGORITHM)
        user_hash.update(user_prompt.encode("utf-8"))

        return (
            system_hash.hexdigest()[: PromptHasher.HASH_LENGTH],
            user_hash.hexdigest()[: PromptHasher.HASH_LENGTH],
        )

    @staticmethod
    def has_changed(
        old_system: str,
        old_user: str,
        new_system: str,
        new_user: str,
    ) -> bool:
        """Check if prompts have changed.

        Args:
            old_system: Original system prompt
            old_user: Original user prompt
            new_system: New system prompt
            new_user: New user prompt

        Returns:
            True if prompts differ
        """
        old_hash = PromptHasher.compute_hash(old_system, old_user)
        new_hash = PromptHasher.compute_hash(new_system, new_user)
        return old_hash != new_hash

    @staticmethod
    def detect_changes(
        old_system: str,
        old_user: str,
        new_system: str,
        new_user: str,
    ) -> dict:
        """Detect what changed between prompt versions.

        Args:
            old_system: Original system prompt
            old_user: Original user prompt
            new_system: New system prompt
            new_user: New user prompt

        Returns:
            Dict with 'system_changed', 'user_changed', 'both_changed'
        """
        system_changed = old_system != new_system
        user_changed = old_user != new_user

        return {
            "system_changed": system_changed,
            "user_changed": user_changed,
            "both_changed": system_changed and user_changed,
            "no_changes": not (system_changed or user_changed),
        }

    @staticmethod
    def compute_similarity(text1: str, text2: str) -> float:
        """Compute similarity ratio between two texts.

        Uses simple character-level comparison.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity ratio between 0.0 and 1.0
        """
        if text1 == text2:
            return 1.0

        if not text1 or not text2:
            return 0.0

        # Simple character-level similarity
        len1, len2 = len(text1), len(text2)
        max_len = max(len1, len2)

        # Count matching characters at same positions
        matches = sum(c1 == c2 for c1, c2 in zip(text1, text2))

        return matches / max_len if max_len > 0 else 0.0

    @staticmethod
    def verify_hash(system_prompt: str, user_prompt: str, expected_hash: str) -> bool:
        """Verify if prompts match expected hash.

        Args:
            system_prompt: System prompt content
            user_prompt: User prompt content
            expected_hash: Expected hash to verify against

        Returns:
            True if hash matches
        """
        actual_hash = PromptHasher.compute_hash(system_prompt, user_prompt)
        return actual_hash == expected_hash
