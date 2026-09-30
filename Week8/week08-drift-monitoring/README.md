# BMD-45 Vehicle Detection: Drift & Observability Monitoring

Welcome to the Drift and Observability Monitoring project for the BMD-45 vehicle detection system! 

In the real world, machine learning models don't just live in a vacuum—they get deployed into dynamic environments. This project simulates what happens when a model trained on daylight CCTV footage (our **reference** distribution) is suddenly evaluated on low-light footage (our **live** traffic). This phenomenon is known as **Data Drift** (or Covariate Shift).

## What Does This Project Do?

This repository contains an automated pipeline to detect and measure data drift based on the model's confidence scores. We use a metric called the **Population Stability Index (PSI)** to quantify how much the live distribution has shifted away from the reference distribution.

Specifically, the pipeline:
1. **Extracts Confidence Scores:** Runs a mock object detector over two distinct camera profiles (`camera_A_daylight` and `camera_B_lowlight`).
2. **Computes PSI:** Bins the confidence scores into a histogram and compares the proportions to calculate the PSI.
3. **Classifies Drift:** Evaluates the PSI against standard thresholds (e.g., > 0.25 is significant drift).
4. **Generates a Report:** Outputs a `drift_report.json` detailing the drift level, summary statistics, and exact PSI.

## Setup & Installation

To run this locally on your own machine:

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

3. **Generate your personal dataset:**
   (Requires a student ID for deterministic generation of synthetic data)
   ```bash
   python generate_for_student.py --student-id <your_id>
   ```

## Running the Pipeline

Once your data is generated, simply run the pipeline:
```bash
python src/run_pipeline.py
```

This will output a `drift_report.json` in the root directory. You can also run the self-checks using `pytest`:
```bash
pytest tests/ -q
```

## Understanding the Results

When testing with our generated dataset (`camera_A_daylight` vs `camera_B_lowlight`), the `drift_report.json` reveals a **significant** drift level (PSI > 0.25). 

This is completely expected! Because our live camera operates in low-light conditions, the visual statistics are significantly different from the daylight reference camera. This causes the model's confidence scores to drop, naturally resulting in a high PSI and triggering our drift alerts.

*(Note: While confidence scores are great for catching this kind of Data Drift, they can miss **Concept Drift**—situations where the data looks the same but the real-world labels have changed. For that, you'd need to monitor ground-truth performance metrics like Accuracy or F1-Score!)*
