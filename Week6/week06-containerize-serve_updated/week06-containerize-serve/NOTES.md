# NOTES.md — Week 6: Containerize and Serve a Detector

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 128687641
Wrote 6 images across 2 camera profiles -> C:\Users\Saide\OneDrive\c ++\daily practice\MLOPS\DS5619-MLOPS\Week6\week06-containerize-serve_updated\week06-containerize-serve\data\fixtures
Wrote 21 annotations -> C:\Users\Saide\OneDrive\c ++\daily practice\MLOPS\DS5619-MLOPS\Week6\week06-containerize-serve_updated\week06-containerize-serve\data\fixtures/_annotations.coco.json

## Built image size

<!-- What image size did `docker images` report for week6-detector? -->
command : docker images week6-detector
234 MB

## Swapping in a real checkpoint

<!-- What's the single biggest thing you'd change about this Dockerfile if
     src/mock_detector.py were swapped for a real torch-based checkpoint?
     (Think about what that does to build time and image size.) -->
If swapping `mock_detector.py` for a real PyTorch-based checkpoint (e.g. YOLOv12-S), the single biggest change would be using a multi-stage build or CPU-only PyTorch to avoid pulling full CUDA packages, and downloading/baking in or volume-mounting the model weights.