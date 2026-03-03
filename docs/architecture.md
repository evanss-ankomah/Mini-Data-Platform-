# Architecture

## Overview

This mini data platform processes sales CSV files end-to-end using four Docker Compose services:

```
  CSV Upload          MinIO              Airflow              PostgreSQL          Metabase
 ──────────►   landing/sales/   ──►   ETL Pipeline   ──►   curated schema  ──►   Dashboards
                    │                     │                     │
                    ├── processed/        │                     ├── fact_orders
                    ├── quarantine/       │                     ├── summary_daily_sales
                    └── errors/           │                     └── etl_audit_runs
                                          │
                                     Tasks:
                                     1. discover_files
                                     2. validate_schema (Pandera)
                                     3. transform_data
                                     4. load_to_postgres (UPSERT)
                                     5. refresh_summary
                                     6. write_audit_row
                                     7. move_file
```

## Components

| Component | Image | Purpose | Port |
|-----------|-------|---------|------|
| PostgreSQL 16 | `postgres:16-alpine` | Curated analytics storage + audit trail | 5432 |
| MinIO | `minio/minio:latest` | S3-compatible file storage (landing, processed, quarantine, errors) | 9000/9001 |
| Airflow 2.9 | Custom (extends `apache/airflow:2.9.3`) | ETL orchestration (LocalExecutor) | 8080 |
| Metabase | `metabase/metabase:latest` | Self-service BI dashboards | 3000 |

## Failure Handling

- **Validation failures**: File → `quarantine/`, error report → `errors/<run_id>.json`, audit row with `FAILED`
- **Load failures**: 3 retries with exponential backoff, then quarantine
- **Idempotency**: `ON CONFLICT (order_id) DO UPDATE` ensures safe reruns
