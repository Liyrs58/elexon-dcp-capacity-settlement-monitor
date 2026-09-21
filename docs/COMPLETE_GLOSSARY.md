# Complete glossary

This glossary uses plain language first and then gives the project meaning. Generic technical terms refer to the code in this repository. Elexon terms refer to the sources in `docs/evidence-register.md`.

## Elexon and Settlement terms

### Elexon

The company that administers the Balancing and Settlement Code arrangements in Great Britain. In this project it is the organisation whose public Circular provides the case context.

### BSC

The Balancing and Settlement Code. It sets rules for electricity market and Settlement arrangements. The project uses the BSC context to frame service obligations and customer impact, not to create new rules.

### Settlement

The process that calculates the financial position associated with electricity market activity. The project treats Settlement timing as an operational dependency described by the Circular.

### Payment run

A scheduled process associated with payments. The synthetic data includes illustrative payment critical runs so the analyst can test how timing context would be monitored.

### DCP

The Data and Calculations Platform. The Circular describes an incident affecting DCP and says it is one of the SVAA supporting services used to calculate Settlement. The public material does not disclose its lower level architecture.

### SVAA

Supplier Volume Allocation Agent. The public service description explains its role in the Settlement process. This project uses the term to understand context and does not model the real service.

### MSID Pair

A Metering System Identifier Pair used in the registration context described by Elexon. The dashboard uses “new MSID Pair” as a synthetic workload name.

### AMSID Pair

An Asset Metering System Identifier Pair used in the flexible asset registration context. The dashboard uses “new AMSID Pair” as a synthetic workload name.

### VLP

Virtual Lead Party. It is a participant role in the flexibility registration context. Synthetic participant types use the label for segmentation only.

### VTP

Virtual Trading Party. It is a participant role in the flexibility registration context. Synthetic participant types use the label for segmentation only.

### AMVLP

Asset Metering Virtual Lead Party. It is a participant role in the registration context. Synthetic participant types use the label for segmentation only.

### FMAR

Flexibility Market Asset Registration. It is a separate public design and implementation programme. The project uses the consultation and API documents as context for future registration design. It is not presented as a confirmed fix for the Circular incident.

### NESO

National Energy System Operator. The public Circular names NESO among the stakeholders Elexon was working with. The project does not model NESO operations.

### MHHS

Market wide Half Hourly Settlement. It is a wider Settlement programme that appears in Elexon context. It is not required for the synthetic queue calculations.

## Operational analytics terms

### Arrival rate

How much work enters a service per unit of time. Here it is the hourly sum of received submissions.

### Throughput

How much work completes per unit of time. Here it is the hourly sum of processed submissions.

### Backlog

Work that has arrived but has not completed. Here it is reconciled by participant and workload.

### Queue growth

Arrivals minus processed work. Positive growth means open work increases under the selected definitions.

### Latency

Time associated with processing. Here it is a synthetic minutes field used for trend and alert demonstrations.

### Forecast

A submitted expectation of future volume. Here it is generated for comparison and does not represent a real participant forecast.

### Forecast variance

The relative difference between actual and forecast volume. It is a descriptive comparison in the generated sample.

### Failure rate

Validation failures divided by received work. It is a quality signal, not a root cause.

### Retry rate

Retries divided by received work. It is a rework signal, not proof of an interface fault.

### Workload segmentation

Splitting results by participant, participant type, submission type or time window so the next investigation is specific.

### Risk state

A four level label made from demo thresholds. It communicates the sample state and does not represent an Elexon alert.

### Threshold

A comparison reference. The repository thresholds are synthetic and editable.

### Sensitivity

How much a result changes when an assumption changes. The scenario page demonstrates sensitivity to demand, throttling and reserved capacity.

### Scenario

A conditional calculation using explicit assumptions. It is not a forecast unless its assumptions and validation support that use.

### Descriptive analysis

What happened in the supplied sample.

### Predictive analysis

What may happen under a stated model. The project only makes a conditional queue projection.

### Prescriptive analysis

Options that could be assessed by an authorised owner. The improvement register contains options, not instructions.

### Root cause

The underlying reason for an observed problem. The Circular does not reveal a lower level DCP root cause, so this project does not claim one.

## Data and software terms

### Synthetic data

Data made for demonstration rather than collected from live operations. Every participant and operational value in this project is synthetic.

### Fixed seed

A fixed random seed that makes generated data repeatable. The generator uses seed `20260914`.

### CSV

Comma separated values. It stores the generated interval and run files.

### SQLite

A small local relational database. The store loads the generated files into SQLite so SQL queries can reproduce the dashboard measures.

### SQL

Structured Query Language. The project uses it for grouped totals, forecast comparisons and run records.

### Python

The language used for generation, validation, calculations, storage and the local web server.

### API

An interface that returns data to another program. The local server provides routes such as `/api/overview` and `/api/scenario`. These are project routes, not Elexon private APIs.

### JSON

A structured text format used for API responses and demo threshold configuration.

### Power BI export

CSV and JSON files arranged for a possible Power BI model. They are an optional presentation layer and do not add live telemetry.

### Validation

Checks that data has the expected structure, types, categories, timestamps, identities and arithmetic relationships before analysis.

### Reconciliation

Checking that two representations agree. The tests reconcile Python totals with SQLite totals and check the backlog roll forward.

### Test

An automated check of an expected property. The project tests calculations, data generation, validation, SQL and store behaviour.

### Deterministic service note

A template filled by code from the current generated state. It is not generated by a language model and must not be sent as a live operational message.

### Human in the loop

The analyst decides what evidence is credible, checks the service context, confirms customer impact and obtains owner approval before action. Code supports those steps but does not replace them.

