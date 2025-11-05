import sys
from collections import deque, defaultdict

def bfs_distances(graph, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def get_all_gate_edges(graph, gates):
    edges = []
    for gate in gates:
        for node in graph[gate]:
            if node.islower():  
                edges.append(f"{gate}-{node}")
    edges.sort() 
    return edges

def solve(edges):
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
        all_gate_edges = get_all_gate_edges(graph, gates)
        if not all_gate_edges:
            break

        adjacent_gates = [n for n in graph[virus] if n.isupper()]
        if adjacent_gates:
            candidates = [f"{g}-{virus}" for g in adjacent_gates]
            to_remove = min(candidates)
        else:
            to_remove = all_gate_edges[0]

        result.append(to_remove)
        gate, node = to_remove.split('-')
        graph[gate].discard(node)
        graph[node].discard(gate)

        dist = bfs_distances(graph, virus)
        gate_dists = {g: dist[g] for g in gates if g in dist}
        if not gate_dists:
            break

        min_dist = min(gate_dists.values())
        next_candidates = []
        for nb in graph[virus]:
            if nb.isupper():
                continue
            if nb in dist and dist[nb] == 1:
                dist_nb = bfs_distances(graph, nb)
                gate_dists_nb = {g: dist_nb[g] for g in gates if g in dist_nb}
                if gate_dists_nb:
                    if min(gate_dists_nb.values()) == min_dist - 1:
                        next_candidates.append(nb)

        if not next_candidates:
            break
        virus = min(next_candidates)

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

