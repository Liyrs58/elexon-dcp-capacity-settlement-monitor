# Testing defence

The test suite checks the calculations and data controls without pretending that a passing test proves a live service is healthy.

## Calculation tests

1. `test_forecast_variance_handles_zero_and_signed_error` checks zero denominator behaviour and both positive and negative variance.
2. `test_time_to_threshold_only_when_queue_is_below_and_growing` checks a valid time estimate and two invalid cases.
3. `test_alert_states_follow_demo_thresholds` checks the four state boundaries using the editable demo settings.
4. `test_scenario_projects_arrivals_capacity_and_throttle` checks demand multiplier, historic throttle, reserved capacity and projected queue arithmetic together.

## Generator tests

5. `test_generator_is_fixed_seed_and_marked_by_synthetic_ids` checks repeatability, row count and the synthetic identifier boundary.
6. `test_hourly_processing_never_exceeds_demo_capacity` checks that generated processing does not exceed the configured demonstration budget in an hour.
7. `test_backlog_rolls_forward_consistently_by_participant_and_workload` checks the queue equation for every segment.
8. `test_service_run_flag_matches_demo_deadline` checks that the delayed flag follows delay greater than deadline.

## Store and evidence tests

9. `test_sqlite_queries_return_expected_windows_and_segments` checks the reporting window, returned rate fields, forecast segment count, overview state and run rows.
10. `test_validation_passes_and_blocks_a_changed_backlog` checks both a valid dataset and blocking behaviour after a queue value is changed or a non finite value is introduced.
11. `test_hypothesis_output_contains_evidence_boundary` checks that all seven findings include a limitation and a next check.
12. `test_sql_and_python_total_arrivals_reconcile` checks that SQLite and Python report the same total arrivals.

## How to explain the limits

The tests prove that the implementation follows its written rules. They do not prove that the rules match Elexon production definitions, that the generated data resembles live telemetry, or that an operational action would be safe. Those questions require service owners, source systems and agreed objectives.

