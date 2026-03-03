"""
Shared test fixtures.
"""
import sys
import os
import pytest
import pandas as pd
from datetime import date, timedelta

# Add plugins to path so we can import etl modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "airflow", "plugins"))


@pytest.fixture
def valid_sales_df():
    """A small DataFrame that passes all validation checks."""
    return pd.DataFrame({
        "order_id": ["ORD-000001", "ORD-000002", "ORD-000003"],
        "order_date": [
            date.today().isoformat(),
            (date.today() - timedelta(days=1)).isoformat(),
            (date.today() - timedelta(days=30)).isoformat(),
        ],
        "customer_id": ["CUST-1234", "CUST-5678", "CUST-9012"],
        "region": ["North America", "Europe", "Asia Pacific"],
        "product": ["Widget Pro", "Gadget X", "ThingaMajig 3000"],
        "quantity": [10, 5, 200],
        "unit_price": [29.99, 499.00, 12.50],
    })


@pytest.fixture
def invalid_sales_df():
    """A DataFrame with multiple validation errors."""
    return pd.DataFrame({
        "order_id": ["BAD123", "ORD-000002", "ORD-000003"],
        "order_date": [
            date.today().isoformat(),
            "2030-12-31",
            date.today().isoformat(),
        ],
        "customer_id": ["CUST-1234", "CUST-5678", "CUST-9012"],
        "region": ["North America", "Antarctica", "Europe"],
        "product": ["Widget Pro", "Gadget X", "ThingaMajig 3000"],
        "quantity": [10, -5, 200],
        "unit_price": [29.99, 0.00, 12.50],
    })
