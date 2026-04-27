from rect import fill
import json
from a_paper import a as a_sizes
import matplotlib.pylab as plt

with open("found.txt", "w") as f:
    pass

options = []

print(a_sizes)

for i, ai in enumerate(a_sizes):
    for j, aj in enumerate(a_sizes[:i]):
        n = (aj[0] * aj[1]) // (ai[0] * ai[1])
        extras = n - 2**(i - j)
        if extras > 0:
            options.append([i, j, 2 ** (i-j), extras])

options.sort(key=lambda x: x[2])

for i, j, n, extras in options:
    small = a_sizes[i]
    large = a_sizes[j]

    nrows = large[0] // (small[0] + small[1])

    best_row = (0, 0, 0, 0)

    for n in range(large[1] // small[1] + 1):
        m = (large[1] - n * small[1]) // small[0]

        for n2 in range(large[1] // small[1] + 1):
            m2 = (large[1] - n2 * small[1]) // small[0]

            if (m + m2) * small[0] > large[1]:
                continue

            if sum(best_row) < n + m + n2 + m2:
                best_row = (n, m, n2, m2)

    largest = (0, 0, 0, 0)
    count0 = large[1] // small[1]
    count1 = large[1] // small[0]
    count2 = sum(best_row)
    for n0 in range(large[0] // small[0] + 1):
        for n1 in range((large[0] - n0 * small[0]) // small[1] + 1):
            for n2 in range((large[0] - n0 * small[0] - n1 * small[1]) // (small[0] + small[1]) + 1):
                total = n0 * count0 + n1 * count1 + n2 * count2
                if total > largest[3]:
                    largest = (n0, n1, n2, total)
    if largest[3] == 2 ** (i - j):
        continue
    print(i, j, n, extras)
    print(largest)
    print()
    plt.fill([0, large[1], large[1], 0, 0], [0, 0, large[0], large[0], 0], "r")
    plt.plot([0, large[1], large[1], 0, 0], [0, 0, large[0], large[0], 0], "k-")

    for x in range(largest[2]):
        o = x * sum(small)
        for a in range(best_row[0]):
            plt.fill([small[1] * b for b in [a, a+1, a+1, a, a]], [o + small[0] * b for b in [0, 0, 1, 1, 0]], "w")
            plt.plot([small[1] * b for b in [a, a+1, a+1, a, a]], [o + small[0] * b for b in [0, 0, 1, 1, 0]], "k-")
        for a in range(best_row[1]):
            plt.fill([large[1] - small[0] * b for b in [a, a+1, a+1, a, a]], [o + small[1] * b for b in [0, 0, 1, 1, 0]], "w")
            plt.plot([large[1] - small[0] * b for b in [a, a+1, a+1, a, a]], [o + small[1] * b for b in [0, 0, 1, 1, 0]], "k-")
        for a in range(best_row[2]):
            plt.fill([large[1] - small[1] * b for b in [a, a+1, a+1, a, a]], [o + small[1] + small[0] * b for b in [0, 0, 1, 1, 0]], "w")
            plt.plot([large[1] - small[1] * b for b in [a, a+1, a+1, a, a]], [o + small[1] + small[0] * b for b in [0, 0, 1, 1, 0]], "k-")
        for a in range(best_row[3]):
            plt.fill([small[0] * b for b in [a, a+1, a+1, a, a]], [o + small[0] + small[1] * b for b in [0, 0, 1, 1, 0]], "w")
            plt.plot([small[0] * b for b in [a, a+1, a+1, a, a]], [o + small[0] + small[1] * b for b in [0, 0, 1, 1, 0]], "k-")
    for x in range(largest[1]):
        o = largest[2] * sum(small) + x * small[1]
        for a in range(count1):
            plt.fill([small[0] * b for b in [a, a+1, a+1, a, a]], [o + small[1] * b for b in [0, 0, 1, 1, 0]], "w")
            plt.plot([small[0] * b for b in [a, a+1, a+1, a, a]], [o + small[1] * b for b in [0, 0, 1, 1, 0]], "k-")
    for x in range(largest[0]):
        o = largest[2] * sum(small) + largest[1] * small[1] + x * small[0]
        for a in range(count0):
            plt.fill([small[1] * b for b in [a, a+1, a+1, a, a]], [o + small[0] * b for b in [0, 0, 1, 1, 0]], "w")
            plt.plot([small[1] * b for b in [a, a+1, a+1, a, a]], [o + small[0] * b for b in [0, 0, 1, 1, 0]], "k-")

    plt.axis("equal")
    plt.savefig(f"output/img/A{j}-A{i}-{largest[3]}-{largest[3] - 2**(i-j)}extra.png")
    plt.clf()
