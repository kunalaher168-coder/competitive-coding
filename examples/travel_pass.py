"""Minimum travel cost when one edge can be taken at half price."""

from __future__ import annotations

import heapq
import json
import sys


def cheapest_route(vertices: int, edges: list[list[int]], source: int, target: int) -> int:
    """Return minimum cost, or -1 when target is unreachable.

    One directed edge may be discounted to floor(weight / 2). All weights must
    be nonnegative. The pass may remain unused.
    """
    if vertices < 1 or not 0 <= source < vertices or not 0 <= target < vertices:
        raise ValueError("invalid vertex count or endpoint")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    for edge in edges:
        if len(edge) != 3:
            raise ValueError("each edge must contain source, target, weight")
        u, v, weight = edge
        if not 0 <= u < vertices or not 0 <= v < vertices or weight < 0:
            raise ValueError("invalid edge")
        graph[u].append((v, weight))

    infinity = float("inf")
    distance = [[infinity, infinity] for _ in range(vertices)]
    distance[source][0] = 0
    queue: list[tuple[int, int, int]] = [(0, source, 0)]

    while queue:
        cost, vertex, used = heapq.heappop(queue)
        if cost != distance[vertex][used]:
            continue
        if vertex == target:
            return cost
        for neighbor, weight in graph[vertex]:
            ordinary = cost + weight
            if ordinary < distance[neighbor][used]:
                distance[neighbor][used] = ordinary
                heapq.heappush(queue, (ordinary, neighbor, used))
            if not used:
                discounted = cost + weight // 2
                if discounted < distance[neighbor][1]:
                    distance[neighbor][1] = discounted
                    heapq.heappush(queue, (discounted, neighbor, 1))
    return -1


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(cheapest_route(**data)))
