# test_app.py

import pytest
import app


# -------------------------
# Addition Tests
# -------------------------
def test_add_positive():
    assert app.add(2, 3) == 5


def test_add_negative():
    assert app.add(-1, -2) == -3


# -------------------------
# Subtraction Tests
# -------------------------
def test_subtract():
    assert app.subtract(10, 4) == 6


# -------------------------
# Even Number Tests
# -------------------------
def test_is_even_true():
    assert app.is_even(4) is True


def test_is_even_false():
    assert app.is_even(5) is False