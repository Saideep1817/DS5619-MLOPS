# Vehicle Detection Service — Containerization & API

## Environment Setup

1. **Virtual Environment & Dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Generate Test Fixtures:**
   ```bash
   python generate_for_student.py --student-id <ID>
   ```
   Creates student-seeded synthetic CCTV camera captures in `data/fixtures/`, providing deterministic test images across different camera profiles and lighting conditions.

---

## Core Implementation

### `load_image_from_upload(file_storage)`
Converts incoming multipart file objects into preprocessed PIL Images:
- Reads the raw binary data from the upload stream into an in-memory `io.BytesIO` buffer.
- Decodes the image via Pillow and normalizes color channels to standard RGB (`.convert("RGB")`), ensuring consistent 3-channel input for the detector regardless of original format (such as RGBA or palette).

### `run_detection(image)`
Manages model inference and structured output formatting:
- Supplies the preprocessed PIL image to the detector module (`det.detect()`).
- Translates detected bounding boxes and categories into COCO-compliant annotation records using `det.detections_to_coco()`.
- Wraps the formatted detections along with the total count into a JSON-serializable dictionary.

### `detect()` Route (`POST /detect`)
Connects the web endpoint to the inference pipeline:
- Validates that an `"image"` field exists in `request.files`, returning an HTTP `400` status with an informative error message if omitted.
- Processes the uploaded file via `load_image_from_upload()`.
- Evaluates the image using `run_detection()` and sends back the serialized detection JSON with an HTTP `200` status code.

### Containerization (`Dockerfile`)
Packages the entire service into a standalone Docker image:
- Utilizes `python:3.12-slim` to maintain a lightweight base footprint.
- Copies `requirements.txt` and installs packages using `--no-cache-dir` to reduce layer size.
- Copies application source code into the `/app` working directory.
- Exposes port `8080` and defines `CMD ["python", "src/app.py"]` to start the Flask server on startup.

---

## Verification & Testing

### Local Service Run
Tested the Flask application directly:
```bash
python src/app.py
```

### Docker Build & Container Execution
Built and launched the isolated container:
```bash
docker build -t week6-detector .
docker run --rm -p 8080:8080 week6-detector
```

### Endpoint Validation
Tested API functionality against the active container:

- **Health Check (`GET /health`):**
  ```bash
  curl http://localhost:8080/health
  ```
  *Response:* `{"status": "ok"}`

- **Vehicle Detection (`POST /detect`):**
  ```bash
  curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect
  ```
  *Response:* Returns detection count and bounding box coordinates structured in COCO format.

---

## Self-Check

Ran the automated smoke test suite to validate route responses and status codes:
```bash
pytest tests/ -q
```
