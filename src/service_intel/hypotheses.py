"""Simple hypothesis tests for the synthetic operational case study."""

from __future__ import annotations

from collections import defaultdict


def _summary(rows: list[dict]) -> dict:
    received = sum(r["submissions_received"] for r in rows)
    processed = sum(r["submissions_processed"] for r in rows)
    failures = sum(r["validation_failure_count"] for r in rows)
    retries = sum(r["retry_count"] for r in rows)
    return {"received": received, "processed": processed, "failures": failures, "retries": retries}


def run_hypotheses(rows: list[dict], runs: list[dict]) -> list[dict]:
    """Return calculated findings with a conclusion and an evidence boundary."""
    if not rows:
        return []
    early = rows[: len(rows) // 2]
    late = rows[len(rows) // 2 :]
    s_early, s_late = _summary(early), _summary(late)
    h1_growth = s_late["received"] / max(1, len(late)) - s_late["processed"] / max(1, len(late))
    h1 = h1_growth > 0 and s_late["received"] > s_early["received"]
    forecast_actual = sum(r["actual_submissions"] for r in rows)
    forecast_expected = sum(r["forecast_submissions"] for r in rows)
    h2_variance = (forecast_actual - forecast_expected) / max(1, forecast_expected)
    h2 = h2_variance > 0.20
    by_workload = defaultdict(lambda: {"actual": 0, "forecast": 0, "peak": 0})
    for r in rows:
        segment = by_workload[r["submission_type"]]
        segment["actual"] += r["actual_submissions"]
        segment["forecast"] += r["forecast_submissions"]
        segment["peak"] = max(segment["peak"], r["backlog_size"])
    top_workload, top_values = max(by_workload.items(), key=lambda item: item[1]["actual"] - item[1]["forecast"])
    h3_share = (top_values["actual"] - top_values["forecast"]) / max(1, forecast_actual - forecast_expected)
    h3 = h3_share > 0.40
    historic = [r for r in rows if r["submission_type"] == "historic resubmission"]
    pair = [r for r in rows if r["submission_type"] != "historic resubmission"]
    h4 = sum(r["actual_submissions"] for r in historic) < sum(r["actual_submissions"] for r in pair)
    delayed = sum(1 for r in runs if r["status"] == "Delayed")
    h5 = delayed > 0 and historic
    critical = [r for r in runs if r["service_run_type"] in {"Settlement-critical", "payment-critical"}]
    h7 = sum(1 for r in critical if r["status"] == "On time") / max(1, len(critical)) >= 0.5

    def item(code, question, result, conclusion, confidence, limitation, next_check):
        return {
            "code": code, "question": question,
            "why_it_matters": "It helps distinguish an early service signal from a later symptom.",
            "data_needed": "Synthetic interval, workload, forecast and scheduled run records.",
            "method": "Transparent comparison of rates, totals and shares.",
            "result": result, "conclusion": conclusion, "confidence": confidence,
            "limitation": limitation, "next_check": next_check,
        }

    return [
        item("H1", "Is demand arriving faster than the service can process it?", f"Late sample net queue growth is {h1_growth:.2f} records per row.", "Supported in this synthetic sample." if h1 else "Not supported in this synthetic sample.", "Medium", "The sample has no private service telemetry.", "Compare arrival and completion definitions with the service owner."),
        item("H2", "Is forecast error an early signal of service pressure?", f"Actual demand is {h2_variance:+.1%} against the generated forecast.", "Supported as a leading signal in this demonstration." if h2 else "Not supported at the chosen demonstration threshold.", "Low to medium", "The generator makes the forecast and demand relationship illustrative.", "Test lead times and false alerts on real historical windows."),
        item("H3", "Does one workload contribute disproportionately to excess demand?", f"{top_workload} contributes {h3_share:.1%} of positive excess demand.", f"Supported for {top_workload}." if h3 else "No single workload dominates at the chosen share threshold.", "Medium", "Workload categories are synthetic and do not identify an Elexon cause.", "Compare workload definitions and processing effort using internal telemetry."),
        item("H4", "Could historic resubmissions create avoidable pressure?", f"Historic resubmissions total {sum(r['actual_submissions'] for r in historic):,} records in the sample.", "Worth testing as a control option, not proven as a cause." if h4 else "Not supported by the sample volume split.", "Low", "Volume alone does not measure processing cost or priority." , "Measure reprocessing effort and customer obligations before throttling."),
        item("H5", "Can temporary demand controls improve recovery?", f"The sample contains {delayed} delayed scheduled run records.", "Scenario testing is needed; the generated history cannot prove an intervention effect.", "Low", "There is no observed before and after intervention in the source data.", "Run a controlled simulation with agreed service constraints."),
        item("H6", "Would capacity expansion alone solve the issue?", "A demand rise can still exceed any fixed capacity under the scenario model.", "Rejected as a universal answer under sustained growth.", "Medium", "This is a queue sensitivity result, not an architecture assessment.", "Stress test multiple demand and capacity cases with service owners."),
        item("H7", "Does prioritising critical work reduce downstream risk?", f"{sum(1 for r in critical if r['status'] == 'On time')} of {len(critical)} critical sample runs are on time.", "Use prioritisation as a scenario to assess." if h7 else "The sample does not show reliable critical completion.", "Low to medium", "Run status is generated from a simple queue rule.", "Define priority classes and completion measures with Settlement owners."),
    ]
