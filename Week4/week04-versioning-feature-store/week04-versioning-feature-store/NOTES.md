# NOTES.md — Week 4: Versioning, Feature Store & Lineage

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 2663842921

## v1 vs. v2 manifest comparison

<!-- What's different between the v1 and v2 feature group's manifest.json?
     (Look at both.) -->
     -> They both have different source_raw_version_id's which are v1 and v2 
     -> They also have different feature_group_version_id's
     -> The v1 feature group has a row_count of 381 while the v2 feature group has a row_count of 113 representing unique rows among them.
     
## Why treat amount_minor_units differently from amount?

<!-- Why does build_features need to treat amount_minor_units differently
     from amount for the aggregates to be comparable across versions? -->
     -> In v1, transaction amount is stored in major units while in v2, transaction amount is stored in minor units. 
     Therefore, in order to compare the aggregates, we need to convert the amount_minor_units to major units by dividing it by 100.
