# Metric defence guide

Use this guide when an interviewer asks “What does that number mean?” Every number shown by the dashboard is either calculated from the generated sample or is a clearly stated public fact.

## Rules for defending a metric

1. State the unit and the time window.
2. State the numerator and denominator when there is one.
3. Say whether the value is public, synthetic, descriptive or conditional.
4. Explain why the measure helps the service question.
5. State what it cannot prove.

## Core measures

### Arrivals

Definition: the sum of `submissions_received` in an interval.

Unit: submissions per hour in the hourly charts.

Source: `src/service_intel/store.py`, `sql/analysis.sql` and the generated registration file.

Why it matters: it shows incoming work that the service must handle.

Limit: the values are synthetic. They do not measure Elexon demand.

Small example: if three workloads receive 10, 6 and 4 submissions in one hour, arrivals equal 20.

### Processed work, or throughput

Definition: the sum of `submissions_processed` in an interval.

Unit: submissions per hour.

Why it matters: comparing throughput with arrivals shows whether the open queue can recover.

Limit: a generated processing budget is not a measured DCP capacity.

Example: 20 arrivals and 15 processed submissions produce five additional open records before any other change.

### Backlog

Definition: generated work not yet completed for a participant and workload at the end of an interval.

Queue equation: previous backlog plus received submissions minus processed submissions.

Unit: open submissions.

Why it matters: it gives a direct view of accumulated work.

Limit: no real customer request or Elexon queue is represented.

Example: a queue of 100 receives 20 and completes 15, so the next queue is 105.

### Net queue growth

Definition: arrivals minus processed work for the interval.

Unit: submissions per interval, or per hour in the scenario page.

Why it matters: a positive value means the queue is growing under the sample definitions.

Limit: it is not a root cause. It also depends on the chosen arrival and completion definitions.

### Processing latency

Definition: generated minutes associated with processing a segment in an interval.

Unit: minutes.

Why it matters: a rising queue can be accompanied by slower completion, which helps decide whether to inspect service performance and deadlines together.

Limit: the generator uses an illustrative pressure relationship and noise. It is not DCP telemetry.

### Validation failure rate

Definition: validation failures divided by received submissions, multiplied by 100.

Unit: percent.

Why it matters: rejected or failed work can create rework and explain part of a pressure pattern.

Limit: a low rate does not prove the service is healthy and a high rate does not identify why records failed.

### Retry rate

Definition: retries divided by received submissions, multiplied by 100.

Unit: percent.

Why it matters: retries can add work and may point to a quality or interface question.

Limit: generated retries do not identify a public technical fault.

### Forecast variance

Definition: `(actual submissions minus forecast submissions) divided by forecast submissions` when forecast is positive.

Unit: relative percentage.

Why it matters: it shows where observed demand in the sample differs from the submitted expectation.

Limit: it does not prove a poor forecasting process caused an incident. The sample forecast and actuals are generated together.

Example: actual 120 and forecast 100 gives `(120 minus 100) / 100 = 0.20`, or plus 20 percent.

### Delayed scheduled run

Definition: a generated run where `delay_minutes` is greater than `deadline_minutes`.

Unit: count of runs in the selected window.

Why it matters: the public Circular makes Settlement and payment timing part of the operational question.

Limit: the run records in the dashboard are synthetic and do not measure Elexon performance.

### Risk state

Definition: a deterministic label from the generated backlog, latency, forecast variance and delayed run values.

Levels: Normal, Elevated, At risk and Critical.

Why it matters: it makes the sample state easy to scan.

Limit: the thresholds in `config/demo_thresholds.json` are invented demo references. They are not BSC limits, Elexon limits or service level commitments.

### Time to demo alert

Definition: `(threshold minus current backlog) divided by net queue growth` when the queue is below the threshold and growing.

Unit: hours.

Why it matters: it shows how a simple queue balance can support early warning.

Limit: it assumes a constant rate and is not a production forecast. It returns no value when the queue is already at the threshold or is not growing.

Example: a queue of 100, a threshold of 300 and growth of 10 per hour gives 20 hours.

## Scenario measures

### Projected arrivals per hour

Definition: new pair arrivals multiplied by the demand multiplier, plus historic arrivals after any throttle.

Limit: it assumes steady rates and does not predict downstream run behaviour.

### Registration capacity after reserve

Definition: demo capacity multiplied by one minus the reserved capacity fraction.

Limit: reserved capacity is a scenario assumption, not a claim that Elexon has or should use a specific architecture.

### Projected backlog

Definition: starting backlog plus net hourly growth multiplied by the selected horizon, bounded at zero.

Limit: no seasonality, recovery surge, dependency delay or unknown constraint is modelled.

## Public context measures

The date of the Circular, the description of DCP as a supporting service used in Settlement, delayed scheduled Settlement and payment runs, increased MSID and AMSID Pair submissions, demand above submitted forecasts, and DCP operating at or near maximum capacity are public statements. They are sourced in `docs/evidence-register.md`. They are not calculated by the dashboard.

