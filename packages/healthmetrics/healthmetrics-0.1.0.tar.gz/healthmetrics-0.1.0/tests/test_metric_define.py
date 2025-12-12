"""Unit tests for MetricDefine class based on examples from metric.qmd."""

import unittest
import polars as pl
import numpy as np

from polars_eval_metrics import MetricDefine, MetricType, MetricScope


class TestMetricDefineBasic(unittest.TestCase):
    """Test basic metric definitions."""

    def test_simple_mae_metric(self):
        """Test creating a simple MAE metric (from metric.qmd line 28)."""
        metric = MetricDefine(name="mae")

        self.assertEqual(metric.name, "mae")
        self.assertEqual(metric.label, "mae")  # Auto-generated from name
        self.assertEqual(metric.type, MetricType.ACROSS_SAMPLE)
        self.assertIsNone(metric.scope)
        self.assertIsNone(metric.within_expr)
        self.assertIsNone(metric.across_expr)

    def test_hierarchical_mae_mean(self):
        """Test MAE with mean aggregation (from metric.qmd line 88)."""
        metric = MetricDefine(name="mae:mean", type=MetricType.ACROSS_SUBJECT)

        self.assertEqual(metric.name, "mae:mean")
        self.assertEqual(metric.label, "mae:mean")
        self.assertEqual(metric.type, MetricType.ACROSS_SUBJECT)
        # The colon notation should be processed during compilation

    def test_custom_label(self):
        """Test metric with custom label."""
        metric = MetricDefine(name="test_metric", label="Custom Test Metric")

        self.assertEqual(metric.name, "test_metric")
        self.assertEqual(metric.label, "Custom Test Metric")


class TestMetricDefineCustomExpressions(unittest.TestCase):
    """Test metrics with custom expressions."""

    def test_percentage_within_threshold(self):
        """Test custom metric for percentage within threshold (from metric.qmd line 136)."""
        metric = MetricDefine(
            name="pct_within_1",
            label="% Predictions Within +/- 1",
            type=MetricType.ACROSS_SAMPLE,
            across_expr=(pl.col("absolute_error") < 1).mean() * 100,
        )

        self.assertEqual(metric.name, "pct_within_1")
        self.assertEqual(metric.label, "% Predictions Within +/- 1")
        self.assertEqual(metric.type, MetricType.ACROSS_SAMPLE)
        self.assertIsNotNone(metric.across_expr)
        self.assertIsInstance(metric.across_expr, pl.Expr)

    def test_percentile_metric(self):
        """Test percentile of per-subject MAE (from metric.qmd line 151)."""
        metric = MetricDefine(
            name="mae_p90_by_subject",
            label="90th Percentile of Subject MAEs",
            type=MetricType.ACROSS_SUBJECT,
            within_expr="mae",
            across_expr=pl.col("value").quantile(0.9, interpolation="linear"),
        )

        self.assertEqual(metric.name, "mae_p90_by_subject")
        self.assertEqual(metric.label, "90th Percentile of Subject MAEs")
        self.assertEqual(metric.type, MetricType.ACROSS_SUBJECT)
        self.assertEqual(metric.within_expr, ["mae"])  # Normalized to list
        self.assertIsInstance(metric.across_expr, pl.Expr)

    def test_weighted_average(self):
        """Test weighted average of per-subject MAE (from metric.qmd line 173)."""
        metric = MetricDefine(
            name="weighted_mae",
            label="Weighted Average of Subject MAEs",
            type=MetricType.ACROSS_SUBJECT,
            within_expr=[
                "mae",  # MAE per subject
                pl.col("weight").mean().alias("avg_weight"),
            ],
            across_expr=(
                (pl.col("value") * pl.col("avg_weight")).sum()
                / pl.col("avg_weight").sum()
            ),
        )

        self.assertEqual(metric.name, "weighted_mae")
        self.assertEqual(metric.label, "Weighted Average of Subject MAEs")
        self.assertEqual(metric.type, MetricType.ACROSS_SUBJECT)
        self.assertEqual(len(metric.within_expr), 2)
        self.assertEqual(metric.within_expr[0], "mae")
        self.assertIsInstance(metric.within_expr[1], pl.Expr)
        self.assertIsInstance(metric.across_expr, pl.Expr)


class TestMetricDefineWithNumpy(unittest.TestCase):
    """Test metrics using NumPy functions."""

    def test_weighted_average_numpy(self):
        """Test weighted average using NumPy (from metric.qmd line 194)."""
        # Define the weighted average expression
        weighted_average = pl.struct(["value", "avg_weight"]).map_batches(
            lambda x: pl.Series(
                [
                    np.average(
                        x.struct.field("value"), weights=x.struct.field("avg_weight")
                    )
                ]
            ),
            return_dtype=pl.Float64,
        )

        metric = MetricDefine(
            name="weighted_mae_numpy",
            label="Weighted Average of Subject MAEs (NumPy)",
            type=MetricType.ACROSS_SUBJECT,
            within_expr=["mae", pl.col("weight").mean().alias("avg_weight")],
            across_expr=weighted_average,
        )

        self.assertEqual(metric.name, "weighted_mae_numpy")
        self.assertEqual(metric.label, "Weighted Average of Subject MAEs (NumPy)")
        self.assertEqual(metric.type, MetricType.ACROSS_SUBJECT)
        self.assertEqual(len(metric.within_expr), 2)
        self.assertIsInstance(metric.across_expr, pl.Expr)


class TestMetricDefineTypes(unittest.TestCase):
    """Test different metric types."""

    def test_all_metric_types(self):
        """Test all available metric types."""
        types_to_test = [
            MetricType.ACROSS_SAMPLE,
            MetricType.ACROSS_SUBJECT,
            MetricType.WITHIN_SUBJECT,
            MetricType.ACROSS_VISIT,
            MetricType.WITHIN_VISIT,
        ]

        for metric_type in types_to_test:
            metric = MetricDefine(name=f"test_{metric_type.value}", type=metric_type)
            self.assertEqual(metric.type, metric_type)

    def test_metric_scopes(self):
        """Test metric scopes."""
        scopes_to_test = [MetricScope.GLOBAL, MetricScope.MODEL, MetricScope.GROUP]

        for scope in scopes_to_test:
            metric = MetricDefine(name=f"test_{scope.value}", scope=scope)
            self.assertEqual(metric.scope, scope)

    def test_string_to_enum_conversion(self):
        """Test that string inputs are converted to proper enum types."""

        # Test MetricType string conversion
        m1 = MetricDefine(name="test", type="across_sample")
        self.assertEqual(m1.type, MetricType.ACROSS_SAMPLE)

        m2 = MetricDefine(name="test", type="WITHIN_SUBJECT")  # Different case
        self.assertEqual(m2.type, MetricType.WITHIN_SUBJECT)

        m3 = MetricDefine(name="test", type="across-visit")  # With hyphen
        self.assertEqual(m3.type, MetricType.ACROSS_VISIT)

        # Test MetricScope string conversion
        m4 = MetricDefine(name="test", scope="global")
        self.assertEqual(m4.scope, MetricScope.GLOBAL)

        m5 = MetricDefine(name="test", scope="MODEL")  # Different case
        self.assertEqual(m5.scope, MetricScope.MODEL)

        # Test None scope remains None
        m6 = MetricDefine(name="test", scope=None)
        self.assertIsNone(m6.scope)

        # Test invalid type string raises error
        with self.assertRaisesRegex(ValueError, "Invalid metric type"):
            MetricDefine(name="test", type="invalid_type")

        # Test invalid scope string raises error
        with self.assertRaisesRegex(ValueError, "Invalid metric scope"):
            MetricDefine(name="test", scope="invalid_scope")

        # Test that enum values still work directly
        m7 = MetricDefine(
            name="test", type=MetricType.ACROSS_VISIT, scope=MetricScope.GROUP
        )
        self.assertEqual(m7.type, MetricType.ACROSS_VISIT)
        self.assertEqual(m7.scope, MetricScope.GROUP)


class TestMetricDefineValidation(unittest.TestCase):
    """Test validation and error handling."""

    def test_empty_name_raises_error(self):
        """Test that empty name raises validation error."""
        with self.assertRaisesRegex(ValueError, "Metric name cannot be empty"):
            MetricDefine(name="")

    def test_whitespace_name_raises_error(self):
        """Test that whitespace-only name raises validation error."""
        with self.assertRaisesRegex(ValueError, "Metric name cannot be empty"):
            MetricDefine(name="   ")

    def test_empty_label_raises_error(self):
        """Test that empty label raises validation error."""
        with self.assertRaisesRegex(ValueError, "Metric label cannot be empty"):
            MetricDefine(name="test", label="   ")

    def test_single_string_within_expr_normalized_to_list(self):
        """Test that single string within_expr is normalized to list."""
        metric = MetricDefine(name="test", within_expr="mae")
        self.assertEqual(metric.within_expr, ["mae"])

    def test_single_expr_within_expr_normalized_to_list(self):
        """Test that single Polars expression within_expr is normalized to list."""
        expr = pl.col("test").mean()
        metric = MetricDefine(name="test", within_expr=expr)
        self.assertEqual(metric.within_expr, [expr])


class TestMetricDefineRepresentation(unittest.TestCase):
    """Test string representation and display methods."""

    def test_repr_simple_metric(self):
        """Test string representation of simple metric."""
        metric = MetricDefine(name="mae")
        repr_str = repr(metric)

        # Check that key information is in the representation
        self.assertIn("name='mae'", repr_str)
        self.assertTrue(
            "type=across_sample" in repr_str.lower()
            or "type=MetricType.ACROSS_SAMPLE" in repr_str
        )

    def test_str_simple_metric(self):
        """Test __str__ output for simple MAE metric."""
        metric = MetricDefine(name="mae")
        str_output = str(metric)

        # Check the header format (uses single quotes in actual output)
        self.assertTrue(str_output.startswith("MetricDefine(name='mae'"))

        # Since this is a simple metric without custom expressions,
        # we check for the basic structure
        lines = str_output.strip().split("\n")
        self.assertGreaterEqual(len(lines), 1)
        self.assertIn("MetricDefine(name='mae'", lines[0])

    def test_str_metric_with_details(self):
        """Test __str__ output for metric with type and label."""
        metric = MetricDefine(
            name="mae", type=MetricType.ACROSS_SAMPLE, label="Mean Absolute Error"
        )
        str_output = str(metric)

        # Check that it shows the basic metric info
        self.assertIn("MetricDefine(name=", str_output)
        self.assertIn("mae", str_output)
        self.assertIn("type=across_sample", str_output)

        # Check for label
        self.assertIn("Label:", str_output)
        self.assertIn("Mean Absolute Error", str_output)

        # Check for across-entity expression section
        self.assertIn("Across-entity expression:", str_output)

        # Check for the LazyFrame section
        self.assertIn("(", str_output)
        self.assertIn("pl.LazyFrame", str_output)
        self.assertIn(".select(", str_output)
        self.assertIn('col("absolute_error")', str_output)
        self.assertIn(".mean()", str_output)
        self.assertIn('.alias("value")', str_output)
        self.assertIn(")", str_output)

    def test_str_metric_with_custom_expression(self):
        """Test __str__ output for metric with custom select expression."""
        metric = MetricDefine(
            name="pct_within_1",
            label="% Within +/- 1",
            type=MetricType.ACROSS_SAMPLE,
            across_expr=(pl.col("absolute_error") < 1).mean() * 100,
        )
        str_output = str(metric)

        # Check basic structure (uses single quotes in actual output)
        self.assertIn("MetricDefine(name='pct_within_1'", str_output)
        self.assertIn("type=across_sample", str_output)
        self.assertIn("Label:", str_output)
        self.assertIn("% Within +/- 1", str_output)

        # Check that custom expression is shown
        self.assertIn("Across-entity expression:", str_output)
        # The actual expression representation will be there
        self.assertTrue(
            "[custom]" in str_output or 'col("absolute_error")' in str_output
        )

    def test_pl_expr_method(self):
        """Test that pl_expr method works if it exists."""
        metric = MetricDefine(name="mae")

        # Check if the method exists, skip test if not implemented yet
        if hasattr(metric, "pl_expr") and callable(getattr(metric, "pl_expr")):
            expr_str = metric.pl_expr()
            self.assertIsInstance(expr_str, str)
            self.assertIn("LazyFrame", expr_str)
        else:
            # Method not implemented yet, that's okay for minimal tests
            pass
