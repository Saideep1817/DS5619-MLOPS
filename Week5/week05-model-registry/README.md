# Lab 5 — Model Registry Governance

**Track A (tabular fraud-detection) · Week 5 · DS5619 Machine Learning Systems Operations**


## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_for_student.py --student-id <your roll number or institute email>
```
## Learning objective

This week's lecture covered the model registry as an artifact store, model
cards as the one-page governance record, and why the registry — not a Slack
thread or someone's memory — is the answer to "what's actually in
production." You'll build a **minimal local model registry** that enforces
those two governance rules as code, not just policy: no promotion to
Production without a complete model card, and no promotion without metrics
that clear a quality bar.

This week's lecture also named where the problem starts: a hyperparameter
search or AutoML run producing many near-identical candidates (like
`candidate_a`/`candidate_b` here, just two of them) — explicitly scoped as
model-development work this course doesn't teach as a lab, because the
registry is what happens *after* that search ends, which is exactly what
you're building.

## Files

- `src/mini_model_registry.py` — implement the four `# TODO` functions.
- `src/run_pipeline.py` — complete driver script. Don't edit.
- `model_card_fields.json` — fill in with real content before running the
  pipeline (it will refuse to run while any `TODO` remains).
- `data/candidate_a/`, `data/candidate_b/` — your two personalized model
  candidates + their metrics, generated above (don't hand-edit).

## Background

`data/candidate_a/` and `data/candidate_b/` are two already-trained
candidate models for a fraud-detector (deliberately simple: a single amount
threshold), each with its own `metrics.json`. One clears production quality
bar, one doesn't — you won't be told which until you run the pipeline and
see the registry enforce it.

## Core Registry Functionality

The core model registry functionality is implemented through four functions in `src/mini_model_registry.py`.

### `register_model(name, model_path, metrics, registry_dir)`

This function handles the registration and versioning of candidate models.

* Automatically assigns the next available version number, such as `v1`, `v2`, and so on, under `.model_registry/models/<name>/`.
* Copies the trained model definition into the version directory as `model.json`.
* Creates a `manifest.json` containing the model name, assigned version ID, evaluation metrics, registration timestamp, and initial stage (`"None"`).
* Returns the newly assigned version ID.

### `generate_model_card(name, version_id, card_fields, registry_dir)`

This function ensures that the model has the required governance documentation before it can be promoted.

* Checks that all required sections are provided: `intended_use`, `training_data`, `limitations`, and `ethical_considerations`.
* Raises a `ValueError` if a required field is missing, empty, or still contains `"TODO"`.
* Reads the model's evaluation metrics from `manifest.json` and includes them in the model card along with the provided documentation.
* Saves the completed documentation as `model_card.json` in the model's version directory.
* Returns the path to the generated model card.

### `promote_model(name, version_id, target_stage, registry_dir)`

This function acts as the model's quality and governance gate.

* Promotion to `"Staging"` is allowed without the Production-specific governance checks.
* Promotion to `"Production"` requires:

  1. A completed `model_card.json` to be present.
  2. The model's F1 score to meet the required threshold of `0.70` or higher.
* If either Production requirement is not satisfied, the function raises a `GovernanceError` and blocks the promotion.
* When a model is successfully promoted to Production, any previously active Production version is changed to `"Archived"`, ensuring that only one version is active in Production.
* Records every stage transition in `manifest["history"]` and writes the updated manifest back to disk.
* Returns the updated manifest.

### `get_production_model(name, registry_dir)`

This function provides a single way to identify the model currently deployed to Production.

* Searches all registered versions of the specified model.
* Reads each version's `manifest.json` and checks its `stage`.
* Returns the manifest of the version whose stage is `"Production"`.
* Returns `None` if no version is currently in Production.
