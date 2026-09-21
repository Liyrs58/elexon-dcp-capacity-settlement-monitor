import sys
import tempfile
import unittest
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from service_intel.generator import DEMO_CAPACITY_PER_HOUR, generate_demo_data  # noqa: E402
from service_intel.hypotheses import run_hypotheses  # noqa: E402
from service_intel.store import DemoStore, prepare_demo_files  # noqa: E402
from service_intel.validation import validate_registration_rows  # noqa: E402


class GeneratorTests(unittest.TestCase):
    def test_generator_is_fixed_seed_and_marked_by_synthetic_ids(self):
        first, first_runs = generate_demo_data(hours=48)
        second, second_runs = generate_demo_data(hours=48)
        self.assertEqual(first, second)
        self.assertEqual(first_runs, second_runs)
        self.assertTrue(all(row["participant_id"].startswith("SYN-") for row in first))
        self.assertEqual(len(first), 48 * 6 * 3)

    def test_hourly_processing_never_exceeds_demo_capacity(self):
        rows, _ = generate_demo_data(hours=96)
        by_hour = defaultdict(int)
        for row in rows:
            by_hour[row["timestamp"]] += row["submissions_processed"]
        self.assertTrue(all(value <= DEMO_CAPACITY_PER_HOUR for value in by_hour.values()))

    def test_backlog_rolls_forward_consistently_by_participant_and_workload(self):
        rows, _ = generate_demo_data(hours=72)
        previous = {}
        for row in rows:
            key = (row["participant_id"], row["submission_type"])
            expected = max(0, previous.get(key, 0) + row["submissions_received"] - row["submissions_processed"])
            self.assertEqual(row["backlog_size"], expected)
            previous[key] = row["backlog_size"]

    def test_service_run_flag_matches_demo_deadline(self):
        _, runs = generate_demo_data(hours=96)
        self.assertTrue(runs)
        for run in runs:
            self.assertEqual(run["downstream_settlement_risk_flag"], int(run["delay_minutes"] > run["deadline_minutes"]))


class StoreTests(unittest.TestCase):
    def test_sqlite_queries_return_expected_windows_and_segments(self):
        with tempfile.TemporaryDirectory() as temp:
            db = prepare_demo_files(Path(temp))
            store = DemoStore(db)
            series = store.hourly_series(24)
            self.assertEqual(len(series), 24)
            self.assertIn("failure_rate_pct", series[-1])
            self.assertIn("retry_rate_pct", series[-1])
            self.assertEqual(len(store.forecast_accuracy()), 18)
            self.assertIn("state", store.overview())
            self.assertTrue(store.contributors())
            self.assertTrue(store.service_runs(168))

    def test_validation_passes_and_blocks_a_changed_backlog(self):
        rows, runs = generate_demo_data(hours=48)
        report = validate_registration_rows(rows)
        self.assertEqual(report["status"], "PASS")
        changed = [dict(row) for row in rows]
        changed[40]["backlog_size"] += 1
        blocked = validate_registration_rows(changed)
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertTrue(blocked["error_count"] > 0)
        changed[2]["processing_latency_minutes"] = math.nan
        non_finite = validate_registration_rows(changed)
        self.assertEqual(non_finite["status"], "BLOCKED")

    def test_hypothesis_output_contains_evidence_boundary(self):
        rows, runs = generate_demo_data()
        findings = run_hypotheses(rows, runs)
        self.assertEqual(len(findings), 7)
        self.assertTrue(all(item["limitation"] and item["next_check"] for item in findings))

    def test_sql_and_python_total_arrivals_reconcile(self):
        with tempfile.TemporaryDirectory() as temp:
            db = prepare_demo_files(Path(temp))
            store = DemoStore(db)
            sql_total = store._query("SELECT SUM(submissions_received) AS total FROM registration_metrics")[0]["total"]
            rows, _ = generate_demo_data()
            python_total = sum(row["submissions_received"] for row in rows)
            self.assertEqual(sql_total, python_total)


if __name__ == "__main__":
    unittest.main()
