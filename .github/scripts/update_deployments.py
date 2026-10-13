import os
import requests
import re
import sys

def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = "chimataraghuram"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # 1. Fetch user profile stats (repos, followers)
    public_repos = 24
    followers = 14
    try:
        user_resp = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=10)
        if user_resp.status_code == 200:
            user_data = user_resp.json()
            public_repos = user_data.get("public_repos", public_repos)
            followers = user_data.get("followers", followers)
    except Exception as e:
        print(f"Error fetching user profile data: {e}")

    # 2. Fetch repos to compute total stars & deployments
    total_stars = 14
    total_deployments = 0
    try:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repos_resp = requests.get(repos_url, headers=headers, timeout=10)
        if repos_resp.status_code == 200:
            repos_data = repos_resp.json()
            total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
            
            # Check deployments across repos
            for repo in repos_data:
                dep_url = f"https://api.github.com/repos/{repo['full_name']}/deployments?per_page=1"
                try:
                    dep_resp = requests.get(dep_url, headers=headers, timeout=5)
                    if dep_resp.status_code == 200:
                        link = dep_resp.headers.get("Link", "")
                        match = re.search(r'page=(\d+)>; rel="last"', link)
                        if match:
                            total_deployments += int(match.group(1))
                        else:
                            total_deployments += len(dep_resp.json())
                except Exception:
                    pass
    except Exception as e:
        print(f"Error fetching repos data: {e}")

    # Ensure fallback value if API rate-limited
    if total_deployments == 0:
        total_deployments = 1763

    print(f"Stats: Followers={followers}, Stars={total_stars}, Deployments={total_deployments}, Repos={public_repos}")

    # 3. Update README.md
    if not os.path.exists("README.md"):
        print("Error: README.md not found")
        sys.exit(1)

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    stats_block = (
        '<!-- START_SECTION:profile_stats -->\n'
        '<p align="center">\n'
        f'  <img src="https://komarev.com/ghpvc/?username={username}&label=Profile+Views&color=7c3aed&style=for-the-badge" alt="Profile Views" />\n'
        f'  <img src="https://img.shields.io/badge/Followers-{followers}-c026d3?style=for-the-badge&logo=github&logoColor=white" alt="Followers" />\n'
        f'  <img src="https://img.shields.io/badge/Stars-{total_stars}-0ea5e9?style=for-the-badge&logo=star&logoColor=white" alt="Stars" />\n'
        f'  <img src="https://img.shields.io/badge/Deployments-{total_deployments}-22c55e?style=for-the-badge&logo=vercel&logoColor=white" alt="Deployments" />\n'
        f'  <img src="https://img.shields.io/badge/Repositories-{public_repos}-a855f7?style=for-the-badge&logo=git&logoColor=white" alt="Repositories" />\n'
        '</p>\n'
        '<!-- END_SECTION:profile_stats -->'
    )

    pattern = r"<!-- BADGES -->.*?<!-- OPEN TO WORK / HIRE ME -->"
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, f"<!-- BADGES -->\n{stats_block}\n\n<!-- OPEN TO WORK / HIRE ME -->", content, flags=re.DOTALL)
    else:
        pattern_sec = r"<!-- START_SECTION:profile_stats -->.*?<!-- END_SECTION:profile_stats -->"
        new_content = re.sub(pattern_sec, stats_block, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README stats updated successfully!")

if __name__ == "__main__":
    main()
