import os
import re
import json
import urllib.request

def fetch_live_stats(username="chimataraghuram"):
    headers = {"User-Agent": "Mozilla/5.0"}
    token = os.environ.get("GITHUB_TOKEN")
    gh_headers = dict(headers)
    if token:
        gh_headers["Authorization"] = f"Bearer {token}"

    views = "2,090"
    followers = 14
    stars = 50
    deployments = 1841
    repos = 24

    # 1. Profile Views from Komarev
    try:
        req = urllib.request.Request(f"https://komarev.com/ghpvc/?username={username}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            svg = resp.read().decode("utf-8")
            m = re.findall(r'>(\d[\d,.]*)<', svg)
            if m:
                views = f"{int(m[-1].replace(',', '')):,}"
    except Exception as e:
        print(f"Views error: {e}")

    # 2. User info (followers, public_repos)
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=gh_headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            followers = data.get("followers", followers)
            repos = data.get("public_repos", repos)
    except Exception as e:
        print(f"User error: {e}")

    # 3. Stars and deployments
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers=gh_headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            repo_list = json.loads(resp.read().decode("utf-8"))
            computed_stars = sum(r.get("stargazers_count", 0) for r in repo_list)
            if computed_stars > 0:
                stars = computed_stars

            dep_count = 0
            for r in repo_list:
                d_url = f"https://api.github.com/repos/{r['full_name']}/deployments?per_page=1"
                try:
                    d_req = urllib.request.Request(d_url, headers=gh_headers)
                    with urllib.request.urlopen(d_req, timeout=5) as d_resp:
                        link = d_resp.headers.get("Link", "")
                        match = re.search(r'page=(\d+)>; rel="last"', link)
                        if match:
                            dep_count += int(match.group(1))
                        else:
                            data_deps = json.loads(d_resp.read().decode("utf-8"))
                            dep_count += len(data_deps)
                except Exception:
                    pass
            if dep_count > 0:
                deployments = dep_count
    except Exception as e:
        print(f"Repos/deployments error: {e}")

    formatted_deployments = f"{deployments:,}" if isinstance(deployments, int) else str(deployments)
    return {
        "views": str(views),
        "followers": str(followers),
        "stars": str(stars),
        "deployments": formatted_deployments,
        "repos": str(repos)
    }

def generate_svg(kind, label, value, stroke, grad_id, stop1, stop2, icon_svg, val_color):
    # Dynamic width based on label and value length
    val_len = len(value)
    base_width = 150 + max(0, val_len - 2) * 14
    rect_width = base_width - 1.5

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{base_width}" height="60" viewBox="0 0 {base_width} 60">
  <defs>
    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{stop1}"/>
      <stop offset="100%" stop-color="{stop2}"/>
    </linearGradient>
  </defs>
  <style>
    .stat-label {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "SF Pro Display", Helvetica, Arial, sans-serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1.2px;
      fill: #8E9BAE;
    }}
    .stat-value {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "SF Pro Display", Helvetica, Arial, sans-serif;
      font-size: 22px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }}
  </style>
  <rect x="0.75" y="0.75" width="{rect_width}" height="58.5" rx="29.25" fill="#0D131D" stroke="{stroke}" stroke-opacity="0.4" stroke-width="1.5"/>
  <circle cx="30" cy="30" r="25" fill="{stroke}" fill-opacity="0.15"/>
  <circle cx="30" cy="30" r="21" fill="url(#{grad_id})"/>
  {icon_svg}
  <line x1="60" y1="14" x2="60" y2="46" stroke="#222F3E" stroke-width="1.2"/>
  <text x="70" y="27" class="stat-label">{label}</text>
  <text x="70" y="49" class="stat-value" fill="{val_color}">{value}</text>
</svg>'''

def update_stat_svgs(stats):
    # 1. Profile Views (Violet)
    views_icon = '''<path d="M18 30 Q30 17 42 30 Q30 43 18 30 Z" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linejoin="round"/>
  <circle cx="30" cy="30" r="5" fill="#FFFFFF"/>'''
    svg_views = generate_svg(
        kind="views", label="PROFILE VIEWS", value=stats["views"],
        stroke="#7C3AED", grad_id="violetGrad", stop1="#8B5CF6", stop2="#6D28D9",
        icon_svg=views_icon, val_color="#A78BFA"
    )
    with open("images/stat_views.svg", "w", encoding="utf-8") as f:
        f.write(svg_views)

    # 2. Followers (Blue)
    followers_icon = '''<circle cx="26" cy="24" r="5" fill="#FFFFFF"/>
  <circle cx="36" cy="26" r="4.2" fill="#FFFFFF" fill-opacity="0.85"/>
  <path d="M16 40 Q16 33 26 33 Q36 33 36 40 Z" fill="#FFFFFF"/>
  <path d="M34 40 Q34 35 41 35 Q46 35 46 40 Z" fill="#FFFFFF" fill-opacity="0.85"/>'''
    svg_followers = generate_svg(
        kind="followers", label="FOLLOWERS", value=stats["followers"],
        stroke="#0284C7", grad_id="blueGrad", stop1="#0EA5E9", stop2="#0284C7",
        icon_svg=followers_icon, val_color="#38BDF8"
    )
    with open("images/stat_followers.svg", "w", encoding="utf-8") as f:
        f.write(svg_followers)

    # 3. Stars (Amber)
    stars_icon = '<polygon points="30,17 34,25.5 43,26.5 36.5,32.5 38.5,41.5 30,36.5 21.5,41.5 23.5,32.5 17,26.5 26,25.5" fill="#FFFFFF"/>'
    svg_stars = generate_svg(
        kind="stars", label="STARS", value=stats["stars"],
        stroke="#D97706", grad_id="amberGrad", stop1="#F59E0B", stop2="#D97706",
        icon_svg=stars_icon, val_color="#FBBF24"
    )
    with open("images/stat_stars.svg", "w", encoding="utf-8") as f:
        f.write(svg_stars)

    # 4. Deployments (Rose)
    deploy_icon = '''<g transform="translate(30, 30) rotate(-45)">
    <path d="M0 -11 C5 -8 7 -1 7 8 L-7 8 C-7 -1 -5 -8 0 -11 Z" fill="#FFFFFF"/>
    <circle cx="0" cy="1" r="2.5" fill="#E11D48"/>
    <path d="M-7 5 L-11 11 L-7 9 Z" fill="#FFFFFF"/>
    <path d="M7 5 L11 11 L7 9 Z" fill="#FFFFFF"/>
    <polygon points="-3,9 0,14 3,9" fill="#FDE047"/>
  </g>'''
    svg_deployments = generate_svg(
        kind="deployments", label="DEPLOYMENTS", value=stats["deployments"],
        stroke="#E11D48", grad_id="roseGrad", stop1="#FB7185", stop2="#E11D48",
        icon_svg=deploy_icon, val_color="#FB7185"
    )
    with open("images/stat_deployments.svg", "w", encoding="utf-8") as f:
        f.write(svg_deployments)

    # 5. Repositories (Emerald)
    repos_icon = '''<g transform="translate(20, 20)">
    <path d="M2 3 A2 2 0 0 1 4 1 H18 A2 2 0 0 1 20 3 V17 A2 2 0 0 1 18 19 H4 A2 2 0 0 1 2 17 Z" fill="#064E3B"/>
    <path d="M5 2 H17 A1 1 0 0 1 18 3 V17 A1 1 0 0 1 17 18 H5 Z" fill="#FFFFFF"/>
    <line x1="7" y1="6" x2="15" y2="6" stroke="#064E3B" stroke-width="1.6" stroke-linecap="round"/>
    <line x1="7" y1="10" x2="13" y2="10" stroke="#064E3B" stroke-width="1.6" stroke-linecap="round"/>
    <line x1="7" y1="14" x2="11" y2="14" stroke="#064E3B" stroke-width="1.6" stroke-linecap="round"/>
  </g>'''
    svg_repos = generate_svg(
        kind="repos", label="REPOSITORIES", value=stats["repos"],
        stroke="#059669", grad_id="emeraldGrad", stop1="#10B981", stop2="#059669",
        icon_svg=repos_icon, val_color="#34D399"
    )
    with open("images/stat_repositories.svg", "w", encoding="utf-8") as f:
        f.write(svg_repos)

    print("All 5 stat SVGs updated with live data!")

if __name__ == "__main__":
    stats = fetch_live_stats()
    print("Fetched stats:", stats)
    update_stat_svgs(stats)
