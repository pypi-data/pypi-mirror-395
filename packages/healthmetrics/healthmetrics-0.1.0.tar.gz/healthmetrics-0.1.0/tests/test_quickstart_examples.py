"""Tests based on quickstart.qmd examples for minimal sufficient coverage."""

import unittest
import polars as pl

from polars_eval_metrics import MetricDefine, MetricEvaluator
from polars_eval_metrics.ard import ARD
from .test_utils import generate_sample_data as generate_test_data


class TestQuickstartSingleMetric(unittest.TestCase):
    """Test single metric evaluation from quickstart.qmd."""

    def test_mae_single_model(self):
        """Test single MAE metric for one model."""
        df = generate_test_data()

        evaluator = MetricEvaluator(
            df=df,
            metrics=MetricDefine(name="mae"),
            ground_truth="actual",
            estimates="model1",
        )

        result = evaluator.evaluate()

        # Check basic structure
        self.assertEqual(result.shape[0], 1)  # One result row
        self.assertIn("metric", result.columns)
        self.assertIn("estimate", result.columns)
        self.assertIn("value", result.columns)
        self.assertIn("label", result.columns)

        # Check values
        self.assertEqual(result["metric"][0], "mae")
        self.assertEqual(result["estimate"][0], "model1")
        self.assertEqual(result["label"][0], "mae")
        formatted_value = result["value"][0]
        self.assertIsInstance(formatted_value, str)
        self.assertNotEqual(formatted_value, "")
        stats = ARD(evaluator.evaluate(collect=False)).get_stats()
        self.assertGreaterEqual(stats["value"][0], 0)  # MAE is non-negative


class TestQuickstartGroupedEvaluation(unittest.TestCase):
    """Test grouped evaluation from quickstart.qmd."""

    def test_mae_rmse_by_treatment(self):
        """Test MAE and RMSE metrics grouped by treatment."""
        df = generate_test_data()

        evaluator = MetricEvaluator(
            df=df,
            metrics=[
                MetricDefine(name="mae"),
                MetricDefine(name="rmse"),
            ],
            ground_truth="actual",
            estimates=["model1", "model2"],
            group_by=["treatment"],
        )

        compact = evaluator.evaluate()

        # Check structure: 2 treatments x 2 models x 2 metrics = 8 rows
        self.assertEqual(compact.shape[0], 8)

        # Check compact columns
        expected_cols = {
            "treatment",
            "estimate",
            "metric",
            "label",
            "value",
        }
        self.assertTrue(expected_cols.issubset(set(compact.columns)))

        # Check unique values
        self.assertEqual(set(compact["treatment"]), {"A", "B"})
        self.assertEqual(set(compact["estimate"]), {"model1", "model2"})
        self.assertEqual(set(compact["metric"]), {"mae", "rmse"})

        # Inspect verbose view for diagnostics
        verbose_result = evaluator.evaluate(verbose=True)
        self.assertTrue(
            {"metric_type", "scope", "stat"}.issubset(set(verbose_result.columns))
        )

        non_null_values = [
            row["value_float"]
            for row in verbose_result["stat"]
            if row["value_float"] is not None
        ]
        if non_null_values:
            self.assertGreaterEqual(min(non_null_values), 0)


class TestQuickstartSubgroupEvaluation(unittest.TestCase):
    """Test subgroup evaluation from quickstart.qmd."""

    def test_subgroup_evaluation(self):
        """Test evaluation with subgroups (gender and race)."""
        df = generate_test_data()

        evaluator = MetricEvaluator(
            df=df,
            metrics=[
                MetricDefine(name="mae"),
                MetricDefine(name="rmse"),
            ],
            ground_truth="actual",
            estimates=["model1", "model2"],
            group_by=["treatment"],
            subgroup_by=["gender", "race"],
        )

        result = evaluator.evaluate()

        # Check that subgroup columns exist
        self.assertIn("subgroup_name", result.columns)
        self.assertIn("subgroup_value", result.columns)

        # Check subgroup names are correct
        self.assertEqual(set(result["subgroup_name"]), {"gender", "race"})

        # Check that we have results for each subgroup
        gender_results = result.filter(pl.col("subgroup_name") == "gender")
        race_results = result.filter(pl.col("subgroup_name") == "race")

        self.assertGreater(len(gender_results), 0)
        self.assertGreater(len(race_results), 0)

        # Check subgroup values
        self.assertIn("F", gender_results["subgroup_value"].to_list())
        self.assertIn("M", gender_results["subgroup_value"].to_list())
        self.assertIn("White", race_results["subgroup_value"].to_list())
        self.assertIn("Black", race_results["subgroup_value"].to_list())
        self.assertIn("Asian", race_results["subgroup_value"].to_list())


class TestQuickstartDataIntegrity(unittest.TestCase):
    """Test data integrity and validation."""

    def test_column_order_and_sorting(self):
        """Test that results are properly sorted and columns are in correct order."""
        df = generate_test_data()

        evaluator = MetricEvaluator(
            df=df,
            metrics=[MetricDefine(name="mae"), MetricDefine(name="rmse")],
            ground_truth="actual",
            estimates=["model1", "model2"],
            group_by=["treatment"],
            subgroup_by=["gender"],
        )

        result = evaluator.evaluate()

        # Check that results are sorted properly
        # Should be sorted by treatment, subgroup_name, subgroup_value, metric, estimate
        prev_treatment = None
        prev_subgroup = None
        prev_metric = None

        for row in result.iter_rows(named=True):
            # Check treatment ordering
            if prev_treatment is not None:
                self.assertGreaterEqual(row["treatment"], prev_treatment)

            # Within same treatment, check subgroup and metric ordering
            if prev_treatment == row["treatment"]:
                if prev_subgroup is not None:
                    self.assertTrue(
                        row["subgroup_value"] >= prev_subgroup
                        or row["subgroup_name"] != "gender"
                    )

                if prev_subgroup == row["subgroup_value"] and prev_metric is not None:
                    self.assertTrue(
                        row["metric"] >= prev_metric or row["estimate"] != "model1"
                    )

            prev_treatment = row["treatment"]
            if row["subgroup_name"] == "gender":
                prev_subgroup = row["subgroup_value"]
            prev_metric = row["metric"]

    def test_lazy_evaluation_option(self):
        """Test that collect=False returns LazyFrame."""
        df = generate_test_data()

        evaluator = MetricEvaluator(
            df=df,
            metrics=MetricDefine(name="mae"),
            ground_truth="actual",
            estimates="model1",
        )

        # Test LazyFrame return
        lazy_result = evaluator.evaluate(collect=False)
        self.assertIsInstance(lazy_result, pl.LazyFrame)

        # Test that it can be collected
        collected_result = lazy_result.collect()
        self.assertIsInstance(collected_result, pl.DataFrame)

        # Test that default behavior returns DataFrame
        default_result = evaluator.evaluate()
        self.assertIsInstance(default_result, pl.DataFrame)


class TestQuickstartErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_missing_columns_error(self):
        """Test error when required columns are missing."""
        df = generate_test_data().drop("actual")  # Remove ground truth column

        with self.assertRaisesRegex(
            ValueError, "Ground truth column 'actual' not found in data"
        ):
            MetricEvaluator(
                df=df,
                metrics=MetricDefine(name="mae"),
                ground_truth="actual",
                estimates="model1",
            )

    def test_empty_estimates_error(self):
        """Test error when no estimates are provided."""
        df = generate_test_data()

        with self.assertRaisesRegex(ValueError, "No estimates provided"):
            MetricEvaluator(
                df=df,
                metrics=MetricDefine(name="mae"),
                ground_truth="actual",
                estimates=[],  # Empty estimates
            )

    def test_empty_metrics_error(self):
        """Test error when no metrics are provided."""
        df = generate_test_data()

        with self.assertRaisesRegex(ValueError, "No metrics provided"):
            MetricEvaluator(
                df=df,
                metrics=[],  # Empty metrics
                ground_truth="actual",
                estimates="model1",
            )


class TestQuickstartEquivalentCalculations(unittest.TestCase):
    """Test that results match equivalent direct Polars calculations."""

    def test_mae_equivalent_calculation(self):
        """Test that MAE matches direct Polars calculation."""
        df = generate_test_data()

        # Framework calculation
        evaluator = MetricEvaluator(
            df=df,
            metrics=MetricDefine(name="mae"),
            ground_truth="actual",
            estimates="model1",
        )
        framework_result = evaluator.evaluate(verbose=True)
        framework_mae = framework_result["stat"][0]["value_float"]

        # Direct Polars calculation (from quickstart.qmd)
        direct_result = df.select(
            (pl.col("model1") - pl.col("actual")).abs().mean().alias("mae")
        )
        direct_mae = direct_result["mae"][0]

        # Should be approximately equal (accounting for floating point precision)
        self.assertLess(abs(framework_mae - direct_mae), 1e-10)

    def test_grouped_mae_equivalent_calculation(self):
        """Test that grouped MAE matches direct Polars calculation."""
        df = generate_test_data()

        # Framework calculation
        evaluator = MetricEvaluator(
            df=df,
            metrics=MetricDefine(name="mae"),
            ground_truth="actual",
            estimates="model1",
            group_by=["treatment"],
        )
        framework_result = evaluator.evaluate(verbose=True).sort("treatment")

        # Direct Polars calculation
        direct_result = (
            df.group_by("treatment")
            .agg(
                [(pl.col("model1") - pl.col("actual")).abs().mean().alias("mae_model1")]
            )
            .sort("treatment")
        )

        # Compare values for each treatment group
        for i in range(len(framework_result)):
            framework_mae = framework_result["stat"][i]["value_float"]
            direct_mae = direct_result["mae_model1"][i]
            self.assertLess(abs(framework_mae - direct_mae), 1e-10)
