# Interview defence handbook

## The central answer

“I used Elexon’s 14 September 2026 Circular as a public case. It reports DCP capacity pressure associated with MSID and AMSID Pair submissions above submitted forecasts and delayed Settlement and payment runs. I built a local monitor with synthetic data to show how a Service Analyst could control the evidence, compare arrivals with processing, identify workload differences, test simple queue scenarios and prepare a careful service note. I have not claimed access to Elexon telemetry or a private technical root cause.”

## Twenty questions and truthful answers

1. **Why did you choose this case?**

Because it connects service reliability, data pressure, Settlement timing, customer communication and future demand planning in one public example.

2. **What is DCP?**

The public material describes it as a Data and Calculations Platform and an SVAA supporting service used in Settlement. I do not claim to know its internal architecture.

3. **What is the first signal you would check?**

I would agree definitions first, then compare arrivals with completed work over a consistent window. A positive difference suggests queue pressure.

4. **Why use backlog?**

It shows accumulated open work. It is more useful when read with arrivals, throughput, age, latency and deadlines.

5. **What is forecast variance?**

Actual minus forecast divided by forecast, where the forecast is positive. In this project it is synthetic and descriptive.

6. **Does a forecast miss prove forecasting caused the incident?**

No. It shows a difference in the sample. It does not prove why the difference occurred or that forecasting caused a real incident.

7. **Why not use machine learning?**

The interview question is about transparent service intelligence. Deterministic measures are easier to validate and explain with limited public data.

8. **What does the scenario model assume?**

Steady hourly arrivals and processing capacity. It excludes recovery surges, seasonality, dependency delays and unknown constraints.

9. **What would you need before throttling work?**

Confirmed service rules, affected customer analysis, workload priority, owner approval, communication and a measured rollback or recovery plan.

10. **Could FMAR fix the incident?**

I would not say that. FMAR is a separate public registration design programme. Its future effect on demand or DCP is an open question.

11. **How did you validate the data?**

The validation layer checks structure, types, categories, timestamps, duplicates, forecast coverage, actual versus received counts, queue reconciliation and fixed seed reproduction.

12. **Why use both Python and SQL?**

Python creates and validates the sample. SQLite provides reproducible grouped reporting. A test checks that totals agree.

13. **What does a passing test mean?**

That the code follows its stated rule. It does not prove the rule is the Elexon production rule.

14. **Which result is most useful?**

The combination of arrivals, processing, queue and scheduled run context. One number alone can mislead.

15. **How would you investigate a concentrated workload?**

Check definitions, volume, retries, validation failures, processing effort and time alignment, then confirm with the service owner before making any judgement.

16. **How would you communicate during an incident?**

State confirmed facts, current impact, uncertainty, customer action if authorised, owner and next update time.

17. **What is not in the project?**

Live data, private APIs, internal capacity limits, named customer impact and an asserted lower level root cause.

18. **What did you personally contribute?**

Problem framing, evidence boundaries, metrics, synthetic model, scenario logic, tests, interpretation and interface review. AI tools helped implement and debug.

19. **What would you improve with real data?**

Agree metric definitions, add freshness and lineage, measure queue age, map service objectives to deadlines, test alert lead time and review false alerts with owners.

20. **What is the main lesson?**

An analyst can make an operational problem clearer without pretending to know more than the evidence supports.

