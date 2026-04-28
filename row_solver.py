"""Solver with assumption that smaller pieces of paper make full rows."""

import json
from a_paper import a as a_sizes
import matplotlib.pylab as plt
import os

if not os.path.isdir("output"):
    os.system("mkdir output")
if not os.path.isdir("output/img"):
    os.system("mkdir output/img")
if not os.path.isdir("output/json"):
    os.system("mkdir output/json")

# Filter combinations of sizes where the extra area due to rounding is more than the size
# of the smaller paper
options = []
for i, ai in enumerate(a_sizes):
    for j, aj in enumerate(a_sizes[:i]):
        n = (aj[0] * aj[1]) // (ai[0] * ai[1])
        extras = n - 2**(i - j)
        if extras > 0:
            options.append([i, j, 2 ** (i-j), extras])

for i, j, n, extras in options:
    small = a_sizes[i]
    large = a_sizes[j]

    # Calculate best combination of portrait and landscape to include in a mixed row
    best_row = (0, 0, 0, 0)
    for n in range(large[1] // small[1] + 1):
        m = (large[1] - n * small[1]) // small[0]
        for n2 in range(large[1] // small[1] + 1):
            m2 = (large[1] - n2 * small[1]) // small[0]
            if (m + m2) * small[0] > large[1]:
                continue
            if sum(best_row) < n + m + n2 + m2:
                best_row = (n, m, n2, m2)

    # Calculate the best combination of rows
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

    # Did we fit more than 2**(m-n)?
    if largest[3] == 2 ** (i - j):
        continue

    # Generate coordinates of rectangles from numbers of rows
    rectangles = []
    for x in range(largest[2]):
        o = x * sum(small)
        for a in range(best_row[0]):
            rectangles.append([[small[1] * a, o], [small[1] * (a + 1), o + small[0]]])
        for a in range(best_row[1]):
            rectangles.append([[large[1] - small[0] * (a + 1), o], [large[1] - small[0] * a, o + small[1]]])
        for a in range(best_row[2]):
            rectangles.append([[large[1] - small[1] * (a + 1), o + small[1]], [large[1] - small[1] * a, o + small[1] + small[0]]])
        for a in range(best_row[3]):
            rectangles.append([[small[0] * a, o + small[0]], [small[0] * (a + 1), o + small[0] + small[1]]])
    for x in range(largest[1]):
        o = largest[2] * sum(small) + x * small[1]
        for a in range(count1):
            rectangles.append([[small[0] * a, o], [small[0] * (a + 1), o + small[1]]])
    for x in range(largest[0]):
        o = largest[2] * sum(small) + largest[1] * small[1] + x * small[0]
        for a in range(count0):
            rectangles.append([[small[1] * a, o], [small[1] * (a + 1), o + small[0]]])

    print(f"Fitting {largest[3]} (greater than {2**(i-j)}) pieces of A{i} paper on a piece of A{j} paper")
    fname = f"A{j}-A{i}-{largest[3]}-{largest[3] - 2**(i-j)}extra"

    # Save json
    with open(f"output/json/{fname}.json", "w") as f:
        json.dump(rectangles, f)

    # Make matplotlib plot
    plt.fill([0, large[1], large[1], 0, 0], [0, 0, large[0], large[0], 0], "r")
    plt.plot([0, large[1], large[1], 0, 0], [0, 0, large[0], large[0], 0], "k-")
    for [x0, y0], [x1, y1] in rectangles:
        plt.fill([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], "w")
        plt.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], "k-")
    plt.axis("equal")
    plt.savefig(f"output/img/{fname}.png")
    plt.clf()


