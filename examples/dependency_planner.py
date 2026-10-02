"""Stable ordering of tasks subject to directed dependencies."""

from __future__ import annotations

import heapq
import json
import sys


def plan(tasks: list[str], dependencies: list[list[str]]) -> dict[str, object]:
    """Return lexicographically smallest valid order, or unresolved nodes."""
    if len(set(tasks)) != len(tasks):
        raise ValueError("task names must be unique")
    outgoing: dict[str, set[str]] = {task: set() for task in tasks}
    degree = {task: 0 for task in tasks}
    for dependency in dependencies:
        if len(dependency) != 2:
            raise ValueError("each dependency needs predecessor and successor")
        before, after = dependency
        if before not in outgoing or after not in outgoing:
            raise ValueError("dependency names an unknown task")
        if after not in outgoing[before]:
            outgoing[before].add(after)
            degree[after] += 1

    ready = [task for task in tasks if degree[task] == 0]
    heapq.heapify(ready)
    ordered: list[str] = []
    while ready:
        task = heapq.heappop(ready)
        ordered.append(task)
        for successor in outgoing[task]:
            degree[successor] -= 1
            if degree[successor] == 0:
                heapq.heappush(ready, successor)
    if len(ordered) != len(tasks):
        return {"order": [], "blocked": sorted(task for task in tasks if degree[task] > 0)}
    return {"order": ordered, "blocked": []}


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(plan(**data)))
