"""Test dataset management."""

from typing import List, Dict, Optional, Callable, Iterator, Any

from prompt_versioner.testing.models import TestCase


class TestDataset:
    """Collection of test cases."""

    def __init__(self, name: str):
        """Initialize test dataset.

        Args:
            name: Dataset name
        """
        self.name = name
        self.test_cases: List[TestCase] = []

    def add_test(
        self,
        name: str,
        inputs: Dict[str, Any],
        expected_output: Optional[Any] = None,
        validation_fn: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """Add a test case to the dataset.

        Args:
            name: Test case name
            inputs: Input dict for the prompt
            expected_output: Optional expected output
            validation_fn: Optional validation function
        """
        self.test_cases.append(
            TestCase(
                name=name,
                inputs=inputs,
                expected_output=expected_output,
                validation_fn=validation_fn,
            )
        )

    def add_tests_from_list(
        self,
        tests: List[Dict[str, Any]],
        validation_fn: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """Add multiple test cases from a list.

        Args:
            tests: List of dicts with 'name', 'inputs', 'expected_output' keys
            validation_fn: Optional validation function for all tests
        """
        for test in tests:
            self.add_test(
                name=test["name"],
                inputs=test["inputs"],
                expected_output=test.get("expected_output"),
                validation_fn=validation_fn,
            )

    def add_tests_from_csv(self, csv_path: str, input_columns: List[str]) -> None:
        """Add test cases from CSV file.

        Args:
            csv_path: Path to CSV file
            input_columns: Column names to use as inputs
        """
        import csv

        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                inputs = {col: row[col] for col in input_columns if col in row}
                expected = row.get("expected_output")

                self.add_test(name=f"test_{i}", inputs=inputs, expected_output=expected)

    def add_tests_from_json(self, json_path: str) -> None:
        """Add test cases from JSON file.

        Args:
            json_path: Path to JSON file
        """
        import json

        with open(json_path, "r") as f:
            data = json.load(f)

        if isinstance(data, list):
            self.add_tests_from_list(data)
        else:
            raise ValueError("JSON must contain a list of test cases")

    def get_tests(self) -> List[TestCase]:
        """Get all test cases.

        Returns:
            List of TestCase objects
        """
        return self.test_cases

    def filter_tests(self, predicate: Callable[[TestCase], bool]) -> "TestDataset":
        """Filter test cases by predicate.

        Args:
            predicate: Function that returns True for tests to keep

        Returns:
            New TestDataset with filtered tests
        """
        filtered = TestDataset(f"{self.name}_filtered")
        filtered.test_cases = [tc for tc in self.test_cases if predicate(tc)]
        return filtered

    def split(self, train_ratio: float = 0.8) -> tuple["TestDataset", "TestDataset"]:
        """Split dataset into train and test sets.

        Args:
            train_ratio: Ratio of tests for training set

        Returns:
            Tuple of (train_dataset, test_dataset)
        """
        import random

        indices = list(range(len(self.test_cases)))
        random.shuffle(indices)

        split_idx = int(len(indices) * train_ratio)
        train_indices = indices[:split_idx]
        test_indices = indices[split_idx:]

        train_dataset = TestDataset(f"{self.name}_train")
        test_dataset = TestDataset(f"{self.name}_test")

        train_dataset.test_cases = [self.test_cases[i] for i in train_indices]
        test_dataset.test_cases = [self.test_cases[i] for i in test_indices]

        return train_dataset, test_dataset

    def __len__(self) -> int:
        """Get number of test cases."""
        return len(self.test_cases)

    def __iter__(self) -> Iterator[TestCase]:
        """Iterate over test cases."""
        return iter(self.test_cases)

    def __getitem__(self, idx: int) -> TestCase:
        """Get test case by index."""
        return self.test_cases[idx]
