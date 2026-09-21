"""Transparent calculations and demo alert logic."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class DemoThresholds:
    """Illustrative thresholds only; they are not Elexon limits or SLAs."""

    elevated_backlog: int = 180
    at_risk_backlog: int = 550
    critical_backlog: int = 900
    elevated_latency_minutes: float = 35
    at_risk_latency_minutes: float = 75
    critical_latency_minutes: float = 120
    elevated_forecast_variance: float = 0.20


def load_demo_thresholds(path: str | Path | None = None) -> DemoThresholds:
    """Load editable demonstration thresholds, never an Elexon limit."""
    if path is None:
        path = Path(__file__).resolve().parents[2] / "config" / "demo_thresholds.json"
    values = json.loads(Path(path).read_text(encoding="utf8"))
    return DemoThresholds(**values)


def forecast_variance(actual: float, forecast: float) -> float | None:
    """Return relative variance; None when the denominator is not meaningful."""
    if forecast <= 0:
        return None
    return (actual - forecast) / forecast


def estimate_hours_to_threshold(
    current_backlog: float,
    threshold: float,
    arrivals_per_hour: float,
    processed_per_hour: float,
) -> float | None:
    """Estimate breach time only when backlog is below threshold and growing."""
    net_growth = arrivals_per_hour - processed_per_hour
    if current_backlog >= threshold or net_growth <= 0:
        return None
    return (threshold - current_backlog) / net_growth


def alert_state(
    backlog: float,
    latency_minutes: float,
    forecast_variance_value: float | None,
    delayed_runs_24h: int,
    thresholds: DemoThresholds = DemoThresholds(),
) -> str:
    """Map synthetic metrics to an interpretable four-level alert."""
    if backlog >= thresholds.critical_backlog or latency_minutes >= thresholds.critical_latency_minutes:
        return "Critical"
    if (
        backlog >= thresholds.at_risk_backlog
        or latency_minutes >= thresholds.at_risk_latency_minutes
        or delayed_runs_24h >= 2
    ):
        return "At risk"
    if (
        backlog >= thresholds.elevated_backlog
        or latency_minutes >= thresholds.elevated_latency_minutes
        or delayed_runs_24h >= 1
        or (
            forecast_variance_value is not None
            and forecast_variance_value >= thresholds.elevated_forecast_variance
        )
    ):
        return "Elevated"
    return "Normal"


def project_queue(
    current_backlog: float,
    new_pair_arrivals_per_hour: float,
    historic_arrivals_per_hour: float,
    capacity_per_hour: float,
    demand_multiplier: float = 1.0,
    historic_throttle: float = 0.0,
    reserved_capacity_fraction: float = 0.0,
    horizon_hours: int = 24,
) -> dict:
    """Steady-rate queue scenario. Every input is an explicit demo assumption."""
    throttle = min(1.0, max(0.0, historic_throttle))
    reserve = min(0.8, max(0.0, reserved_capacity_fraction))
    multiplier = max(0.0, demand_multiplier)
    arrivals = max(0.0, new_pair_arrivals_per_hour) * multiplier
    arrivals += max(0.0, historic_arrivals_per_hour) * (1 - throttle)
    available_capacity = max(0.0, capacity_per_hour) * (1 - reserve)
    net_growth = arrivals - available_capacity
    projected = max(0.0, current_backlog + net_growth * max(0, horizon_hours))
    return {
        "new_pair_arrivals_per_hour": round(new_pair_arrivals_per_hour, 2),
        "historic_arrivals_per_hour": round(historic_arrivals_per_hour, 2),
        "projected_arrivals_per_hour": round(arrivals, 2),
        "registration_capacity_after_reserve_per_hour": round(available_capacity, 2),
        "net_queue_growth_per_hour": round(net_growth, 2),
        "current_backlog": int(current_backlog),
        "projected_backlog": int(round(projected)),
        "horizon_hours": int(horizon_hours),
        "historic_throttle_fraction": throttle,
        "reserved_capacity_fraction": reserve,
        "demand_multiplier": multiplier,
    }
