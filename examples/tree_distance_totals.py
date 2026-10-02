"""Sum of distances from every vertex in an undirected tree."""

from __future__ import annotations

import json
import sys


def distance_totals(vertices: int, edges: list[list[int]]) -> list[int]:
    """Return one distance sum per vertex in O(V) time and space."""
    if vertices < 1 or len(edges) != vertices - 1:
        raise ValueError("expected a nonempty tree with V-1 edges")

    graph: list[list[int]] = [[] for _ in range(vertices)]
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("each edge needs two endpoints")
        u, v = edge
        if not 0 <= u < vertices or not 0 <= v < vertices or u == v:
            raise ValueError("invalid tree edge")
        graph[u].append(v)
        graph[v].append(u)

    parent = [-1] * vertices
    parent[0] = 0
    depth = [0] * vertices
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -1:
                raise ValueError("edges contain a cycle")
            parent[neighbor] = vertex
            depth[neighbor] = depth[vertex] + 1
            order.append(neighbor)
    if len(order) != vertices:
        raise ValueError("edges are disconnected")

    subtree = [1] * vertices
    for vertex in reversed(order[1:]):
        subtree[parent[vertex]] += subtree[vertex]

    total = [0] * vertices
    total[0] = sum(depth)
    for vertex in order[1:]:
        total[vertex] = total[parent[vertex]] + vertices - 2 * subtree[vertex]
    return total


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(distance_totals(**data)))
