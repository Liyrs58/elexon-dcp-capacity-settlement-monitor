# Methodology

## Evidence boundary

The public Circular EL04799 is the starting point. It says that DCP was under capacity pressure, registration demand was above submitted forecasts, and scheduled Settlement and payment runs were late. It does not disclose the internal technical cause. Every operational value in this project is synthetic.

## Analytical flow

The workflow follows eleven steps.

1. Define the service and customer question.
2. Validate the generated data before analysis.
3. Compare arrivals with completed work.
4. Measure queue growth, latency, failures and retries.
5. Compare generated actual demand with generated forecasts.
6. Segment by participant type and workload.
7. Test explicit hypotheses.
8. Quantify a conditional scenario.
9. Describe possible customer and Settlement impact.
10. Record evidence gaps and ownership.
11. Capture a proportionate improvement idea.

The model is intentionally transparent. It uses arithmetic, grouped SQL queries, deterministic thresholds and scenario sensitivity. It does not use machine learning because the public source does not contain enough operational history to train or validate a useful model.

## Queue calculation

For each participant and workload, the generated backlog follows this equation:

`closing backlog = opening backlog + received submissions minus processed submissions`

Scenario projection uses:

`projected backlog = current backlog + projected arrivals minus available capacity multiplied by hours`

The result is a conditional demonstration. It is not a forecast of Elexon operations.

## Hypotheses

The hypothesis page reports a result, conclusion, confidence, limitation and next check for each question. A result can reject a hypothesis or leave it open. A pattern in the generated sample cannot establish a real Elexon cause.

## Validation

The generator checks required fields, types, non negative values, allowed categories, duplicate identities, timestamp order, forecast coverage, actual versus received counts, queue reconciliation and fixed seed regeneration. A failure blocks publication when the files are rebuilt.

## SQL and Python

SQLite provides the query layer. Python provides generation, validation, scenario logic and narrative assembly. Important calculations are kept simple enough to compare independently. SQL examples are in `sql/analysis.sql`. Power BI compatible CSV exports are created in `data/powerbi_export/`.
