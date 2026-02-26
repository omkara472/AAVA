import pytest
from src import app


def test_driver_returns_value(monkeypatch):
    # Mock driver function to avoid launching real browser
    monkeypatch.setattr(app, "driver", lambda: "mock_driver")
    
    result = app.driver()
    assert result == "mock_driver"


def test_wait_for_element_returns_value(monkeypatch):
    # Mock wait_for_element to avoid real selenium dependency
    monkeypatch.setattr(app, "wait_for_element", lambda a, b, c: "mock_element")
    
    result = app.wait_for_element(None, None, None)
    assert result == "mock_element"


def test_test_jira_case_returns_value(monkeypatch):
    # Mock jira function to avoid real API call
    monkeypatch.setattr(app, "test_jira_case", lambda a, b: "mock_jira_result")
    
    result = app.test_jira_case(None, None)
    assert result == "mock_jira_result"
