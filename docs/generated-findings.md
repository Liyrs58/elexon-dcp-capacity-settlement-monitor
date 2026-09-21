# Generated findings

These figures were calculated from the fixed seed `20260914` on 21 September 2026. They are synthetic demonstration results.

The sample has 6,048 interval rows and 28 scheduled run rows.
The latest generated state is At risk with backlog 602, 24 hour backlog change +158, arrivals 26.58 per hour and processing 20.00 per hour.

| Hypothesis | Result | Conclusion |
| --- | --- | --- |
| H1 | Late sample net queue growth is 0.20 records per row. | Supported in this synthetic sample. |
| H2 | Actual demand is +22.3% against the generated forecast. | Supported as a leading signal in this demonstration. |
| H3 | new MSID Pair contributes 40.1% of positive excess demand. | Supported for new MSID Pair. |
| H4 | Historic resubmissions total 1,295 records in the sample. | Worth testing as a control option, not proven as a cause. |
| H5 | The sample contains 2 delayed scheduled run records. | Scenario testing is needed; the generated history cannot prove an intervention effect. |
| H6 | A demand rise can still exceed any fixed capacity under the scenario model. | Rejected as a universal answer under sustained growth. |
| H7 | 26 of 28 critical sample runs are on time. | Use prioritisation as a scenario to assess. |

These figures do not describe Elexon operations and do not establish a private cause.
