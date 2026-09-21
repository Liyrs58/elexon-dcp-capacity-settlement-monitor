# Full project audit

## Scope

This audit covers the local DCP Capacity and Settlement Service Risk Monitor as it existed before the current refinement pass. It covers the Python service, generated data, SQL, tests, web interface, interview documents, source register and Power BI export files.

The project uses the public 14 September 2026 Circular as the operational case. The Circular supports statements about DCP capacity pressure, higher MSID and AMSID Pair submission volumes than submitted forecasts, delayed Settlement and payment runs, and temporary submission controls. It does not disclose a lower level technical cause. The operating data in this repository is synthetic.

## What already works

1. The app starts locally and serves a working dashboard.
2. The public incident boundary is stated in the README, the evidence register and the interface.
3. The generator uses a fixed seed and creates participant, workload, queue, forecast, latency, quality and scheduled run fields.
4. The analysis layer uses arrival rate, processing rate, backlog, latency, forecast variance, delayed run context and a simple queue projection.
5. Validation checks run before publication and can block a changed or inconsistent dataset.
6. Python and SQL totals are reconciled by tests.
7. The interface includes operational views for overview, investigation, scenarios, hypotheses, customer impact, improvement ideas, analyst approach, service note and evidence boundaries.
8. The service note is deterministic and clearly marked as a demonstration.

## Findings by severity

### Critical

#### C1. The project did not yet have a single audit and defence trail

Evidence: the repository had methodology, limitations and interview notes, but no complete audit linking every screen, metric, claim, code path and test to a defence answer.

Action: this file records the baseline. The new defence documents must remain linked from the README so that the project can be reviewed as one coherent case.

#### C2. Synthetic evidence could still be mistaken for operational telemetry

Evidence: the interface labels the sample as synthetic, but the page contains public incident language beside generated state, generated delayed runs and invented alert thresholds.

Risk: a viewer could confuse a demonstration state with the real 14 September event.

Action: keep the synthetic banner visible, label generated values close to their use, and state on every decision oriented page that a real decision needs confirmed telemetry, agreed metric definitions and an authorised owner.

### High

#### H1. The visual language looked like a polished software marketing page

Evidence: dark branded rail, initials mark, interview case study label, rounded cards, pill tags, floating shadows, decorative icons, large hero headings and formula styling.

Risk: the design could look generated or portfolio led rather than like an internal operational tool used by an analyst.

Action: use a lighter navigation area, flatter panels, smaller headings, restrained status labels and denser tables. Keep the information hierarchy and working calculations.

#### H2. The pages did not always lead with a single operational question

Evidence: the original overview and scenario page use phrases such as “read the signals together” and “what this can support” before stating the question being answered.

Risk: an interviewer has to infer why the page exists.

Action: give each page a direct question heading and a short sentence explaining the decision or investigation it supports.

#### H3. Metric defence was distributed across several documents

Evidence: formulas appear in code, README, methodology and interview notes, but not in one place with source, units, calculation window, limits and a worked example.

Risk: Rudra may understand the dashboard but struggle when asked to defend one number precisely.

Action: add a metric defence guide with one entry for every displayed measure.

#### H4. The human decision boundary was present but not prominent enough

Evidence: the service note and evidence page say that owners must confirm impacts and actions, but the main operational pages do not consistently distinguish analysis from an authorised instruction.

Risk: scenario controls or improvement ideas could be read as recommendations to change a live service.

Action: add visible analyst boundary text to scenarios, customer impact, the improvement register and the service note.

#### H5. The teaching material was not yet complete enough for a technical interview

Evidence: the repository had interview notes and a methodology document, but not a screen defence guide, code walkthrough, SQL guide, Python guide, testing defence, complete glossary or technical masterclass.

Risk: the project could be demonstrated without being fully explainable.

Action: add the required teaching documents and keep examples tied to the actual code and synthetic values.

#### H6. Hypothesis conclusions need careful wording

Evidence: H1 to H3 can be supported inside the generated sample because the generator deliberately creates an interpretable pressure pattern.

Risk: words such as “supported” may sound like proof of the Elexon incident or its cause.

Action: retain the calculations but use wording such as “supported in this demonstration” and show the generator limitation beside each result.

### Medium

#### M1. Help text was limited

Evidence: the dashboard has a few explanatory paragraphs, but several labels such as forecast variance, backlog and time to demo alert depend on prior reading.

Action: add concise definitions beside key measures and include a complete glossary.

#### M2. The navigation contained many sections for a short interview demonstration

Evidence: nine page entries are visible at once.

Risk: the viewer may spend time browsing instead of following the operational story.

Action: keep all pages available, but make the first four pages the main walkthrough path and label the remaining pages as evidence and handoff material.

#### M3. Root and documentation copies can drift

Evidence: both the repository root and `docs` contain evidence and interview documents.

Action: keep the root files as convenient entry points, but state which document is canonical and check that both copies have the same claims.

#### M4. The dashboard has no permanent screenshot set in the project record

Evidence: the app can be opened, but a reviewer cannot see the pages without running it.

Action: store before and after browser screenshots under `output/playwright` and link them from the README where useful.

### Low

#### L1. Decorative symbols add little operational meaning

Evidence: navigation symbols, the initials mark and formula chip are visual styling rather than service information.

Action: remove or reduce them while keeping accessible text labels.

#### L2. Some headings use portfolio language

Evidence: examples include “case study”, “signal”, “what this can support” and “read the signals together”.

Action: use plain terms such as “Current service state”, “Scenario assumptions” and “Evidence to confirm”.

#### L3. The interface uses more whitespace and card separation than the data needs

Evidence: several pages place small amounts of text in large rounded panels.

Action: use flatter sections and compact tables where a table is the clearest explanation.

## Evidence boundary review

The following statements are safe when presented with their sources:

1. The Circular reports a DCP incident affecting a supporting Settlement service.
2. Scheduled Settlement and payment services did not complete on time.
3. Elexon identified significantly increased MSID and AMSID Pair submissions and demand above submitted forecasts.
4. DCP was operating at or near maximum capacity.
5. Elexon introduced temporary submission controls while assessing demand and service performance.
6. The Circular does not disclose a lower level technical cause.
7. FMAR is a separate public design and implementation programme and must not be presented as a confirmed fix for this incident.

The following are synthetic or conditional and must stay labelled:

1. Participant identifiers and participant level contributions.
2. Arrival, processing, backlog, latency, failure, retry and forecast values.
3. Demo thresholds and risk states.
4. Scheduled run outcomes in the generated sample.
5. Hypothesis results and scenario projections.
6. Any suggested throttling, prioritisation, reserved capacity or workload isolation option.

## Current audit conclusion

The analytical core is credible for an interview demonstration. The main work is to make the boundary between public fact, synthetic evidence, conditional analysis and authorised action impossible to miss. The visual redesign should make the dashboard feel like a calm internal service review tool. The new teaching documents should make every visible result explainable without inventing Elexon internals.

