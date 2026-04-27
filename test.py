import pytest
from rect import fill


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
    results = fill((2*n, m), (m, n))
    for r in results:
        print(r)
        assert len(r) == 2


@pytest.mark.parametrize("n", [4, 8, 16, 32, 64])
@pytest.mark.parametrize("m", [4, 8, 16, 32, 64])
def test_halves_add_1(n, m):
    results = fill((2*n + 1, m), (m, n))
    for r in results:
        print(r)
        assert len(r) == 2
