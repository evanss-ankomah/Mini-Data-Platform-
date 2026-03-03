# Data Retention & Access Policy

## Retention Schedule

| Data | Location | Retention | Action |
|------|----------|-----------|--------|
| Raw CSVs (processed) | MinIO `processed/` | 90 days | Auto-expire via MinIO lifecycle rule |
| Quarantined CSVs | MinIO `quarantine/` | 30 days | Review → reprocess or delete |
| Error reports | MinIO `errors/` | 30 days | Delete after investigation |
| Fact orders | PostgreSQL `curated.fact_orders` | Indefinite | Partition by year if >10M rows |
| Daily summaries | PostgreSQL `curated.summary_daily_sales` | Indefinite | Small table |
| Audit logs | PostgreSQL `audit.etl_audit_runs` | 1 year | Purge via scheduled job |
| Airflow logs | Container volume | 14 days | Cleanup DAG or cron |

## Access Control

| Role | Purpose | Permissions |
|------|---------|-------------|
| `admin` | PostgreSQL superuser | Full access (infrastructure only) |
| `etl_writer` | Used by Airflow | Read/write on `curated.*`, read/write on `audit.*` |
| `bi_reader` | Used by Metabase | Read-only on `curated.*` and `audit.*` |

## Notes

- All secrets stored in `.env` (gitignored) and GitHub Actions Secrets
- No PII is stored in this platform — sales data contains order-level (not personal) information
- MinIO lifecycle rules should be configured via `mc ilm` if long-term automation is needed
