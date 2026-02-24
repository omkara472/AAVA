import pytest
from src import app

def test_driver_returns_value():
    result = app.driver()
    assert result is not None


def test_wait_for_element_returns_value():
    result = app.wait_for_element(None, None, None)
    assert result is not None


def test_test_jira_case_returns_value():
    result = app.test_jira_case(None, None)
    assert result is not None
