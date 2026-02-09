import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test data extracted from input JSON
TEST_CASES = [
    {
        "test_case": "TC01_Minimal_Story",
        "base_url": "https://nithyavakapatla.atlassian.net",
        "email": "user@example.com",
        "api_key": "JIRA_API_TOKEN",
        "project_key": "AAVA",
        "issue_type": "Story",
        "summary": "Employee applies for leave",
        "description": "As an employee, I want to apply for leave.",
        "reporter_id": "ACCOUNT_ID_123"
    },
    {
        "test_case": "TC02_Task",
        "base_url": "https://nithyavakapatla.atlassian.net",
        "email": "user@example.com",
        "api_key": "JIRA_API_TOKEN",
        "project_key": "AAVA",
        "issue_type": "Task",
        "summary": "Validate leave balance",
        "description": "System validates leave balance before submission.",
        "reporter_id": "ACCOUNT_ID_123"
    },
    {
        "test_case": "TC03_Bug",
        "base_url": "https://nithyavakapatla.atlassian.net",
        "email": "user@example.com",
        "api_key": "JIRA_API_TOKEN",
        "project_key": "AAVA",
        "issue_type": "Bug",
        "summary": "Leave request submission fails",
        "description": "Error occurs when overlapping dates are selected.",
        "reporter_id": "ACCOUNT_ID_123"
    }
]

@pytest.mark.parametrize("case", TEST_CASES, ids=[tc["test_case"] for tc in TEST_CASES])
def test_create_jira_issue(case):
    """
    Test creating a Jira issue via REST API.
    Validates HTTP response, issue fields, and error handling.
    """
    url = f'{case["base_url"]}/rest/api/3/issue'
    auth = HTTPBasicAuth(case["email"], case["api_key"])
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "project": {
                "key": case["project_key"]
            },
            "summary": case["summary"],
            "description": case["description"],
            "issuetype": {
                "name": case["issue_type"]
            },
            "reporter": {
                "id": case["reporter_id"]
            }
        }
    }

    # Send POST request to create issue
    response = requests.post(url, json=payload, headers=headers, auth=auth)

    # Assert HTTP status code
    assert response.status_code == 201, (
        f"Failed to create issue. Status: {response.status_code}, Response: {response.text}"
    )

    # Validate response structure
    resp_json = response.json()
    assert "id" in resp_json, "Response missing 'id' field"
    assert "key" in resp_json, "Response missing 'key' field"
    assert resp_json["key"].startswith(case["project_key"]), (
        f"Issue key does not start with project key: {resp_json['key']}"
    )

    # Optionally, fetch the created issue and validate fields
    issue_url = f'{case["base_url"]}/rest/api/3/issue/{resp_json["id"]}'
    issue_resp = requests.get(issue_url, headers=headers, auth=auth)
    assert issue_resp.status_code == 200, (
        f"Failed to fetch created issue. Status: {issue_resp.status_code}, Response: {issue_resp.text}"
    )
    issue_data = issue_resp.json()
    assert issue_data["fields"]["summary"] == case["summary"], "Summary mismatch"
    assert issue_data["fields"]["description"] == case["description"], "Description mismatch"
    assert issue_data["fields"]["issuetype"]["name"] == case["issue_type"], "Issue type mismatch"
    assert issue_data["fields"]["project"]["key"] == case["project_key"], "Project key mismatch"

    # Clean up: Optionally delete the created issue to keep environment clean
    # Uncomment below lines if you want to delete after test
    # del_resp = requests.delete(issue_url, headers=headers, auth=auth)
    # assert del_resp.status_code == 204, (
    #     f"Failed to delete created issue. Status: {del_resp.status_code}, Response: {del_resp.text}"
    # )

