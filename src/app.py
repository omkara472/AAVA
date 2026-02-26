import pytest


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


def test_subtract_positive_numbers():
    assert subtract(5, 3) == 2


def test_subtract_result_negative():
    assert subtract(3, 5) == -2