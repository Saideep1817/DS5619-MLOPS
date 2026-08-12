# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301018

## What was hardcoded, and what would switching it have required?

<!-- What specifically was hardcoded in the original script, and what would
     have had to happen to change the threshold or switch formats before
     your refactor? -->
-> Here the Hardcoded values are input_path , input_format , high_value_threshold , output_path and these are hardcoded in config directory with files named as pipelined.yaml , pipeline.yaml , pipeline_json.yaml

-> We need to manually change in the yaml file to change the values , and again run the pipeline for the changes to take effect.

