import pytest

from source import solve


def test_solve_5_res():
    assert solve(0, 0, 0, 0, 0, 0) == '5'


@pytest.mark.parametrize('a, b, c, d, e, f, y0', [
    (0, 0, 0, 4, 0, 28, 7.),
    (0, 4, 0, 0, 28, 0, 7.),

    (0, 4, 0, 4,  0,  0, 0.),
    (0, 4, 0, 4, 28, 28, 7.),
    (0, 4, 0, 0, 28,  0, 7.),
])
def test_solve_4_res(a, b, c, d, e, f, y0):
    assert solve(a, b, c, d, e, f) == f'4 {y0}'


@pytest.mark.parametrize('a, b, c, d, e, f, x0', [
    (0, 0, 3, 0, 0, 21, 7.),
    (3, 0, 0, 0, 21, 0, 7.),

    (3, 0, 3, 0,  0,  0, 0.),
    (3, 0, 3, 0, 21, 21, 7.),
 ])
def test_solve_3_res(a, b, c, d, e, f, x0):
    assert solve(a, b, c, d, e, f) == f'3 {x0}'


@pytest.mark.parametrize('a, b, c, d, e, f, x0, y0', [
    (2, 0, 2, 2, 14, 14, 7., 0.),
    (2, 2, 0, 2, 14, 14, 0., 7.),
])
def test_solve_2_res(a, b, c, d, e, f, x0, y0):
    assert solve(a, b, c, d, e, f) == f'2 {x0} {y0}'


@pytest.mark.parametrize('a, b, c, d, e, f, k, n', [
    (0, 0, -30, 10, 0, 20, 3., 2.),
    (-30, 10, 0, 0, 20, 0, 3., 2.),
    (0, 100, 10, -30, 0, 0, 3., 0.),
    (10, -30, 0, 20, 0, 0, 3., 0.),
    (9, 7, 19 * 9, 19 * 7, 3, 19 * 3, -9 / 7, 3 / 7),
])
def test_solve_1_res(a, b, c, d, e, f, k, n):
    assert solve(a, b, c, d, e, f) == f'1 {k} {n}'


def test_solve_0_res():
    assert solve(0, 0, 0, 0, 5, 12) == '0'
