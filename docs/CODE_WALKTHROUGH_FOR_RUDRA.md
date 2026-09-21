# Code walkthrough for Rudra

This is the shortest route through the implementation. Read the files in this order.

## 1. `src/service_intel/generator.py`

This file creates the synthetic sample. It fixes the seed, defines six synthetic participants and three workload types, advances time by hour, creates arrivals and forecasts, allocates a generated processing budget, rolls the queue forward and creates illustrative scheduled runs.

The important ownership decision is that the fields mimic the shape of an operational dataset without pretending to be Elexon data. The IDs begin with `SYN`, which makes the boundary visible.

The backlog equation is:

`new backlog = previous backlog + submissions received minus submissions processed`

The generator also adds latency, validation failures, retries, priority fields and risk flags. These are modelling fields for the demonstration.

## 2. `src/service_intel/validation.py`

This file prevents analysis from running on a structurally broken generated dataset.

It checks required columns, numeric types, finite values, non negative counts, allowed categories, timestamps, duplicate identities, forecast coverage, actual versus received counts, backlog reconciliation and fixed seed reproduction.

The public interface displays PASS or BLOCKED. A real service would need additional controls such as freshness, source lineage, access rights and reconciliation with operational systems.

## 3. `src/service_intel/analysis.py`

This file contains small, testable calculations.

1. `forecast_variance` returns a signed relative difference and avoids division by zero.
2. `estimate_hours_to_threshold` returns a time only when the queue is below the reference and net growth is positive.
3. `alert_state` applies demo references in order from Critical to Normal.
4. `project_queue` applies the scenario assumptions and returns rounded display values.

These functions are deliberately plain so a reviewer can inspect the arithmetic.

## 4. `src/service_intel/hypotheses.py`

This file turns the operational questions into seven structured findings. Each finding has a question, why it matters, method, result, conclusion, confidence, limitation and next check.

The limitation is part of the result. For example, a positive forecast difference is supported in this generated sample, but the generator controls the relationship between demand and forecast, so it cannot prove a real forecasting cause.

## 5. `src/service_intel/store.py`

This file creates the SQLite database, loads the generated rows, executes grouped queries and exposes the results needed by the server.

The store keeps SQL totals as the reporting layer. It also exports Power BI friendly files and returns context, customer impact, improvement ideas and validation results.

The main defence point is reconciliation. Python creates and checks the data. SQLite groups it for the dashboard. A test compares totals so those layers do not silently disagree.

## 6. `src/service_intel/narrative.py`

This file builds the service note from current generated values using a deterministic template. There is no language model in the note path. The interface warns that it is fabricated demonstration text.

## 7. `server.py`

This file serves the static web files and returns JSON from routes such as `/api/overview`, `/api/timeseries`, `/api/forecast`, `/api/scenario`, `/api/hypotheses`, `/api/customer-impact`, `/api/improvements` and `/api/validation`.

The API is local to this project. It is not an Elexon API and does not connect to a live service.

## 8. `web/index.html`

This file defines the visible pages and their explanatory text. The page structure follows the analyst journey: current state, investigation, scenario, hypotheses, customer impact, improvement, approach, communication and evidence.

## 9. `web/dashboard.js`

This file loads the local routes, updates metric values, draws SVG charts and fills tables. It contains no hidden model. The charts are simple line and bar drawings from returned rows.

## 10. `web/styles.css`

This file provides the layout. The refinement pass uses flatter panels, lighter navigation, smaller headings and fewer decorative treatments so the page reads like an internal review tool.

## One calculation traced end to end

1. The generator writes `submissions_received` and `submissions_processed`.
2. Validation checks the queue roll forward.
3. SQLite groups the rows by timestamp.
4. The store returns arrivals, processed work and queue size.
5. The server exposes those values through `/api/timeseries`.
6. The browser draws the lines and labels the units.
7. The test checks the arithmetic independently.

That chain is what to explain when asked how a number reaches the screen.

