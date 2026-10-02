# Design notes

These examples are original public exercises. Each demonstrates a technique rather than reproducing a private assignment.

## One-use travel pass

**Question.** Find cheapest directed route when one edge may be taken at half price.

**Design.** A vertex alone does not describe progress: whether the pass was used changes future choices. Dijkstra therefore stores two distances per vertex. Every edge has an ordinary transition, plus a discounted transition from the unused state.

**Correctness.** Each valid journey maps to a path through this expanded graph, and each expanded-graph path maps to a valid journey. Edge costs are nonnegative, so the first destination removed from the heap is optimal.

**Checks.** Directed edges, zero weights, an unused pass, unreachable destination, and randomized comparison with Bellman-Ford.

## Tree distance totals

**Question.** For every vertex in a tree, sum its distances to all other vertices.

**Design.** Root at vertex zero. One traversal records parents and depths. A reverse traversal computes subtree sizes. Moving the root across an edge to a child reduces distance to its subtree and increases distance to every other vertex, giving `answer[child] = answer[parent] + V - 2 * subtree[child]`.

**Correctness.** The initial answer is the sum of depths. Every tree vertex has one parent except the root, so applying the edge relation in traversal order derives each remaining answer exactly once.

**Checks.** Single vertex, path, invalid graph, and randomized comparison with breadth-first search from every vertex.

## Distinct-value window

**Question.** Find earliest longest contiguous range containing at most a given number of distinct values.

**Design.** Expand the right boundary and count values. Shrink the left boundary only while the distinct-value limit is exceeded. Update the best range only for a strictly longer valid window.

**Correctness.** After shrinking, the current range is valid. Any longer valid range ending at the same right boundary must start no later than the maintained left boundary, which would contradict the shrink condition.

**Checks.** Empty input, zero limit, repeated values, tie behavior, and randomized exhaustive ranges.

## Single-server scheduler

**Question.** Execute arriving jobs one at a time, choosing shortest duration among ready jobs and input order for ties.

**Design.** Sort arrivals once. Move available jobs into a heap ordered by duration and index. When idle, advance time to the next arrival.

**Correctness.** The heap contains exactly the jobs available when a choice is made. Its minimum matches the selection rule. Executed jobs leave the heap once.

**Checks.** Idle gaps, equal durations, zero-duration jobs, and randomized comparison with direct scanning.

## Dependency planner

**Question.** Produce a stable task order subject to prerequisites, or report unresolved tasks when ordering is impossible.

**Design.** Count unique incoming edges. Repeatedly emit the alphabetically first zero-degree task, decrement its successors, and add newly available tasks. Remaining positive-degree nodes identify unresolved work; this set can include tasks downstream of a cycle.

**Correctness.** Every emitted task has all prerequisites already emitted. If all tasks emit, the order is valid. If tasks remain, no remaining task has zero incoming degree, so a directed cycle exists.

**Checks.** Duplicate edges, unknown names, cycles, and comparison with all permutations on small acyclic graphs.
