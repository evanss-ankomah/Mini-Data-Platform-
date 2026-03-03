"""
generate_sample_data.py — Generate fake sales CSV files for testing.

Usage:
    python scripts/generate_sample_data.py --rows 50 --output data/sample_sales.csv
    python scripts/generate_sample_data.py --rows 50 --invalid 5 --output data/sample_with_errors.csv
"""
import argparse
import csv
import random
from datetime import date, timedelta

REGIONS = [
    "North America",
    "Europe",
    "Asia Pacific",
    "Latin America",
    "Middle East & Africa",
]

PRODUCTS = [
    "Widget Pro",
    "Gadget X",
    "ThingaMajig 3000",
    "Super Connector",
    "Data Cable Premium",
    "Cloud Storage Box",
    "Smart Sensor Kit",
    "Power Adapter Plus",
    "Wireless Hub",
    "Mega Battery Pack",
]


def generate_valid_row(order_num: int) -> dict:
    order_date = date.today() - timedelta(days=random.randint(0, 365))
    return {
        "order_id": f"ORD-{order_num:06d}",
        "order_date": order_date.isoformat(),
        "customer_id": f"CUST-{random.randint(1000, 9999)}",
        "region": random.choice(REGIONS),
        "product": random.choice(PRODUCTS),
        "quantity": random.randint(1, 500),
        "unit_price": round(random.uniform(5.00, 999.99), 2),
    }


def generate_invalid_row(order_num: int) -> dict:
    """Generate a row with deliberate errors."""
    error_type = random.choice(["bad_id", "future_date", "bad_region", "neg_qty", "zero_price"])

    row = generate_valid_row(order_num)
    if error_type == "bad_id":
        row["order_id"] = str(random.randint(10000, 99999))
    elif error_type == "future_date":
        row["order_date"] = "2030-12-31"
    elif error_type == "bad_region":
        row["region"] = "Antarctica"
    elif error_type == "neg_qty":
        row["quantity"] = -random.randint(1, 100)
    elif error_type == "zero_price":
        row["unit_price"] = 0.00

    return row


def main():
    parser = argparse.ArgumentParser(description="Generate sample sales CSV data")
    parser.add_argument("--rows", type=int, default=50, help="Number of valid rows")
    parser.add_argument("--invalid", type=int, default=0, help="Number of invalid rows to inject")
    parser.add_argument("--output", type=str, default="sample_sales.csv", help="Output CSV file path")
    args = parser.parse_args()

    fieldnames = ["order_id", "order_date", "customer_id", "region", "product", "quantity", "unit_price"]
    rows = []

    # Valid rows
    for i in range(1, args.rows + 1):
        rows.append(generate_valid_row(i))

    # Invalid rows (start numbering after valid)
    for i in range(args.rows + 1, args.rows + 1 + args.invalid):
        rows.append(generate_invalid_row(i))

    # Shuffle so invalid rows are mixed in
    random.shuffle(rows)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {args.rows} valid + {args.invalid} invalid = {len(rows)} rows -> {args.output}")


if __name__ == "__main__":
    main()
