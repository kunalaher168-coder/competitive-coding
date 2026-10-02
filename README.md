# Competitive Programming and Technical QA Portfolio

Public, independently reconstructed examples of algorithm design, testing, and technical review. These examples show methods used in private work without reproducing task statements, evaluation materials, source assets, or client information.

## Demonstrations

| Example | Skill shown | Method | Complexity |
| --- | --- | --- | --- |
| [One-use travel pass](examples/travel_pass.py) | Stateful shortest path | Dijkstra over `(vertex, pass_used)` | `O((V + E) log V)` |
| [Tree distance totals](examples/tree_distance_totals.py) | Tree dynamic programming | Subtree sizes and rerooting | `O(V)` |
| [Distinct-value window](examples/distinct_window.py) | Sliding window | Frequency map and two pointers | `O(N)` |
| [Single-server scheduler](examples/job_scheduler.py) | Event simulation | Heap by arrival time, deterministic tie rules | `O(N log N)` |
| [Dependency planner](examples/dependency_planner.py) | Graph validation | Kahn topological ordering and cycle detection | `O(V + E)` |

All examples use Python 3.10+ and the standard library. Each has a small command-line interface that accepts JSON on standard input and writes JSON on standard output.

```powershell
python -m unittest discover -s tests -v
echo '{"vertices": 3, "edges": [[0, 1, 8], [1, 2, 6]], "source": 0, "target": 2}' | python examples/travel_pass.py
```

## Work represented

- Graph algorithms: shortest paths with state, priority queues, graph traversal, and reachability.
- Tree algorithms: traversal, aggregate queries, dynamic programming, and rerooting.
- Array algorithms: sliding windows, prefix aggregates, two pointers, and boundary cases.
- Simulation and ordering: event handling, deterministic rules, dependency graphs, and cycle detection.
- Quality engineering: independent expected results, edge-case design, adversarial test coverage, and clear explanations.
- Technical review: multi-file trace inspection, reproducible defect descriptions, and evidence-based recommendations.
- Visual review workflow: frame selection and contact-sheet inspection using synthetic or authorized material only.

The [design notes](CASE_STUDIES.md) explain each example. The [work-sample notes](WORK_SAMPLES.md) explain the public scope. Original client materials stay private. No acceptance score, production deployment, or client endorsement is claimed here.

## Repository layout

```text
examples/       Independent Python implementations
tests/          Standard-library tests, including small brute-force checks
WORK_SAMPLES.md Anonymized work summary and publication boundaries
CASE_STUDIES.md Correctness arguments and test strategy
.github/       Automated test workflow
PROFILE_SNIPPET.md Short text for a GitHub profile or pinned repository
```

## Verification

Run the test command above. The tests compare selected implementations against independent brute-force models on small inputs and check explicit edge cases.
