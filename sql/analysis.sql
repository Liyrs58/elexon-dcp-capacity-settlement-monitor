-- All inputs in these tables are generated demonstration data.

-- Hourly arrivals, completed work, queue, latency and retry/failure counts.
SELECT
    timestamp,
    SUM(submissions_received) AS arrivals,
    SUM(submissions_processed) AS processed,
    SUM(backlog_size) AS queue_size,
    ROUND(AVG(processing_latency_minutes), 1) AS average_latency_minutes,
    SUM(validation_failure_count) AS validation_failures,
    SUM(retry_count) AS retries,
    SUM(net_queue_growth) AS net_queue_growth,
    SUM(CASE WHEN settlement_critical_indicator = 1 THEN submissions_processed ELSE 0 END) AS critical_processed,
    SUM(CASE WHEN settlement_critical_indicator = 1 THEN submissions_received ELSE 0 END) AS critical_received,
    ROUND(100.0 * SUM(validation_failure_count) / NULLIF(SUM(submissions_received), 0), 2) AS failure_rate_percent,
    ROUND(100.0 * SUM(retry_count) / NULLIF(SUM(submissions_received), 0), 2) AS retry_rate_percent
FROM registration_metrics
GROUP BY timestamp
ORDER BY timestamp;

-- Segment forecast variance and generated queue contribution.
SELECT
    participant_id,
    participant_type,
    submission_type,
    SUM(actual_submissions) AS actual,
    SUM(forecast_submissions) AS forecast,
    SUM(actual_submissions - forecast_submissions) AS absolute_variance,
    ROUND(100.0 * (SUM(actual_submissions) - SUM(forecast_submissions))
          / NULLIF(SUM(forecast_submissions), 0), 1) AS variance_percent,
    MAX(backlog_size) AS peak_segment_backlog,
    SUM(retry_count) AS retries
FROM registration_metrics
GROUP BY participant_id, participant_type, submission_type
ORDER BY absolute_variance DESC;

-- Scheduled synthetic Settlement/payment runs and delay flags.
SELECT
    timestamp,
    service_run_type,
    delay_minutes,
    deadline_minutes,
    status,
    downstream_settlement_risk_flag
FROM service_runs
ORDER BY timestamp;
