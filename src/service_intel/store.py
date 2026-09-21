"""SQLite persistence and small query layer for the synthetic dataset."""

from __future__ import annotations

import csv
from pathlib import Path
import sqlite3
import json

from service_intel.analysis import alert_state, estimate_hours_to_threshold, forecast_variance, load_demo_thresholds
from service_intel.generator import PARTICIPANTS, WORKLOADS, generate_demo_data
from service_intel.hypotheses import run_hypotheses
from service_intel.validation import validate_registration_rows


SCHEMA = """
CREATE TABLE IF NOT EXISTS registration_metrics (
    timestamp TEXT NOT NULL,
    participant_id TEXT NOT NULL,
    participant_type TEXT NOT NULL,
    submission_type TEXT NOT NULL,
    submissions_received INTEGER NOT NULL,
    submissions_processed INTEGER NOT NULL,
    backlog_size INTEGER NOT NULL,
    processing_latency_minutes REAL NOT NULL,
    validation_failure_count INTEGER NOT NULL,
    retry_count INTEGER NOT NULL,
    service_run_type TEXT NOT NULL,
    forecast_submissions INTEGER NOT NULL,
    actual_submissions INTEGER NOT NULL,
    service_level_deadline_minutes INTEGER NOT NULL,
    downstream_settlement_risk_flag INTEGER NOT NULL,
    demo_capacity_per_hour INTEGER NOT NULL,
    priority_class TEXT NOT NULL,
    settlement_critical_indicator INTEGER NOT NULL,
    payment_critical_indicator INTEGER NOT NULL,
    net_queue_growth INTEGER NOT NULL,
    forecast_error_pct REAL NOT NULL,
    risk_state TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_registration_timestamp ON registration_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_registration_segment ON registration_metrics(participant_type, submission_type);
CREATE TABLE IF NOT EXISTS service_runs (
    timestamp TEXT NOT NULL,
    service_run_type TEXT NOT NULL,
    scheduled_at TEXT NOT NULL,
    delay_minutes INTEGER NOT NULL,
    deadline_minutes INTEGER NOT NULL,
    status TEXT NOT NULL,
    downstream_settlement_risk_flag INTEGER NOT NULL,
    demo_queue_at_schedule INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_run_timestamp ON service_runs(timestamp);
"""

DATA_DICTIONARY = {
    "timestamp": "Synthetic hourly interval in ISO format",
    "participant_id": "Synthetic participant identifier beginning SYN",
    "participant_type": "Synthetic VLP, VTP, AMVLP or Supplier category",
    "submission_type": "Synthetic registration workload category",
    "submissions_received": "Generated arrivals in the interval",
    "submissions_processed": "Generated completed records in the interval",
    "backlog_size": "Generated open queue after processing",
    "processing_latency_minutes": "Generated service latency indicator",
    "validation_failure_count": "Generated validation failures",
    "retry_count": "Generated retries",
    "forecast_submissions": "Generated submitted forecast",
    "actual_submissions": "Generated actual arrivals",
    "service_level_deadline_minutes": "Synthetic deadline for the demonstration",
    "downstream_settlement_risk_flag": "Generated risk flag",
    "demo_capacity_per_hour": "Synthetic processing budget",
    "priority_class": "Synthetic priority label for scenario analysis",
    "settlement_critical_indicator": "Synthetic indicator for critical registration work",
    "payment_critical_indicator": "Synthetic indicator for payment related work",
    "net_queue_growth": "Closing backlog minus opening backlog",
    "forecast_error_pct": "Generated actual minus forecast as a percentage",
    "risk_state": "Generated row level state using demonstration thresholds",
}


def _connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def prepare_demo_files(data_dir: Path, force: bool = False) -> Path:
    """Write reproducible CSVs and a SQLite database from the fixed-seed generator."""
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "synthetic_service_metrics.sqlite"
    metrics_path = data_dir / "synthetic_registration_metrics.csv"
    runs_path = data_dir / "synthetic_service_runs.csv"
    export_check = data_dir / "powerbi_export" / "validation_report.json"
    if db_path.exists() and metrics_path.exists() and runs_path.exists() and export_check.exists() and not force:
        return db_path

    metrics, runs = generate_demo_data()
    validation = validate_registration_rows(metrics)
    if validation["status"] != "PASS":
        raise ValueError("Synthetic data validation blocked publication: " + "; ".join(validation["errors"]))
    with metrics_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics[0]))
        writer.writeheader()
        writer.writerows(metrics)
    with runs_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(runs[0]))
        writer.writeheader()
        writer.writerows(runs)

    if db_path.exists():
        db_path.unlink()
    con = _connect(db_path)
    try:
        con.executescript(SCHEMA)
        con.executemany(
            """INSERT INTO registration_metrics VALUES (
                :timestamp,:participant_id,:participant_type,:submission_type,
                :submissions_received,:submissions_processed,:backlog_size,
                :processing_latency_minutes,:validation_failure_count,:retry_count,
                :service_run_type,:forecast_submissions,:actual_submissions,
                :service_level_deadline_minutes,:downstream_settlement_risk_flag,
                :demo_capacity_per_hour,:priority_class,:settlement_critical_indicator,
                :payment_critical_indicator,:net_queue_growth,:forecast_error_pct,:risk_state
            )""",
            metrics,
        )
        con.executemany(
            """INSERT INTO service_runs VALUES (
                :timestamp,:service_run_type,:scheduled_at,:delay_minutes,
                :deadline_minutes,:status,:downstream_settlement_risk_flag,
                :demo_queue_at_schedule
            )""",
            runs,
        )
        con.commit()
    finally:
        con.close()
    powerbi_dir = data_dir / "powerbi_export"
    powerbi_dir.mkdir(exist_ok=True)
    dimensions = {
        "dim_participant.csv": ("participant_id,participant_type\n" + "\n".join(f"{pid},{ptype}" for pid, ptype in sorted(PARTICIPANTS)) + "\n"),
        "dim_submission_type.csv": ("submission_type\n" + "\n".join(WORKLOADS) + "\n"),
        "validation_report.json": json.dumps(validation, indent=2),
        "data_dictionary.json": json.dumps(DATA_DICTIONARY, indent=2),
    }
    for name, content in dimensions.items():
        (powerbi_dir / name).write_text(content, encoding="utf8")
    with (powerbi_dir / "fact_service_interval.csv").open("w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics[0]))
        writer.writeheader()
        writer.writerows(metrics)
    with (powerbi_dir / "fact_service_runs.csv").open("w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=list(runs[0]))
        writer.writeheader()
        writer.writerows(runs)
    return db_path


class DemoStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.thresholds = load_demo_thresholds()

    def _query(self, sql: str, params: tuple = ()) -> list[dict]:
        con = _connect(self.db_path)
        try:
            return [dict(row) for row in con.execute(sql, params).fetchall()]
        finally:
            con.close()

    def hourly_series(self, hours: int = 168) -> list[dict]:
        return self._query(
            """WITH cutoff AS (SELECT datetime(MAX(timestamp), ?) AS t FROM registration_metrics)
            SELECT timestamp,
                   SUM(submissions_received) AS received,
                   SUM(submissions_processed) AS processed,
                   SUM(backlog_size) AS backlog,
                   ROUND(AVG(processing_latency_minutes), 1) AS latency,
                   SUM(validation_failure_count) AS failures,
                   SUM(retry_count) AS retries,
                   ROUND(100.0 * SUM(validation_failure_count) / NULLIF(SUM(submissions_received), 0), 2) AS failure_rate_pct,
                   ROUND(100.0 * SUM(retry_count) / NULLIF(SUM(submissions_received), 0), 2) AS retry_rate_pct,
                   SUM(forecast_submissions) AS forecast
            FROM registration_metrics, cutoff
            WHERE datetime(registration_metrics.timestamp) > cutoff.t
            GROUP BY timestamp ORDER BY timestamp""",
            (f"-{hours} hours",),
        )

    def latest_metrics(self) -> dict:
        row = self._query(
            """SELECT timestamp, SUM(submissions_received) AS received,
                      SUM(submissions_processed) AS processed,
                      SUM(backlog_size) AS backlog,
                      ROUND(AVG(processing_latency_minutes), 1) AS latency,
                      SUM(validation_failure_count) AS failures,
                      SUM(retry_count) AS retries,
                      SUM(forecast_submissions) AS forecast,
                      MAX(demo_capacity_per_hour) AS capacity
               FROM registration_metrics WHERE timestamp=(SELECT MAX(timestamp) FROM registration_metrics)
               GROUP BY timestamp"""
        )[0]
        return row

    def overview(self) -> dict:
        latest = self.latest_metrics()
        series = self.hourly_series(48)
        previous = series[-25] if len(series) >= 25 else (series[0] if series else latest)
        growth = latest["backlog"] - previous["backlog"]
        recent = self._query(
            """SELECT SUM(actual_submissions) AS actual, SUM(forecast_submissions) AS forecast,
                      SUM(submissions_received) AS received, SUM(submissions_processed) AS processed,
                      SUM(validation_failure_count) AS failures, SUM(retry_count) AS retries
               FROM registration_metrics
               WHERE datetime(timestamp) > datetime((SELECT MAX(timestamp) FROM registration_metrics), '-24 hours')"""
        )[0]
        run_count = self._query(
            """SELECT SUM(CASE WHEN status='Delayed' THEN 1 ELSE 0 END) AS delayed,
                      COUNT(*) AS total, AVG(delay_minutes) AS average_delay
               FROM service_runs
               WHERE datetime(timestamp) > datetime((SELECT MAX(timestamp) FROM service_runs), '-24 hours')"""
        )[0]
        variance = forecast_variance(recent["actual"] or 0, recent["forecast"] or 0)
        state = alert_state(latest["backlog"], latest["latency"], variance, run_count["delayed"] or 0, self.thresholds)
        arrival_per_hour = (recent["received"] or 0) / 24
        processed_per_hour = (recent["processed"] or 0) / 24
        time_to_critical = estimate_hours_to_threshold(latest["backlog"], self.thresholds.critical_backlog, arrival_per_hour, processed_per_hour)
        failure_rate = (recent["failures"] or 0) / max(1, recent["received"] or 0)
        retry_rate = (recent["retries"] or 0) / max(1, recent["received"] or 0)
        return {
            **latest,
            "state": state,
            "backlog_change_24h": growth,
            "forecast_variance_24h": variance,
            "arrivals_per_hour_24h": round(arrival_per_hour, 2),
            "processed_per_hour_24h": round(processed_per_hour, 2),
            "failure_rate_24h": round(failure_rate, 4),
            "retry_rate_24h": round(retry_rate, 4),
            "delayed_runs_24h": run_count["delayed"] or 0,
            "total_runs_24h": run_count["total"] or 0,
            "average_run_delay_24h": round(run_count["average_delay"] or 0, 1),
            "hours_to_critical_backlog": round(time_to_critical, 1) if time_to_critical is not None else None,
            "demo_thresholds": self.thresholds.__dict__,
        }

    def contributors(self, hours: int = 168) -> list[dict]:
        rows = self._query(
            """WITH cutoff AS (SELECT datetime(MAX(timestamp), ?) AS t FROM registration_metrics)
            SELECT participant_id, participant_type, submission_type,
                   SUM(actual_submissions) AS actual,
                   SUM(forecast_submissions) AS forecast,
                   SUM(submissions_processed) AS processed,
                   MAX(backlog_size) AS peak_segment_backlog,
                   SUM(validation_failure_count) AS failures,
                   SUM(retry_count) AS retries
            FROM registration_metrics, cutoff
            WHERE datetime(registration_metrics.timestamp) > cutoff.t
            GROUP BY participant_id, participant_type, submission_type""",
            (f"-{hours} hours",),
        )
        for row in rows:
            row["variance"] = forecast_variance(row["actual"], row["forecast"])
        return sorted(rows, key=lambda r: (r["actual"] - r["forecast"], r["actual"]), reverse=True)

    def forecast_accuracy(self) -> list[dict]:
        rows = self._query(
            """SELECT participant_id, participant_type, submission_type,
                      SUM(actual_submissions) AS actual,
                      SUM(forecast_submissions) AS forecast,
                      SUM(submissions_received - submissions_processed) AS net_work_added,
                      MAX(backlog_size) AS peak_segment_backlog
               FROM registration_metrics
               GROUP BY participant_id, participant_type, submission_type"""
        )
        for row in rows:
            row["variance"] = forecast_variance(row["actual"], row["forecast"])
            row["variance_pct"] = row["variance"] * 100 if row["variance"] is not None else None
        return sorted(rows, key=lambda r: (r["variance"] or 0), reverse=True)

    def service_runs(self, hours: int = 168) -> list[dict]:
        return self._query(
            """WITH cutoff AS (SELECT datetime(MAX(timestamp), ?) AS t FROM service_runs)
               SELECT * FROM service_runs, cutoff
               WHERE datetime(service_runs.timestamp) > cutoff.t
               ORDER BY timestamp""",
            (f"-{hours} hours",),
        )

    def scenario_inputs(self) -> dict:
        rows = self._query(
            """SELECT submission_type, SUM(submissions_received) AS received
               FROM registration_metrics
               WHERE datetime(timestamp) >= datetime((SELECT MAX(timestamp) FROM registration_metrics), '-72 hours')
               GROUP BY submission_type"""
        )
        means = {r["submission_type"]: (r["received"] or 0) / 72 for r in rows}
        latest = self.latest_metrics()
        return {
            "current_backlog": latest["backlog"],
            "capacity_per_hour": latest["capacity"],
            "new_pair_arrivals_per_hour": means.get("new MSID Pair", 0) + means.get("new AMSID Pair", 0),
            "historic_arrivals_per_hour": means.get("historic resubmission", 0),
        }

    def validation(self) -> dict:
        rows, runs = generate_demo_data()
        return validate_registration_rows(rows) | {"run_row_count": len(runs)}

    def hypotheses(self) -> list[dict]:
        rows, runs = generate_demo_data()
        return run_hypotheses(rows, runs)

    def operational_context(self) -> dict:
        return {
            "service": "Elexon Settlement and Insight service context",
            "analyst_role": "Validate evidence, monitor risk, investigate, coordinate and communicate.",
            "elexon": "Administers the BSC and the Settlement arrangements.",
            "neso": "Balances physical electricity supply and demand in real time.",
            "customer": "BSC Parties and affected service users whose submissions or Settlement outcomes may be impacted.",
            "service_owner": "Authorised Elexon owner who decides operational action after reviewing evidence.",
            "vendor": "Relevant BSC Agent or service provider asked for throughput, failures, latency, dependencies and recovery evidence.",
            "analyst_boundary": "The analyst prepares evidence and recommendations. The analyst does not authorise payment delays or claim a private root cause.",
        }

    def customer_impact(self) -> dict:
        overview = self.overview()
        state = overview["state"]
        return {
            "state": state,
            "who_may_be_affected": "Participants submitting registration data and teams relying on scheduled Settlement or payment activity.",
            "potential_settlement_impact": "A delayed supporting service may delay a downstream run. The sample does not quantify a real impact.",
            "potential_payment_impact": "A payment critical run may need confirmation if its deadline is missed.",
            "customer_action": "Confirm whether new submissions or historic resubmissions are subject to an active instruction from the authorised owner.",
            "uncertainty": "The sample contains no real customer identifiers, private queue data or internal service objectives.",
            "next_owner": "Service owner with Settlement operations and relevant service provider input.",
            "next_update": "Agree a next update time with the incident lead before communicating externally.",
        }

    def improvements(self) -> list[dict]:
        return [
            {"id": "IMP01", "problem": "Forecasts can become stale as flexible asset demand changes.", "action": "Use rolling participant forecasts with base, expected and high cases.", "benefit": "Earlier warning of demand pressure.", "risk": "Forecast administration and inconsistent submissions.", "owner": "Service owner and participant relationship team.", "measure": "Forecast error and warning lead time.", "status": "Candidate"},
            {"id": "IMP02", "problem": "A rising queue may be noticed after a critical run is already late.", "action": "Monitor arrivals, completions, queue age and latency together.", "benefit": "Faster controlled escalation.", "risk": "False alerts without agreed definitions.", "owner": "Operations and service provider.", "measure": "Alert precision and time to acknowledgement.", "status": "Candidate"},
            {"id": "IMP03", "problem": "Non critical historic resubmissions may compete with urgent work during a constrained period.", "action": "Assess controlled scheduling or throttling with customer and rule checks.", "benefit": "More capacity for critical workloads if feasible.", "risk": "Customer obligations and queue ageing.", "owner": "Authorised service owner.", "measure": "Critical completion and recovery time.", "status": "Hypothesis"},
            {"id": "IMP04", "problem": "Incident knowledge can be lost between shifts.", "action": "Use a structured incident note and review log.", "benefit": "Clearer handover and repeatable learning.", "risk": "Documentation becomes stale.", "owner": "Service analyst and incident lead.", "measure": "Completeness of handover fields.", "status": "Candidate"},
        ]
