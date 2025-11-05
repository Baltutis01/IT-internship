import sys
from collections import deque, defaultdict

def bfs_distances(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """

    graph = defaultdict(set)
    gates = set()
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
        if u.isupper():
            gates.add(u)
        if v.isupper():
            gates.add(v)

    virus = 'a'
    result = []

    while True:
        dist_v = bfs_distances(graph, virus)
        gate_dists = {g: dist_v[g] for g in gates if g in dist_v}
        if not gate_dists:
            break

        min_dist = min(gate_dists.values())
        closest_gates = [g for g, d in gate_dists.items() if d == min_dist]
        target_gate = min(closest_gates)


        candidates = []
        for node in graph[target_gate]:
            if node in dist_v and dist_v[node] == min_dist - 1:
                candidates.append(node)
        if not candidates:
            break

        to_cut = min(candidates)
        result.append(f"{target_gate}-{to_cut}")
        graph[target_gate].discard(to_cut)
        graph[to_cut].discard(target_gate)
        
        dist_v = bfs_distances(graph, virus)
        gate_dists = {g: dist_v[g] for g in gates if g in dist_v}
        if not gate_dists:
            break
        current_min = min(gate_dists.values())

        next_moves = []
        for nb in graph[virus]:
            if nb.isupper():
                continue
            dist_nb = bfs_distances(graph, nb)
            gate_dists_nb = {g: dist_nb[g] for g in gates if g in dist_nb}
            if not gate_dists_nb:
                continue
            if min(gate_dists_nb.values()) == current_min - 1:
                next_moves.append(nb)

        if not next_moves:
            break
        virus = min(next_moves)

    return result

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))
    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()

