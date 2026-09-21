# Power BI handoff

Power BI was not run or tested in this repository. The following model is a practical handoff based on the generated CSV exports.

## Tables

`fact_service_interval` stores one row for each synthetic participant, workload and hour.

`fact_service_runs` stores scheduled Settlement and payment run outcomes.

`dim_participant` stores the synthetic participant identifier and category.

`dim_submission_type` stores the workload category.

## Relationships

Join `fact_service_interval.participant_id` to `dim_participant.participant_id`.

Join `fact_service_interval.submission_type` to `dim_submission_type.submission_type`.

Keep `fact_service_runs` separate because scheduled run records are not participant submissions.

## Suggested measures

```DAX
Arrivals = SUM(fact_service_interval[submissions_received])
Processed = SUM(fact_service_interval[submissions_processed])
Backlog = SUM(fact_service_interval[backlog_size])
Forecast Variance = DIVIDE([Arrivals] - SUM(fact_service_interval[forecast_submissions]), SUM(fact_service_interval[forecast_submissions]))
Failure Rate = DIVIDE(SUM(fact_service_interval[validation_failure_count]), [Arrivals])
Retry Rate = DIVIDE(SUM(fact_service_interval[retry_count]), [Arrivals])
Delayed Runs = CALCULATE(COUNTROWS(fact_service_runs), fact_service_runs[status] = "Delayed")
```

These measures describe the generated sample. They are not Elexon service measures or agreed operational definitions.
