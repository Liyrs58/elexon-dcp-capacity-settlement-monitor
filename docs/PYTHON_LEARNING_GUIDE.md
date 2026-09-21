# Python learning guide

## Data generation

`generator.py` uses a seeded random number generator so the same inputs produce the same sample. It loops through hours, participants and workloads. It creates a forecast, an actual arrival count and a processing allocation, then calculates the next backlog.

The seed is a reproducibility control, not a claim about the real event.

## Validation

`validation.py` uses sets for required columns and allowed categories, a dictionary for previous queue values, a set for duplicate identities and standard numeric checks for finite values.

The validation function returns a report dictionary. The store blocks publication if the status is `BLOCKED`.

## Analysis functions

`forecast_variance` demonstrates a safe denominator check.

`estimate_hours_to_threshold` demonstrates a domain guard. A time estimate is meaningless when the queue has already crossed the reference or is shrinking.

`alert_state` demonstrates ordered rules. Critical is checked before At risk, then Elevated, then Normal.

`project_queue` demonstrates a small scenario model. It clamps throttle, reserve and multiplier inputs to sensible demo ranges, calculates arrivals and available capacity, then projects the queue.

## Store and server

`store.py` uses SQLite connections inside short lived contexts for queries. This keeps the local app simple and avoids leaving file handles open.

`server.py` uses standard library HTTP handling. Each API route maps to a store method and returns JSON. The route names are visible in the tests and in the browser network requests.

## Python concepts worth practising

1. Lists hold rows.
2. Dictionaries hold one record or a JSON response.
3. Dataclasses hold threshold settings.
4. Functions keep calculations reusable.
5. Type hints document expected inputs.
6. Exceptions prevent malformed input from being treated as valid.
7. Context managers close database resources.
8. Unit tests check small behaviours without opening the browser.

## How to defend using AI tools

“I used Cursor and Codex as implementation and debugging assistance. I owned the case framing, evidence boundary, metric definitions, scenario assumptions, interpretation and review of the outputs. I can trace each displayed number through the generator, validation, SQL or Python function and the browser route.”

