import sys


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """

    depth = len(lines) - 3
    rooms = []
    for i in range(4):
        room = []
        for j in range(depth):
            room.append(lines[2 + j][3 + 2 * i])
        rooms.append(tuple(room))
    initial_rooms = tuple(rooms)
    initial_hallway = ('.',) * 11
    targets = ('A', 'B', 'C', 'D')
    costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    entrances = (2, 4, 6, 8)
    allowed_hallway_positions = {0, 1, 3, 5, 7, 9, 10}
    cache = {}

    def dfs(hallway, rooms):
        key = (hallway, rooms)
        if key in cache:
            return cache[key]

        finished = True
        for i in range(4):
            if rooms[i] != (targets[i],) * depth:
                finished = False
                break
        if finished:
            cache[key] = 0
            return 0

        min_energy = float('inf')

        for pos, amph in enumerate(hallway):
            if amph == '.':
                continue
            target_room_idx = ord(amph) - ord('A')
            room = rooms[target_room_idx]
            if all(c == amph or c == '.' for c in room):
                target_level = None
                for level in range(depth - 1, -1, -1):
                    if room[level] == '.':
                        target_level = level
                        break
                if target_level is None:
                    continue
                entrance_pos = entrances[target_room_idx]
                start, end = min(pos, entrance_pos), max(pos, entrance_pos)
                blocked = any(hallway[i] != '.' for i in range(start, end + 1) if i != pos)
                if blocked:
                    continue
                steps = abs(pos - entrance_pos) + (target_level + 1)
                energy = costs[amph] * steps
                new_hallway = list(hallway)
                new_hallway[pos] = '.'
                new_hallway = tuple(new_hallway)
                new_rooms = list(rooms)
                new_room = list(room)
                new_room[target_level] = amph
                new_rooms[target_room_idx] = tuple(new_room)
                new_rooms = tuple(new_rooms)
                total = energy + dfs(new_hallway, new_rooms)
                if total < min_energy:
                    min_energy = total

        for room_idx, room in enumerate(rooms):
            if all(c == targets[room_idx] or c == '.' for c in room):
                if not any(c != '.' and c != targets[room_idx] for c in room):
                    continue
            top_amph = None
            top_level = None
            for level in range(depth):
                if room[level] != '.':
                    top_amph = room[level]
                    top_level = level
                    break
            if top_amph is None:
                continue
            entrance_pos = entrances[room_idx]
            for hall_pos in allowed_hallway_positions:
                start, end = min(entrance_pos, hall_pos), max(entrance_pos, hall_pos)
                if any(hallway[i] != '.' for i in range(start, end + 1)):
                    continue
                steps = (top_level + 1) + abs(hall_pos - entrance_pos)
                energy = costs[top_amph] * steps
                new_hallway = list(hallway)
                new_hallway[hall_pos] = top_amph
                new_hallway = tuple(new_hallway)
                new_rooms = list(rooms)
                new_room = list(room)
                new_room[top_level] = '.'
                new_rooms[room_idx] = tuple(new_room)
                new_rooms = tuple(new_rooms)
                total = energy + dfs(new_hallway, new_rooms)
                if total < min_energy:
                    min_energy = total

        cache[key] = min_energy
        return min_energy

    return dfs(initial_hallway, initial_rooms)


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
      lines.append(line.rstrip('\n'))
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
