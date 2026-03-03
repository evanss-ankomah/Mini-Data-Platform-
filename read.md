You are Claude Opus 4.6 acting as a Principal Data Engineer and reviewer.

Context:
We are building an “industry-grade mini data platform” using Docker Compose with:
- MinIO (CSV landing zone)
- Apache Airflow (orchestration)
- PostgreSQL (curated storage)
- Metabase (BI dashboards)
You can also make reference to the task.md file for more information.
Constraints:
- Keep it realistic but not overcomplicated.

Your job:
Design the complete blueprint that a coding agent (Codex GPT-5.3) will implement. You are NOT writing the full codebase; you are producing an implementation-ready spec and standards.

Deliverables (must be concrete):
1) Architecture: data flow and responsibilities of each component + failure paths (quarantine, retries).
2) Repo structure: exact folder tree and what goes in each file.
3) Data contract: propose a contracts/<dataset>_contract.yml format with:
   - columns, types, required/optional, constraints, and business rules
   - examples of valid/invalid rows
4) PostgreSQL schema:
   - curated table(s) for analytics (facts)
   - summary table(s) for dashboards
   - etl_audit_runs table (run_id, file_key, rows_in, rows_loaded, status, error_message, started_at, finished_at)
   - keys, indexes, and UPSERT strategy (idempotent reruns)
5) Pipeline design (Airflow DAG):
   - task breakdown (discover → validate → transform → load → audit → move file)
   - retry/backoff rules
   - logging requirements (structured logs)
   - how to move files to processed/ or quarantine/ and write an error report to MinIO
6) Data quality strategy:
   - pick ONE: Pandera or Great Expectations and justify briefly
   - specify exact checks (type checks, null checks, range checks, uniqueness, date sanity, etc.)
7) Security & governance:
   - Postgres roles: etl_writer (write) and bi_reader (read-only)
   - secrets handling (.env.example + GitHub Secrets)
   - short retention policy + access notes (docs/)
8) Testing plan:
   - unit tests (what functions to test, test cases)
   - integration test flow using docker compose (generate CSV → upload to MinIO → run pipeline → assert Postgres rows + audit row)
9) GitHub Actions plan:
   - CI steps (lint, unit tests, docker compose smoke, integration test, data-flow validation)
   - CD approach using self-hosted runner (docker compose up -d)
10) Definition of Done:
   - checklist that proves the platform works end-to-end + what screenshots must be captured for README.

Output format:
- Use headings
- Provide the final folder tree in a code block
- Provide the full proposed data contract YAML example
- Provide SQL DDL snippets for tables + roles
- Provide the acceptance checklist at the end

Assume the use case is: Sales CSV uploads (orders) with fields like order_id, order_date, customer_id, region, product, quantity, unit_price.