import os
import requests
import re
import sys

def main():
    # Attempt to fetch with a PAT if provided, otherwise use GITHUB_TOKEN or none
    token = os.environ.get("PAT") or os.environ.get("GITHUB_TOKEN")
    
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = "https://api.github.com/users/chimataraghuram"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Error fetching user data: {resp.status_code}")
            sys.exit(1)
        
        data = resp.json()
        total_repos = data.get("public_repos", 0)
        followers = data.get("followers", 0)
        
        # If PAT is provided, we can fetch total repositories including private ones
        if os.environ.get("PAT"):
            auth_url = "https://api.github.com/user"
            auth_resp = requests.get(auth_url, headers={"Authorization": f"Bearer {os.environ.get('PAT')}"})
            if auth_resp.status_code == 200:
                auth_data = auth_resp.json()
                if auth_data.get("login") == "chimataraghuram":
                    total_repos = auth_data.get("public_repos", 0) + auth_data.get("total_private_repos", 0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Found {total_repos} repositories and {followers} followers.")

    if not os.path.exists("README.md"):
        print("Error: README.md not found")
        sys.exit(1)

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    badge = f'<img src="https://img.shields.io/badge/Repositories-{total_repos}-a855f7?style=for-the-badge&logo=github" />'
    pattern = r"<!-- START_SECTION:repositories -->.*?<!-- END_SECTION:repositories -->"
    
    if not re.search(pattern, content, flags=re.DOTALL):
        print("Error: Could not find repositories section tags in README.md")
        sys.exit(1)

    replacement = f"<!-- START_SECTION:repositories -->\n  {badge}\n  <!-- END_SECTION:repositories -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    followers_badge = f'<img src="https://img.shields.io/badge/Followers-{followers}-c026d3?style=for-the-badge" />'
    followers_pattern = r"<!-- START_SECTION:followers -->.*?<!-- END_SECTION:followers -->"
    
    if not re.search(followers_pattern, new_content, flags=re.DOTALL):
        print("Error: Could not find followers section tags in README.md")
        sys.exit(1)

    followers_replacement = f"<!-- START_SECTION:followers -->\n  {followers_badge}\n  <!-- END_SECTION:followers -->"
    new_content = re.sub(followers_pattern, followers_replacement, new_content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated successfully!")

if __name__ == "__main__":
    main()
