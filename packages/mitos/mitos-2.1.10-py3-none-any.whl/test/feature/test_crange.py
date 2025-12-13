import pytest

from mitos.feature import LinearSequenceIndexError, crange


@pytest.mark.parametrize(
    "start, stop, step, expected",
    [
        (2, 8, 2, [2, 4, 6]),  # positive step
        (8, 2, -2, [8, 6, 4]),  # negative step
        (0, 9, 3, [0, 3, 6]),  # start = 0, stop = max
    ],
)
def test_linear_valid(start, stop, step, expected):
    result = list(crange(start, stop, step, circular=False, length=10))
    assert result == expected


def test_linear_out_of_bounds():
    assert list(crange(-5, 7, 2, circular=False, length=0)) == [-5, -3, -1, 1, 3, 5]


@pytest.mark.parametrize(
    "start, stop, step",
    [
        (8, 2, 2),  # wrong direction, positive step
        (2, 8, -1),  # wrong direction, negative step
    ],
)
def test_linear_invalid_direction(start, stop, step):
    with pytest.raises(LinearSequenceIndexError):
        list(crange(start, stop, step, circular=False, length=10))


def test_zero_step():
    with pytest.raises(ValueError):
        list(crange(2, 5, 0, circular=False, length=10))


@pytest.mark.parametrize(
    "start, stop, step, expected",
    [
        (8, 3, 1, [8, 9, 0, 1, 2]),  # wrap around, postitive step, restart = 0
        (7, 5, 2, [7, 9, 1, 3]),  # wrap around, postitive step, restart != 0
        (2, 8, -1, [2, 1, 0, 9]),  # wrap around, negative step
        (3, 5, -3, [3, 0, 7]),  # wrap around, negative step < -1, restart = 0
        (3, 5, -2, [3, 1, 9, 7]),  # wrap around, negative step < -1, restart != 0
        (3, 7, 1, [3, 4, 5, 6]),  # no wrap around, positive step
        (7, 3, -1, [7, 6, 5, 4]),  # no wrap around, negative step
        (8, 13, 1, [8, 9, 10, 11, 12]),  # out of range, positive step
        (3, -3, -1, [3, 2, 1, 0, -1, -2]),  # out of range, negative step
        (0, 0, 3, []),  # start = stop
    ],
)
def test_circular_sequence(start, stop, step, expected):
    result = list(crange(start, stop, step, circular=True, length=10))
    assert result == expected
