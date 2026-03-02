import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import app

def test_load_test_cases_returns_value():
    result = app.load_test_cases(None)
    assert result is not None


def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_execute_steps_returns_value():
    result = app.execute_steps(None, None)
    assert result is not None


def test_pytest_generate_tests_returns_value():
    result = app.pytest_generate_tests(None)
    assert result is not None


def test_test_manual_case_returns_value():
    result = app.test_manual_case(None, None)
    assert result is not None
