# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301018


## Quarantine count vs. the 7 known injected problems

<!-- How many rows ended up quarantined, and does that match the 7 known
     injected problems? (It won't match exactly — some rows may trip more
     than one expectation. Explain the discrepancy if there is one.) -->

     Actually the no of rows that ended up quarantined are 8 in my dataset.
     1. expect_column_not_null for amount failed 2 times , rows 75,190
     2. expect_column_not_null for card_id failed 1 time , row 417
     3. expect_column_positive for amount failed 3 times , rows 75,190,349
     4. expect_column_in_set for merchant_category failed 1 time , row 526
     5. expect_column_unique for transaction_id failed 1 time , row 327

     Total rows quarantined = 8