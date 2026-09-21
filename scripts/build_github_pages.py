"""Build a static GitHub Pages copy of the dashboard from the fixed seed data."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from service_intel.store import DemoStore, prepare_demo_files  # noqa: E402
from service_intel.narrative import build_demo_note  # noqa: E402


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf8")


def main() -> None:
    data_dir = ROOT / "data"
    db_path = prepare_demo_files(data_dir)
    store = DemoStore(db_path)
    site = ROOT / "site"
    if site.exists():
        shutil.rmtree(site)
    site.mkdir()

    for filename in ("index.html", "styles.css", "dashboard.js"):
        shutil.copy2(ROOT / "web" / filename, site / filename)
    (site / ".nojekyll").write_text("", encoding="utf8")

    api = site / "api"
    write_json(api / "overview.json", store.overview())
    write_json(api / "timeseries.json", store.hourly_series(168))
    write_json(api / "runs.json", store.service_runs(168))
    write_json(api / "contributors.json", store.contributors(168))
    write_json(api / "contributors-336.json", store.contributors(336))
    write_json(api / "forecast.json", store.forecast_accuracy())
    contributors = store.contributors(168)
    write_json(api / "incident-note.json", build_demo_note(store.overview(), contributors[0] if contributors else None))
    write_json(api / "validation.json", store.validation())
    write_json(api / "hypotheses.json", store.hypotheses())
    write_json(api / "customer-impact.json", store.customer_impact())
    write_json(api / "improvements.json", store.improvements())
    write_json(api / "context.json", store.operational_context())
    write_json(api / "scenario-inputs.json", store.scenario_inputs())

    print(f"Built static site at {site}")


if __name__ == "__main__":
    main()
