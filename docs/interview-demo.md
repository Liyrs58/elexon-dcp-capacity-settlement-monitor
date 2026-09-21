# Interview demo notes

## 30-second explanation

“I used Elexon’s 14 September circular as a case study. It reports DCP capacity pressure associated with MSID and AMSID Pair submissions exceeding submitted forecasts, with scheduled Settlement and payment runs delayed. I built a local dashboard around the service questions an analyst could ask: are arrivals outpacing throughput, is the queue growing, which workloads differ from forecast, and what might alternative demand controls do? All the operating data and thresholds are synthetic, so I’m demonstrating the method rather than claiming access to Elexon telemetry or knowing the internal root cause.”

## 90-second walkthrough

“The starting point is the public evidence boundary. The circular tells us the DCP service was under capacity pressure, some Settlement and payment runs were late, and submission volumes were higher than submitted forecasts. It does not tell us whether the constraint was a database, server, API or something else, so I have not invented one.

“On the overview page, I compare generated arrivals with completed work and show queue, latency and a separate table of synthetic scheduled-run outcomes. The state badge uses simple thresholds that are visible in the README and explicitly labelled demo settings. I’d replace them with agreed operational objectives before using a monitor at work.

“The driver page segments actual-versus-forecast differences by fictional participant and workload. That helps direct a next investigation; it doesn’t blame a participant or prove a forecast was wrong for a specific operational reason.

“In the scenario lab, I vary new-pair demand, historic resubmission throttling and capacity held outside the registration queue. It uses a steady-rate queue equation, so it shows sensitivities, not a forecast. The note page assembles a deterministic update template and reminds the analyst to confirm affected customers, run schedules, metric definitions and the next update time.

“I defined the problem framing, evidence boundaries, measures and scenarios, then used AI development tools to help implement and debug the local prototype. I checked the arithmetic and tests. The useful lesson is that clear service measures can structure an investigation and customer update, while operational decisions still need verified telemetry and service-owner input.”

## Five likely technical questions

### 1. Why use synthetic data?

The public circular gives the incident summary, not timestamped arrivals, queue, latency, failures or participant-level telemetry. Synthetic data makes the prototype reproducible without implying access to internal information. Every row, identifier, threshold and run outcome is generated and labelled.

### 2. How is the alert state chosen?

It is deterministic: the code checks demo backlog and latency references, recent generated forecast variance, and generated delayed-run count. The threshold table is disclosed in the README. In a real service I would first agree metric definitions, data freshness, service objectives and escalation ownership with the relevant teams.

### 3. What does forecast variance mean here?

`(generated actual − generated forecast) / generated forecast`, where forecast is greater than zero. It is grouped by participant/workload. It describes a difference in this constructed sample; it cannot establish why a real forecast differed or whether the forecast method was poor.

### 4. How do you estimate time to a queue threshold?

I divide the remaining distance to the demo reference by recent average net queue growth (`arrivals/hour − processed/hour`). I return no estimate when the queue is already at/above the reference or when net growth is zero or negative. It assumes the recent rates continue, so it is only a conditional indicator.

### 5. Why SQLite and simple rules instead of machine learning?

SQLite and Python’s standard library keep the demo easy to run and inspect. The public evidence is too limited to train or validate a model, and the interview goal is to show operational reasoning. Simple arithmetic makes assumptions and failure cases easier to explain.

## Five claims not to make

1. “I found the actual DCP root cause.” The public circular does not state a lower-level cause.
2. “This dashboard detected the September Elexon incident.” The sample is synthetic and has no live connection.
3. “These are Elexon or BSC limits/SLAs.” All dashboard thresholds and capacity values are demo assumptions.
4. “Elexon’s forecasting caused the incident” or “a specific participant caused it.” The circular says volumes exceeded submitted forecasts; it does not establish blame or the reason for the gap.
5. “FMAR or AI will fix the DCP issue.” The FMAR documents describe a separate proposed future registration service; the dashboard is decision support, not added processing capacity.

## Three minute technical walkthrough

“I started with the Circular and wrote down exactly what it confirms and what it leaves open. It confirms service pressure, higher registration demand than submitted forecasts and delayed Settlement and payment runs. It does not reveal the internal technical bottleneck.

“I then created a fixed seed synthetic dataset with participant type, workload, arrivals, completed work, forecast, backlog, latency, failures, retries and scheduled run context. Before calculating any metric, the validation layer checks the structure, types, categories, timestamps, duplicates, forecast coverage and backlog equation. If a blocking check fails, the generated dataset cannot be published.

“The SQL layer groups the same records by interval, participant and workload. Python runs the generation, validation, scenarios and hypothesis tests. I compare important totals through both paths. The dashboard makes the queue balance visible, then shows which segment deserves investigation.

“The hypothesis page asks whether demand is exceeding processing, whether forecast error is an early signal, whether one workload contributes a large share, whether historic resubmissions are worth testing as a control, whether capacity alone is enough and whether priority treatment could protect critical runs. The sample can reject a hypothesis. None of these results proves an Elexon cause.

“The customer page is deliberately part of the product. It records who may be affected, what Settlement or payment question must be checked, who owns the next action and when the next update should happen. The improvement register turns a finding into a controlled action with a measure and a risk.

“That is how I would work as a Service Analyst. I would validate the evidence, quantify the operational effect, coordinate with the service owner and provider, communicate confirmed facts and uncertainty, then measure recovery and capture learning.”

## Calculated demonstration findings

The current generated sample supports H1. Late sample arrivals exceed completed work, so the queue grows. H2 is supported at the demonstration threshold because generated actual demand is more than 20 percent above the generated forecast. H3 is tested by workload share rather than assumed in advance. H4 is treated as a control question, not a proven cause. H5 is open because the generated history has no observed intervention. H6 is rejected as a universal answer under sustained demand growth. H7 remains a scenario question because critical completion is created by demonstration rules.

The exact values are generated when the app starts and can be checked on the Hypothesis tests page and through `/api/hypotheses`.

## Fifteen questions to prepare for

1. Why are the values synthetic?
2. How do you know the data is valid?
3. Why did you choose arrivals, processing and backlog?
4. Why use SQL as well as Python?
5. Why did you not use machine learning?
6. Why are the thresholds not Elexon limits?
7. How do you distinguish demand pressure from slower processing?
8. How would you reduce false alerts?
9. What would you ask the service provider?
10. What would you ask an affected customer?
11. Which action would need an authorised decision?
12. How would BSC processes affect the response?
13. What hypothesis could not be determined from public data?
14. How would this become a production service?
15. How did the project reflect Elexon’s values?

## Three insights to emphasise

1. An unusual value is a reason to investigate, not proof of an error.
2. A useful operational dashboard combines data quality, service measures, customer impact and ownership.
3. Good analysis makes uncertainty visible. It does not invent a technical root cause.
