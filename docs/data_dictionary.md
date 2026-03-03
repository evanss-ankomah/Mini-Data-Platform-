# Data Dictionary

## `curated.fact_orders`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `order_id` | VARCHAR(20) | No | Primary key. Unique order identifier (format: `ORD-NNNNNN`) |
| `order_date` | DATE | No | Date the order was placed |
| `customer_id` | VARCHAR(20) | No | Customer identifier (format: `CUST-NNNN`) |
| `region` | VARCHAR(50) | No | Sales region (North America, Europe, Asia Pacific, Latin America, Middle East & Africa) |
| `product` | VARCHAR(100) | No | Product name |
| `quantity` | INTEGER | No | Number of units ordered (must be > 0) |
| `unit_price` | NUMERIC(10,2) | No | Price per unit in USD (must be > 0) |
| `total_amount` | NUMERIC(12,2) | No | Computed: `quantity × unit_price` |
| `loaded_at` | TIMESTAMPTZ | No | Timestamp when the row was inserted/last updated |
| `source_file` | VARCHAR(255) | No | Original MinIO object key for traceability |

## `curated.summary_daily_sales`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `summary_date` | DATE | No | Aggregate date (PK part 1) |
| `region` | VARCHAR(50) | No | Sales region (PK part 2) |
| `total_orders` | INTEGER | No | Count of orders for this date+region |
| `total_quantity` | BIGINT | No | Sum of all quantities |
| `total_revenue` | NUMERIC(14,2) | No | Sum of all total_amounts |
| `avg_order_value` | NUMERIC(10,2) | No | Average total_amount per order |
| `updated_at` | TIMESTAMPTZ | No | Last refresh timestamp |

## `audit.etl_audit_runs`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `run_id` | UUID | No | Primary key (auto-generated) |
| `dag_run_id` | VARCHAR(255) | Yes | Airflow DAG run identifier |
| `file_key` | VARCHAR(500) | No | MinIO object key that was processed |
| `rows_in` | INTEGER | Yes | Total rows read from CSV |
| `rows_valid` | INTEGER | Yes | Rows that passed validation |
| `rows_loaded` | INTEGER | Yes | Rows successfully loaded to fact table |
| `status` | VARCHAR(20) | No | `RUNNING`, `SUCCESS`, or `FAILED` |
| `error_message` | TEXT | Yes | Error details if status = FAILED |
| `started_at` | TIMESTAMPTZ | No | Pipeline start timestamp |
| `finished_at` | TIMESTAMPTZ | Yes | Pipeline completion timestamp |
