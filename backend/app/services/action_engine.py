from dataclasses import dataclass
from typing import Any
import duckdb
import pandas as pd
from app.schemas.chat import ActionSpec

SUPPORTED_OPERATIONS = {"count", "average", "sum", "min", "max", "filter", "sort", "groupby", "top_n", "unique", "null_analysis"}


def clean_rows(df: pd.DataFrame) -> list[dict]:
    return df.astype(object).where(pd.notna(df), None).to_dict("records")


@dataclass
class ExecutionResult:
    result: dict[str, Any]
    steps: list[str]


def normalize_columns(df: pd.DataFrame) -> dict[str, str]:
    return {column.lower().strip(): column for column in df.columns}


def validate_action(action: ActionSpec, df: pd.DataFrame) -> None:
    columns = normalize_columns(df)
    if action.operation not in SUPPORTED_OPERATIONS:
        raise ValueError(f"Unsupported operation: {action.operation}")
    for value in [action.target_column, action.groupby_column, action.filter.column if action.filter else None]:
        if value and value.lower().strip() not in columns:
            raise ValueError(f"Unknown column: {value}")


def quote_identifier(identifier: str) -> str:
    return "\"" + identifier.replace("\"", "\"\"") + "\""


def _col(df: pd.DataFrame, requested: str | None) -> str | None:
    if requested is None:
        return None
    return normalize_columns(df)[requested.lower().strip()]


def execute_action(action: ActionSpec, df: pd.DataFrame) -> ExecutionResult:
    validate_action(action, df)
    steps: list[str] = []
    working = df.copy()
    target = _col(df, action.target_column)
    if action.filter:
        filter_col = _col(df, action.filter.column)
        working = working[working[filter_col].astype(str).str.lower() == str(action.filter.value).lower()]
        steps.append(f"Filter {filter_col}={action.filter.value}")

    if action.operation == "count":
        value = int(len(working) if target is None else working[target].count())
        steps.append(f"Count {'rows' if target is None else target}")
        return ExecutionResult({"value": value}, steps)
    if action.operation in {"average", "sum", "min", "max"}:
        if target is None:
            raise ValueError("target_column is required")
        numeric = pd.to_numeric(working[target], errors="coerce")
        metric = {"average": "mean"}.get(action.operation, action.operation)
        value = getattr(numeric, metric)()
        steps.append(f"Compute {action.operation} for {target}")
        return ExecutionResult({"value": None if pd.isna(value) else float(value), "column": target}, steps)
    if action.operation == "filter":
        steps.append("Return filtered rows")
        return ExecutionResult({"rows": clean_rows(working.head(action.limit))}, steps)
    if action.operation == "sort":
        if target is None:
            raise ValueError("target_column is required")
        sorted_df = working.sort_values(target, ascending=action.sort_direction == "asc")
        steps.append(f"Sort by {target} {action.sort_direction}")
        return ExecutionResult({"rows": clean_rows(sorted_df.head(action.limit))}, steps)
    if action.operation == "top_n":
        if target is None:
            raise ValueError("target_column is required")
        numeric = pd.to_numeric(working[target], errors="coerce")
        ranked = working.assign(_rank_value=numeric).sort_values("_rank_value", ascending=False).drop(columns=["_rank_value"]).head(action.limit)
        rows = clean_rows(ranked)
        steps.append(f"Select top {action.limit} by {target}")
        return ExecutionResult({"rows": rows}, steps)
    if action.operation == "groupby":
        if target is None or action.groupby_column is None:
            raise ValueError("target_column and groupby_column are required")
        group_col = _col(df, action.groupby_column)
        con = duckdb.connect(database=":memory:")
        con.register("sheet", working)
        group_ident = quote_identifier(group_col)
        target_ident = quote_identifier(target)
        result_df = con.execute(f"SELECT {group_ident}, AVG(TRY_CAST({target_ident} AS DOUBLE)) AS average FROM sheet GROUP BY {group_ident} ORDER BY average DESC").df()
        result = clean_rows(result_df)
        steps.append(f"Group by {group_col} and average {target}")
        return ExecutionResult({"rows": result}, steps)
    if action.operation == "unique":
        if target is None:
            raise ValueError("target_column is required")
        steps.append(f"Find unique values in {target}")
        return ExecutionResult({"values": working[target].dropna().astype(str).unique().tolist()[: action.limit]}, steps)
    if action.operation == "null_analysis":
        rows = [{"column": col, "nulls": int(working[col].isna().sum())} for col in working.columns]
        steps.append("Count null values for each column")
        return ExecutionResult({"rows": rows}, steps)
    raise ValueError("Unsupported action")
