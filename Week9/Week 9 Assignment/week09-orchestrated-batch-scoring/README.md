# Mini Orchestrator: Building a Tiny Airflow for Batch Scoring

Welcome to the Mini Orchestrator project for our batch scoring system! 

In the real world, data pipelines and ML workflows don't just magically run in perfect sequence—they get deployed into messy environments where strict dependencies must be respected, and external APIs fail unexpectedly. This project simulates what happens when we build a bare-bones task orchestrator to reliably manage a batch scoring pipeline.

## What Does This Project Do?

This repository contains a custom-built miniature task orchestrator (similar to a lightweight Apache Airflow) that dynamically schedules and runs a machine learning batch scoring pipeline. 

Specifically, the pipeline:
1. **Extracts:** Gathers a set of images from our local fixtures folder.
2. **Scores:** Runs a mock object detector over the images to count detected objects.
3. **Loads:** Writes out the aggregated counts to a `batch_report.json` file.
4. **Notifies:** Simulates a flaky webhook call to an alerting service (like Slack).

To manage this, our orchestrator handles:
* **Topological Sort:** Uses Kahn's Algorithm to ensure tasks always execute in the mathematically correct order based on their dependencies (e.g., we cannot load data before scoring it).
* **Automatic Retries:** Catches failures in flaky tasks (like our mock `notify` webhook) and safely retries them so the pipeline doesn't crash from a temporary network hiccup.

## Setup & Installation

To run this locally on our own machine:

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate our personal dataset:**
   (Requires a student ID for deterministic generation of synthetic data)
   ```bash
   python generate_for_student.py --student-id <student_id>
   ```

## Running the Pipeline

Once our data is generated, simply run the pipeline:
```bash
python src/run_pipeline.py
```

This will execute the DAG and output a `dag_run_summary.json` and `batch_report.json` in the root directory. We can also run the self-checks and unit tests using `pytest`:
```bash
pytest tests/ -q
```

## Understanding the Results

When running our pipeline, the `dag_run_summary.json` reveals the exact execution order computed by the orchestrator (e.g., `extract` -> `score` -> `load`, `notify`) and the number of attempts each task took.

We will notice that the `notify` task typically requires 3 attempts to succeed. This is completely expected! Because we deliberately simulated a flaky downstream service, the orchestrator naturally caught the failures, waited, and retried the task without bringing down the rest of the pipeline.

*(Note: While automatically retrying failed tasks is a great resilience strategy, it introduces a risk of "retry storms" and massive cost spikes under a **FinOps** lens when dealing with expensive, metered third-party APIs. For real-world deployments, strict retry limits and exponential backoffs are essential!)*
