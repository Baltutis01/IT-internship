import sys




def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    result = []
    start = ['a','a']
    y, i = 0, 0
    n = len(edges)
    while i < n:
        if y == 0 or y == len(start):
            y = len(start)-1
        if edges[i][0]  == start[y][-1]:
            if edges[i][1].isupper():
                result.append(start[y]+edges[i][1])
            else:
                start[y] += edges[i][1]
            y += 1
            i += 1
            continue
        if edges[i][1] == start[y][-1]:
            if edges[i][0].isupper():
                result.append(start[y]+edges[i][0])
            else:
                start[y] += edges[i][0]
            y += 1
            i += 1
            continue
        if start[y][:-1] != start[0][:-1]:
            start.append(start[y][:-1])
        else:
            start.append(start[0][-1])
        y -= 1

    reverse = [s[::-1] for s in result if s[::-1] and s[::-1][0].isupper()]
    sort = sorted(reverse, key=lambda x: (len(x), x))
    result = [f"{s[0]}-{s[1]}" for s in sort if len(s) >= 2]


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

