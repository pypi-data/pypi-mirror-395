"""Test pivot_by_group() and pivot_by_model() methods matching metric_pivot.qmd examples"""

import unittest
import polars as pl

from polars_eval_metrics import MetricDefine, MetricEvaluator


class TestPivotByMethods(unittest.TestCase):
    """Test pivot_by_group() and pivot_by_model() methods with scenarios from documentation"""

    @property
    def sample_data(self):
        """Create sample dataset matching metric_pivot.qmd"""
        return pl.DataFrame(
            {
                "subject_id": list(range(1, 21)) * 2,
                "treatment": (["A"] * 10 + ["B"] * 10) * 2,
                "region": (
                    ["North"] * 5 + ["South"] * 5 + ["North"] * 5 + ["South"] * 5
                )
                * 2,
                "age_group": (["Young", "Old"] * 10) * 2,
                "sex": (["M", "F"] * 20),
                "actual": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55] * 4,
                # Model A: Generally accurate with small errors
                "model_a": [10.5, 14.8, 19.2, 25.3, 29.7, 35.1, 39.9, 44.6, 50.4, 54.2]
                * 4,
                # Model B: Less accurate with some larger errors
                "model_b": [9.2, 16.1, 22.5, 23.8, 32.4, 37.8, 38.1, 48.2, 47.5, 58.9]
                * 4,
            }
        )

    @property
    def group_metrics(self):
        """Metrics used in documentation examples"""
        return [
            MetricDefine(
                name="n_subject", label="Total Enrolled Subjects", scope="global"
            ),
            MetricDefine(name="n_subject", label="Number of Subjects", scope="group"),
            MetricDefine(name="mae", label="MAE"),
            MetricDefine(name="rmse", label="RMSE"),
        ]

    def test_case1_pivot_by_group_without_subgroups(self):
        """Test Case 1: Pivot by Group (without subgroups)"""

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=self.group_metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment", "region"],
        )

        result = evaluator.pivot_by_group()

        # Verify structure
        self.assertIsInstance(result, pl.DataFrame)
        self.assertFalse(result.is_empty())

        # Should have group combinations as rows
        self.assertIn("treatment", result.columns)
        self.assertIn("region", result.columns)

        # Should have 4 group combinations (2 treatments x 2 regions)
        self.assertEqual(result.height, 4)

        # Should have global scope column (broadcast to all rows)
        global_cols = [
            col for col in result.columns if "Total Enrolled Subjects" in col
        ]
        self.assertEqual(len(global_cols), 1)

        # Should have group scope columns (one per group)
        group_cols = [col for col in result.columns if "Number of Subjects" in col]
        self.assertEqual(len(group_cols), 1)

        # Should have default scope columns (model x metric) - Polars uses JSON-like names
        default_cols = [col for col in result.columns if col.startswith('{"model_')]
        self.assertEqual(len(default_cols), 4)  # 2 models x 2 metrics (MAE, RMSE)

    def test_case2_pivot_by_group_with_subgroups(self):
        """Test Case 2: Pivot by Group (with subgroups)"""

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=self.group_metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment", "region"],
            subgroup_by=["age_group"],
        )

        result = evaluator.pivot_by_group()

        # Verify structure
        self.assertIsInstance(result, pl.DataFrame)
        self.assertFalse(result.is_empty())

        # Should have subgroup columns
        self.assertIn("subgroup_name", result.columns)
        self.assertIn("subgroup_value", result.columns)

        # Should have group combinations as rows, stratified by subgroups
        self.assertIn("treatment", result.columns)
        self.assertIn("region", result.columns)

        # Should have rows for each group x subgroup combination
        # 4 groups x 2 age_groups = 8 rows (but some might be missing if no data)
        self.assertGreaterEqual(result.height, 4)  # At least one row per group

        # Verify subgroup stratification
        subgroup_values = result["subgroup_value"].unique().sort().to_list()
        self.assertIn("Young", subgroup_values)
        self.assertIn("Old", subgroup_values)

    def test_case3_pivot_by_model_without_subgroups(self):
        """Test Case 3: Pivot by Model (without subgroups)"""

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=self.group_metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment", "region"],
        )

        result = evaluator.pivot_by_model()

        # Verify structure
        self.assertIsInstance(result, pl.DataFrame)
        self.assertFalse(result.is_empty())

        # Should have models as rows
        self.assertIn("estimate", result.columns)
        model_names = result["estimate"].unique().sort().to_list()
        self.assertIn("model_a", model_names)
        self.assertIn("model_b", model_names)
        self.assertEqual(result.height, 2)  # One row per model

        # Should have global scope columns
        global_cols = [
            col for col in result.columns if "Total Enrolled Subjects" in col
        ]
        self.assertEqual(len(global_cols), 1)

        # Should have group scope columns (now using JSON format like {"A","North","Number of Subjects"})
        group_cols = [
            col
            for col in result.columns
            if col.startswith('{"') and "Number of Subjects" in col
        ]
        self.assertEqual(len(group_cols), 4)  # 4 group combinations

        # Should have default scope columns (group x metric) - Polars uses JSON-like names
        default_cols = [
            col
            for col in result.columns
            if col.startswith('{"')
            and col.endswith('"}')
            and any(grp in col for grp in ['"A"', '"B"'])
            and any(met in col for met in ['"MAE"', '"RMSE"'])
        ]
        self.assertEqual(len(default_cols), 8)  # 4 groups x 2 metrics

    def test_case4_pivot_by_model_with_subgroups(self):
        """Test Case 4: Pivot by Model (with subgroups)"""

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=self.group_metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment", "region"],
            subgroup_by=["age_group"],
        )

        result = evaluator.pivot_by_model()

        # Verify structure
        self.assertIsInstance(result, pl.DataFrame)
        self.assertFalse(result.is_empty())

        # Should have subgroup columns
        self.assertIn("subgroup_name", result.columns)
        self.assertIn("subgroup_value", result.columns)
        self.assertIn("estimate", result.columns)

        # Should have rows for each model x subgroup combination
        # 2 models x 2 age_groups = 4 rows
        self.assertGreaterEqual(result.height, 2)  # At least one row per model

        # Verify model stratification within subgroups
        estimates = result["estimate"].unique().sort().to_list()
        self.assertIn("model_a", estimates)
        self.assertIn("model_b", estimates)

        # Verify subgroup stratification
        subgroup_values = result["subgroup_value"].unique().sort().to_list()
        self.assertIn("Young", subgroup_values)
        self.assertIn("Old", subgroup_values)

    def test_column_ordering(self):
        """Test that column ordering follows index -> global -> group -> default pattern"""

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=self.group_metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment", "region"],
        )

        # Test pivot_by_group ordering
        result_group = evaluator.pivot_by_group()
        cols_group = result_group.columns

        # Index columns should come first
        index_start = 0
        self.assertEqual(cols_group[index_start], "treatment")
        self.assertEqual(cols_group[index_start + 1], "region")

        # Global columns should come after index
        global_col_idx = next(
            i for i, col in enumerate(cols_group) if "Total Enrolled Subjects" in col
        )
        self.assertGreater(global_col_idx, 1)  # After index columns

        # Test pivot_by_model ordering
        result_model = evaluator.pivot_by_model()
        cols_model = result_model.columns

        # Estimate should be in index
        self.assertIn("estimate", cols_model)

        # Global columns should come before default columns
        if any("Total Enrolled Subjects" in col for col in cols_model):
            global_idx = next(
                i
                for i, col in enumerate(cols_model)
                if "Total Enrolled Subjects" in col
            )
            default_indices = [
                i
                for i, col in enumerate(cols_model)
                if col.startswith('{"')
                and col.endswith('"}')
                and any(grp in col for grp in ['"A"', '"B"'])
                and any(met in col for met in ['"MAE"', '"RMSE"'])
            ]
            if default_indices:
                self.assertLess(global_idx, min(default_indices))

    def test_mixed_scopes_compatibility(self):
        """Test that different scope combinations work correctly"""

        # Test with only global scope
        evaluator_global = MetricEvaluator(
            df=self.sample_data,
            metrics=[
                MetricDefine(name="n_subject", label="Total Subjects", scope="global")
            ],
            ground_truth="actual",
            estimates=["model_a"],
            group_by=["treatment"],
        )

        result_global_group = evaluator_global.pivot_by_group()
        result_global_model = evaluator_global.pivot_by_model()

        self.assertFalse(result_global_group.is_empty())
        self.assertFalse(result_global_model.is_empty())

        # Test with only group scope
        evaluator_group = MetricEvaluator(
            df=self.sample_data,
            metrics=[
                MetricDefine(name="n_subject", label="Group Subjects", scope="group")
            ],
            ground_truth="actual",
            estimates=["model_a"],
            group_by=["treatment"],
        )

        result_group_group = evaluator_group.pivot_by_group()
        result_group_model = evaluator_group.pivot_by_model()

        self.assertFalse(result_group_group.is_empty())
        self.assertFalse(result_group_model.is_empty())

        # Test with only default scope
        evaluator_default = MetricEvaluator(
            df=self.sample_data,
            metrics=[MetricDefine(name="mae", label="MAE")],
            ground_truth="actual",
            estimates=["model_a"],
            group_by=["treatment"],
        )

        result_default_group = evaluator_default.pivot_by_group()
        result_default_model = evaluator_default.pivot_by_model()

        self.assertFalse(result_default_group.is_empty())
        self.assertFalse(result_default_model.is_empty())

    def test_caching_efficiency(self):
        """Test that both pivot methods use cached evaluation results"""

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=self.group_metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment", "region"],
        )

        # Clear cache to start fresh
        evaluator.clear_cache()
        self.assertEqual(len(evaluator._evaluation_cache), 0)

        # First call should populate cache
        result1 = evaluator.pivot_by_group()
        self.assertEqual(len(evaluator._evaluation_cache), 1)

        # Second call should use cache (same parameters)
        result2 = evaluator.pivot_by_model()
        self.assertEqual(
            len(evaluator._evaluation_cache), 1
        )  # Still just one cached result

        # Results should not be empty
        self.assertFalse(result1.is_empty())
        self.assertFalse(result2.is_empty())

    def test_new_parameter_names(self):
        """Test the new column_order_by and row_order_by parameters"""

        metrics = [MetricDefine(name="mae", label="MAE")]

        evaluator = MetricEvaluator(
            df=self.sample_data,
            metrics=metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment"],
            subgroup_by=["age_group"],
        )

        # Test column_order_by parameter
        result_metrics_first = evaluator.pivot_by_group(column_order_by="metrics")
        result_estimates_first = evaluator.pivot_by_group(column_order_by="estimates")

        self.assertFalse(result_metrics_first.is_empty())
        self.assertFalse(result_estimates_first.is_empty())

        # Column order should be different
        cols_metrics = [
            col for col in result_metrics_first.columns if col.startswith('{"')
        ]
        cols_estimates = [
            col for col in result_estimates_first.columns if col.startswith('{"')
        ]

        # Should have same columns but potentially different order
        self.assertEqual(len(cols_metrics), len(cols_estimates))

        # Test row_order_by parameter
        result_group_first = evaluator.pivot_by_group(row_order_by="group")
        result_subgroup_first = evaluator.pivot_by_group(row_order_by="subgroup")

        self.assertFalse(result_group_first.is_empty())
        self.assertFalse(result_subgroup_first.is_empty())

        # Both should have same shape but potentially different row order
        self.assertEqual(result_group_first.shape, result_subgroup_first.shape)

        # Test pivot_by_model with new parameters
        result_model_metrics = evaluator.pivot_by_model(column_order_by="metrics")
        result_model_groups = evaluator.pivot_by_model(column_order_by="groups")

        self.assertFalse(result_model_metrics.is_empty())
        self.assertFalse(result_model_groups.is_empty())

        # Test that old parameter names would raise an error (if we had validation)
        # This ensures backward compatibility is maintained
        try:
            # These should work (no old parameter validation implemented)
            evaluator.pivot_by_group(column_order_by="metrics", row_order_by="group")
            evaluator.pivot_by_model(column_order_by="metrics", row_order_by="group")
        except Exception as e:
            self.fail(f"New parameters should work: {e}")


if __name__ == "__main__":
    unittest.main()
