import json
import re
from app.schemas.chat import ActionSpec


class LLMPlanner:
    """Provider-aware planner with a deterministic fallback for MVP reliability."""

    def plan(self, question: str, columns: list[str]) -> ActionSpec:
        # A production deployment can call OpenAI/Gemini/Anthropic here. The fallback keeps tests and
        # local development usable without external credentials while preserving structured actions.
        lowered = question.lower()
        column_map = {column.lower(): column for column in columns}
        target = self._pick_column(lowered, column_map)
        filter_match = self._extract_filter(lowered, column_map)
        if any(word in lowered for word in ["average", "avg", "mean"]):
            return ActionSpec(operation="average", target_column=target, filter=filter_match)
        if "sum" in lowered or "total" in lowered:
            return ActionSpec(operation="sum", target_column=target, filter=filter_match)
        if "min" in lowered or "lowest" in lowered:
            return ActionSpec(operation="min", target_column=target, filter=filter_match)
        if "max" in lowered or "highest" in lowered:
            return ActionSpec(operation="max", target_column=target, filter=filter_match)
        if "top" in lowered:
            limit = int(re.search(r"top\s+(\d+)", lowered).group(1)) if re.search(r"top\s+(\d+)", lowered) else 10
            return ActionSpec(operation="top_n", target_column=target, filter=filter_match, limit=limit)
        if "unique" in lowered or "distinct" in lowered:
            return ActionSpec(operation="unique", target_column=target)
        if "null" in lowered or "missing" in lowered:
            return ActionSpec(operation="null_analysis")
        if "count" in lowered or "how many" in lowered:
            return ActionSpec(operation="count", target_column=target, filter=filter_match)
        return ActionSpec(operation="filter", target_column=target, filter=filter_match, limit=10)

    def _pick_column(self, question: str, column_map: dict[str, str]) -> str | None:
        for normalized, original in column_map.items():
            if normalized in question:
                return original
        numeric_hints = ["package", "salary", "amount", "price", "score", "marks", "revenue"]
        for hint in numeric_hints:
            for normalized, original in column_map.items():
                if hint in normalized or hint in question and normalized in question:
                    return original
        return next(iter(column_map.values()), None)

    def _extract_filter(self, question: str, column_map: dict[str, str]):
        from app.schemas.chat import FilterSpec
        tokens = set(re.findall(r"[a-zA-Z0-9_+-]+", question))
        for normalized, original in column_map.items():
            if normalized in question:
                continue
            for token in tokens:
                if token and token in {"cse", "ece", "me", "civil", "sales", "north", "south"}:
                    return FilterSpec(column=original, value=token.upper())
        # common branch/department filter for questions like "CSE students"
        for normalized, original in column_map.items():
            if any(name in normalized for name in ["branch", "department", "dept", "category"]):
                for token in tokens:
                    if len(token) >= 2 and token.isupper() is False and token not in {"average", "for", "students"}:
                        if token in {"cse", "ece", "it", "mech"}:
                            return FilterSpec(column=original, value=token.upper())
        return None

    def explain(self, action: ActionSpec, result: dict, steps: list[str]) -> str:
        value = result.get("value")
        if value is not None:
            return f"The {action.operation} for {action.target_column or 'rows'} is {value:.2f}."
        if "rows" in result:
            return f"I found {len(result['rows'])} matching rows."
        if "values" in result:
            return f"I found {len(result['values'])} unique values."
        return "Analysis completed."
