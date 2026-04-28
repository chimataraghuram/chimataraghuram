import os
import requests
import re

token = os.environ.get("GITHUB_TOKEN")
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Count live deployments across all repos with Vercel/GitHub Pages deployments
live_repos = [
    "chimataraghuram/PORTFOLIO",
    "chimataraghuram/PROJECT-FINDER",
    "chimataraghuram/TECHBOY-AI",
    "chimataraghuram/House-Prediction",
    "chimataraghuram/Enchanted-Wings-Marvels-of-butterfly-species",
]

total_deployments = 0
for repo in live_repos:
    url = f"https://api.github.com/repos/{repo}/deployments?per_page=1"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Skipping {repo}: {resp.status_code}")
        continue
    link = resp.headers.get("Link", "")
    match = re.search(r'page=(\d+)>; rel="last"', link)
    if match:
        total_deployments += int(match.group(1))
    else:
        total_deployments += len(resp.json())
    print(f"  {repo}: counted")

print(f"Total deployments across all live repos: {total_deployments}")

# Update README.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

badge = f'  <img src="https://img.shields.io/badge/Deployments-{total_deployments}-22c55e?style=for-the-badge&logo=vercel" />'
pattern = r"<!-- START_SECTION:deployments -->.*?<!-- END_SECTION:deployments -->"
replacement = f"<!-- START_SECTION:deployments -->\n{badge}\n  <!-- END_SECTION:deployments -->"

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("README updated successfully.")
