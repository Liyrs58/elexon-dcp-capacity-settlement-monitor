# Data dictionary

All operational rows are synthetic. An identifier beginning with `SYN` is fictional.

| Field | Meaning | Control or use |
| --- | --- | --- |
| timestamp | Synthetic hourly interval | Ordering and trend analysis |
| participant_id | Fictional participant identifier | Segmentation only |
| participant_type | VLP, VTP, AMVLP or Supplier | Workload grouping |
| submission_type | New MSID Pair, new AMSID Pair or historic resubmission | Workload grouping |
| submissions_received | Records arriving in the interval | Arrival rate |
| submissions_processed | Records completed in the interval | Throughput |
| backlog_size | Open records after processing | Queue reconciliation |
| processing_latency_minutes | Generated latency indicator | Trend and alert input |
| validation_failure_count | Generated rejected or failed checks | Quality signal |
| retry_count | Generated repeated attempts | Rework signal |
| forecast_submissions | Generated submitted forecast | Forecast comparison |
| actual_submissions | Same generated arrival count | Forecast comparison |
| service_level_deadline_minutes | Synthetic deadline | Demonstration only |
| downstream_settlement_risk_flag | Generated flag from demo rules | Investigation cue |
| demo_capacity_per_hour | Synthetic processing budget | Scenario input |

The scheduled run file stores synthetic Settlement critical and payment critical run records separately from registration workload rows.
