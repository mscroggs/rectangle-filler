from rect import fill
import json

a = [(841, 1190)]

for i in range(1, 11):
    a.append((max(a[-1]) // 2, min(a[-1])))

with open("found.txt", "w") as f:
    pass

options = []

for diff in range(1, 10):
    for i in range(diff + 1, 11):
        j = i - diff
        n = (a[j][0] * a[j][1]) // (a[i][0] * a[i][1])
        extras = n - 2**diff
        if extras > 0:
            options.append([i, j, 2 ** diff, extras])

options.sort(key=lambda x: -x[3])

for i, j, n, extras in options:
    with open("found.txt", "a") as f:
        f.write(f"A{i} into A{j} ({n} - {n + extras})\n")
    print(f"A{i} into A{j}")
    results = fill(a[j], a[i], bound=n + 1)
    assert len(results[0]) >= 2**diff
    print(f"Can fit {len(results[0])} copies")
    with open(f"output/a{j}-a{i}.txt", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print()
