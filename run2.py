import sys


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """


    internal = []
    to_gates = []
    for u, v in edges:
        if u.isupper():
            to_gates.append((v, u))
            continue
        if v.isupper():
            to_gates.append((u, v))
            continue
        else:
            internal.append((min(u, v), max(u, v)))
    internal.sort(key=lambda x: (x[0], x[1]))
    to_gates.sort(key=lambda x: (x[0], x[1]))
    edges = internal + to_gates
    result = []
    virus = 'a'
    count_gates = 0

    while count_gates < len(to_gates):
        paths = []
        stack = [(virus, virus)]
        while stack:
            node, path = stack.pop()
            for u, v in edges:
                if u == node:
                    if v.isupper():
                        paths.append(path + v)
                    elif v not in path:
                        stack.append((v, path + v))
                elif v == node:
                    if u.isupper():
                        paths.append(path + u)
                    elif u not in path:
                        stack.append((u, path + u))
        min_len = min(len(p) for p in paths)
        best_path = min([p for p in paths if len(p) == min_len])
        result.append(f"{best_path[-1]}-{best_path[-2]}")
        edges = [(u, v) for u, v in edges if not (u == best_path[-2] and v == best_path[-1])]
        if len(best_path) > 1:
            virus = best_path[1]
        count_gates += 1
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

