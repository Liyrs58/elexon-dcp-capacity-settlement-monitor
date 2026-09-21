# Settlement Service Intelligence — interview prototype

**A local, synthetic-data demonstration of how a Service Analyst could structure operational monitoring and investigation around Elexon Circular EL04799.** It is not an Elexon product, does not connect to Elexon systems, and does not contain Elexon operational data.

## What this demonstrates

The 14 September 2026 circular reports an incident affecting the Data and Calculations Platform (DCP), downstream delays to scheduled Settlement and payment runs, and a significant increase in MSID/AMSID Pair submissions above submitted forecasts while DCP was at or near maximum capacity. It does not identify a lower-level technical cause. See the [circular](https://elexonexternal.newsweaver.com/924j6pkkru/1gsurqf0ylu) and [Newscast 1135](https://elexonexternal.newsweaver.com/1gmbg04lik/1guzn2hox2r).

This prototype turns that public service problem into five interview-friendly questions:

1. **Control:** are the generated signals inside clearly stated demo expectations?
2. **Detect:** are arrivals rising faster than throughput, and is the queue or latency worsening?
3. **Investigate:** which generated participant/workload segments have the largest volume or forecast deviation?
4. **Communicate:** what concise checks and customer-impact questions should an analyst record?
5. **Recommend:** how do transparent demand, throttling and capacity-reserve assumptions change a simple queue projection?

The page keeps four evidence classes separate: public Circular facts, FMAR consultation proposals/draft material, other Newscast items that are adjacent but separate, and synthetic demo data. The FMAR programme is future consultation context; its materials do not establish it is the DCP service in EL04799 or that it resolves the incident. The separate [Newscast research map](../../work/newsweaver-1135-source-review.md) records how the linked industry items were categorized.

The design follows the Service Analyst workflow in the supplied Elexon research pack: observe, validate, identify risk, investigate, form a hypothesis, test it, assess customer and Settlement impact, recommend a proportionate option, communicate clearly, monitor recovery and capture learning.

## Synthetic-data disclosure

The dashboard and generated files display synthetic labels. Every participant ID begins with `SYN-`. The generator uses a fixed seed (`20260914`) and produces 14 demo days (6,048 participant/workload/hour rows plus 28 scheduled-run rows). The sample timeline uses 1–14 January 2026 only as a reproducible index; it is not a representation of events on those dates.

The generator is intentionally simple and documented:

- It creates six fictional participant IDs, three workload types, and hourly arrivals.
- Hour-of-day profile and stepped demand factors create a visible change in load. Forecasts use the generated stable baseline while actuals use the stepped factors plus seeded variation.
- A **synthetic processing budget of 20 items/hour** is allocated in proportion to remaining queued items multiplied by a demo workload weight, with rotating tie breaks. This number and allocation rule are demo parameters, not DCP capacity or a claim about Elexon's scheduling.
- Segment latency is generated from a simple queue-pressure formula plus small seeded noise. Scheduled Settlement/payment run delays are separately generated from the total demo queue at the run time. This is a storytelling rule for the scenario, not a causal model or measured relationship.
- Validation failures and retries are seeded sample counts. Their definitions are illustrative and do not match any asserted Elexon operational metric.
- The demo alert thresholds are invented for readability: Elevated at backlog 180, latency 35 minutes, one delayed run, or forecast variance +20%; At risk at backlog 550, latency 75 minutes, or two delayed runs; Critical at backlog 900 or latency 120 minutes. They are not BSC limits, Elexon thresholds or service-level commitments.

## Analytics

### Descriptive

- Hourly submissions received and processed.
- Current and changing backlog, average synthetic processing latency, validation failures and retries.
- Hourly failure/retry rates use generated counts divided by generated arrivals; a zero-arrival hour has no defined rate.
- Generated actual versus forecast by participant and workload.
- Synthetic scheduled-run delay status.

### Predictive

- Time to the **demo** critical-backlog reference is estimated only when the queue is below that reference and current average arrivals exceed current average processing. It assumes those rates continue unchanged.
- The scenario lab projects a steady hourly queue balance: `projected backlog = max(0, current backlog + (projected arrivals − available processing capacity) × hours)`.
- Scenario inputs allow +0% to +100% new-pair demand, 0% to 100% historic-resubmission throttling, and 0% to 30% capacity held outside the registration queue. A 72-hour starting rate is held constant. The model does not forecast run outcomes.

### Hypothesis testing

The Hypothesis tests page calculates seven explicit questions. Each result includes the question, why it matters, method, result, conclusion, confidence, limitation and next check. The sample is allowed to reject a hypothesis. These conclusions are about the generated sample only.

### Prescriptive

The dashboard lists operational ideas to assess with service owners: rolling base/expected/high forecasts, monitoring arrivals against throughput and queue age, workload segmentation, evaluating non-critical resubmission scheduling, stress testing above forecasts, and clear customer updates. They are questions and options, not instructions or claims about Elexon's current controls or architecture.

## Operational workstation pages

- Executive service view with current state, queue, throughput, forecast variance, latency, quality signals and scheduled run context.
- Service trends with arrivals, processing, backlog, latency, failures and retries.
- Investigation with participant and workload segmentation.
- Hypothesis tests with calculated conclusions and evidence limits.
- Scenario lab for demand, throttling and reserved capacity assumptions.
- Customer and Settlement impact with ownership and communication fields.
- Improvement register with problem, action, benefit, risk, owner and measure.
- Analyst approach with the BSC, customer, provider and decision boundaries.
- Incident note with deterministic plain English wording.
- Evidence and limits with the public facts and unknowns.

## Architecture

```text
Fixed-seed Python generator
          │
          ├── synthetic_registration_metrics.csv
          ├── synthetic_service_runs.csv
          └── SQLite database
                    │
              Python analysis/API
                    │
        Local browser dashboard (HTML/CSS/JS)
```

The app uses only Python’s standard library at runtime: `http.server`, `sqlite3`, `csv` and JSON. SQLite is used instead of DuckDB so the interviewer can run the project with the standard Python installation and inspect the database without package installation. The dashboard uses browser native SVG for charts and does not load third party scripts. SQL examples are in [`sql/analysis.sql`](sql/analysis.sql). Key calculations are in [`src/service_intel/analysis.py`](src/service_intel/analysis.py); validation is in [`src/service_intel/validation.py`](src/service_intel/validation.py); hypotheses are in [`src/service_intel/hypotheses.py`](src/service_intel/hypotheses.py).

## Run it

From the workspace folder:

```bash
cd outputs/dcp-capacity-settlement-monitor
python3 app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The app creates or reuses the generated CSV and SQLite files in `data/` when it starts. To rebuild those generated files from the fixed seed, remove the three files in `data/` and restart.

To stop the local server, press `Ctrl+C` in that terminal.

## Tests

From the project folder:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover fixed-seed reproducibility, queue roll-forward, processing-budget bounds, run-risk flags, forecast variance edge cases, alerts, time-to-threshold validity, scenario arithmetic, and SQLite query windows.

The same suite can be run with `python3 -m pytest -q` when pytest is available. The current environment returned 12 passing tests with that command. The standard library command remains the no dependency option.

On first generation, `data/powerbi_export/` contains a fact interval export, a fact scheduled run export, participant and workload dimensions, a validation report and a data dictionary. Power BI was not run or tested in this repository. These files are a compatible handoff, not a claim of a finished Power BI report.

## Limits and correct interpretation

- This tool cannot monitor or detect the real Elexon incident. It contains no private telemetry and runs locally without an Elexon connection.
- The Circular confirms service-level capacity pressure and submission growth beyond submitted forecasts. It does not establish a database, server, CPU, network, API or other lower-level bottleneck.
- Alert thresholds and capacity are synthetic demo settings, not BSC rules, Elexon SLAs, or actual DCP limits.
- A forecast miss in the generated sample is descriptive. It does not prove that forecasting caused a real incident.
- The FMAR design and API material is proposed/draft context. The API v0.6 server is a placeholder; no production endpoint, throughput, or security model is inferred.
- A monitoring dashboard can support investigation and communication. It does not itself add processing capacity or resolve a service problem.
- Real recommendations require service-owner validation, agreed metric definitions, appropriate operational data, customer-impact checks, and knowledge of the actual process and constraints.

## Interview ownership

The candidate’s ownership story should focus on framing the question, separating evidence from assumptions, choosing interpretable measures, defining scenario logic, and reviewing outputs/tests. Cursor/Codex and other AI development tools may be acknowledged as implementation/debugging assistance; do not imply every line was manually written.

See [`interview-demo.md`](interview-demo.md) for the 30-second explanation, 90-second walkthrough, technical questions, and claims to avoid. See [`evidence-register.md`](evidence-register.md) for cited public claims and their evidence status.

The supporting analyst documents are in [`docs/`](docs/): methodology, data dictionary, limitations, runbook, incident playbook, FAQ, job description mapping, values mapping and the extended interview demo.

## Defence and learning pack

1. [`FULL_AUDIT.md`](docs/FULL_AUDIT.md) records the review findings and evidence boundary.
2. [`METRIC_DEFENCE_GUIDE.md`](docs/METRIC_DEFENCE_GUIDE.md) explains every displayed measure with formulas and limits.
3. [`COMPLETE_GLOSSARY.md`](docs/COMPLETE_GLOSSARY.md) defines the Elexon, operational and technical terms used by the project.
4. [`SCREEN_BY_SCREEN_DEFENCE.md`](docs/SCREEN_BY_SCREEN_DEFENCE.md) gives a truthful explanation for every page, chart and table.
5. [`CODE_WALKTHROUGH_FOR_RUDRA.md`](docs/CODE_WALKTHROUGH_FOR_RUDRA.md), [`SQL_LEARNING_GUIDE.md`](docs/SQL_LEARNING_GUIDE.md) and [`PYTHON_LEARNING_GUIDE.md`](docs/PYTHON_LEARNING_GUIDE.md) trace the implementation.
6. [`TESTING_DEFENCE.md`](docs/TESTING_DEFENCE.md) explains the twelve automated checks and their limits.
7. [`HUMAN_IN_THE_LOOP.md`](docs/HUMAN_IN_THE_LOOP.md), [`MY_CONTRIBUTION.md`](docs/MY_CONTRIBUTION.md) and [`SOURCE_DEFENCE.md`](docs/SOURCE_DEFENCE.md) make ownership and claims explicit.
8. [`INTERVIEW_DEFENCE_HANDBOOK.md`](docs/INTERVIEW_DEFENCE_HANDBOOK.md), [`TEACH_ME_LIKE_16.md`](docs/TEACH_ME_LIKE_16.md) and [`TECHNICAL_MASTERCLASS.md`](docs/TECHNICAL_MASTERCLASS.md) provide the interview and learning path.
9. [`HUMAN_REVIEW_CHECKLIST.md`](docs/HUMAN_REVIEW_CHECKLIST.md) is the final review before showing a result or using a number in conversation.
10. [`INTERVIEW_QUESTIONS_AND_ANSWERS.md`](docs/INTERVIEW_QUESTIONS_AND_ANSWERS.md) contains full spoken answers to the twenty interview questions and the additional technical terms used by the project.
