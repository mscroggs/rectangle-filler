import json


def overlaps(
    size: tuple[int, int],
    p1: tuple[int, int, bool],
    p2: tuple[int, int, bool],
) -> bool:
    p1x = [p1[0], p1[0] + (size[0] if p1[2] else size[1])]
    p1y = [p1[1], p1[1] + (size[1] if p1[2] else size[0])]
    p2x = [p2[0], p2[0] + (size[0] if p2[2] else size[1])]
    p2y = [p2[1], p2[1] + (size[1] if p2[2] else size[0])]

    return max(p1x[0], p2x[0]) < min(p1x[1], p2x[1]) and  max(p1y[0], p2y[0]) < min(p1y[1], p2y[1])


def fill(
    large: tuple[int, int],
    small: tuple[int, int],
    placed: list[tuple[int, int, bool]] = [],
    remaining: list[tuple[int, int]] | None = None,
    bound: int | None = None,
) -> list[list[tuple[int, int, bool]]]:
    if bound is not None and len(placed) > bound - 5:
        print(placed)
    if remaining is None:
        remaining = [(i, j) for i in range(large[0] + 1) for j in range(large[1] + 1)]
    if len(placed) == 0:
        start = (0, -1)
    else:
        start = placed[-1]
    results = [placed]

    for (i, j) in remaining:
        for o in [False, True]:
            if i + (small[0] if o else small[1]) > large[0]:
                continue
            if j + (small[1] if o else small[0]) > large[1]:
                continue
            if all(not overlaps(small, (i, j, o), p) for p in placed):
                x = (i, i + (small[0] if o else small[1]))
                y = (j, j + (small[1] if o else small[0]))
                rem = [(a, b) for a, b in remaining if not (x[0] <= a < x[1] and y[0] <= b < y[1]) and (a > i or (a == i and b > j))]
                if len(placed) + len(rem) // (small[0] * small[1]) < (len(results[0]) if bound is None else bound):
                    return results
                for res in fill(large, small, placed + [(i, j, o)], rem, bound=bound):
                    if len(res) > len(results[0]):
                        results = [res]
                    elif len(res) == len(results[0]):
                        results.append(res)
                    if bound is not None and len(res) > bound:
                        with open("found.txt", "a") as f:
                            f.write(json.dumps(res) + "\n")
    return results
