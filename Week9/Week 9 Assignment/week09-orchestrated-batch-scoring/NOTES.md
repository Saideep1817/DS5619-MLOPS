# NOTES.md — Week 9: Orchestrated Batch Scoring

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 1347026626
Wrote 40 images across 2 camera profiles -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week9\Week 9 Assignment\week09-orchestrated-batch-scoring\data\fixtures
Wrote 152 annotations -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week9\Week 9 Assignment\week09-orchestrated-batch-scoring\data\fixtures/_annotations.coco.json



## notify retry count

<!-- How many attempts did notify take in your run? (Check
     dag_run_summary.json.) -->
It took 3 attempts.

## Branch independence

<!-- Why does load still succeed even though notify — its "sibling" in the
     DAG — failed on its first two attempts? What does that tell you about
     how failures in one branch of a DAG should (or shouldn't) affect an
     unrelated branch? -->
`load` succeeded because its execution dependency is strictly on `score`, which had already completed successfully. In a DAG, task scheduling is governed entirely by directed upstream dependencies, not sibling relationships. Since `load` and `notify` are separate branches emanating from `score`, transient failures or retries in `notify` have no bearing on the inputs or execution contract of `load`.

This highlights key principles in robust data engineering:
- **Fault Isolation & Blast Radius Containment:** Independent branches remain isolated so that transient issues in auxiliary or non-critical tasks (such as telemetry, Slack webhooks, or alerting) never block or bring down core operational deliverables (such as writing out scored results to `batch_report.json`).
- **Graceful Degradation:** A system can successfully deliver primary batch outputs even if an external notification service experiences downtime.

## Retry cost under FinOps

<!-- Tying back to this week's FinOps content: if notify were a metered API
     call you paid for per attempt, what would you change about the retry
     strategy, and why is "retry every failed task the same way" a risky
     default once cost enters the picture? -->

If `notify` were a metered API call, we would make the following changes to the retry strategy:
1. **Differentiate Error Types:** Only retry on transient/recoverable errors (like 503 Service Unavailable or network timeouts). Deterministic errors (like 400 Bad Request or 401 Unauthorized) should fail immediately without retrying, as they will never succeed and will just burn money.
2. **Use Exponential Backoff:** Instead of a fixed, short delay, we would increase the wait time between each retry attempt (e.g., 1s, 2s, 4s). This prevents "retry storms" that flood the API and quickly rack up bills during a sustained outage.
3. **Set a Strict Retry Limit:** Cap the `max_retries` to a low number based on the FinOps budget to ensure the worst-case scenario is capped financially.

A blanket "retry every failed task the same way" default is risky once cost enters the picture because tasks have different side effects and financial profiles. Retrying a local, pure data transformation might only cost a fraction of a cent in compute, but blindly retrying a premium third-party service or a heavy BigQuery job can lead to massive cost spikes if the underlying service has a prolonged failure.
