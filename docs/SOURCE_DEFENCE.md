# Source defence

## Public incident sources

### Circular EL04799

Source: [Temporary pause on new MSID and AMSID Pair submissions](https://elexonexternal.newsweaver.com/924j6pkkru/1gsurqf0ylu)

Status: verified public source, dated 14 September 2026.

Supports: DCP incident, downstream Settlement and payment run delays, increased MSID and AMSID Pair submissions, demand above submitted forecasts, DCP at or near maximum capacity and temporary submission controls.

Does not support: a database, CPU, server, network, API or other lower level cause; named customer impact; internal thresholds; or a claim that forecasting caused the incident.

### Newscast 1135

Source: [Elexon Newscast item](https://elexonexternal.newsweaver.com/1gmbg04lik/1guzn2hox2r)

Status: verified public context.

Supports: the public announcement context and link to the Circular.

## Service and programme sources

### SVAA service description

Source: [SVA and SSA BSC service description](https://bscdocs.elexon.co.uk/service-descriptions/sva-ssa-bsc-service-description)

Status: verified public source.

Supports: high level service context for SVAA and Settlement. It does not provide private DCP telemetry.

### DCP demand survey

Source: [Help shape the Data and Calculation Platform requirements](https://www.elexon.co.uk/bsc/article/help-shape-the-data-and-calculation-platform-requirements/)

Status: verified public source.

Supports: public evidence that future demand and requirements were being considered. It does not provide the generated values in this project.

### FMAR consultation

Source: [FMAR design and implementation consultation](https://www.elexon.co.uk/flexibility-markets/consultation/fmar-design-implementation-consultation/)

Status: verified public source.

Supports: public programme context. It does not prove that FMAR fixes the Circular incident.

### FMAR API documentation

Source: [FMAR API documentation version 0.6](https://fmar-elexon.github.io/fmar-api/docs/v0.6/)

Status: verified public technical documentation supplied for the case context.

Supports: public design and interface context for FMAR. It does not reveal DCP internal architecture or live operational data.

## Project generated sources

### Synthetic generator

Source: `src/service_intel/generator.py`.

Status: synthetic assumption.

Supports: every generated participant, timestamp, workload, forecast, queue, latency, failure, retry and run value in the dashboard.

### Demo thresholds

Source: `config/demo_thresholds.json` and `src/service_intel/analysis.py`.

Status: synthetic assumption.

Supports: the four displayed demo states only. They are not Elexon limits, BSC limits or service level commitments.

### Scenario model

Source: `src/service_intel/analysis.py`.

Status: conditional calculation.

Supports: sensitivity comparisons under explicit steady rate assumptions. It is not a production forecast.

## Claim handling rule

If a sentence cannot be placed in one of these source categories, remove it or rewrite it as a question for the service owner.

