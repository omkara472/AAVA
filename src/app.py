# test_calculator.py

import pytest
import calculator


def test_add():
    assert calculator.add(2, 3) == 5


def test_multiply():
    assert calculator.multiply(4, 5) == 20


def test_divide():
    assert calculator.divide(10, 2) == 5