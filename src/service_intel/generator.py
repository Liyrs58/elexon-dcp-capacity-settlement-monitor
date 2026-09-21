"""Fixed-seed synthetic operating data. None of these values are Elexon telemetry."""

from __future__ import annotations

from datetime import datetime, timedelta
import math
import random


SEED = 20260914
HOURS = 14 * 24
START = datetime(2026, 1, 1)
DEMO_CAPACITY_PER_HOUR = 20
PARTICIPANTS = (
    ("SYN-VLP-01", "VLP"),
    ("SYN-VTP-01", "VTP"),
    ("SYN-AMVLP-01", "AMVLP"),
    ("SYN-VLP-02", "VLP"),
    ("SYN-VTP-02", "VTP"),
    ("SYN-SUP-01", "Supplier"),
)
WORKLOADS = ("new MSID Pair", "new AMSID Pair", "historic resubmission")
BASE_RATES = {
    "SYN-VLP-01": (2.4, 0.25, 0.30),
    "SYN-VTP-01": (0.9, 1.25, 0.35),
    "SYN-AMVLP-01": (0.20, 2.55, 0.40),
    "SYN-VLP-02": (1.35, 0.55, 0.30),
    "SYN-VTP-02": (0.55, 1.15, 0.45),
    "SYN-SUP-01": (0.25, 0.15, 0.95),
}
WORKLOAD_WEIGHTS = {
    "new MSID Pair": 1.20,
    "new AMSID Pair": 1.20,
    "historic resubmission": 0.55,
}


def _hour_factor(hour: int) -> float:
    if 9 <= hour <= 16:
        return 1.45
    if 6 <= hour <= 8 or 17 <= hour <= 20:
        return 0.95
    if 21 <= hour <= 22:
        return 0.70
    return 0.48


def _growth_factor(day: int) -> float:
    """A stepped illustrative demand ramp, not a model of real market growth."""
    if day < 4:
        return 0.90
    if day < 8:
        return 1.05
    if day < 11:
        return 1.45
    return 1.90


def _count(rng: random.Random, mean: float) -> int:
    # A compact, seeded approximation to a count distribution using only stdlib.
    return max(0, int(round(rng.gauss(mean, max(0.65, math.sqrt(mean) * 0.42)))))


def _allocate(work: list[dict], capacity: int, rotation: int = 0) -> list[int]:
    """Allocate budget by remaining queue × workload weight, rotating ties."""
    remaining = min(capacity, sum(item["work"] for item in work))
    result = [0] * len(work)
    while remaining > 0:
        active = [i for i, item in enumerate(work) if result[i] < item["work"]]
        if not active:
            break
        scores = {i: (work[i]["work"] - result[i]) * work[i]["weight"] for i in active}
        total_score = sum(scores.values())
        if total_score <= 0:
            break
        quotas = {i: remaining * scores[i] / total_score for i in active}
        allocated = 0
        for i in active:
            take = min(work[i]["work"] - result[i], int(quotas[i]))
            result[i] += take
            allocated += take
        remaining -= allocated
        if remaining <= 0:
            break
        active = [i for i in active if result[i] < work[i]["work"]]
        if not active:
            break
        fractional = sorted(
            active,
            key=lambda i: (-(quotas[i] - int(quotas[i])), (i - rotation) % len(work)),
        )
        # Largest-remainder assignment handles the final indivisible items.
        for i in fractional:
            if remaining <= 0:
                break
            result[i] += 1
            remaining -= 1
    return result


def generate_demo_data(
    seed: int = SEED,
    hours: int = HOURS,
    start: datetime = START,
) -> tuple[list[dict], list[dict]]:
    """Return registration metrics and synthetic scheduled-run records."""
    rng = random.Random(seed)
    queues = {(pid, workload): 0 for pid, _ in PARTICIPANTS for workload in WORKLOADS}
    registration_rows: list[dict] = []
    service_runs: list[dict] = []

    for tick in range(hours):
        at = start + timedelta(hours=tick)
        day = tick // 24
        growth = _growth_factor(day)
        specs: list[dict] = []
        for participant_id, participant_type in PARTICIPANTS:
            for idx, workload in enumerate(WORKLOADS):
                baseline = BASE_RATES[participant_id][idx]
                actual_mean = baseline * _hour_factor(at.hour) * growth
                forecast_mean = baseline * _hour_factor(at.hour) * 1.02
                received = _count(rng, actual_mean)
                forecast = _count(rng, forecast_mean)
                key = (participant_id, workload)
                before = queues[key]
                specs.append({
                    "participant_id": participant_id,
                    "participant_type": participant_type,
                    "submission_type": workload,
                    "key": key,
                    "before": before,
                    "received": received,
                    "forecast": forecast,
                    "work": before + received,
                    "weight": WORKLOAD_WEIGHTS[workload],
                })

        processed = _allocate(specs, DEMO_CAPACITY_PER_HOUR, rotation=tick)
        total_queue_before = sum(item["before"] for item in specs)
        backlog_values: list[int] = []
        latency_values: list[float] = []
        for item, processed_count in zip(specs, processed):
            backlog = max(0, item["work"] - processed_count)
            queues[item["key"]] = backlog
            backlog_values.append(backlog)
            latency_noise = rng.uniform(-2.0, 2.0)
            latency_values.append(max(2.0, round(7.0 + total_queue_before * 0.075 + latency_noise, 1)))

        total_queue_after = sum(backlog_values)
        for item, processed_count, backlog, latency in zip(specs, processed, backlog_values, latency_values):
            failures = sum(1 for _ in range(item["received"]) if rng.random() < 0.025)
            retries = failures + sum(1 for _ in range(item["received"]) if rng.random() < 0.018)
            risk_flag = int(total_queue_after >= 450 or latency >= 75)
            registration_rows.append({
                "timestamp": at.isoformat(timespec="minutes"),
                "participant_id": item["participant_id"],
                "participant_type": item["participant_type"],
                "submission_type": item["submission_type"],
                "submissions_received": item["received"],
                "submissions_processed": processed_count,
                "backlog_size": backlog,
                "processing_latency_minutes": latency,
                "validation_failure_count": failures,
                "retry_count": retries,
                "service_run_type": "registration",
                "forecast_submissions": item["forecast"],
                "actual_submissions": item["received"],
                "service_level_deadline_minutes": 120,
                "downstream_settlement_risk_flag": risk_flag,
                "demo_capacity_per_hour": DEMO_CAPACITY_PER_HOUR,
                "priority_class": "standard" if item["submission_type"] == "historic resubmission" else "priority",
                "settlement_critical_indicator": int(item["submission_type"] != "historic resubmission"),
                "payment_critical_indicator": int(item["submission_type"] == "new MSID Pair"),
                "net_queue_growth": backlog - item["before"],
                "forecast_error_pct": round(((item["received"] - item["forecast"]) / item["forecast"] * 100) if item["forecast"] else 0.0, 2),
                "risk_state": "Critical" if total_queue_after >= 900 else ("At risk" if total_queue_after >= 550 or latency >= 75 else ("Elevated" if total_queue_after >= 180 or latency >= 35 else "Normal")),
            })

        # A separate synthetic scheduled-run table keeps Settlement/payment events
        # distinct from participant registration workload records.
        if at.hour in (7, 13):
            run_type = "Settlement-critical" if at.hour == 7 else "payment-critical"
            delay = max(0, int(round((total_queue_after - 120) * 0.18 + rng.uniform(-3, 5))))
            deadline = 60 if at.hour == 7 else 45
            service_runs.append({
                "timestamp": at.isoformat(timespec="minutes"),
                "service_run_type": run_type,
                "scheduled_at": at.isoformat(timespec="minutes"),
                "delay_minutes": delay,
                "deadline_minutes": deadline,
                "status": "Delayed" if delay > deadline else "On time",
                "downstream_settlement_risk_flag": int(delay > deadline),
                "demo_queue_at_schedule": total_queue_after,
            })

    return registration_rows, service_runs
