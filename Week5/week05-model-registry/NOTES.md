# NOTES.md — Week 5: Model Registry Governance

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
18
student_id: 112301018
seed: 474473176
candidate_a: f1=0.51 (below 0.70 bar)
candidate_b: f1=0.841 (clears 0.70 bar)

Record this seed in NOTES.md when you submit (see ASSIGNMENT.md).

## Which candidate reached Production, and why?

<!-- Which candidate ended up in Production, and why? -->
Candidate_b was the one who reached production as it satisfied both the conditions of  having a model_card.json and also having the f1 score greater than 0.70.

## Gating stale feature data

<!-- What would you need to add to promote_model's gate if you also wanted
     to block promotion of a model trained on stale (e.g. >30-day-old)
     feature data? -->
     We could add an additional gate in promote_model() that checks the age of the feature data used to train the model. The registry would compare the feature data's timestamp with the current date. If the feature data is more than 30 days old, the promotion would be blocked and the model would not be allowed to move to Production. This helps ensure that only models trained on sufficiently recent feature data are deployed.It is possible only when we add feature data creation in manifest.json at register_model function.

## Scaling the gate to 40 candidates

<!-- Tying back to this week's AutoML/HPO framing: if a hyperparameter
     search had handed you 40 candidates instead of 2, what in your
     register_model/promote_model design would need to change (or
     genuinely wouldn't) to gate 40 instead of 2? -->
     The register_model() and promote_model() designs would not fundamentally need to change to handle 40 candidates instead of 2. Both functions operate on one model/version at a time, so the same registration and governance gates can be applied independently to all 40 candidates.
     