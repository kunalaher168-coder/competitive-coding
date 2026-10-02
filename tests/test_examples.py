"""Independent small-input checks for the public algorithm examples."""

from __future__ import annotations

import itertools
import random
import sys
import unittest
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from dependency_planner import plan
from distinct_window import longest_window
from job_scheduler import schedule
from travel_pass import cheapest_route
from tree_distance_totals import distance_totals


class TravelPassTests(unittest.TestCase):
    def test_edges_and_unreachable(self) -> None:
        self.assertEqual(cheapest_route(3, [[0, 1, 8], [1, 2, 6]], 0, 2), 10)
        self.assertEqual(cheapest_route(2, [], 0, 1), -1)
        self.assertEqual(cheapest_route(1, [], 0, 0), 0)
        with self.assertRaises(ValueError):
            cheapest_route(2, [[0, 1, -1]], 0, 1)

    def test_against_bellman_ford(self) -> None:
        rng = random.Random(104)
        for vertices in range(1, 7):
            for _ in range(40):
                edges = [[u, v, rng.randrange(10)] for u in range(vertices) for v in range(vertices) if rng.randrange(3) == 0]
                source, target = rng.randrange(vertices), rng.randrange(vertices)
                distance = [float("inf")] * (2 * vertices)
                distance[source] = 0
                expanded = []
                for u, v, weight in edges:
                    expanded.extend(((u, v, weight), (u, v + vertices, weight // 2), (u + vertices, v + vertices, weight)))
                for _ in range(2 * vertices - 1):
                    for u, v, weight in expanded:
                        distance[v] = min(distance[v], distance[u] + weight)
                expected = min(distance[target], distance[target + vertices])
                self.assertEqual(cheapest_route(vertices, edges, source, target), -1 if expected == float("inf") else expected)


class TreeDistanceTests(unittest.TestCase):
    def test_path_and_invalid_graph(self) -> None:
        self.assertEqual(distance_totals(4, [[0, 1], [1, 2], [2, 3]]), [6, 4, 4, 6])
        self.assertEqual(distance_totals(1, []), [0])
        with self.assertRaises(ValueError):
            distance_totals(4, [[0, 1], [1, 2], [2, 0]])

    def test_against_breadth_first_search(self) -> None:
        rng = random.Random(271)
        for vertices in range(1, 30):
            edges = [[vertex, rng.randrange(vertex)] for vertex in range(1, vertices)]
            graph = [[] for _ in range(vertices)]
            for u, v in edges:
                graph[u].append(v)
                graph[v].append(u)
            expected = []
            for root in range(vertices):
                distance = [-1] * vertices
                distance[root] = 0
                queue = deque([root])
                while queue:
                    u = queue.popleft()
                    for v in graph[u]:
                        if distance[v] < 0:
                            distance[v] = distance[u] + 1
                            queue.append(v)
                expected.append(sum(distance))
            self.assertEqual(distance_totals(vertices, edges), expected)


class DistinctWindowTests(unittest.TestCase):
    def test_boundaries(self) -> None:
        self.assertEqual(longest_window([], 2), {"start": 0, "end": 0, "length": 0})
        self.assertEqual(longest_window([1, 2, 3], 0), {"start": 0, "end": 0, "length": 0})
        self.assertEqual(longest_window([1, 2, 1, 3, 3], 2), {"start": 0, "end": 3, "length": 3})
        with self.assertRaises(ValueError):
            longest_window([], -1)

    def test_against_exhaustive_windows(self) -> None:
        rng = random.Random(919)
        for size in range(9):
            for _ in range(40):
                values = [rng.randrange(4) for _ in range(size)]
                limit = rng.randrange(5)
                candidates = [(end - start, -start, start, end) for start in range(size + 1) for end in range(start, size + 1) if len(set(values[start:end])) <= limit]
                length, _, start, end = max(candidates)
                self.assertEqual(longest_window(values, limit), {"start": start, "end": end, "length": length})


class SchedulerTests(unittest.TestCase):
    def test_idle_time_and_ties(self) -> None:
        jobs = [[5, 3], [5, 1], [5, 1], [10, 2]]
        self.assertEqual(schedule(jobs), [
            {"job": 1, "start": 5, "finish": 6},
            {"job": 2, "start": 6, "finish": 7},
            {"job": 0, "start": 7, "finish": 10},
            {"job": 3, "start": 10, "finish": 12},
        ])
        self.assertEqual(schedule([]), [])
        with self.assertRaises(ValueError):
            schedule([[0, -1]])

    def test_against_direct_selection(self) -> None:
        rng = random.Random(488)
        for size in range(10):
            for _ in range(30):
                jobs = [[rng.randrange(8), rng.randrange(5)] for _ in range(size)]
                remaining = set(range(size))
                expected = []
                time = 0
                while remaining:
                    available = [index for index in remaining if jobs[index][0] <= time]
                    if not available:
                        time = min(jobs[index][0] for index in remaining)
                        available = [index for index in remaining if jobs[index][0] <= time]
                    index = min(available, key=lambda item: (jobs[item][1], item))
                    start = time
                    time += jobs[index][1]
                    expected.append({"job": index, "start": start, "finish": time})
                    remaining.remove(index)
                self.assertEqual(schedule(jobs), expected)


class DependencyPlannerTests(unittest.TestCase):
    def test_cycle_and_duplicate_edge(self) -> None:
        self.assertEqual(plan(["a", "b"], [["a", "b"], ["a", "b"]]), {"order": ["a", "b"], "blocked": []})
        self.assertEqual(plan(["a", "b", "c"], [["a", "b"], ["b", "a"], ["b", "c"]]), {"order": [], "blocked": ["a", "b", "c"]})
        with self.assertRaises(ValueError):
            plan(["a", "a"], [])

    def test_against_permutations(self) -> None:
        rng = random.Random(731)
        for size in range(1, 6):
            tasks = [chr(97 + i) for i in range(size)]
            for _ in range(20):
                dependencies = [[tasks[i], tasks[j]] for i in range(size) for j in range(i + 1, size) if rng.randrange(2)]
                valid = []
                for order in itertools.permutations(tasks):
                    position = {task: index for index, task in enumerate(order)}
                    if all(position[before] < position[after] for before, after in dependencies):
                        valid.append(list(order))
                self.assertEqual(plan(tasks, dependencies), {"order": min(valid), "blocked": []})


if __name__ == "__main__":
    unittest.main()
