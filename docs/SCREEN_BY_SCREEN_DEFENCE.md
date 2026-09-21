# Screen by screen defence

Use this guide to walk through the dashboard in a clear order. The first four screens make the shortest interview story. The remaining screens show how the analyst controls evidence and communicates carefully.

## 1. Overview: Is the demo queue under pressure?

Purpose: give a service owner a compact view of current sample state.

What to point to:

1. Demo service state is a label from synthetic thresholds.
2. Open registration queue is the latest generated backlog.
3. Latest hour throughput is completed generated work.
4. Forecast variance compares generated actuals with generated forecast.
5. Synthetic runs delayed gives timing context for illustrative Settlement and payment runs.
6. Arrivals versus processed shows whether incoming work is above completion.
7. Queue and latency shows accumulated work beside processing time.
8. Scheduled runs gives a small table of timing records.
9. Validation and retries shows quality signals.

Defence answer: “I start with the measures that tell me whether work is arriving faster than it is completing, then I add backlog, latency and scheduled run context. Every value here is synthetic, so the screen demonstrates the structure of a service review rather than reporting Elexon operations.”

What not to say: “This shows the actual DCP state.”

## 2. Drivers and forecast: Which workloads are driving the queue?

Purpose: decide where an analyst should investigate first.

Charts and tables:

1. Forecast variance bars rank synthetic participant and workload segments by positive actual minus forecast volume.
2. Questions before acting keeps the investigation focused on concentration, throughput, rework and deadlines.
3. Segment investigation gives actual, forecast, variance, peak queue and retries.

Defence answer: “A large positive difference is a prioritisation signal for investigation. It is not blame and it does not establish why a forecast differed.”

## 3. Scenario analysis: What happens if demand changes?

Purpose: show sensitivity to explicit assumptions.

Controls:

1. New pair demand increase changes new workload arrivals.
2. Historic resubmissions throttled reduces historic resubmission arrivals.
3. Capacity reserved outside the registration queue reduces demo registration capacity.
4. Projection horizon changes the number of hours applied.

Outputs:

1. Starting backlog.
2. Projected backlog.
3. Net queue growth per hour.
4. Time to the demo alert reference where the calculation is valid.
5. A queue projection chart.

Defence answer: “This is a steady rate queue calculation. It helps compare trade offs, but it does not forecast a real service or decide whether throttling is allowed.”

## 4. Hypothesis tests: Which explanations fit the sample?

Purpose: show disciplined investigation logic.

Each card gives the question, why it matters, method, result, conclusion, confidence, limitation and next check. The cards test demand against processing, forecast difference, workload concentration, historic resubmissions, capacity alone and priority context.

Defence answer: “The conclusion is limited to the generated sample. The next check always moves back to agreed definitions and real telemetry.”

## 5. Customer impact: Who could be affected?

Purpose: translate service measures into customer and Settlement questions.

What to point to:

1. Possible affected groups are described without inventing named customers.
2. Settlement and payment impact is framed as a question about delayed supporting activity.
3. Customer action says to confirm any instruction with the authorised owner.
4. Next owner and next update are explicit handoff points.
5. Evidence to request gives throughput, quality, dependencies and recovery questions.

Defence answer: “I would not send a customer message from the dashboard alone. I would confirm the affected service, dates, customer action and next update with the incident owner.”

## 6. Improvement register: What should be tested with the service owner?

Purpose: turn observations into controlled improvement questions.

Every row has a problem, proposed action, benefit, risk, measure and status. Examples include rolling forecasts, earlier queue warning, scheduling non critical historic resubmissions and retaining incident knowledge.

Defence answer: “The register records options for review. It does not claim that Elexon should implement a particular control.”

## 7. Analyst approach: How would I investigate?

Purpose: show alignment with the Service Analyst role.

The sequence is service question, BSC context, evidence validation, impact measurement, segmentation, hypothesis tests, communication, recovery monitoring and learning.

Defence answer: “The sequence protects operational accuracy. I understand the service and deadline before I interpret a number, and I keep an authorised owner in the decision loop.”

## 8. Service note: How would I write the update?

Purpose: demonstrate concise operational communication.

The note is assembled by deterministic template logic. It states the synthetic state, the generated investigation lead and the checks still needed. The page warns that it is not an operational update.

Defence answer: “The value is the structure of the note: confirmed facts, current signal, investigation lead, customer checks and next update. The figures must be replaced with verified data before sending.”

## 9. Evidence and limits: What is known, and what still needs evidence?

Purpose: keep evidence boundaries visible.

The three columns separate public statements, unknown internal information and checks that would be appropriate if telemetry were available. The validation panel shows whether the generated dataset passed controls. The operational ideas section contains options to assess.

Defence answer: “This is the page I use to stop the project overclaiming. The Circular supports the service pressure story, but not a database, CPU, server, API or architecture explanation.”

## Recommended walkthrough order

1. Overview.
2. Drivers and forecast.
3. Scenario analysis.
4. Evidence and limits.
5. Customer impact.
6. Service note.

The hypothesis and improvement pages can be opened when the interviewer asks for more detail.

