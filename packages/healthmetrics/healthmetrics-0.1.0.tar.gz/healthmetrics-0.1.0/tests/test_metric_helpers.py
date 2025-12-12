"""Tests for metric helper functions."""

import unittest

from polars_eval_metrics import (
    create_metrics,
    MetricType,
    MetricScope,
)
from polars_eval_metrics.metric_helpers import create_metric_from_dict


class TestCreateMetricFromDict(unittest.TestCase):
    """Test creating single metrics from dictionary."""

    def test_simple_metric(self):
        """Test creating a simple metric."""
        config = {"name": "mae", "label": "Mean Absolute Error"}
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "mae")
        self.assertEqual(metric.label, "Mean Absolute Error")
        self.assertEqual(metric.type, MetricType.ACROSS_SAMPLE)
        self.assertIsNone(metric.scope)

    def test_metric_with_type(self):
        """Test metric with specific type."""
        config = {"name": "mae_subject", "type": "across_subject"}
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "mae_subject")
        self.assertEqual(metric.type, MetricType.ACROSS_SUBJECT)

    def test_metric_with_scope(self):
        """Test metric with scope."""
        config = {"name": "global_mae", "scope": "global"}
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "global_mae")
        self.assertEqual(metric.scope, MetricScope.GLOBAL)

    def test_direct_within_expression(self):
        """Test metric with direct within expression."""
        config = {"name": "custom_mae", "within_expr": "absolute_error.mean()"}
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "custom_mae")
        self.assertEqual(metric.within_expr, ["absolute_error.mean()"])

    def test_direct_across_expression(self):
        """Test metric with direct across expression."""
        config = {
            "name": "mean_mae",
            "type": "across_subject",
            "across_expr": "value.mean()",
        }
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "mean_mae")
        self.assertEqual(metric.across_expr, "value.mean()")

    def test_metric_without_scope(self):
        """Test metric without scope specified."""
        config = {"name": "no_scope_mae"}
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "no_scope_mae")
        self.assertIsNone(metric.scope)  # Default is None

    def test_auto_label_generation(self):
        """Test that label is auto-generated from name."""
        config = {"name": "rmse"}
        metric = create_metric_from_dict(config)

        self.assertEqual(metric.name, "rmse")
        self.assertEqual(metric.label, "rmse")


class TestCreateMetrics(unittest.TestCase):
    """Test unified create_metrics function."""

    def test_multiple_dict_configs(self):
        """Test creating multiple metrics from dict configs."""
        configs = [
            {"name": "mae", "label": "Mean Absolute Error"},
            {"name": "rmse", "label": "Root Mean Squared Error"},
            {"name": "me", "type": "across_sample"},
        ]

        metrics = create_metrics(configs)

        self.assertEqual(len(metrics), 3)
        self.assertEqual(metrics[0].name, "mae")
        self.assertEqual(metrics[0].label, "Mean Absolute Error")
        self.assertEqual(metrics[1].name, "rmse")
        self.assertEqual(metrics[1].label, "Root Mean Squared Error")
        self.assertEqual(metrics[2].name, "me")
        self.assertEqual(metrics[2].type, MetricType.ACROSS_SAMPLE)

    def test_simple_names(self):
        """Test creating metrics from names."""
        names = ["mae", "rmse", "me"]
        metrics = create_metrics(names)

        self.assertEqual(len(metrics), 3)
        self.assertEqual(metrics[0].name, "mae")
        self.assertEqual(metrics[0].label, "mae")
        self.assertEqual(metrics[1].name, "rmse")
        self.assertEqual(metrics[1].label, "rmse")
        self.assertEqual(metrics[2].name, "me")
        self.assertEqual(metrics[2].label, "me")

        # All should have default settings
        for metric in metrics:
            self.assertEqual(metric.type, MetricType.ACROSS_SAMPLE)
            self.assertIsNone(metric.scope)

    def test_empty_list(self):
        """Test creating metrics from empty list."""
        metrics = create_metrics([])
        self.assertEqual(metrics, [])

    def test_mixed_configurations(self):
        """Test metrics with different configuration levels."""
        configs = [
            {"name": "simple"},
            {"name": "with_type", "type": "within_subject"},
            {
                "name": "complex",
                "label": "Complex Metric",
                "type": "across_subject",
                "scope": "model",
                "within_expr": "error.mean()",
                "across_expr": "value.quantile(0.9, interpolation='linear')",
            },
        ]

        metrics = create_metrics(configs)

        self.assertEqual(len(metrics), 3)
        self.assertEqual(metrics[0].name, "simple")
        self.assertEqual(metrics[1].type, MetricType.WITHIN_SUBJECT)
        self.assertEqual(metrics[2].scope, MetricScope.MODEL)
        self.assertEqual(metrics[2].within_expr, ["error.mean()"])
        self.assertEqual(
            metrics[2].across_expr, "value.quantile(0.9, interpolation='linear')"
        )

    def test_single_name(self):
        """Test creating metrics from single name."""
        metrics = create_metrics(["mae"])

        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0].name, "mae")
        self.assertEqual(metrics[0].label, "mae")


class TestErrorHandling(unittest.TestCase):
    """Test error handling in helper functions."""

    def test_missing_name_error(self):
        """Test error when name is missing."""
        config = {"label": "Missing Name"}

        with self.assertRaisesRegex(
            ValueError, "Metric configuration must include 'name'"
        ):
            create_metric_from_dict(config)

    def test_invalid_type_error(self):
        """Test error with invalid metric type."""
        config = {"name": "test", "type": "invalid_type"}

        with self.assertRaisesRegex(ValueError, "Invalid metric type"):
            create_metric_from_dict(config)

    def test_invalid_scope_error(self):
        """Test error with invalid scope."""
        config = {"name": "test", "scope": "invalid_scope"}

        with self.assertRaisesRegex(ValueError, "Invalid metric scope"):
            create_metric_from_dict(config)
