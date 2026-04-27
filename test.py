from rect import fill


def test_2_by_1():
    results = fill((2, 2), (1, 2))
    for r in results:
        print(r)
    assert len(results) == 2
    assert len(results[0]) == 2
    assert len(results[1]) == 2
