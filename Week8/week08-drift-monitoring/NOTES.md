# NOTES.md — Week 8: Drift and Observability Monitoring

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 845347575
Wrote 40 images across 2 camera profiles -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week8\week08-drift-monitoring\data\fixtures
Wrote 161 annotations -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week8\week08-drift-monitoring\data\fixtures/_annotations.coco.json
Sanity-checked PSI (using the mock detector, not your drift_monitor.py): 0.2719

## Drift level vs. expectation

<!-- What drift level did the report show, and does that match what you'd
     expect given the two cameras were built with deliberately different
     visual statistics? -->
The drift report showed a "significant" drift level, with a PSI of 0.2719.
This matches what we would expect. The reference camera (`camera_A_daylight`) and the live camera (`camera_B_lowlight`) were built with deliberately different visual statistics (daylight vs lowlight conditions). These different conditions naturally lead to significant variations in the confidence scores (and general model performance), which results in a high Population Stability Index (PSI). Therefore, detecting a significant drift level is the anticipated outcome when comparing these two distinct distributions.


## What confidence-score-only monitoring misses

<!-- What would you monitor IN ADDITION to confidence score if you had
     access to ground-truth labels a day later? (Tie this to the kinds of
     drift from the lecture — which one does confidence-score-only
     monitoring miss?) -->
If we had access to ground-truth labels a day later, the best thing to monitor in addition to the confidence score would be actual performance metrics like **Accuracy, Precision, Recall, or F1-score**. 

Monitoring only confidence scores is great for catching **Data Drift (Covariate Shift)**—like when our camera switches from day to night and the model gets less confident because the inputs look different. However, it completely misses **Concept Drift**. 

In Concept Drift, the relationship between the input and the target variable changes. For example, if a "defect" in a product gets redefined but the images look the same, the model will still confidently predict the old definition. It will be confidently wrong. You can only catch this by comparing the model's predictions against the actual ground-truth labels to see that the real-world performance is dropping.
