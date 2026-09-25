# NOTES.md — Week 7: CI/CD Integration Testing

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 3293293598
Wrote 6 images across 2 camera profiles -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week7\week07-cicd\week07-cicd\data\fixtures
Wrote 30 annotations -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week7\week07-cicd\week07-cicd\data\fixtures/_annotations.coco.json

Record this seed in NOTES.md when you submit (see README.md).

## Why gate integration-test on needs: [lint, unit-test]?

<!-- Why does integration-test need needs: [lint, unit-test] instead of
     just running in parallel with them — what's the actual cost being
     avoided? -->

The integration-test job builds a Docker image, starts a container, and runs HTTP requests against it — this is significantly more expensive in both time and compute than linting or unit testing. By gating it with `needs: [lint, unit-test]`, we avoid wasting those resources on code that already has syntax/style errors or failing unit tests. If either of the fast, cheap checks fails, the expensive Docker build never runs, saving CI minutes and giving faster feedback on simple mistakes.
