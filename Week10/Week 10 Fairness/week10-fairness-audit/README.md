# Week 10: Fairness and Robustness Audit

## Project Objective

In safety-critical computer vision applications (such as autonomous driving and traffic monitoring), overall accuracy or aggregate mAP often conceals significant performance disparities across different groups. This project implements a **fairness and adversarial robustness audit** on a multi-class vehicle detector:

1. **Class-Disparity Fairness Audit:** Adapts fair machine learning concepts (such as equal opportunity / true positive rate across subgroups) to computer vision by auditing recall independently across 14 vehicle categories. It systematically surfaces categories that fall below a minimum acceptable recall threshold (90%), highlighting disparities that affect smaller, vulnerable road users (e.g., bicycles, two-wheelers).
2. **Adversarial Robustness Testing:** Tests detector resilience against white-box adversarial color perturbations (L-infinity budget, FGSM-style) across multiple noise levels (`eps` in `{0, 10, 20, 30, 40}`) to measure class fragility and observe how attacks degrade detection recall.
3. **Automated Reporting:** Generates a structured JSON report (`fairness_report.json`) documenting per-category detection rates, underperforming classes, and vulnerability rankings under attack.

---

## Implemented Functions & Architecture

The project codebase is organized under `src/` and consists of the following core modules and functions:

### 1. `src/fairness_audit.py` (Fairness Audit Module)

- **`compute_iou(box_a, box_b) -> float`**  
  Calculates the Intersection-over-Union (IoU) between two bounding boxes formatted as `[x, y, w, h]`. Converts boxes to `(x1, y1, x2, y2)` coordinates, clamps intersection width and height to non-negative values, and computes `intersection_area / union_area` (returns `0.0` if union area is zero).

- **`match_ground_truth(gt_boxes, detections, iou_threshold=0.3) -> list[bool]`**  
  Determines whether each ground-truth bounding box was successfully detected. Compares each ground-truth box against all candidate proposals from `mock_detector.Detection` and returns a boolean array marking whether each box achieved an `IoU >= iou_threshold` with at least one prediction.

- **`audit_by_category(coco_path, fixtures_dir, iou_threshold=0.3, transform=None) -> dict`**  
  Loads image metadata and COCO ground-truth annotations (`_annotations.coco.json`). Runs the detector over each image (applying an optional PIL image `transform` if supplied), checks recall across ground-truth annotations via `match_ground_truth`, and aggregates results per category:
  ```python
  {category_name: {"total": int, "detected": int, "recall": float}}
  ```

- **`find_underperforming_categories(category_stats, recall_threshold=0.90) -> list[tuple]`**  
  Filters all categories whose recall falls strictly below `recall_threshold` and returns them as `(category_name, recall)` tuples sorted worst-first (lowest recall first).

---

### 2. `src/adversarial.py` (Adversarial Robustness Module)

- **`perturb_image(img, eps) -> Image`**  
  Executes an L-infinity-bounded white-box adversarial perturbation on an RGB image without mutating the original image in place. Because the detector targets reddish pixels (`r > 120` and `r - g > 40` and `r - b > 40`), the attack decreases the red channel by `eps` while increasing the green and blue channels by `eps`, clamping all pixel values to `[0, 255]`.

- **`audit_under_attack(coco_path, fixtures_dir, eps_values=(0, 10, 20, 30, 40), iou_threshold=0.3) -> dict`**  
  Executes `audit_by_category` iteratively across each perturbation budget `eps` in `eps_values` using `perturb_image` as the image transformation. Returns a mapping `{eps: category_stats}`, where `eps=0` serves as the baseline clean audit.

- **`find_most_fragile(attack_stats, eps, top_k=3) -> list[tuple]`**  
  Measures the vulnerability of each category at a given perturbation level `eps` by calculating the drop in recall:  
  `drop = clean_recall - attacked_recall` (where clean recall is measured at `eps=0`).  
  Returns the top `k` most fragile categories sorted by largest drop first (with alphabetical tie-breaking).

---

### 3. `src/run_pipeline.py` (Driver Pipeline)

- Ties the audit and robustness modules together.
- Evaluates the clean dataset to flag underperforming classes.
- Evaluates robustness across `eps` in `{0, 10, 20, 30, 40}`.
- Exports the consolidated results to `fairness_report.json`.
- Prints per-category recall summaries, under-attack matrices, and fragility rankings to standard output.

---

## Project Setup & Execution

### 1. Environment Setup

Create and activate a Python virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install the required dependencies (`pillow` and `pytest`):

```bash
pip install -r requirements.txt
```

### 3. Generate Fixtures

Generate personalized synthetic dataset fixtures seeded with your student ID:

```bash
python generate_for_student.py --student-id <your-student-id>
```

This creates 60 synthetic camera images under `data/fixtures/` and outputs `data/fixtures/_annotations.coco.json`.

### 4. Run Tests

Run the test suite to verify the fairness audit and adversarial attack implementations:

```bash
pytest tests/ -q
```

### 5. Run the Audit Pipeline

Execute the full audit and robustness pipeline:

```bash
python src/run_pipeline.py
```

This prints per-category recall statistics and robustness tables to the terminal and outputs `fairness_report.json`.
