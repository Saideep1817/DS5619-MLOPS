# Lab 4: Versioning, Feature Store & Lineage

This lab implements a simplified, local feature store with data lineage and versioning capabilities. The implementation focuses on the following four core functions:

## Core Functions Implemented

### 1. `snapshot_raw_version`
Generates raw data snapshots under `.feature_store/raw_versions/`. It is designed to be idempotent:
* Computes a SHA-256 hash of the CSV file.
* Checks existing manifests for a matching content hash to return the same version ID if the file hasn't changed.
* Saves version details (metadata, headers, row counts, etc.) in a JSON manifest for new data.

### 2. `build_features`
Processes transactions to build per-card aggregate features while handling schema updates:
* Auto-detects whether the schema is v1 or v2 (by checking for `country_code` vs `country`).
* Unifies the amount scale by converting `amount_minor_units` (cents) to standard float units in v2 before doing calculations.
* Calculates metrics such as average transaction amount, maximum transaction amount, card present percentage, and the latest event timestamp for each unique `card_id`.

### 3. `register_feature_group`
Saves generated features as a new immutable version under `.feature_store/feature_groups/`:
* Assigns the next incremental version ID (`v1`, `v2`, etc.).
* Stores the processed features in a `features.json` file.
* Creates a metadata `manifest.json` tracking feature schema, row counts, and parent raw version lineage.

### 4. `get_lineage`
Traces the lineage of feature groups:
* Resolves the feature group version back to the original raw dataset.
* Reads the feature group's manifest and retrieves the referenced raw data manifest, merging them into a unified dependency graph.
