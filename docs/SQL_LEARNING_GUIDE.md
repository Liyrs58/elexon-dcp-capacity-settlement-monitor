# SQL learning guide

The SQL layer is intentionally small. The generated rows are loaded into SQLite and grouped for reporting.

## Hourly service signals

The first query groups `registration_metrics` by timestamp. It sums arrivals, processed work, queue size, failures, retries and critical work. It calculates failure rate and retry rate by dividing counts by arrivals and using `NULLIF` to avoid division by zero.

Why it exists: the overview chart needs one row per hour instead of one row per participant and workload.

Interview answer: “I grouped the facts at the reporting grain used by the chart, then calculated rates from counts rather than averaging percentages blindly.”

## Segment forecast variance

The second query groups by participant and submission type. It sums actual and forecast values, calculates absolute and relative variance, finds peak backlog and sums retries.

Why it exists: the driver page needs a ranked investigation list.

Important detail: the percentage is calculated from grouped totals. That avoids giving a tiny segment the same weight as a large segment simply because it has a percentage.

## Scheduled run context

The third query selects generated run time, run type, delay, deadline, status and risk flag from `service_runs`.

Why it exists: the public case includes delayed Settlement and payment activity, so timing context belongs beside queue measures.

## Store queries

`hourly_series(hours)` applies a time window and returns the grouped signal rows.

`overview()` reads the latest row, compares it with the row 24 hours earlier, calculates the generated forecast variance and counts delayed runs.

`contributors(hours)` ranks segments by actual minus forecast.

`forecast_accuracy()` returns the full participant and workload comparison.

`service_runs(hours)` returns the scheduled run table.

`scenario(...)` calculates the conditional queue model using Python because the controls are inputs rather than stored facts.

## SQL concepts to know

1. `SUM` adds facts.
2. `AVG` gives an average, here used for latency.
3. `GROUP BY` defines the reporting grain.
4. `ORDER BY` ranks or sorts results.
5. `CASE WHEN` creates conditional totals.
6. `NULLIF` prevents division by zero.
7. A time window limits the evidence used for a page.

## What SQL does not decide

SQL does not decide whether a signal is a root cause, whether a threshold is appropriate, or whether a customer action is allowed. It produces a reproducible summary for the analyst to interpret.

