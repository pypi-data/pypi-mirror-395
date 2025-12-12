"""Test subgroup_value sorting in both pivot methods."""

import unittest
import polars as pl

from polars_eval_metrics import MetricDefine, MetricEvaluator


class TestSubgroupSorting(unittest.TestCase):
    """Test that subgroup_value is sorted correctly as the primary sort key."""

    @property
    def sample_data(self):
        """Data with deliberately unsorted subgroup values."""
        return pl.DataFrame(
            {
                "treatment": ["A", "A", "A", "B", "B", "B"] * 4,
                "priority": [3, 1, 2, 3, 1, 2] * 4,  # Unsorted: 3, 1, 2
                "subject_id": list(range(1, 25)),
                "actual": [1.0, 2.0, 3.0] * 8,
                "model_1": [1.1, 2.1, 2.9] * 8,
                "model_2": [0.9, 1.9, 3.1] * 8,
            }
        )

    @property
    def string_data(self):
        """Data with string subgroup values in reverse order."""
        return pl.DataFrame(
            {
                "treatment": ["A", "A", "A", "B", "B", "B"] * 4,
                "category": ["Z", "B", "A", "Z", "B", "A"] * 4,  # Reverse: Z, B, A
                "subject_id": list(range(1, 25)),
                "actual": [1.0, 2.0, 3.0] * 8,
                "model_1": [1.1, 2.1, 2.9] * 8,
            }
        )

    def test_numeric_subgroup_sorting_pivot_by_model(self):
        """Test numeric subgroup_value sorting in pivot_by_model."""
        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates={"model_1": "Model A", "model_2": "Model B"},
            group_by={"treatment": "Treatment"},
            subgroup_by={"priority": "Priority"},
        )

        result = evaluator.pivot_by_model()

        # Should be sorted by subgroup_value first: 1, 2, 3
        subgroup_order = result["subgroup_value"].unique(maintain_order=True).to_list()
        self.assertEqual(
            subgroup_order,
            ["1", "2", "3"],
            f"Expected ['1', '2', '3'], got {subgroup_order}",
        )

    def test_numeric_subgroup_sorting_pivot_by_group(self):
        """Test numeric subgroup_value sorting in pivot_by_group."""
        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates={"model_1": "Model A", "model_2": "Model B"},
            group_by={"treatment": "Treatment"},
            subgroup_by={"priority": "Priority"},
        )

        result = evaluator.pivot_by_group()

        # Should be sorted by subgroup_value first: 1, 2, 3
        subgroup_order = result["subgroup_value"].unique(maintain_order=True).to_list()
        self.assertEqual(
            subgroup_order,
            ["1", "2", "3"],
            f"Expected ['1', '2', '3'], got {subgroup_order}",
        )

    def test_string_subgroup_sorting_pivot_by_model(self):
        """Test string subgroup_value sorting in pivot_by_model."""
        evaluator = MetricEvaluator(
            df=self.string_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates={"model_1": "Model"},
            group_by={"treatment": "Treatment"},
            subgroup_by={"category": "Category"},
        )

        result = evaluator.pivot_by_model()

        # Should be sorted alphabetically: A, B, Z
        subgroup_order = result["subgroup_value"].unique(maintain_order=True).to_list()
        self.assertEqual(
            subgroup_order,
            ["A", "B", "Z"],
            f"Expected ['A', 'B', 'Z'], got {subgroup_order}",
        )

    def test_string_subgroup_sorting_pivot_by_group(self):
        """Test string subgroup_value sorting in pivot_by_group."""
        evaluator = MetricEvaluator(
            df=self.string_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates={"model_1": "Model"},
            group_by={"treatment": "Treatment"},
            subgroup_by={"category": "Category"},
        )

        result = evaluator.pivot_by_group()

        # Should be sorted alphabetically: A, B, Z
        subgroup_order = result["subgroup_value"].unique(maintain_order=True).to_list()
        self.assertEqual(
            subgroup_order,
            ["A", "B", "Z"],
            f"Expected ['A', 'B', 'Z'], got {subgroup_order}",
        )

    def test_subgroup_priority_over_treatment(self):
        """Test that subgroup_value sorting takes priority over treatment sorting."""
        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates={"model_1": "Model"},
            group_by={"treatment": "Treatment"},
            subgroup_by={"priority": "Priority"},
        )

        result = evaluator.pivot_by_group(row_order_by="subgroup")

        # Check that within each subgroup_value, treatments are sorted
        # But subgroup_value is the primary sort key
        first_few_rows = (
            result.select(["subgroup_value", "Treatment"]).head(6).to_dicts()
        )

        # Should see: (1,A), (1,B), (2,A), (2,B), (3,A), (3,B)
        expected_pattern = [
            ("1", "A"),
            ("1", "B"),
            ("2", "A"),
            ("2", "B"),
            ("3", "A"),
            ("3", "B"),
        ]

        actual_pattern = [
            (row["subgroup_value"], row["Treatment"]) for row in first_few_rows
        ]
        self.assertEqual(
            actual_pattern,
            expected_pattern,
            f"Expected {expected_pattern}, got {actual_pattern}",
        )

    def test_consistent_sorting_between_methods(self):
        """Test that both pivot methods produce consistent subgroup ordering."""
        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates={"model_1": "Model A", "model_2": "Model B"},
            group_by={"treatment": "Treatment"},
            subgroup_by={"priority": "Priority"},
        )

        result_model = evaluator.pivot_by_model()
        result_group = evaluator.pivot_by_group()

        model_order = (
            result_model["subgroup_value"].unique(maintain_order=True).to_list()
        )
        group_order = (
            result_group["subgroup_value"].unique(maintain_order=True).to_list()
        )

        self.assertEqual(
            model_order,
            group_order,
            f"Methods inconsistent: model={model_order}, group={group_order}",
        )
        self.assertEqual(model_order, ["1", "2", "3"])


if __name__ == "__main__":
    unittest.main()
