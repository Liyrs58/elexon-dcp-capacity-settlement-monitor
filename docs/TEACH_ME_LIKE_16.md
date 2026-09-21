# Teach me like I am 16

Imagine a school canteen.

Students arrive with lunch requests. Staff complete requests. If more requests arrive than staff can complete, unfinished requests form a queue.

In this project:

1. Arrivals are new lunch requests.
2. Throughput is requests completed.
3. Backlog is unfinished requests.
4. Latency is how long a request takes.
5. Forecast is how many requests the canteen expected.
6. Forecast variance is the difference between expected and actual requests.
7. A retry is a request that has to be attempted again.
8. A scheduled run is an important delivery that must finish by a time.

The Circular is like a notice saying the canteen system was under pressure, demand was higher than expected and some important deliveries were late. It does not say whether the problem was the kitchen, the ordering screen, the staff rota or something else.

The dashboard asks five simple questions:

1. Is more work arriving than can be completed?
2. Is the queue getting bigger?
3. Which type of request is contributing most?
4. What might happen if demand rises or some less urgent work is scheduled later?
5. What must be confirmed before telling customers anything?

The data is made up for practice. It is like a school exercise using invented lunch orders. It helps show the method but cannot tell us what really happened inside Elexon.

## The most important idea

A chart is evidence for a question, not an answer to every question. If the queue is growing, we know the sample has more incoming work than completed work. We do not automatically know why.

