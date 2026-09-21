"""Standard-library local web server for the demonstration dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from service_intel.analysis import project_queue
from service_intel.narrative import build_demo_note
from service_intel.store import DemoStore, prepare_demo_files


ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
DATA_DIR = ROOT / "data"


def create_handler(store: DemoStore):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:
            print(f"[dashboard] {self.address_string()} {fmt % args}")

        def _json(self, payload: object, status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _file(self, path: Path, content_type: str) -> None:
            if not path.is_file():
                self.send_error(404)
                return
            body = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            if parsed.path == "/":
                return self._file(WEB_DIR / "index.html", "text/html; charset=utf-8")
            if parsed.path == "/styles.css":
                return self._file(WEB_DIR / "styles.css", "text/css; charset=utf-8")
            if parsed.path == "/dashboard.js":
                return self._file(WEB_DIR / "dashboard.js", "text/javascript; charset=utf-8")
            if parsed.path == "/api/overview":
                return self._json(store.overview())
            if parsed.path == "/api/timeseries":
                hours = int(query.get("hours", [168])[0])
                return self._json(store.hourly_series(max(24, min(hours, 336))))
            if parsed.path == "/api/contributors":
                hours = int(query.get("hours", [168])[0])
                return self._json(store.contributors(max(24, min(hours, 336))))
            if parsed.path == "/api/forecast":
                return self._json(store.forecast_accuracy())
            if parsed.path == "/api/runs":
                hours = int(query.get("hours", [168])[0])
                return self._json(store.service_runs(max(24, min(hours, 336))))
            if parsed.path == "/api/scenario":
                params = store.scenario_inputs()
                result = project_queue(
                    current_backlog=params["current_backlog"],
                    new_pair_arrivals_per_hour=params["new_pair_arrivals_per_hour"],
                    historic_arrivals_per_hour=params["historic_arrivals_per_hour"],
                    capacity_per_hour=params["capacity_per_hour"],
                    demand_multiplier=float(query.get("multiplier", [1.0])[0]),
                    historic_throttle=float(query.get("throttle", [0.0])[0]),
                    reserved_capacity_fraction=float(query.get("reserve", [0.0])[0]),
                    horizon_hours=int(query.get("horizon", [24])[0]),
                )
                return self._json(result)
            if parsed.path == "/api/incident-note":
                contributors = store.contributors(168)
                positive = [r for r in contributors if r["actual"] > r["forecast"]]
                top = positive[0] if positive else None
                return self._json(build_demo_note(store.overview(), top))
            if parsed.path == "/api/validation":
                return self._json(store.validation())
            if parsed.path == "/api/hypotheses":
                return self._json(store.hypotheses())
            if parsed.path == "/api/context":
                return self._json(store.operational_context())
            if parsed.path == "/api/customer-impact":
                return self._json(store.customer_impact())
            if parsed.path == "/api/improvements":
                return self._json(store.improvements())
            self.send_error(404)

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    db_path = prepare_demo_files(DATA_DIR)
    store = DemoStore(db_path)
    server = ThreadingHTTPServer((host, port), create_handler(store))
    print("Synthetic demonstration dashboard ready")
    print(f"Open http://{host}:{port}")
    print("All operating metrics, participants and thresholds shown are synthetic.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()
