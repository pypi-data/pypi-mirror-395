"""Tests for ARD (Analysis Results Data) structure."""

from __future__ import annotations

from typing import Any, Iterable
import unittest

import polars as pl

from polars_eval_metrics.ard import ARD


def stat_struct(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "type": None,
        "value_float": None,
        "value_int": None,
        "value_bool": None,
        "value_str": None,
        "value_struct": None,
        "format": None,
    }
    base.update(overrides)
    return base


def dataset(rows: Iterable[dict[str, Any]]) -> pl.DataFrame:
    normalised: list[dict[str, Any]] = []
    for row in rows:
        base = {
            "groups": None,
            "subgroups": None,
            "estimate": None,
            "metric": None,
            "label": None,
            "stat": stat_struct(),
            "context": None,
            "id": None,
        }
        base.update(row)
        normalised.append(base)
    return pl.DataFrame(normalised)


class TestARDBasics(unittest.TestCase):
    """Test basic ARD functionality."""

    def test_empty_ard(self) -> None:
        ard = ARD()
        self.assertEqual(len(ard), 0)
        collected = ard.collect()
        self.assertEqual(collected.shape, (0, 11))
        self.assertEqual(collected.schema["stat_fmt"], pl.Utf8)
        self.assertEqual(collected.schema["warning"], pl.List(pl.Utf8))
        self.assertEqual(collected.schema["error"], pl.List(pl.Utf8))

    def test_empty_get_stats(self) -> None:
        ard = ARD()
        values = ard.get_stats()
        self.assertEqual(values.shape, (0, 2))

    def test_from_frame(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"treatment": "A", "site": "01"},
                    "subgroups": {"gender": None},
                    "estimate": "model1",
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                    "context": {"n": 100},
                },
                {
                    "groups": {"treatment": "B", "site": "01"},
                    "subgroups": {"gender": "M"},
                    "estimate": "model1",
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.5),
                    "context": {"n": 85},
                },
            ]
        )

        ard = ARD(df)
        self.assertEqual(len(ard), 2)

        collected = ard.collect()
        self.assertIn("groups", collected.columns)
        self.assertIn("stat", collected.columns)

    def test_filter_by_groups(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "groups": {"trt": "B"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=2.8),
                },
                {
                    "groups": {"trt": "A"},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.1),
                },
            ]
        )

        ard = ARD(df)
        filtered = ARD(ard.lazy.filter(pl.col("groups").struct.field("trt") == "A"))
        self.assertEqual(len(filtered), 2)

    def test_filter_by_metrics(self) -> None:
        df = dataset(
            [
                {
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.5),
                },
                {
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=2.8),
                },
            ]
        )

        ard = ARD(df)
        filtered = ARD(ard.lazy.filter(pl.col("metric") == "mae"))
        self.assertEqual(len(filtered), 2)

        filtered_all = ARD(ard.lazy.filter(pl.col("metric").is_in(["mae", "rmse"])))
        self.assertEqual(len(filtered_all), 3)

    def test_filter_missing_group_key(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "groups": {"trt": "B"},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.5),
                },
            ]
        )

        ard = ARD(df)
        with self.assertRaises(pl.exceptions.StructFieldNotFoundError):
            ard.lazy.filter(
                pl.col("groups").struct.field("unknown") == "value"
            ).collect()

    def test_filter_subgroups_and_context(self) -> None:
        df = dataset(
            [
                {
                    "subgroups": {"gender": "F"},
                    "context": {"fold": "1"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=1.2),
                },
                {
                    "subgroups": {"gender": "M"},
                    "context": {"fold": "2"},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=2.5),
                },
            ]
        )

        ard = ARD(df)
        sub_filtered = ARD(
            ard.lazy.filter(pl.col("subgroups").struct.field("gender") == "F")
        )
        self.assertEqual(len(sub_filtered), 1)
        ctx_filtered = ARD(
            ard.lazy.filter(pl.col("context").struct.field("fold") == "2")
        )
        self.assertEqual(len(ctx_filtered), 1)


class TestARDTransformations(unittest.TestCase):
    """Test ARD transformation methods."""

    def test_unnest_groups(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"treatment": "A", "site": "01"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                }
            ]
        )

        ard = ARD(df)
        unnested = ard.unnest(["groups"])

        self.assertIn("treatment", unnested.columns)
        self.assertIn("site", unnested.columns)
        self.assertEqual(unnested["treatment"][0], "A")

    def test_struct_harmonization(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A", "site": None},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "groups": {"trt": None, "site": "01"},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.5),
                },
                {
                    "groups": {"trt": None, "site": None},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.1),
                },
            ]
        )

        ard = ARD(df)
        unnested = ard.unnest(["groups"])

        self.assertTrue({"trt", "site"}.issubset(set(unnested.columns)))
        null_row = unnested.filter(pl.col("trt").is_null() & pl.col("site").is_null())
        self.assertEqual(null_row.height, 1)

    def test_unnest_comprehensive(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "groups": {"trt": "A"},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.1),
                },
                {
                    "groups": {"trt": "B"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=2.8),
                },
                {
                    "groups": {"trt": "B"},
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=3.9),
                },
            ]
        )

        ard = ARD(df)
        unnested = ard.unnest(["groups"])

        self.assertIn("trt", unnested.columns)
        self.assertEqual(unnested.shape[0], 4)

    def test_null_handling(self) -> None:
        df = dataset(
            [
                {
                    "groups": None,
                    "estimate": None,
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                }
            ]
        )

        ard = ARD(df)
        collected = ard.collect()
        self.assertIsNone(collected["groups"][0])
        self.assertIsNone(collected["estimate"][0])

        with_empty = ard.with_null_as_empty()
        df_empty = with_empty.collect()
        self.assertEqual(df_empty["estimate"][0], "")

        with_null = ard.with_empty_as_null()
        df_null = with_null.collect()
        self.assertIn(df_null["estimate"][0], (None, ""))

    def test_null_struct_round_trip(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A", "site": "01"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "groups": None,
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.5),
                },
            ]
        )

        ard = ARD(df)
        filled = ard.with_null_as_empty().unnest(["groups"])
        self.assertIn("trt", filled.columns)
        self.assertEqual(filled["trt"].null_count(), 1)

        round_tripped = ard.with_null_as_empty().with_empty_as_null().collect()
        self.assertIsNone(round_tripped["groups"][1])
        self.assertIsNone(round_tripped["context"][1])

    def test_to_long_prefers_cached_format(self) -> None:
        df = dataset(
            [
                {
                    "metric": "mae",
                    "estimate": "model1",
                    "stat": stat_struct(type="float", value_float=3.14159),
                    "stat_fmt": "cached-mae",
                }
            ]
        )
        ard = ARD(df)
        long_df = ard.to_long()
        self.assertIn("value", long_df.columns)
        self.assertEqual(long_df["value"][0], "cached-mae")

    def test_to_wide_prefers_cached_format(self) -> None:
        df = dataset(
            [
                {
                    "metric": "mae",
                    "estimate": "model1",
                    "stat": stat_struct(type="float", value_float=1.23456),
                    "stat_fmt": "cached-wide",
                }
            ]
        )
        ard = ARD(df)
        wide = ard.to_wide(index=["estimate"], columns=["metric"])
        self.assertIn("mae", wide.columns)
        self.assertEqual(wide["mae"][0], "cached-wide")


class TestARDStatHandling(unittest.TestCase):
    """Test stat value handling."""

    def test_stat_struct_contents(self) -> None:
        df = dataset(
            [
                {
                    "metric": "count",
                    "stat": stat_struct(type="int", value_int=42),
                },
                {
                    "metric": "mean",
                    "stat": stat_struct(type="float", value_float=3.14159),
                },
                {
                    "metric": "label",
                    "stat": stat_struct(type="string", value_str="significant"),
                },
                {
                    "metric": "flag",
                    "stat": stat_struct(type="bool", value_bool=True),
                },
                {
                    "metric": "ci",
                    "stat": stat_struct(
                        type="struct", value_struct={"lower": 2.5, "upper": 3.5}
                    ),
                },
            ]
        )

        ard = ARD(df)
        collected = ard.collect()

        self.assertEqual(collected["stat"][0]["value_int"], 42)
        self.assertEqual(collected["stat"][1]["value_float"], 3.14159)
        self.assertEqual(collected["stat"][2]["value_str"], "significant")
        self.assertIs(collected["stat"][3]["value_bool"], True)
        self.assertEqual(
            collected["stat"][4]["value_struct"], {"lower": 2.5, "upper": 3.5}
        )

    def test_get_stats(self) -> None:
        df = dataset(
            [
                {
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.5),
                },
            ]
        )

        ard = ARD(df)
        values = ard.get_stats()
        self.assertIn("value", values.columns)
        self.assertEqual(values["value"][0], 3.2)

        with_meta = ard.get_stats(include_metadata=True)
        self.assertIn("type", with_meta.columns)
        self.assertIn("format", with_meta.columns)
        self.assertIn("formatted", with_meta.columns)


class TestARDDisplay(unittest.TestCase):
    """Test display and printing methods."""

    def test_repr(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A"},
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                }
            ]
        )

        ard = ARD(df)
        repr_str = repr(ard)

        self.assertTrue(repr_str.startswith("ARD(summary="))
        self.assertIn("'n_rows': 1", repr_str)

    def test_summary(self) -> None:
        df = dataset(
            [
                {
                    "groups": {"trt": "A"},
                    "estimate": "m1",
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=3.2),
                },
                {
                    "groups": {"trt": "B"},
                    "estimate": "m1",
                    "metric": "mae",
                    "stat": stat_struct(type="float", value_float=2.8),
                },
                {
                    "groups": {"trt": "A"},
                    "estimate": "m2",
                    "metric": "rmse",
                    "stat": stat_struct(type="float", value_float=4.1),
                },
            ]
        )

        ard = ARD(df)
        summary = ard.summary()

        self.assertEqual(summary["n_rows"], 3)
        self.assertEqual(summary["n_metrics"], 2)
        self.assertEqual(summary["n_estimates"], 2)
        self.assertIn("mae", summary["metrics"])
        self.assertIn("rmse", summary["metrics"])
