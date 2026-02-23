import pytest

@pytest.mark.smoke
def test_valid_login():
    assert "Dashboard" == "Dashboard"

@pytest.mark.regression
def test_invalid_login():
    assert "Error" == "Error"

@pytest.mark.regression
def test_empty_username():
    assert "" == ""