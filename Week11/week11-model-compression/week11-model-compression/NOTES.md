# NOTES.md — Week 11: Model Compression Benchmark

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
student_id: 112301018
seed: 3827338215
Wrote 256 weights (40 informative) -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week11\week11-model-compression\week11-model-compression\data/weights.json
Wrote 300 eval examples -> C:\Users\Saide\OneDrive\cpp\daily_practice\MLOPS\DS5619-MLOPS\Week11\week11-model-compression\week11-model-compression\data/eval_data.json

Record this seed in NOTES.md when you submit (see README.md).

## pruned_dense_fp32 vs. pruned_sparse_coo

<!-- Compare pruned_dense_fp32 and pruned_sparse_coo in your report — same
     weights, same accuracy, very different size_bytes. Explain why in your
     own words (tie it to the lecture's pruning pitfall). -->

In our benchmark results:
- `pruned_dense_fp32`: 1024 bytes (1.00x), 99.67% accuracy
- `pruned_sparse_coo`: 616 bytes (1.66x), 99.67% accuracy

Both models share the exact same pruned weights, which is why their accuracy (99.67%) is identical. However, their file sizes are very different:

1. **The Pruning Pitfall (`pruned_dense_fp32`):** Just setting small weights to `0.0` does not automatically save any memory if you keep them in a standard dense array. The system still reserves space for all 256 slots at 4 bytes each (`256 * 4 = 1024 bytes`). The zeros are still physically stored in memory.
2. **Sparse Storage (`pruned_sparse_coo`):** To actually save bytes, we need a sparse format like COO that simply ignores zeros. But there is a trade-off: for every non-zero weight that survives, we must store its value (4 bytes) AND its index location (4 bytes), costing 8 bytes per entry.
3. **The Net Benefit:** Because 70% of the weights were pruned, only 77 non-zero weights remain. At 8 bytes each, the model takes `77 * 8 = 616 bytes`. Sparse formats only save space when you prune enough weights (over 50%) to overcome the overhead of storing index pointers.


## The 0.95-sparsity experiment

<!-- Try editing PRUNE_SPARSITY in src/run_pipeline.py to 0.95 and re-run —
     what happens to accuracy, and why does that make sense given only 40
     of the 256 weights are actually informative? -->

When setting `PRUNE_SPARSITY = 0.95`:
- The accuracy drops sharply from **99.67% down to 80.67%**.
- The number of surviving non-zero weights shrinks from 77 down to just 13.

**Why this makes sense:**
- In our 256-weight model, only **40 weights are informative** (carrying the real classification signal), and the remaining **216 weights are just near-zero noise**.
- Magnitude pruning removes the smallest weights first.
- At **70% sparsity**, we prune 179 weights (`0.70 * 256`). Since 179 is less than the 216 noise weights, we only cut out garbage, leaving all 40 informative weights intact—accuracy stays near 100%.
- At **95% sparsity**, we prune 243 weights (`0.95 * 256`). Because there are only 216 noise weights available, pruning is forced to eat into the informative weights, discarding 27 of the 40 real weights. With only 13 informative weights left, the model loses most of its actual signal, and accuracy falls off a cliff.

