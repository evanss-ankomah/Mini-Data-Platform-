"""
validate.py — Pandera schema validation for sales order CSVs.
"""
import pandas as pd
import pandera as pa
from pandera import Column, Check
from datetime import date, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Pandera Schema ────────────────────────────────────────────
VALID_REGIONS = [
    "North America",
    "Europe",
    "Asia Pacific",
    "Latin America",
    "Middle East & Africa",
]

sales_schema = pa.DataFrameSchema(
    columns={
        "order_id": Column(
            str,
            [Check.str_matches(r"^ORD-\d{6,10}$")],
            nullable=False,
            unique=True,
        ),
        "order_date": Column(
            "datetime64[ns]",
            [
                Check.greater_than_or_equal_to(pd.Timestamp("2020-01-01")),
                Check.less_than_or_equal_to(
                    pd.Timestamp(date.today() + timedelta(days=1))
                ),
            ],
            nullable=False,
        ),
        "customer_id": Column(
            str,
            [Check.str_matches(r"^CUST-\d{4,8}$")],
            nullable=False,
        ),
        "region": Column(
            str,
            [Check.isin(VALID_REGIONS)],
            nullable=False,
        ),
        "product": Column(
            str,
            [Check.str_length(min_value=2, max_value=100)],
            nullable=False,
        ),
        "quantity": Column(
            int,
            [
                Check.greater_than(0),
                Check.less_than_or_equal_to(100000),
            ],
            nullable=False,
        ),
        "unit_price": Column(
            float,
            [
                Check.greater_than(0),
                Check.less_than_or_equal_to(999999.99),
            ],
            nullable=False,
        ),
    },
    coerce=True,
    strict=True,
    name="SalesOrderSchema",
)


def validate_dataframe(
    df: pd.DataFrame, file_key: str = ""
) -> tuple[pd.DataFrame, list[dict]]:
    """
    Validate a DataFrame against the sales schema.

    Returns:
        (valid_df, errors) — valid rows as a DataFrame, and a list of
        error dicts for rejected rows.
    """
    errors = []

    try:
        validated = sales_schema.validate(df, lazy=True)
        logger.info(
            "Validation passed — %d rows OK",
            len(validated),
            extra={"task_name": "validate", "file_key": file_key},
        )
        return validated, errors

    except pa.errors.SchemaErrors as exc:
        # Collect per-failure details
        failure_cases = exc.failure_cases
        for _, row in failure_cases.iterrows():
            errors.append(
                {
                    "row": int(row.get("index", -1)) if pd.notna(row.get("index")) else -1,
                    "column": str(row.get("column", "")),
                    "check": str(row.get("check", "")),
                    "error": str(row.get("failure_case", "")),
                }
            )

        # Identify bad row indexes
        bad_indexes = set()
        for e in errors:
            if e["row"] >= 0:
                bad_indexes.add(e["row"])

        if bad_indexes:
            valid_df = df.drop(index=list(bad_indexes)).reset_index(drop=True)
        else:
            # If we can't identify specific rows, reject entire file
            valid_df = pd.DataFrame(columns=df.columns)

        logger.warning(
            "Validation found %d error(s), %d valid rows remain",
            len(errors),
            len(valid_df),
            extra={"task_name": "validate", "file_key": file_key},
        )
        return valid_df, errors
