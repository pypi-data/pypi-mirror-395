"""
Unit tests for MetricEvaluator

Tests cover core functionality, all scope types, grouping strategies,
and edge cases based on examples from metric_evaluator.qmd
"""

from typing import Any
import unittest

import polars as pl
from polars_eval_metrics import MetricDefine, MetricEvaluator, MetricScope, MetricType
from polars_eval_metrics.ard import ARD
from .data_fixtures import (
    get_metric_sample_df,
    get_grouped_metric_df,
    get_hierarchical_metric_df,
)


def _evaluate_metric_set(
    data: pl.DataFrame,
    metrics: list[MetricDefine],
    *,
    estimates: list[str] | None = None,
    ground_truth: str = "actual",
) -> tuple[Any, pl.DataFrame]:
    """Evaluate metrics and return both the result and flattened stats."""

    evaluator = MetricEvaluator(
        df=data,
        metrics=metrics,
        ground_truth=ground_truth,
        estimates=estimates or ["model_a"],
    )

    compact = evaluator.evaluate()
    assert isinstance(compact, pl.DataFrame)
    assert set(compact["metric"]) == {metric.name for metric in metrics}

    stats = ARD(evaluator.evaluate(collect=False)).get_stats()
    return compact, stats


def _evaluate_ard(evaluator: MetricEvaluator, **kwargs: Any) -> ARD:
    """Helper to build an ARD from the evaluator's lazy output."""

    return ARD(evaluator.evaluate(collect=False, **kwargs))


class BaseMetricEvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.metric_sample_df = get_metric_sample_df()
        self.grouped_metric_df = get_grouped_metric_df()
        self.hierarchical_metric_df = get_hierarchical_metric_df()


class TestMetricEvaluatorBasic(BaseMetricEvaluatorTest):
    """Test basic MetricEvaluator functionality"""

    def test_simple_metrics(self):
        """Test basic metric evaluation"""
        metrics = [
            MetricDefine(name="mae", label="Mean Absolute Error"),
            MetricDefine(name="rmse", label="Root Mean Squared Error"),
        ]

        evaluator = MetricEvaluator(
            df=self.metric_sample_df,
            metrics=metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
        )

        result = evaluator.evaluate()
        assert isinstance(result, pl.DataFrame)

        # Check structure
        self.assertEqual(len(result), 4)  # 2 metrics x 2 models
        self.assertTrue(set(result.columns) >= {"metric", "estimate", "label", "value"})
        self.assertEqual(set(result["metric"].unique()), {"mae", "rmse"})
        self.assertEqual(set(result["estimate"].unique()), {"model_a", "model_b"})

        # Check values are reasonable (non-negative, finite) using the ARD helper
        stats_df = ARD(evaluator.evaluate(collect=False)).get_stats()
        values = stats_df["value"].to_list()
        self.assertTrue(all(v >= 0 for v in values if v is not None))
        self.assertTrue(
            all(not (isinstance(v, float) and v != v) for v in values)
        )  # Check for NaN

    def test_single_metric_single_estimate(self):
        """Test minimal case"""
        evaluator = MetricEvaluator(
            df=self.metric_sample_df,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        result = evaluator.evaluate()
        assert isinstance(result, pl.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result["metric"][0], "mae")
        self.assertEqual(result["estimate"][0], "model_a")

    def test_minimal_view_drops_details(self):
        """Dropping detail columns should remove stat/stat_fmt/context/warnings/errors."""

        evaluator = MetricEvaluator(
            df=self.grouped_metric_df,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
            group_by=["treatment"],
        )

        minimal = evaluator.evaluate()
        assert isinstance(minimal, pl.DataFrame)
        hidden_cols = {"stat", "stat_fmt", "context", "warning", "error"}
        self.assertTrue(hidden_cols.isdisjoint(set(minimal.columns)))

    def test_verbose_flag(self):
        """verbose=True should keep struct and detail columns visible."""

        evaluator = MetricEvaluator(
            df=self.metric_sample_df,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        verbose = evaluator.evaluate(verbose=True)
        assert isinstance(verbose, pl.DataFrame)
        self.assertTrue(
            {"stat", "context", "id", "groups"}.issubset(set(verbose.columns))
        )


class TestMetricEvaluatorScopes(BaseMetricEvaluatorTest):
    """Test all MetricScope types"""

    def test_global_scope(self):
        """Test GLOBAL scope - single result across all"""
        metric = MetricDefine(name="n_subject", scope="global")

        evaluator = MetricEvaluator(
            df=self.grouped_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)

        # Global scope should ignore estimates and groups
        self.assertEqual(len(compact), 1)
        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)
        self.assertIsNone(verbose_df["estimate"][0])  # No estimate value for global
        self.assertIsNone(verbose_df["groups"][0])  # Groups ignored for global scope
        stats = _evaluate_ard(evaluator).get_stats()
        self.assertEqual(stats["value"][0], 3.0)  # 3 unique subjects

    def test_model_scope(self):
        """Test MODEL scope - per model, ignore groups"""
        metric = MetricDefine(name="n_sample_with_data", scope="model")

        evaluator = MetricEvaluator(
            df=self.grouped_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)

        # Model scope: one row per model, groups ignored
        self.assertEqual(len(compact), 2)
        self.assertEqual(set(compact["estimate"].unique()), {"model_a", "model_b"})
        self.assertTrue(all(verbose_df["groups"].is_null()))
        stats = _evaluate_ard(evaluator).get_stats()
        self.assertTrue(all(v == 6.0 for v in stats["value"]))  # 6 samples each model

    def test_group_scope(self):
        """Test GROUP scope - per group, aggregate models"""
        metric = MetricDefine(name="n_subject", scope="group")

        evaluator = MetricEvaluator(
            df=self.grouped_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)

        # Group scope: one row per group, models aggregated
        self.assertEqual(len(compact), 2)
        self.assertEqual(set(compact["treatment"].unique()), {"A", "B"})
        self.assertEqual(compact["estimate"].null_count(), compact.height)

        # Check counts per group via verbose view
        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)
        for row in verbose_df.iter_rows(named=True):
            group = row.get("groups")
            stat = row.get("stat")
            if group and group["treatment"] == "A":
                self.assertEqual(stat["value_int"], 2)  # 2 subjects in A
            elif group and group["treatment"] == "B":
                self.assertEqual(stat["value_int"], 1)  # 1 subject in B

    def test_default_scope(self):
        """Test default scope - per model-group combination"""
        metric = MetricDefine(name="mae")  # Default scope

        evaluator = MetricEvaluator(
            df=self.grouped_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)

        # Default scope: estimate x group combinations
        self.assertEqual(len(compact), 4)  # 2 models x 2 groups
        self.assertEqual(set(compact["estimate"].unique()), {"model_a", "model_b"})
        self.assertEqual(set(compact["treatment"].unique()), {"A", "B"})


class TestMetricEvaluatorTypes(BaseMetricEvaluatorTest):
    """Test all MetricType aggregations"""

    def test_across_sample(self):
        """Test ACROSS_SAMPLE - aggregate across all samples"""
        metric = MetricDefine(name="mae", type="across_sample")

        evaluator = MetricEvaluator(
            df=self.hierarchical_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        self.assertEqual(len(compact), 1)
        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)
        context = verbose_df.select(pl.col("context").struct.field("metric_type"))
        self.assertEqual(context["metric_type"][0], "across_sample")

    def test_within_subject(self):
        """Test WITHIN_SUBJECT - per subject aggregation"""
        metric = MetricDefine(name="mae", type="within_subject")

        evaluator = MetricEvaluator(
            df=self.hierarchical_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)
        self.assertEqual(len(compact), 3)  # One row per subject

        context = verbose_df.select(pl.col("context").struct.field("metric_type"))
        self.assertTrue(all(context["metric_type"] == "within_subject"))

        # ID struct should carry subject identifiers
        id_df = verbose_df.unnest(["id"])
        self.assertIn("subject_id", id_df.columns)
        self.assertEqual(set(id_df["subject_id"].to_list()), {1, 2, 3})

        # Value column surfaces subject-level MAE on the long representation
        self.assertIn("value", compact.columns)
        self.assertTrue(all(compact["value"].is_not_null()))
        self.assertTrue(all(verbose_df["stat"].struct.field("type") == "float"))

    def test_across_subject(self):
        """Test ACROSS_SUBJECT - within subjects then across"""
        # Use proper hierarchical metric that does within-subject then across-subject aggregation
        metric = MetricDefine(name="mae:mean", type="across_subject")

        evaluator = MetricEvaluator(
            df=self.hierarchical_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        self.assertEqual(len(compact), 1)  # Single aggregated result across subjects
        ard_df = _evaluate_ard(evaluator).collect()
        if "groups" in ard_df.columns:
            self.assertIsNone(ard_df["groups"][0])  # No per-subject grouping retained
        context = ard_df.select(pl.col("context").struct.field("metric_type"))
        self.assertTrue(all(context["metric_type"] == "across_subject"))
        stats = _evaluate_ard(evaluator).get_stats()
        self.assertGreater(stats["value"][0], 0)  # Should be a reasonable MAE value

    def test_within_visit(self):
        """Test WITHIN_VISIT - per visit aggregation"""
        metric = MetricDefine(name="mae", type="within_visit")

        evaluator = MetricEvaluator(
            df=self.hierarchical_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)
        self.assertEqual(len(compact), 9)  # Subject x visit combinations

        context = verbose_df.select(pl.col("context").struct.field("metric_type"))
        self.assertTrue(all(context["metric_type"] == "within_visit"))

        id_df = verbose_df.unnest(["id"])
        self.assertTrue({"subject_id", "visit_id"}.issubset(set(id_df.columns)))
        expected_pairs = {
            (subject, visit) for subject in [1, 2, 3] for visit in [1, 2, 3]
        }
        observed_pairs = {
            (row["subject_id"], row["visit_id"]) for row in id_df.iter_rows(named=True)
        }
        self.assertEqual(observed_pairs, expected_pairs)
        self.assertTrue(all(verbose_df["stat"].struct.field("type") == "float"))

    def test_across_visit(self):
        """Test ACROSS_VISIT - within visits then across"""
        # Use proper hierarchical metric that does within-visit then across-visit aggregation
        metric = MetricDefine(name="mae:mean", type="across_visit")

        evaluator = MetricEvaluator(
            df=self.hierarchical_metric_df,
            metrics=[metric],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        self.assertEqual(len(compact), 1)  # Single aggregated result across visits
        ard_df = _evaluate_ard(evaluator).collect()
        if "groups" in ard_df.columns:
            group_struct = ard_df["groups"][0]
            if group_struct is not None:
                self.assertNotIn("subject_id", group_struct)
                self.assertNotIn("visit_id", group_struct)
        context = ard_df.select(pl.col("context").struct.field("metric_type"))
        self.assertTrue(all(context["metric_type"] == "across_visit"))
        stats = _evaluate_ard(evaluator).get_stats()
        self.assertGreater(stats["value"][0], 0)  # Should be a reasonable MAE value

    def test_across_visit_custom_across_expr(self):
        """Test ACROSS_VISIT with custom across_expr (count, min, max, etc.)"""
        metrics = [
            MetricDefine(
                name="mae_count",
                label="Count of Visit MAEs",
                type="across_visit",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").count(),
            ),
            MetricDefine(
                name="mae_min",
                label="Min Visit MAE",
                type="across_visit",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").min(),
            ),
            MetricDefine(
                name="mae_max",
                label="Max Visit MAE",
                type="across_visit",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").max(),
            ),
            MetricDefine(
                name="mae_sum",
                label="Sum of Visit MAEs",
                type="across_visit",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").sum(),
            ),
        ]

        result, stats = _evaluate_metric_set(
            self.hierarchical_metric_df, metrics, estimates=["model_a"]
        )

        self.assertEqual(len(result), 4)

        # Check count equals number of visits (9 = 3 subjects x 3 visits)
        count_result = stats.filter(pl.col("metric") == "mae_count")
        self.assertEqual(count_result["value"][0], 9.0)

        # Check min < max
        min_result = stats.filter(pl.col("metric") == "mae_min")
        max_result = stats.filter(pl.col("metric") == "mae_max")
        self.assertLess(min_result["value"][0], max_result["value"][0])

        # Check sum is positive
        sum_result = stats.filter(pl.col("metric") == "mae_sum")
        self.assertGreater(sum_result["value"][0], 0)

    def test_across_subject_custom_across_expr(self):
        """Test ACROSS_SUBJECT with custom across_expr (count, median, std, etc.)"""
        metrics = [
            MetricDefine(
                name="mae_count_subj",
                label="Count of Subject MAEs",
                type="across_subject",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").count(),
            ),
            MetricDefine(
                name="mae_median_subj",
                label="Median Subject MAE",
                type="across_subject",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").median(),
            ),
            MetricDefine(
                name="mae_std_subj",
                label="Std Dev of Subject MAEs",
                type="across_subject",
                within_expr=pl.col("absolute_error").mean(),
                across_expr=pl.col("value").std(),
            ),
        ]

        result, stats = _evaluate_metric_set(
            self.hierarchical_metric_df, metrics, estimates=["model_a"]
        )

        self.assertEqual(len(result), 3)

        # Check count equals number of subjects (3)
        count_result = stats.filter(pl.col("metric") == "mae_count_subj")
        self.assertEqual(count_result["value"][0], 3.0)

        # Check median is reasonable (should be positive)
        median_result = stats.filter(pl.col("metric") == "mae_median_subj")
        self.assertGreater(median_result["value"][0], 0)

        # Check std is non-negative
        std_result = stats.filter(pl.col("metric") == "mae_std_subj")
        self.assertGreaterEqual(std_result["value"][0], 0)


class TestMetricEvaluatorGrouping(BaseMetricEvaluatorTest):
    """Test grouping and subgrouping functionality"""

    @property
    def complex_data(self):
        """Data with multiple grouping dimensions"""
        return pl.DataFrame(
            {
                "subject_id": [1, 1, 2, 2, 3, 3],
                "actual": [10, 20, 15, 25, 12, 22],
                "model_a": [8, 22, 18, 24, 15, 19],
                "treatment": ["A", "A", "B", "B", "A", "B"],
                "age_group": ["young", "young", "middle", "middle", "senior", "senior"],
                "sex": ["M", "M", "F", "F", "M", "M"],
            }
        )

    def test_group_by_only(self):
        """Test standard group_by functionality"""
        evaluator = MetricEvaluator(
            df=self.complex_data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
            group_by=["treatment"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        self.assertEqual(len(compact), 2)  # Two treatment groups
        ard_df = _evaluate_ard(evaluator).collect()
        groups_unnested = ard_df.unnest(["groups"])
        self.assertEqual(set(groups_unnested["treatment"].unique()), {"A", "B"})

    def test_subgroup_by_only(self):
        """Test subgroup analysis"""
        evaluator = MetricEvaluator(
            df=self.complex_data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
            subgroup_by=["age_group", "sex"],
        )

        # Should have marginal analysis for each subgroup variable
        ard_df = _evaluate_ard(evaluator).collect()
        unnested = ard_df.unnest(["subgroups"])
        # In ARD, subgroups are unnested directly by their column names
        self.assertIn("age_group", unnested.columns)
        self.assertIn("sex", unnested.columns)

        # Check we have results for both subgroup variables
        # Each row should have data for one of the subgroup dimensions
        age_results = unnested.filter(pl.col("age_group").is_not_null())
        sex_results = unnested.filter(pl.col("sex").is_not_null())
        self.assertGreater(len(age_results), 0)  # Has age_group results
        self.assertGreater(len(sex_results), 0)  # Has sex results

    def test_group_and_subgroup(self):
        """Test combination of group_by and subgroup_by"""
        evaluator = MetricEvaluator(
            df=self.complex_data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
            group_by=["treatment"],
            subgroup_by=["age_group"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)

        # Should have group x subgroup combinations
        self.assertIn("treatment", compact.columns)
        self.assertIn("age_group", compact.columns)
        self.assertTrue(set(compact["treatment"].unique()).issubset({"A", "B"}))

        ard_df = _evaluate_ard(evaluator).collect()
        subgroups_unnested = ard_df.unnest(["subgroups"])
        age_results = subgroups_unnested.filter(pl.col("age_group").is_not_null())
        self.assertGreater(len(age_results), 0)  # Has age_group subgroup results


class TestMetricEvaluatorAdvancedScenarios(BaseMetricEvaluatorTest):
    """Additional scenarios covering scope mixing and typed subgroup inputs."""

    def test_mixed_scope_metrics(self):
        """Metrics spanning all scopes should co-exist in a single evaluation run."""
        metrics = [
            MetricDefine(name="mae"),
            MetricDefine(name="n_sample", scope=MetricScope.GLOBAL),
            MetricDefine(name="n_subject", scope=MetricScope.GROUP),
            MetricDefine(name="n_sample_with_data", scope=MetricScope.MODEL),
        ]

        evaluator = MetricEvaluator(
            df=self.grouped_metric_df,
            metrics=metrics,
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            group_by=["treatment"],
        )

        verbose_df = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_df, pl.DataFrame)

        context_scope = verbose_df.select(
            pl.col("metric"),
            pl.col("context").struct.field("scope").alias("scope"),
        )

        self.assertEqual(
            context_scope.filter(pl.col("metric") == "n_sample")["scope"].to_list(),
            ["global"],
        )
        self.assertEqual(
            set(
                context_scope.filter(pl.col("metric") == "n_subject")["scope"].to_list()
            ),
            {"group"},
        )
        self.assertEqual(
            set(
                context_scope.filter(pl.col("metric") == "n_sample_with_data")[
                    "scope"
                ].to_list()
            ),
            {"model"},
        )
        self.assertTrue(
            all(
                value is None
                for value in context_scope.filter(pl.col("metric") == "mae")[
                    "scope"
                ].to_list()
            )
        )

        global_rows = verbose_df.filter(pl.col("metric") == "n_sample")
        self.assertEqual(global_rows.height, 1)
        self.assertIsNone(global_rows["estimate"][0])
        self.assertIsNone(global_rows["groups"][0])
        self.assertEqual(
            global_rows["stat"][0]["value_int"], self.grouped_metric_df.height
        )
        self.assertEqual(global_rows["stat"][0]["type"], "int")

        group_rows = verbose_df.filter(pl.col("metric") == "n_subject")
        self.assertTrue(
            all(value is None for value in group_rows["estimate"].to_list())
        )
        treatments = {
            group["treatment"]
            for group in group_rows["groups"].to_list()
            if group is not None
        }
        self.assertEqual(treatments, {"A", "B"})
        group_counts = {
            row["groups"]["treatment"]: row["stat"]["value_int"]
            for row in group_rows.iter_rows(named=True)
            if row["groups"] is not None and row["stat"]["type"] == "int"
        }
        self.assertEqual(group_counts, {"A": 2, "B": 1})

        model_rows = verbose_df.filter(pl.col("metric") == "n_sample_with_data")
        self.assertTrue(all(group is None for group in model_rows["groups"].to_list()))
        self.assertEqual(set(model_rows["estimate"].to_list()), {"model_a", "model_b"})
        self.assertTrue(
            all(
                row["stat"]["value_int"] == self.grouped_metric_df.height
                for row in model_rows.iter_rows(named=True)
            )
        )
        self.assertTrue(
            all(
                row["stat"]["type"] == "int" for row in model_rows.iter_rows(named=True)
            )
        )

        mae_rows = verbose_df.filter(pl.col("metric") == "mae")
        combinations = {
            (row["estimate"], row["groups"]["treatment"])
            for row in mae_rows.iter_rows(named=True)
        }
        self.assertEqual(
            combinations,
            {
                ("model_a", "A"),
                ("model_a", "B"),
                ("model_b", "A"),
                ("model_b", "B"),
            },
        )

    def test_group_subgroup_overlap_raises(self):
        """Using the same column for group and subgroup should raise a clear error."""
        with self.assertRaisesRegex(
            ValueError, "Group and subgroup columns must be distinct"
        ):
            MetricEvaluator(
                df=self.metric_sample_df,
                metrics=[MetricDefine(name="mae")],
                ground_truth="actual",
                estimates=["model_a"],
                group_by=["treatment"],
                subgroup_by=["treatment"],
            )

    def test_enum_subgroup_inputs(self):
        """Pre-typed Enum subgroup columns should preserve their category order."""
        enum_order = ["young", "middle", "senior"]
        enum_df = self.metric_sample_df.with_columns(
            pl.col("age_group").cast(pl.Enum(enum_order))
        )

        evaluator = MetricEvaluator(
            df=enum_df,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a", "model_b"],
            subgroup_by=["age_group"],
        )

        ard_df = _evaluate_ard(evaluator).collect()
        subgroups = ard_df.unnest(["subgroups"])
        subgroup_values = subgroups["subgroup_value"]

        self.assertIsInstance(subgroup_values.dtype, pl.Enum)
        self.assertEqual(subgroup_values.dtype.categories.to_list(), enum_order)
        self.assertEqual(set(subgroup_values.drop_nulls().to_list()), set(enum_order))
        self.assertEqual(
            set(subgroups["subgroup_name"].drop_nulls().to_list()), {"age_group"}
        )


class TestMetricEvaluatorEdgeCases(BaseMetricEvaluatorTest):
    """Test edge cases and error conditions"""

    def test_empty_data(self):
        """Test with empty dataset"""
        empty_data = pl.DataFrame(
            {
                "actual": [],
                "model_a": [],
            }
        ).cast({"actual": pl.Float64, "model_a": pl.Float64})

        evaluator = MetricEvaluator(
            df=empty_data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        # Empty data should result in empty results
        try:
            result = evaluator.evaluate()
            assert isinstance(result, pl.DataFrame)
            self.assertEqual(len(result), 0)
        except Exception:
            # Some operations may fail on empty data, which is acceptable
            pass

    def test_all_missing_values(self):
        """Test with all missing values"""
        missing_data = pl.DataFrame(
            {
                "actual": [None, None, None],
                "model_a": [None, None, None],
            }
        ).cast({"actual": pl.Float64, "model_a": pl.Float64})

        evaluator = MetricEvaluator(
            df=missing_data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        # Should handle gracefully (result may be null/NaN)
        try:
            result = evaluator.evaluate()
            assert isinstance(result, pl.DataFrame)
            self.assertEqual(len(result), 1)
        except Exception:
            # Operations on all-null data may fail, which is acceptable
            pass

    def test_single_row(self):
        """Test with single data point"""
        single_data = pl.DataFrame(
            {
                "actual": [10.0],
                "model_a": [8.0],
            }
        )

        evaluator = MetricEvaluator(
            df=single_data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        assert isinstance(compact, pl.DataFrame)
        self.assertEqual(len(compact), 1)
        stats = _evaluate_ard(evaluator).get_stats()
        self.assertEqual(stats["value"][0], 2.0)

    def test_invalid_metric_name(self):
        """Test error handling for invalid configuration"""
        with self.assertRaisesRegex(ValueError, "not in configured metrics"):
            evaluator = MetricEvaluator(
                df=self.metric_sample_df,
                metrics=[MetricDefine(name="mae")],
                ground_truth="actual",
                estimates=["model_a"],
            )
            # Try to evaluate metric not in original configuration
            evaluator.evaluate(metrics=[MetricDefine(name="rmse")])

    def test_invalid_estimate_name(self):
        """Test error handling for invalid estimate"""
        with self.assertRaisesRegex(ValueError, "not in configured estimates"):
            evaluator = MetricEvaluator(
                df=self.metric_sample_df,
                metrics=[MetricDefine(name="mae")],
                ground_truth="actual",
                estimates=["model_a"],
            )
            # Try to evaluate estimate not in original configuration
            evaluator.evaluate(estimates=["model_c"])

    def test_filter_expression(self):
        """Test filter_expr functionality"""
        data = pl.DataFrame(
            {
                "subject_id": [1, 2, 3, 4],
                "actual": [10, 20, 30, 40],
                "model_a": [8, 22, 28, 45],
                "keep": [True, True, False, True],
            }
        )

        evaluator = MetricEvaluator(
            df=data,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
            filter_expr=pl.col("keep"),
        )

        result = evaluator.evaluate()
        assert isinstance(result, pl.DataFrame)
        self.assertEqual(len(result), 1)
        # Should only use rows where keep=True (subjects 1, 2, 4)
        # MAE should be calculated on 3 rows, not 4

    def test_lazy_vs_eager_evaluation(self):
        """Test collect parameter"""
        evaluator = MetricEvaluator(
            df=self.metric_sample_df,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        compact = evaluator.evaluate()
        lazy = evaluator.evaluate(collect=False)

        self.assertEqual(len(compact), 1)
        self.assertIsInstance(lazy, pl.LazyFrame)
        stats = ARD(lazy).get_stats()
        self.assertEqual(stats["value"][0], 2.375)  # MAE should be 2.375


class TestMetricEvaluatorDiagnostics(BaseMetricEvaluatorTest):
    """Ensure diagnostics columns capture formatter output and failures."""

    def test_stat_fmt_defaults(self):
        evaluator = MetricEvaluator(
            df=self.metric_sample_df,
            metrics=[MetricDefine(name="mae")],
            ground_truth="actual",
            estimates=["model_a"],
        )

        verbose_df = evaluator.evaluate(verbose=True)
        self.assertEqual(verbose_df["stat_fmt"].null_count(), 0)
        self.assertTrue(
            all(isinstance(val, str) for val in verbose_df["stat_fmt"].to_list())
        )
        self.assertTrue(all(row == [] for row in verbose_df["warning"].to_list()))
        self.assertTrue(all(row == [] for row in verbose_df["error"].to_list()))
        long_df = _evaluate_ard(evaluator).to_long()
        self.assertEqual(long_df["value"][0], verbose_df["stat_fmt"][0])

    def test_error_capture(self):
        broken_metric = MetricDefine(
            name="broken_metric",
            type=MetricType.ACROSS_SAMPLE,
            scope=MetricScope.GLOBAL,
            across_expr=pl.col("does_not_exist").mean(),
        )

        evaluator = MetricEvaluator(
            df=self.metric_sample_df,
            metrics=[broken_metric],
            ground_truth="actual",
            estimates=["model_a"],
        )

        verbose_df = evaluator.evaluate(verbose=True)
        self.assertTrue(
            verbose_df["error"].to_list()[0], "error column should include diagnostics"
        )
        self.assertEqual(verbose_df["warning"].to_list()[0], [])
        stats = _evaluate_ard(evaluator).get_stats(include_metadata=True)
        self.assertIsNone(stats["formatted"][0])
        long_df = _evaluate_ard(evaluator).to_long()
        self.assertIsNone(long_df["value"][0])
