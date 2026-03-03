"""
transform.py — Cleaning, type casting, derived columns.
"""
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


def transform_dataframe(df: pd.DataFrame, file_key: str = "") -> pd.DataFrame:
    """
    Apply transformations to validated sales data:
    1. Strip whitespace from string columns
    2. Normalize region casing (title case)
    3. Ensure correct types
    4. Compute total_amount = quantity * unit_price
    5. De-duplicate by order_id (keep last occurrence)
    """
    if df.empty:
        logger.info(
            "Empty DataFrame — nothing to transform",
            extra={"task_name": "transform", "file_key": file_key},
        )
        return df

    # 1. Strip whitespace on string columns
    str_cols = df.select_dtypes(include=["object"]).columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # 2. Normalize region casing
    region_map = {
        "north america": "North America",
        "europe": "Europe",
        "asia pacific": "Asia Pacific",
        "latin america": "Latin America",
        "middle east & africa": "Middle East & Africa",
    }
    df["region"] = df["region"].str.strip().str.lower().map(region_map).fillna(df["region"])

    # 3. Ensure types
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    # 4. Derived column
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)

    # 5. De-duplicate by order_id (keep last)
    before = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="last").reset_index(drop=True)
    dupes_removed = before - len(df)
    if dupes_removed:
        logger.info(
            "Removed %d duplicate order_id(s)", dupes_removed,
            extra={"task_name": "transform", "file_key": file_key},
        )

    logger.info(
        "Transform complete — %d rows", len(df),
        extra={"task_name": "transform", "file_key": file_key},
    )
    return df
