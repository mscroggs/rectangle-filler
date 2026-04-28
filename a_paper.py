a = [(841, 1190)]

while max(a[-1]) > 1:
    a.append((max(a[-1]) // 2, min(a[-1])))


if __name__ == "__main__":
    for i, size in enumerate(a):
        print(f"A{i} paper is {size[0]}mm by {size[1]}mm")
