import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from service_intel.analysis import (  # noqa: E402
    DemoThresholds,
    alert_state,
    estimate_hours_to_threshold,
    forecast_variance,
    project_queue,
)


class AnalysisTests(unittest.TestCase):
    def test_forecast_variance_handles_zero_and_signed_error(self):
        self.assertIsNone(forecast_variance(5, 0))
        self.assertAlmostEqual(forecast_variance(120, 100), 0.2)
        self.assertAlmostEqual(forecast_variance(80, 100), -0.2)

    def test_time_to_threshold_only_when_queue_is_below_and_growing(self):
        self.assertAlmostEqual(estimate_hours_to_threshold(100, 300, 15, 5), 20)
        self.assertIsNone(estimate_hours_to_threshold(300, 300, 15, 5))
        self.assertIsNone(estimate_hours_to_threshold(100, 300, 5, 15))

    def test_alert_states_follow_demo_thresholds(self):
        thresholds = DemoThresholds()
        self.assertEqual(alert_state(0, 10, 0.0, 0, thresholds), "Normal")
        self.assertEqual(alert_state(180, 10, 0.0, 0, thresholds), "Elevated")
        self.assertEqual(alert_state(550, 10, 0.0, 0, thresholds), "At risk")
        self.assertEqual(alert_state(100, 120, 0.0, 0, thresholds), "Critical")

    def test_scenario_projects_arrivals_capacity_and_throttle(self):
        result = project_queue(
            current_backlog=100,
            new_pair_arrivals_per_hour=10,
            historic_arrivals_per_hour=4,
            capacity_per_hour=20,
            demand_multiplier=1.5,
            historic_throttle=0.5,
            reserved_capacity_fraction=0.1,
            horizon_hours=10,
        )
        self.assertEqual(result["projected_arrivals_per_hour"], 17)
        self.assertEqual(result["registration_capacity_after_reserve_per_hour"], 18)
        self.assertEqual(result["projected_backlog"], 90)


if __name__ == "__main__":
    unittest.main()
