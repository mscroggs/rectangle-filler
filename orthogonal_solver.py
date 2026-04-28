"""Slow solver with assumption that all paper is either portrait or landscape."""

import pytest
import json
from a_paper import a as a_sizes

with open("found.txt", "w") as f:
    pass


def fill(
    large: tuple[int, int],
    small: tuple[int, int],
    placed: list[tuple[int, int, bool]] = [],
    remaining: list[tuple[int, int]] | None = None,
    bound: int | None = None,
    info: str = "",
) -> list[list[tuple[int, int, bool]]]:
    print(info)
    if remaining is None:
        remaining = [(i, j) for i in range(large[0] + 1) for j in range(large[1] + 1)]
    results = [placed]

    for index, (i, j) in enumerate(remaining):
        for o in [False, True]:
            d = small if o else small[::-1]
            if i + d[0] > large[0] or j + d[1] > large[1]:
                continue
            x = (i, i + d[0])
            y = (j, j + d[1])
            if all((a, j - 1) in remaining for a in range(*x)) or all(
                (i - 1, a) in remaining for a in range(*y)
            ):
                continue
            rem = [
                (a, b)
                for a, b in remaining
                if not (x[0] <= a < x[1] and y[0] <= b < y[1])
                and (a > i or (a == i and b > j))
            ]
            if len(placed) + len(rem) // (small[0] * small[1]) < (
                len(results[0]) if bound is None else bound
            ):
                return results
            for res in fill(
                large,
                small,
                placed + [(i, j, o)],
                rem,
                bound=bound,
                info=f"{info} {index}/{len(remaining)}",
            ):
                if len(res) > len(results[0]) and len(res) >= (
                    len(results[0]) if bound is None else bound
                ):
                    print(len(res), res)
                    results = [res]
                elif len(res) == len(results[0]):
                    print(len(res), res)
                    results.append(res)
                if bound is not None and len(res) > bound:
                    with open("found.txt", "a") as f:
                        f.write(f"{len(res)} -> " + json.dumps(res) + "\n")
    return results


if __name__ == "__main__":
    options = []
    for i, ai in enumerate(a_sizes):
        for j, aj in enumerate(a_sizes[:i]):
            n = (aj[0] * aj[1]) // (ai[0] * ai[1])
            extras = n - 2 ** (i - j)
            if extras > 0:
                options.append([i, j, 2 ** (i - j), extras])

    options.sort(key=lambda x: -x[3])

    for i, j, n, extras in options:
        with open("found.txt", "a") as f:
            f.write(f"A{i} into A{j} ({n} - {n + extras})\n")
        print(f"A{i} into A{j}")
        results = fill(a_sizes[j], a_sizes[i], bound=n + 1)
        assert len(results[0]) >= 2 ** (i - j)
        print(f"Can fit {len(results[0])} copies")
        with open(f"output/a{j}-a{i}.txt", "w") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
        print()


def test_2_by_1():
    results = fill((2, 2), (1, 2))
    for r in results:
        print(r)
    assert len(results) == 2
    assert len(results[0]) == 2
    assert len(results[1]) == 2


@pytest.mark.parametrize("n", [1, 2, 4, 8, 16, 32, 64])
@pytest.mark.parametrize("m", [1, 2, 4, 8, 16, 32, 64])
def test_halves(n, m):
    results = fill((2 * n, m), (m, n))
    for r in results:
        print(r)
        assert len(r) == 2


@pytest.mark.parametrize("n", [4, 8, 16, 32, 64])
@pytest.mark.parametrize("m", [4, 8, 16, 32, 64])
def test_halves_add_1(n, m):
    results = fill((2 * n + 1, m), (m, n))
    for r in results:
        print(r)
        assert len(r) == 2
