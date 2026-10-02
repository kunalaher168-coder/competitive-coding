"""Deterministic, non-preemptive single-server job scheduler."""

from __future__ import annotations

import heapq
import json
import sys


def schedule(jobs: list[list[int]]) -> list[dict[str, int]]:
    """Schedule by shortest duration, then input index, among arrived jobs.

    Each job is [arrival_time, duration]. Returns records in execution order.
    """
    for job in jobs:
        if len(job) != 2 or job[0] < 0 or job[1] < 0:
            raise ValueError("jobs require nonnegative arrival and duration")

    arrivals = sorted((arrival, index, duration) for index, (arrival, duration) in enumerate(jobs))
    ready: list[tuple[int, int]] = []
    result: list[dict[str, int]] = []
    time = 0
    next_arrival = 0

    while next_arrival < len(arrivals) or ready:
        if not ready and next_arrival < len(arrivals):
            time = max(time, arrivals[next_arrival][0])
        while next_arrival < len(arrivals) and arrivals[next_arrival][0] <= time:
            _, index, duration = arrivals[next_arrival]
            heapq.heappush(ready, (duration, index))
            next_arrival += 1
        duration, index = heapq.heappop(ready)
        start = time
        time += duration
        result.append({"job": index, "start": start, "finish": time})
    return result


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(schedule(**data)))
