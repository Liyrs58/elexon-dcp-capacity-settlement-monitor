# Elexon Service Analyst interview questions and answers

This document contains spoken answers for the project. The answers are written so they can be shortened in a real interview. The figures in the examples are synthetic unless the answer explicitly refers to the public Circular.

## Part one: twenty interview questions

### 1. Why did you choose this case?

I chose the 14 September 2026 Circular because it connects several parts of the Service Analyst role. It involves service performance, data pressure, Settlement timing, customers, incident communication and future demand planning. The Circular gives enough public context to build a serious analytical case without pretending to know Elexon private telemetry.

### 2. What is DCP?

DCP means Data and Calculations Platform. The public material describes it as one of the SVAA supporting services used to calculate Settlement. The Circular says DCP was affected by an incident and was operating at or near maximum capacity. It does not publish the internal architecture or lower level technical cause, so I have not invented one.

### 3. What is the first signal you would check?

I would first agree what counts as received work and completed work, then compare arrivals with throughput over the same reporting window. If arrivals are higher than completed work for a sustained period, the queue should grow. I would then check backlog age, latency, validation failures, retries and any affected scheduled deadlines.

### 4. Why use backlog?

Backlog shows accumulated open work. It helps distinguish a short arrival spike from a sustained service pressure pattern. I would never read it alone. A queue can grow because demand increased, because processing slowed, because work was retried, or because the definitions changed.

### 5. What is forecast variance?

In this project it is actual submissions minus forecast submissions, divided by forecast submissions when the forecast is positive.

For example, actual demand of 120 against a forecast of 100 gives a variance of 20 percent. It tells me where observed demand differs from the submitted expectation in the sample. It does not prove that the forecasting process was poor or caused a real incident.

### 6. Does a forecast miss prove forecasting caused the incident?

No. The Circular says registration volumes were higher than submitted forecasts. That is a public fact about the difference between demand and expectation. It does not explain why the difference happened, whether the forecast was reasonable when submitted, or whether forecasting caused the service pressure.

### 7. Why not use machine learning?

The available evidence is too limited to train or validate a useful production model. The interview goal is transparent operational reasoning. Simple calculations make the assumptions, failure cases and evidence limits visible. If real telemetry became available, I would first establish reliable definitions and a baseline before considering a more complex model.

### 8. What does the scenario model assume?

It assumes steady hourly arrivals and steady processing capacity over the selected horizon. It does not model recovery surges, seasonality, dependency delays, changing priorities, unknown constraints or real scheduled run behaviour. That is why I call it a conditional scenario and not a production forecast.

### 9. What would you need before throttling work?

I would need confirmed service rules, workload priority definitions, customer impact analysis, operational ownership, a communication plan, monitoring during the change and a recovery or rollback plan. The dashboard can compare assumptions, but it cannot authorise a control.

### 10. Could FMAR fix the incident?

I would not claim that. FMAR is a separate public design and implementation programme for flexibility market asset registration. Its future relationship with DCP demand and the Circular incident is an open question. The project uses FMAR for context, not as a confirmed remedy.

### 11. How did you validate the data?

The validation layer checks required fields, types, finite values, non negative counts, allowed categories, timestamps, duplicate identities, forecast coverage, actual versus received counts, backlog reconciliation and fixed seed reproduction. If a blocking check fails, the generated dataset is not published for analysis.

### 12. Why use Python and SQL?

Python is useful for repeatable generation, validation, scenario calculations and hypothesis logic. SQLite and SQL are useful for grouped reporting by hour, participant and workload. I also test that important Python and SQL totals reconcile, so the reporting layer does not silently disagree with the generated data.

### 13. What does a passing test mean?

A passing test means the implementation follows the rule written in the test. It does not prove that the rule is the same as an Elexon production definition, that the synthetic data resembles live telemetry, or that an operational action is safe.

### 14. Which result is most useful?

The combination of arrivals, throughput, backlog, latency and scheduled run context is more useful than any one number. Together they show incoming work, completed work, accumulated work, processing time and potential timing impact. The combination also helps separate a demand question from a processing question.

### 15. How would you investigate a concentrated workload?

I would check the workload definition, volume, forecast difference, queue contribution, retries, validation failures, processing effort and time alignment. I would compare like with like and avoid assigning blame from one bar chart. I would then ask the service owner or provider to confirm whether the pattern matches the operational process.

### 16. How would you communicate during an incident?

I would state confirmed facts first, then the current measured signal, customer or Settlement impact if confirmed, the uncertainty that remains, any authorised customer action, the responsible owner and the next update time. I would not send the synthetic note or an unverified hypothesis as an operational update.

### 17. What is not in the project?

There is no live Elexon connection, private telemetry, private API, named customer data, internal capacity limit, internal architecture description or proven lower level root cause. The participant IDs, operational values, thresholds and scheduled run outcomes are generated for demonstration.

### 18. What did you personally contribute?

I owned the problem framing, evidence boundary, data shape, metric definitions, validation rules, scenario assumptions, hypothesis questions, interpretation and interface review. I used Cursor and Codex as implementation and debugging assistance. I did not claim that I manually typed every line.

### 19. What would you improve with real data?

I would agree metric definitions with service owners, add data freshness and lineage checks, measure queue age, map thresholds to real service objectives and run deadlines, test alert lead time and false alerts, and review the results with the teams who own the process and customer communication.

### 20. What is the main lesson?

An analyst can make an operational problem clearer without pretending to know more than the evidence supports. A useful monitor combines data quality, service measures, investigation logic, customer impact and ownership.

## Part two: technical terms you may be asked about

### 21. What is the BSC?

The Balancing and Settlement Code is the rule framework for electricity market and Settlement arrangements in Great Britain. In this project it provides process context. I do not use the dashboard to create or interpret a new BSC rule.

### 22. What is Settlement?

Settlement is the process that calculates the financial position associated with electricity market activity. In this case, the important service question is whether supporting processing delays could affect scheduled Settlement or payment activity.

### 23. What is SVAA?

SVAA means Supplier Volume Allocation Agent. It is a defined service role in the Settlement arrangements. The Circular identifies DCP as one of the supporting services used by SVAA. The project uses the public service description for context and does not reproduce the live service.

### 24. What is an MSID Pair?

An MSID Pair is a pair of Metering System Identifiers used in the registration context described by Elexon. The dashboard uses “new MSID Pair” as a synthetic workload label. It does not model the real registration process.

### 25. What is an AMSID Pair?

An AMSID Pair is an Asset Metering System Identifier Pair used in the flexible asset registration context. The dashboard uses “new AMSID Pair” as a synthetic workload label and does not claim that the generated fields reproduce the real interface.

### 26. What are VLP, VTP and AMVLP?

They are participant roles used in the flexibility and registration context. VLP means Virtual Lead Party, VTP means Virtual Trading Party and AMVLP means Asset Metering Virtual Lead Party. In the project they are segmentation labels for fictional participants, not evidence about any named organisation.

### 27. What is FMAR?

FMAR means Flexibility Market Asset Registration. It is a public design and implementation programme. The consultation and API material describe proposed future registration arrangements. I keep it separate from the Circular and do not present it as a confirmed fix.

### 28. What is an API?

An API is an interface through which one system exchanges data with another. This project has local routes such as `/api/overview` and `/api/scenario`. They serve the local synthetic dashboard and are not Elexon private APIs.

### 29. What is telemetry?

Telemetry is measured operational information collected from a live service, such as timestamps, queue length, processing duration or error events. This project has no Elexon telemetry. Its operational values are generated.

### 30. What is synthetic data?

Synthetic data is made for demonstration rather than collected from live operations. The generator uses fictional IDs, a fixed seed and documented assumptions. It allows the calculations to be tested without implying access to private data.

### 31. What is a fixed seed?

A fixed seed makes the random part of data generation repeatable. The project uses seed `20260914`. If the code and inputs stay the same, the generated sample can be recreated and checked.

### 32. What is a schema?

A schema describes the expected fields, types and structure of a dataset. The validation layer checks that the required registration fields exist and contain appropriate values before analysis.

### 33. What is data grain?

Data grain means what one row represents. In this project one registration row represents one participant, one workload and one hour. Knowing the grain prevents accidental double counting.

### 34. What is aggregation?

Aggregation combines detailed rows into a reporting view, such as summing arrivals by hour or by participant and workload. SQL performs these groupings for the dashboard.

### 35. What is throughput?

Throughput is completed work per unit of time. Here it is the sum of generated processed submissions in an hour.

### 36. What is processing latency?

Processing latency is the time associated with completing work. Here it is a generated value in minutes. In a live service I would confirm whether it means time from receipt to completion, time spent processing, or another agreed definition.

### 37. What is backlog reconciliation?

It is the arithmetic check that the new queue equals the previous queue plus received work minus processed work. It is one of the most important controls in this project.

### 38. What is failure rate?

Failure rate is generated validation failure count divided by received submissions, expressed as a percentage. It is a quality signal. It does not explain why a record failed.

### 39. What is retry rate?

Retry rate is generated retry count divided by received submissions, expressed as a percentage. It can show rework pressure, but it does not prove an interface or architecture fault.

### 40. What is a risk state?

A risk state is a simple label created from demo backlog, latency, forecast variance and delayed run rules. The labels are Normal, Elevated, At risk and Critical. They are not Elexon alerts or service commitments.

### 41. What is a threshold?

A threshold is a comparison reference used to identify a state or trigger an investigation. The project thresholds are invented for readability and must not be called BSC limits, Elexon limits or SLAs.

### 42. What is time to threshold?

It is the distance from the current queue to a demo reference divided by positive net queue growth. If the queue is already above the reference or is shrinking, the project returns no estimate because the calculation would be misleading.

### 43. What is a queue model?

A queue model represents how open work changes over time. The project uses current queue plus arrivals minus processing capacity. It is useful for a transparent sensitivity calculation and is too simple to be a production forecast.

### 44. What is sensitivity analysis?

Sensitivity analysis changes one or more assumptions and observes how the result changes. The scenario page changes demand, historic resubmission throttling, reserved capacity and horizon.

### 45. What is a hypothesis?

A hypothesis is a specific explanation that can be checked against evidence. For example, “arrivals are exceeding processing” can be tested by comparing rates. A hypothesis is not a conclusion until the evidence and limitations are considered.

### 46. What is descriptive analysis?

Descriptive analysis explains what changed in the available sample. The dashboard uses it for arrivals, processed work, queue, latency and forecast differences.

### 47. What is predictive analysis?

Predictive analysis estimates what may happen under stated assumptions. The project only makes a conditional queue projection and labels it clearly.

### 48. What is prescriptive analysis?

Prescriptive analysis considers possible actions. The improvement register contains options to assess with service owners. It does not authorise throttling, prioritisation or capacity changes.

### 49. What is reconciliation between Python and SQL?

It means checking that the same total calculated by Python agrees with the total returned by SQLite. This protects against a reporting query silently disagreeing with the source rows.

### 50. Why use SQLite?

SQLite is a small local relational database included with Python. It keeps the project easy to run and makes grouped SQL queries inspectable without adding a database service.

### 51. What is a CSV file?

A CSV file stores rows and columns as comma separated text. The generator writes the synthetic registration and scheduled run files in this format.

### 52. What is JSON?

JSON is a structured text format used for API responses, configuration and validation reports. The demo threshold settings are stored in JSON.

### 53. What is data freshness?

Data freshness is how recently the underlying source was updated. Before using a real alert, I would check freshness so that an old queue value is not mistaken for the current state.

### 54. What is data lineage?

Data lineage records where a value came from and how it was transformed. In this project the lineage is simple: generator, validation, SQLite query, local API and browser chart. A production service would need confirmed source lineage.

### 55. What is an SLA?

An SLA is a service level agreement. The dashboard does not contain Elexon SLAs. Its thresholds are demonstration references only.

### 56. What is root cause analysis?

Root cause analysis investigates the underlying reason for a problem. The project structures questions that could support it, but does not claim the root cause of the DCP incident because the public Circular does not provide that evidence.

### 57. What is a critical workload?

A critical workload is work linked to an important deadline or service outcome. In this project the critical indicators and scheduled run outcomes are synthetic. A real definition would need agreement with service owners.

### 58. What is human in the loop?

It means that an analyst and authorised owner remain responsible for interpretation and action. Code can calculate and highlight. People must confirm evidence, customer impact, rules, communication and decisions.

## Part three: short formula examples

### Queue example

Previous queue 100, arrivals 20, processed 15.

New queue = 100 + 20 minus 15 = 105.

### Forecast example

Actual 120, forecast 100.

Forecast variance = `(120 minus 100) / 100 = 0.20`, or 20 percent.

### Time to threshold example

Current queue 100, demo threshold 300, arrivals 15 per hour, processed 5 per hour.

Net growth = 10 per hour.

Time to demo threshold = `(300 minus 100) / 10 = 20 hours`.

### Scenario example

If projected arrivals are 31 per hour and available capacity is 20 per hour, net queue growth is 11 per hour. Over 24 hours, a starting queue of 602 becomes approximately 866 before rounding and display rules. The result is conditional on steady rates.

## Final answer pattern

When unsure, use this structure:

“In this project, the measure means ____. I calculate it using ____. It helps answer ____. The limitation is ____. With real Elexon data, I would confirm ____ with the service owner.”

