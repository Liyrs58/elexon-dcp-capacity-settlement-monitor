# Technical masterclass

## Service intelligence as a chain

A credible operational analysis has five layers.

1. **Context** explains the service, rule, customer and deadline.
2. **Control** checks whether the data is complete, timely and internally consistent.
3. **Detection** measures changes in arrivals, completion, queue, latency and quality.
4. **Investigation** compares segments and tests explanations.
5. **Communication** gives confirmed facts, uncertainty, ownership and next action.

This project keeps those layers separate. The public Circular supplies context. The generator supplies a repeatable exercise. Validation supplies control. SQL and Python supply detection and investigation. The interface and note template supply communication.

## Why the queue model is useful

At its simplest, a queue changes by incoming work minus completed work. That identity is understandable, testable and useful for an early warning. It becomes a forecast only when rates, seasonality, dependencies, recovery behaviour and data quality are credible.

The project therefore calls the page a scenario analysis. It does not call it a production forecast.

## Why the evidence boundary matters

The Circular confirms a service problem and its broad operational context. It does not give private telemetry or a lower level technical explanation. A technically impressive answer that invents a database or API bottleneck would be weaker than a modest answer that states exactly what the evidence supports.

## Why segmentation matters

Aggregates can hide concentration. Participant and workload segmentation helps decide where to request evidence. It should not be used to blame a participant without definitions, comparable exposure, workload effort and owner review.

## Why simple tests beat false precision

The repository has a fixed seed, queue checks, arithmetic tests and Python to SQL reconciliation. These controls demonstrate reliability of the exercise. They do not create operational truth. That distinction is the technical judgement the project is designed to show.

