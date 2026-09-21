# Analyst FAQ

## Why are the values synthetic?

The Circular provides a service level description but not private telemetry. Synthetic values make the method reproducible without implying access to confidential information.

## How do you know the data is valid?

The generator runs checks for structure, types, duplicates, categories, timestamps, forecast coverage, non negative values, backlog reconciliation and fixed seed regeneration.

## Why use SQL?

SQL is a clear way to group the same operational records by time, participant and workload. It also provides an independent check on important Python calculations.

## Why use Python?

Python keeps generation, validation, scenario logic and tests reproducible.

## Why not machine learning?

The public evidence does not provide enough operational history to train and validate a useful model. Transparent calculations are easier to challenge in an interview and safer to interpret.

## What would you ask for in a live setting?

I would ask for agreed definitions, data freshness, arrival and completion counts, queue age, latency, failures, retries, changes, dependencies, affected deadlines, customer impact and recovery measures.

## What did you not determine?

The project does not determine the private DCP architecture, lower level technical cause, real capacity limit or responsibility of any participant.
