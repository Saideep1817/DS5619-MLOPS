# model-compression

## Objective
The objective of this project is to explore and benchmark two fundamental model compression techniques—**magnitude-based pruning** and **INT8 quantization**—against a linear classifier. It evaluates the trade-offs across the three key Pareto dimensions: **storage size**, **inference latency**, and **accuracy**, while illustrating why pruning requires a sparse format to actually save storage.

---

## Core Functions (`src/compression.py`)

- **`model_size_bytes(weights, dtype_bytes)`**  
  Computes the memory footprint in bytes for storing weights in a dense array format given the data type byte width (e.g., 4 bytes for FP32, 1 byte for INT8).

- **`prune_weights(weights, sparsity)`**  
  Applies magnitude-based unstructured pruning. Finds the fraction `sparsity` of weights with the smallest absolute values and sets them to `0.0` without mutating the original list.

- **`sparse_coo_size_bytes(weights, value_bytes=4, index_bytes=4)`**  
  Calculates the storage size in a sparse Coordinate (COO) format. Only non-zero weights are stored, each paying for both its value (4 bytes) and its index location (4 bytes).

- **`quantize_int8(weights)`**  
  Applies symmetric linear quantization, scaling float weights into signed 8-bit integers (`[-127, 127]`) with `scale = max|w| / 127`.

- **`dequantize_int8(quantized_weights, scale)`**  
  Converts INT8 quantized integers back to approximate float values (`w ≈ q * scale`) for inference.

- **`predict(weights, features)`**  
  Runs linear classification inference (`dot_product(weights, features) > 0`).

- **`benchmark_model(label, weights, eval_examples, dtype_bytes, n_latency_reps=50)`**  
  Benchmarks a weight variant against the evaluation dataset, measuring its storage size in bytes, accuracy, and average wall-clock latency (ms).

---

## Getting Started

### 1. Setup Environment
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

*(On Windows PowerShell, use `.\.venv\Scripts\activate`)*

### 2. Run Compression Pipeline
```bash
python src/run_pipeline.py
```
This benchmarks the four variants (`baseline_fp32`, `pruned_dense_fp32`, `pruned_sparse_coo`, `quantized_int8`) and outputs `compression_report.json`.

### 3. Run Self-Check Tests
```bash
pytest tests/ -q
```

