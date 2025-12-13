import pytest

from mitos.feature import LinearSequenceIndexError, length


def test_linear_sequence():
    # start <= stop
    assert length(1, 10, False, 100) == 10
    # start > stop
    with pytest.raises(LinearSequenceIndexError):
        length(10, 1, False, 100)
    # start = stop
    assert length(0, 0, False, 100) == 1


def test_circular_sequence():
    # start <= stop
    assert length(1, 10, True, 100) == 10
    # start > stop
    assert length(10, 1, True, 100) == 92
    # start and stop at end
    assert length(99, 1, True, 100) == 3
    # start = stop
    assert length(0, 0, True, 100) == 1
