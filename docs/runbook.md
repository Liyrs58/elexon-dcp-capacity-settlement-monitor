# Analyst runbook

## Trigger

Start an investigation when arrivals exceed processing for a sustained period, backlog grows, latency rises, quality signals worsen, or a critical scheduled run is late.

## Validate

Check data freshness, required fields, duplicates, category values, timestamp order and backlog reconciliation. If a blocking check fails, mark the analysis invalid and notify the owner.

## Investigate

Compare arrivals with completions. Segment by participant type, workload and interval. Check forecasts, failures, retries and queue age. Record what changed before the signal appeared.

## Assess impact

Identify affected workload, Settlement or payment deadlines, customer groups and actions that may be required. Separate confirmed impact from possible impact.

## Engage

Ask the service owner and relevant service provider for throughput, backlog, failed jobs, retry behaviour, latency, dependencies, change history and recovery estimate. Do not infer an internal cause from a chart.

## Mitigate

Consider only authorised options. Examples include prioritising critical work, scheduling non critical resubmissions, improving demand forecasts or increasing capacity where evidence supports it.

## Communicate

State the time window, source, confirmed facts, uncertainty, customer action, owner and next update time. Use plain language.

## Monitor and close

Measure recovery against agreed objectives. Record the decision, evidence, customer communication and lessons. Update the runbook when a control changes.
