import pandas as pd
from app.schemas.chat import ActionSpec, FilterSpec
from app.services.action_engine import execute_action


def test_average_with_filter() -> None:
    df = pd.DataFrame({"Branch": ["CSE", "ECE", "CSE"], "Package": [10, 20, 30]})
    result = execute_action(ActionSpec(operation="average", target_column="Package", filter=FilterSpec(column="Branch", value="CSE")), df)
    assert result.result["value"] == 20
    assert result.steps == ["Filter Branch=CSE", "Compute average for Package"]
