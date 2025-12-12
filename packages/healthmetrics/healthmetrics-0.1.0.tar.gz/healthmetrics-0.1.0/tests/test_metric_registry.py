import unittest
import polars as pl

from polars_eval_metrics import (
    MetricDefine,
    MetricEvaluator,
    MetricRegistry,
    MetricScope,
)

from polars_eval_metrics.metric_registry import MetricInfo
from .data_fixtures import get_metric_sample_df


class TestMetricRegistry(unittest.TestCase):
    def test_metric_registry_registers_custom_entries(self) -> None:
        """Custom registry entries should be discoverable through helper APIs."""
        error_name = "test_registry_offset_error"
        metric_name = "test_registry_offset_metric"
        summary_name = "test_registry_offset_summary"

        MetricRegistry.register_error(
            error_name,
            lambda estimate, ground_truth: (
                pl.col(estimate) - pl.col(ground_truth)
            ).abs(),
        )
        MetricRegistry.register_metric(
            metric_name,
            lambda: pl.col(error_name).max().alias("value"),
        )
        MetricRegistry.register_summary(
            summary_name,
            pl.col("value").median(),
        )

        self.assertTrue(MetricRegistry.has_error(error_name))
        self.assertIn(metric_name, MetricRegistry.list_metrics())
        self.assertIn(summary_name, MetricRegistry.list_summaries())

        metric_info = MetricRegistry.get_metric(metric_name)
        summary_expr = MetricRegistry.get_summary(summary_name)

        self.assertIsInstance(metric_info, MetricInfo)
        self.assertIsInstance(metric_info.expr, pl.Expr)
        self.assertIsInstance(summary_expr, pl.Expr)

    def test_metric_registry_evaluator_integration(self) -> None:
        """Registered metrics should work end-to-end within MetricEvaluator."""
        metric_sample_df = get_metric_sample_df()
        error_name = "test_registry_bias_error"
        metric_name = "test_registry_bias_metric"

        MetricRegistry.register_error(
            error_name,
            lambda estimate, ground_truth: pl.col(estimate) - pl.col(ground_truth),
        )
        MetricRegistry.register_metric(
            metric_name,
            lambda: pl.col(error_name).mean().alias("value"),
        )

        metrics = [
            MetricDefine(
                name=metric_name,
                scope=MetricScope.MODEL,
                label="Mean Bias",
            )
        ]

        evaluator = MetricEvaluator(
            df=metric_sample_df,
            metrics=metrics,
            ground_truth="actual",
            estimates={"model_a": "Model A", "model_b": "Model B"},
        )

        detailed = evaluator.evaluate(verbose=True).with_columns(
            pl.col("stat").struct.field("value_float").alias("_value_float")
        )
        assert isinstance(detailed, pl.DataFrame)

        expected_bias = (
            metric_sample_df.lazy()
            .select(
                [
                    (pl.col("model_a") - pl.col("actual")).alias("model_a_bias"),
                    (pl.col("model_b") - pl.col("actual")).alias("model_b_bias"),
                ]
            )
            .collect()
        )
        expected_a = expected_bias["model_a_bias"].drop_nulls().mean()
        expected_b = expected_bias["model_b_bias"].drop_nulls().mean()

        actual_a = detailed.filter(pl.col("estimate") == "model_a").filter(
            pl.col("metric") == metric_name
        )["_value_float"][0]
        actual_b = detailed.filter(pl.col("estimate") == "model_b").filter(
            pl.col("metric") == metric_name
        )["_value_float"][0]

        self.assertAlmostEqual(actual_a, expected_a)
        self.assertAlmostEqual(actual_b, expected_b)

        context_scope = detailed.select(
            pl.col("context").struct.field("scope").alias("scope")
        )
        self.assertEqual(set(context_scope["scope"].drop_nulls().to_list()), {"model"})

    def test_struct_metric_output(self) -> None:
        """Custom metric can surface structured payloads directly in the stat struct."""
        metric_sample_df = get_metric_sample_df()
        metric_name = "mae_with_bounds"

        MetricRegistry.register_metric(
            metric_name,
            MetricInfo(
                expr=pl.struct(
                    [
                        pl.col("absolute_error").mean().alias("mean"),
                        (pl.col("absolute_error").mean() - 0.5).alias("lower"),
                        (pl.col("absolute_error").mean() + 0.5).alias("upper"),
                    ]
                ),
                value_kind="struct",
            ),
        )

        evaluator = MetricEvaluator(
            df=metric_sample_df,
            metrics=[MetricDefine(name=metric_name)],
            ground_truth="actual",
            estimates={"model_a": "Model A"},
        )

        verbose_result = evaluator.evaluate(verbose=True)
        assert isinstance(verbose_result, pl.DataFrame)
        stat = verbose_result["stat"][0]

        self.assertEqual(stat["type"], "struct")
        payload = stat["value_struct"]
        self.assertIsInstance(payload, dict)
        self.assertEqual(set(payload.keys()), {"mean", "lower", "upper"})
        self.assertLess(payload["lower"], payload["upper"])
