import os
import requests
import re
import sys

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found in environment")
        sys.exit(1)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Fetch all repositories dynamically to check for deployments
    live_repos = []
    repos_url = "https://api.github.com/users/chimataraghuram/repos?per_page=100"
    try:
        repos_resp = requests.get(repos_url, headers=headers)
        if repos_resp.status_code == 200:
            repos_data = repos_resp.json()
            live_repos = [repo["full_name"] for repo in repos_data]
        else:
            print(f"Warning: Could not fetch repos (status {repos_resp.status_code}). Falling back to empty list.")
    except Exception as e:
        print(f"Error fetching repos: {e}")

    total_deployments = 0
    for repo in live_repos:
        print(f"Fetching deployments for {repo}...")
        url = f"https://api.github.com/repos/{repo}/deployments?per_page=1"
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                print(f"  Warning: Skipping {repo} due to status code {resp.status_code}")
                continue
            
            link = resp.headers.get("Link", "")
            match = re.search(r'page=(\d+)>; rel="last"', link)
            if match:
                count = int(match.group(1))
            else:
                count = len(resp.json())
            
            total_deployments += count
            print(f"  Success: Counted {count} deployments.")
        except Exception as e:
            print(f"  Error fetching {repo}: {e}")

    print(f"\nFinal tally: {total_deployments} deployments.")

    # Update README.md
    if not os.path.exists("README.md"):
        print("Error: README.md not found")
        sys.exit(1)

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    badge = f'  <img src="https://img.shields.io/badge/Deployments-{total_deployments}-22c55e?style=for-the-badge&logo=vercel" />'
    pattern = r"<!-- START_SECTION:deployments -->.*?<!-- END_SECTION:deployments -->"
    
    if not re.search(pattern, content, flags=re.DOTALL):
        print("Error: Could not find deployment section tags in README.md")
        sys.exit(1)

    replacement = f"<!-- START_SECTION:deployments -->\n{badge}\n  <!-- END_SECTION:deployments -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated successfully!")

if __name__ == "__main__":
    main()
