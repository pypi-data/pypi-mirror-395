"""Shared utility helpers for metric formatting and parsing."""

# pyre-strict

import ast
from enum import Enum
import re
import textwrap
from typing import Sequence, Type

import polars as pl


def parse_enum_value(
    value: object,
    enum_cls: Type[Enum],
    *,
    field: str,
    allow_none: bool = False,
) -> Enum | None:
    """Normalize arbitrary inputs into enum values."""

    if value is None:
        if allow_none:
            return None
        raise ValueError(f"{field} must not be None")

    if isinstance(value, enum_cls):
        return value

    if isinstance(value, str):
        try:
            return enum_cls(value)
        except ValueError:
            normalized = value.lower().replace("-", "_")
            for member in enum_cls:
                if member.value == normalized or member.name.lower() == normalized:
                    return member

        valid_options = ", ".join(member.value for member in enum_cls)
        raise ValueError(
            f"Invalid {field}: '{value}'. Valid options are: {valid_options}"
        )

    raise ValueError(
        f"{field} must be a {enum_cls.__name__} enum or string, got {type(value)}"
    )


def clean_polars_expr_string(expr_str: str) -> str:
    """Remove Polars internal representation artifacts from expression strings."""

    cleaned = re.sub(r"dyn \w+:\s*", "", expr_str)
    if cleaned.startswith("[") and cleaned.endswith("]"):
        cleaned = cleaned[1:-1]
    return cleaned.replace("[(", "(").replace(")]", ")")


def format_polars_expr(expr: object, *, max_width: int = 70) -> str:
    """Format a single Polars expression for readable display."""

    expr_str = clean_polars_expr_string(str(expr))
    if isinstance(expr, pl.Expr) and ".alias(" not in expr_str:
        expr_str = clean_polars_expr_string(str(expr.alias("value")))

    if len(expr_str) <= max_width:
        return expr_str

    return textwrap.fill(
        expr_str,
        width=max_width,
        subsequent_indent="      ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def format_polars_expr_list(
    exprs: Sequence[pl.Expr],
    *,
    indent: str = "    ",
    max_width: int = 70,
) -> str:
    """Format a sequence of Polars expressions with indentation."""

    expr_list = list(exprs)
    if not expr_list:
        return "[]"
    if len(expr_list) == 1:
        return format_polars_expr(expr_list[0], max_width=max_width)

    lines: list[str] = ["["]
    for index, expr in enumerate(expr_list):
        formatted = format_polars_expr(expr, max_width=max_width)
        comma = "," if index < len(expr_list) - 1 else ""
        expr_lines = formatted.split("\n")
        if len(expr_lines) == 1:
            lines.append(f"{indent}  {formatted}{comma}")
        else:
            lines.append(f"{indent}  {expr_lines[0]}")
            for line in expr_lines[1:]:
                lines.append(f"{indent}  {line}")
            lines[-1] += comma
    lines.append(f"{indent}]")
    return "\n".join(lines)


def parse_pivot_column(column: str) -> tuple[str, ...] | None:
    """Parse structured column labels produced by Polars pivoting."""

    try:
        parsed = ast.literal_eval(column)
    except (SyntaxError, ValueError):
        parsed = None

    if isinstance(parsed, dict):
        prioritized = [parsed.get("estimate"), parsed.get("metric")]
        tokens = [str(value) for value in prioritized if value is not None]
        if not tokens:
            tokens = [str(value) for value in parsed.values()]
        return tuple(tokens) if tokens else None

    if isinstance(parsed, (list, tuple)):
        return tuple(str(token) for token in parsed)

    if column.startswith('{"') and column.endswith('"}') and '","' in column:
        inner = column[2:-2]
        return tuple(inner.split('","'))

    return None


def parse_pivot_columns(columns: Sequence[str]) -> dict[str, tuple[str, ...]]:
    """Return mapping of structured pivot columns to their token tuples."""

    return {
        column: tokens
        for column in columns
        if (tokens := parse_pivot_column(column)) is not None
    }
