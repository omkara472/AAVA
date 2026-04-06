import requests
import base64


def github_automation(repo_name, new_branch, api_token, code):
    try:
        owner, repo = repo_name.split("/")
        base_branch = "main"

        headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github+json"
        }

        file_name = "app.py"  # default file name

        # 1. Get base branch SHA
        ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{base_branch}"
        ref_resp = requests.get(ref_url, headers=headers)
        ref_resp.raise_for_status()
        base_sha = ref_resp.json()['object']['sha']

        # 2. Create new branch
        create_ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
        ref_payload = {
            "ref": f"refs/heads/{new_branch}",
            "sha": base_sha
        }
        create_ref_resp = requests.post(create_ref_url, json=ref_payload, headers=headers)

        if create_ref_resp.status_code not in [201, 422]:
            return f"Branch creation failed: {create_ref_resp.text}"

        # 3. Upload code file
        create_file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_name}"
        encoded_content = base64.b64encode(code.encode()).decode()

        file_payload = {
            "message": "Add code file",
            "content": encoded_content,
            "branch": new_branch
        }

        file_resp = requests.put(create_file_url, json=file_payload, headers=headers)
        if file_resp.status_code not in [201, 200]:
            return f"File upload error: {file_resp.text}"

        # 4. Create Pull Request
        pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        pr_payload = {
            "title": "Add new code file",
            "head": new_branch,
            "base": base_branch,
            "body": "Automated PR with pasted code"
        }

        pr_resp = requests.post(pr_url, json=pr_payload, headers=headers)
        pr_resp.raise_for_status()

        pr_link = pr_resp.json().get("html_url", "N/A")

        return f"✅ Success! PR created: {pr_link}"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# 🔥 Example usage
if __name__ == "__main__":
    repo_name = "omkara472/demo-repo"
    new_branch = "feature/test"
    api_token = "ghp_xxx"

    code = """
print("Hello Omkar 🚀")
"""

    result = github_automation(repo_name, new_branch, api_token, code)
    print(result)