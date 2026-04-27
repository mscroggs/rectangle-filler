a = [(841, 1190)]

for i in range(1, 11):
    a.append((max(a[-1]) // 2, min(a[-1])))
