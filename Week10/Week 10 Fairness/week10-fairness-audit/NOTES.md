# NOTES.md — Week 10: Fairness and Robustness Audit

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 4038677473
Wrote 60 images across 2 camera profiles -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week10\Week 10 Fairness\week10-fairness-audit\data\fixtures
Wrote 236 annotations -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week10\Week 10 Fairness\week10-fairness-audit\data\fixtures/_annotations.coco.json
Sanity-checked recall (using the mock detector, not your fairness_audit.py):      
  Two-wheeler           75.0% <-- below threshold
  Bicycle               81.8% <-- below threshold
  Three-wheeler         88.2% <-- below threshold
  Other                 88.2% <-- below threshold
  Bus                   92.9%
  Mini-bus              93.3%
  SUV                   93.8%
  Truck                 95.0%
  Tempo-traveller       95.5%
  LCV                  100.0%
  Sedan                100.0%
  Hatchback            100.0%
  MUV                  100.0%
  Van                  100.0

Record this seed in NOTES.md when you submit (see README.md).

## Which classes got flagged?

<!-- Which classes got flagged, and does that match what you'd expect given
     how generate_for_student.py built the fixtures? -->

The classes that got flagged (below the 90% recall threshold) are Two-wheeler (75.0%), Bicycle (81.8%), Three-wheeler (88.2%), and Other (88.2%).

Yes, this matches expectations. In generate_for_student.py, small vehicles are assigned much smaller bounding box multipliers (0.35 for Bicycle, 0.45 for Two-wheeler, and 0.7 for Three-wheeler), and camera_B_lowlight scales them down by another 0.7x with higher noise. Because the mock detector discards any pixel blob smaller than 20 pixels, these small targets are frequently missed. In fact, the generator script uses an explicit check (_signal_is_clean) that retries seeds until both Bicycle and Two-wheeler fall below 90% recall while large vehicles remain above 90%.

## If the grouping variable were a protected attribute

<!-- Tying back to the framing note: what would change about this audit's
     stakes and your obligations as an engineer if the grouping variable
     were a protected demographic attribute instead of a vehicle class? -->

If the grouping variable were a protected demographic attribute (e.g., skin tone, gender, etc.) instead of a vehicle class, the stakes would shift from a technical performance/fairness audit to a civil rights/ethical compliance scenario. The core obligation would change from "ensure the system works reasonably well for all classes" to "actively prevent disparate harm against protected groups." With a protected attribute, the model's decisions could expose the organization to legal liability, regulatory sanctions (e.g., under GDPR, anti-discrimination laws), and severe reputational damage. The audit's goal would transform from a diagnostic step in model improvement to a legally-required due diligence process to prevent discrimination. This would likely necessitate including such groups in the training data, deploying human-in-the-loop oversight for high-stakes decisions, and incorporating fairness-aware model development techniques (like re-weighting or adversarial debiasing) explicitly to ensure equitable outcomes, not just acceptable recall.

## Which attack could corrupt this audit?

<!-- Name one lifecycle stage and attack from the lecture (data poisoning,
     model theft, or adversarial examples) that could silently corrupt THIS
     audit's result, and one control from the lecture that would reduce the
     risk. -->

Data poisoning during the training phase could silently corrupt this audit. For example, a sophisticated adversary could inject adversarially-crafted "ghost" negative images into the training set that appear benign but are specifically designed to degrade detection performance on small vehicles (e.g., bicycles, two-wheelers), while leaving large vehicles (trucks, sedans) relatively untouched. If enough such examples were added, the trained model's recall for small vehicles would drop significantly, making them appear underperforming in this audit even if the evaluation pipeline and adversarial attack code were otherwise correct. This would silently shift the "fairness" boundary without any obvious signal during model training or validation.

One control from the lecture that would reduce this risk is input validation. By implementing rigorous checks on the distribution and quality of training data, and specifically monitoring for unusual patterns or outliers (like the intentionally small vehicle sizes in generate_for_student.py, or added adversarial examples designed to push targets below the 20-pixel detection threshold), an organization could detect and reject poisoned samples before they degrade model performance. Additionally, regular model retraining with fresh, untainted data, combined with continuous monitoring of per-class recall on a diverse validation set, would help ensure that the model's fairness properties remain stable over time.


## Would SHAP or LIME explain a missed detection?

<!-- Pick one missed ground-truth box in a flagged class. An auditor asks
     you to explain WHY the detector missed it, not just that it did. Would
     SHAP or LIME actually help you answer that for a bounding-box detector
     — and if not, what's different about this detector's inputs/outputs
     that breaks the assumption both tools make? -->

No, SHAP or LIME wouldn’t really help explain a missed detection (for example, a missed Two-wheeler in one of the low-light images).

The fundamental issue is that both tools are designed to explain an existing output—they tell you which pixels caused a specific prediction or probability score. But for a missed detection, the detector produced nothing at all. There is no bounding box, confidence score, or output value to trace back to the input pixels.

Additionally, object detectors don't output a fixed class score; they output a variable list of boxes and coordinates. Tools like LIME work by blanking out patches of the image, which just disrupts the connected pixel shapes the detector relies on anyway rather than explaining why the original object was overlooked.

## What did your attack show?

<!-- Using fairness_report.json["adversarial"]: at what eps does each flagged
     class fall further? Which class is most fragile, and is it the same
     class the clean audit flagged? Compare the drop ranking
     (most_fragile) with lowest_recall_under_attack — do they agree, and
     which is the better measure of who is hurt? What does that say about who bears the
     cost of an attack (or of an unmonitored failure)? Then: what would
     adversarial training or input validation look like for this detector,
     and why does a rule this simple break so much more easily than a CNN
     (or does it)? -->

Drop across eps: Bicycle, Three-wheeler, and Other start dropping right away at eps=10 (Bicycle falls from 81.8% to 63.6%). Two-wheeler holds steady at 75% until eps=20, where it drops to 58.3%. By eps=40, Bicycle crashes down to just 13.6%.

Fragility vs. Clean Audit: At eps=20, Van is listed as the most fragile because its recall dropped the most (by 33.3%). This is different from the clean audit, which originally flagged Two-wheelers and Bicycles.

Drop ranking vs. Lowest recall: They do not agree. Van had the largest drop only because it started at 100%. But under attack, Bicycle (50.0%) and Two-wheeler (58.3%) have the lowest actual recall.

Who is hurt: Lowest recall is the better measure of real harm. Missing 1 out of 3 vans is bad, but missing half or more of all bicycles is dangerous. The cost of failure falls heaviest on the smaller, vulnerable road users.

Defense & CNN comparison: Input validation would mean adding a simple blur/denoising filter before detection to wipe out pixel noise. Adversarial training would mean tuning the color thresholds using noisy images. This simple detector breaks much faster than a CNN because it uses rigid pixel rules (r - g > 40)—a tiny bit of noise instantly breaks the connected shape, while CNNs look at broader visual patterns.