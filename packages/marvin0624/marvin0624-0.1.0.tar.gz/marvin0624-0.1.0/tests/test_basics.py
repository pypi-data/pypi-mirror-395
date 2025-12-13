from marvin0624 import add, subtract, mean


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_mean():
    assert mean([1, 2, 3]) == 2