"""Deterministic, explicitly synthetic incident-note wording."""

from __future__ import annotations


def build_demo_note(overview: dict, top_contributor: dict | None) -> dict:
    state = overview["state"]
    backlog = overview["backlog"]
    latency = overview["latency"]
    delta = overview["backlog_change_24h"]
    variance = overview["forecast_variance_24h"]
    variance_text = "not calculable from this window" if variance is None else f"{variance:+.0%}"
    contributor_text = "No segment stands out in the selected synthetic window."
    if top_contributor:
        contributor_text = (
            f"The largest positive forecast deviation in this generated sample is "
            f"{top_contributor['participant_id']} / {top_contributor['submission_type']} "
            f"({top_contributor['actual'] - top_contributor['forecast']:+,} submissions)."
        )
    note = (
        "SYNTHETIC DEMONSTRATION — not an Elexon incident update.\n\n"
        f"State: {state}. Generated registration backlog is {backlog:,}; the prior-24-hour "
        f"backlog change is {delta:+,}. Generated average processing latency is {latency:.1f} minutes. "
        f"Generated submissions are {variance_text} against the sample forecast. "
        f"The demo run table marks {overview['delayed_runs_24h']} of "
        f"{overview['total_runs_24h']} synthetic scheduled runs as delayed.\n\n"
        f"Investigation lead: {contributor_text}\n\n"
        "Next checks before communicating operationally: confirm metric definitions and data freshness; "
        "compare arrivals, completed work and backlog by workload; validate any affected run schedule "
        "with service owners; check participant/customer impact; agree the next update time with the "
        "incident lead. This sample contains no customer or Elexon operational data."
    )
    return {"label": "DEMO TEMPLATE • SYNTHETIC ONLY", "note": note}

