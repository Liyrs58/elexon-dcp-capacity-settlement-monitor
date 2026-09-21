"""Validation controls for the synthetic service dataset."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
import math

from service_intel.generator import PARTICIPANTS, WORKLOADS, generate_demo_data


REQUIRED_COLUMNS = {
    "timestamp", "participant_id", "participant_type", "submission_type",
    "submissions_received", "submissions_processed", "backlog_size",
    "processing_latency_minutes", "validation_failure_count", "retry_count",
    "forecast_submissions", "actual_submissions", "service_level_deadline_minutes",
    "downstream_settlement_risk_flag", "demo_capacity_per_hour", "priority_class",
    "settlement_critical_indicator", "payment_critical_indicator", "net_queue_growth",
    "forecast_error_pct", "risk_state",
}
ALLOWED_PARTICIPANT_TYPES = {p_type for _, p_type in PARTICIPANTS}
ALLOWED_WORKLOADS = set(WORKLOADS)
ALLOWED_PRIORITY_CLASSES = {"priority", "standard"}
ALLOWED_RISK_STATES = {"Normal", "Elevated", "At risk", "Critical"}
NUMERIC_COLUMNS = {
    "submissions_received", "submissions_processed", "backlog_size",
    "processing_latency_minutes", "validation_failure_count", "retry_count",
    "forecast_submissions", "actual_submissions", "service_level_deadline_minutes",
    "downstream_settlement_risk_flag", "demo_capacity_per_hour", "settlement_critical_indicator",
    "payment_critical_indicator", "net_queue_growth", "forecast_error_pct",
}
NON_NEGATIVE_COLUMNS = NUMERIC_COLUMNS.difference({"net_queue_growth", "forecast_error_pct"})


def _digest(rows: list[dict]) -> str:
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf8")).hexdigest()


def validate_registration_rows(rows: list[dict]) -> dict:
    """Run blocking controls before analytical calculations are published."""
    errors: list[str] = []
    warnings: list[str] = []
    if not rows:
        errors.append("No registration rows were supplied")
        return {"status": "BLOCKED", "errors": errors, "warnings": warnings, "row_count": 0}

    missing = sorted(REQUIRED_COLUMNS.difference(rows[0]))
    if missing:
        errors.append("Missing required columns: " + ", ".join(missing))

    ordered = sorted(rows, key=lambda row: (row.get("participant_id", ""), row.get("submission_type", ""), row.get("timestamp", "")))
    previous: dict[tuple[str, str], tuple[str, int]] = {}
    seen: set[tuple] = set()
    for index, row in enumerate(rows):
        key = (row.get("participant_id"), row.get("submission_type"))
        identity = (row.get("timestamp"),) + key
        if identity in seen:
            errors.append(f"Duplicate row at position {index}")
        seen.add(identity)
        try:
            datetime.fromisoformat(str(row.get("timestamp")))
        except (TypeError, ValueError):
            errors.append(f"Invalid timestamp at position {index}")
        if row.get("participant_type") not in ALLOWED_PARTICIPANT_TYPES:
            errors.append(f"Invalid participant type at position {index}")
        if row.get("submission_type") not in ALLOWED_WORKLOADS:
            errors.append(f"Invalid submission type at position {index}")
        if row.get("priority_class") not in ALLOWED_PRIORITY_CLASSES:
            errors.append(f"Invalid priority class at position {index}")
        if row.get("risk_state") not in ALLOWED_RISK_STATES:
            errors.append(f"Invalid risk state at position {index}")
        for column in NUMERIC_COLUMNS:
            value = row.get(column)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"Non numeric value in {column} at position {index}")
                continue
            if isinstance(value, float) and not math.isfinite(value):
                errors.append(f"Non finite value in {column} at position {index}")
            elif column in NON_NEGATIVE_COLUMNS and value < 0:
                errors.append(f"Negative value in {column} at position {index}")
        if row.get("actual_submissions") != row.get("submissions_received"):
            errors.append(f"Actual and received counts disagree at position {index}")

    for row in ordered:
        key = (row["participant_id"], row["submission_type"])
        before = previous.get(key)
        if before is not None:
            expected = before[1] + row["submissions_received"] - row["submissions_processed"]
            if expected != row["backlog_size"]:
                errors.append(
                    f"Backlog reconciliation failed for {key} at {row['timestamp']}: expected {expected}, got {row['backlog_size']}"
                )
            if row["timestamp"] <= before[0]:
                errors.append(f"Timestamp order failed for {key} at {row['timestamp']}")
        previous[key] = (row["timestamp"], row["backlog_size"])

    first_forecast = sum(row["forecast_submissions"] for row in rows)
    if first_forecast <= 0:
        errors.append("Forecast coverage is empty")

    regenerated, _ = generate_demo_data(hours=max(1, len(rows) // (len(PARTICIPANTS) * len(WORKLOADS))))
    if _digest(rows) != _digest(regenerated):
        errors.append("Fixed seed regeneration did not reproduce the supplied rows")

    return {
        "status": "BLOCKED" if errors else "PASS",
        "errors": errors[:20],
        "warnings": warnings[:20],
        "error_count": len(errors),
        "warning_count": len(warnings),
        "row_count": len(rows),
        "checks": [
            "schema and required fields", "types and finite non negative values",
            "categories and timestamps", "duplicate identity", "forecast coverage",
            "actual equals received", "segment backlog reconciliation", "fixed seed regeneration",
        ],
    }
