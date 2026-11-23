#!/usr/bin/env python3
"""
Pokémon Contribution Battle SVG Generator
Fetches real GitHub contribution data and generates an animated SVG
with 50 Pokémon each having unique attacks on the contribution graph.
"""

import os
import json
import random
import hashlib
import datetime
import urllib.request
import urllib.error

# ─── Configuration ────────────────────────────────────────────────────────────
USERNAME = os.environ.get("GITHUB_USERNAME", "chimataraghuram")
TOKEN    = os.environ.get("GITHUB_TOKEN", "")
OUT_FILE = "pokemon_contribution_battle.svg"

# ─── Exact 50-Pokémon roster ──────────────────────────────────────────────────
POKEMON_ROSTER = [
    # (name, color, body_shape, attack_name, attack_color, attack_type)
    # attack_type: "thunder","fire","water","rock","psychic","dark","steel",
    #              "ghost","dragon","fighting","grass","ice","normal","flying"
    ("Pikachu",   "#FFE135", "mouse",    "Thunderbolt",    "#FFE135", "thunder"),
    ("Charizard", "#FF5500", "dragon",   "Fire Blast",     "#FF4400", "fire"),
    ("Blastoise", "#1A6BB5", "turtle",   "Hydro Pump",     "#00AAFF", "water"),
    ("Bulbasaur", "#78C850", "bulb",     "Razor Leaf",     "#00FF66", "grass"),
    ("Onix",      "#A8A878", "snake",    "Rock Throw",     "#888888", "rock"),
    ("Arcanine",  "#E88020", "dog",      "Flamethrower",   "#FF6600", "fire"),
    ("Gengar",    "#705898", "ghost",    "Shadow Ball",    "#7700CC", "ghost"),
    ("Alakazam",  "#F8D030", "psychic",  "Psychic",        "#FF69B4", "psychic"),
    ("Machamp",   "#C03028", "fighter",  "Dynamic Punch",  "#FF4444", "fighting"),
    ("Dragonite", "#F4A460", "dragon",   "Draco Meteor",   "#FF8C00", "dragon"),
    ("Lucario",   "#4A6FA5", "jackal",   "Aura Sphere",    "#0088FF", "fighting"),
    ("Greninja",  "#1A1A2E", "ninja",    "Water Shuriken", "#00FFFF", "water"),
    ("Garchomp",  "#6B6B9A", "shark",    "Dragon Rush",    "#8800FF", "dragon"),
    ("Gyarados",  "#1A5276", "serpent",  "Hurricane",      "#00BFFF", "water"),
    ("Snorlax",   "#6C8E6E", "bear",     "Hyper Beam",     "#FFFFFF", "normal"),
    ("Eevee",     "#C8A05E", "fox",      "Swift",          "#FFD700", "normal"),
    ("Sylveon",   "#F02050", "ribbon",   "Moonblast",      "#FFB6C1", "psychic"),
    ("Umbreon",   "#1C1C1C", "dark_fox", "Dark Pulse",     "#6600CC", "dark"),
    ("Scizor",    "#8B1A1A", "bug",      "Bullet Punch",   "#CC0000", "steel"),
    ("Tyranitar", "#728C00", "dino",     "Stone Edge",     "#666666", "rock"),
    ("Mewtwo",    "#9966CC", "psychic2", "Psystrike",      "#CC00FF", "psychic"),
    ("Mew",       "#FF99CC", "cat",      "Transform",      "#FF66AA", "psychic"),
    ("Lugia",     "#B0C4DE", "bird",     "Aeroblast",      "#AADDFF", "psychic"),
    ("Ho-Oh",     "#FF6600", "phoenix",  "Sacred Fire",    "#FF4400", "fire"),
    ("Rayquaza",  "#006400", "wyrm",     "V-create",       "#00FF00", "dragon"),
    ("Kyogre",    "#1E3A8A", "whale",    "Origin Pulse",   "#0044FF", "water"),
    ("Groudon",   "#CC2200", "titan",    "Precipice Blades","#FF2200","fire"),
    ("Dialga",    "#1B6CA8", "diamond",  "Roar of Time",   "#0066FF", "steel"),
    ("Palkia",    "#9B4B9B", "pearl",    "Spacial Rend",   "#CC44CC", "dragon"),
    ("Giratina",  "#4A235A", "ghost2",   "Shadow Force",   "#550088", "ghost"),
    ("Moltres",   "#FF8C00", "fire_bird","Sky Attack",     "#FF6600", "fire"),
    ("Zapdos",    "#F5C518", "elec_bird","Discharge",      "#FFEE00", "thunder"),
    ("Articuno",  "#66CCFF", "ice_bird", "Blizzard",       "#AAEEFF", "ice"),
    ("Suicune",   "#6BB8FF", "deer",     "Sheer Cold",     "#00CCFF", "water"),
    ("Entei",     "#CC4400", "lion",     "Sacred Fire",    "#FF5500", "fire"),
    ("Raikou",    "#F0C040", "tiger",    "Thunder",        "#FFDD00", "thunder"),
    ("Metagross", "#666699", "metal",    "Meteor Mash",    "#9999CC", "steel"),
    ("Salamence", "#6633CC", "dragon2",  "Outrage",        "#8844FF", "dragon"),
    ("Blaziken",  "#CC3300", "chicken",  "Blast Burn",     "#FF4400", "fire"),
    ("Sceptile",  "#339933", "gecko",    "Leaf Storm",     "#00FF44", "grass"),
    ("Zekrom",    "#2C2C2C", "dragon3",  "Fusion Bolt",    "#44CCFF", "thunder"),
    ("Reshiram",  "#F0F0F0", "dragon4",  "Fusion Flare",   "#FFAA44", "fire"),
    ("Zoroark",   "#6B1B1B", "illusion", "Night Daze",     "#880011", "dark"),
    ("Decidueye", "#2D5A27", "archer",   "Spirit Shackle", "#44AA44", "ghost"),
    ("Infernape", "#CC5500", "monkey",   "Flare Blitz",    "#FF7700", "fire"),
    ("Empoleon",  "#2255AA", "emperor",  "Hydro Cannon",   "#0077FF", "water"),
    ("Cinderace", "#FF4455", "bunny",    "Pyro Ball",      "#FF2244", "fire"),
    ("Mimikyu",   "#997755", "ghost3",   "Play Rough",     "#FF99CC", "ghost"),
    ("Gardevoir", "#FFFFFF", "elegant",  "Moonblast",      "#FF88BB", "psychic"),
    ("Darkrai",   "#1A1A2A", "nightmare","Dark Void",      "#440066", "dark"),
]

# ─── SVG Dimensions ───────────────────────────────────────────────────────────
CELL_SIZE   = 11
CELL_GAP    = 2
GRID_LEFT   = 20
GRID_TOP    = 60
WEEKS       = 53
DAYS        = 7
GRID_W      = WEEKS * (CELL_SIZE + CELL_GAP)
GRID_H      = DAYS  * (CELL_SIZE + CELL_GAP)
SVG_W       = GRID_W + GRID_LEFT + 20
SVG_H       = GRID_H + GRID_TOP  + 100

# Contribution level colors (dark theme)
LEVEL_COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}

# ─── Fetch contribution data ───────────────────────────────────────────────────
def fetch_contributions():
    """Fetch real contribution data from GitHub GraphQL API."""
    if not TOKEN:
        print("WARNING: No GITHUB_TOKEN — using zero contributions for structure test.")
        return _zero_contributions()

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"login": USERNAME}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "pokemon-contribution-generator",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        # Build 53×7 grid: grid[week][day] = level (0-4)
        grid = []
        for week in weeks:
            days_in_week = []
            for d in week["contributionDays"]:
                c = d["contributionCount"]
                if c == 0:    lvl = 0
                elif c <= 2:  lvl = 1
                elif c <= 5:  lvl = 2
                elif c <= 9:  lvl = 3
                else:         lvl = 4
                days_in_week.append(lvl)
            # Pad to 7 days
            while len(days_in_week) < 7:
                days_in_week.append(0)
            grid.append(days_in_week)
        # Pad to 53 weeks
        while len(grid) < 53:
            grid.append([0]*7)
        return grid[:53]
    except Exception as e:
        print(f"WARNING: Could not fetch contributions: {e} — using zero grid.")
        return _zero_contributions()


def _zero_contributions():
    return [[0]*7 for _ in range(53)]

# ─── SVG Building ─────────────────────────────────────────────────────────────
def cell_id(week, day):
    return f"c{week}_{day}"

def cell_x(week):
    return GRID_LEFT + week * (CELL_SIZE + CELL_GAP)

def cell_y(day):
    return GRID_TOP + day * (CELL_SIZE + CELL_GAP)


def pokemon_sprite_path(name, color, body_shape, cx, cy, size=18):
    """Return SVG group with simple pixel-art-inspired Pokémon shape."""
    s = size
    hs = s // 2
    # Each shape is a unique combination of circles/rects/polygons
    shapes = {
        "mouse":    f'<ellipse cx="{cx}" cy="{cy}" rx="{hs}" ry="{int(hs*0.8)}" fill="{color}"/>'
                    f'<ellipse cx="{cx-hs+2}" cy="{cy-int(hs*0.5)}" rx="3" ry="5" fill="{color}"/>'
                    f'<ellipse cx="{cx+hs-2}" cy="{cy-int(hs*0.5)}" rx="3" ry="5" fill="{color}"/>',
        "dragon":   f'<polygon points="{cx},{cy-hs} {cx+hs},{cy+hs} {cx-hs},{cy+hs}" fill="{color}"/>'
                    f'<circle cx="{cx}" cy="{cy-hs}" r="4" fill="{color}"/>',
        "turtle":   f'<ellipse cx="{cx}" cy="{cy}" rx="{hs}" ry="{int(hs*0.75)}" fill="{color}"/>'
                    f'<circle cx="{cx}" cy="{cy}" r="{int(hs*0.4)}" fill="#1A6BB5"/>',
        "bulb":     f'<circle cx="{cx}" cy="{cy+3}" r="{hs}" fill="{color}"/>'
                    f'<ellipse cx="{cx}" cy="{cy-hs+2}" rx="{int(hs*0.6)}" ry="{int(hs*0.4)}" fill="#336633"/>',
        "snake":    f'<rect x="{cx-int(hs*0.4)}" y="{cy-hs}" width="{int(hs*0.8)}" height="{s}" rx="3" fill="{color}"/>',
        "dog":      f'<ellipse cx="{cx}" cy="{cy}" rx="{hs}" ry="{int(hs*0.7)}" fill="{color}"/>'
                    f'<ellipse cx="{cx-hs+3}" cy="{cy-int(hs*0.4)}" rx="4" ry="3" fill="{color}"/>',
        "ghost":    f'<path d="M{cx-hs},{cy+hs} Q{cx},{cy-hs} {cx+hs},{cy+hs} Q{cx+int(hs*0.5)},{cy+int(hs*0.5)} {cx},{cy+hs} Q{cx-int(hs*0.5)},{cy+int(hs*0.5)} {cx-hs},{cy+hs}Z" fill="{color}"/>',
        "psychic":  f'<circle cx="{cx}" cy="{cy}" r="{hs}" fill="{color}"/>'
                    f'<ellipse cx="{cx}" cy="{cy}" rx="{int(hs*0.5)}" ry="{int(hs*0.3)}" fill="#F8D030" opacity="0.5"/>',
        "fighter":  f'<rect x="{cx-hs}" y="{cy-hs}" width="{s}" height="{s}" rx="3" fill="{color}"/>',
        "psychic2": f'<circle cx="{cx}" cy="{cy}" r="{hs}" fill="{color}"/>'
                    f'<circle cx="{cx}" cy="{cy}" r="{int(hs*0.3)}" fill="#6600CC"/>',
        "cat":      f'<circle cx="{cx}" cy="{cy}" r="{int(hs*0.8)}" fill="{color}"/>'
                    f'<circle cx="{cx-5}" cy="{cy-int(hs*0.5)}" r="2" fill="{color}"/>'
                    f'<circle cx="{cx+5}" cy="{cy-int(hs*0.5)}" r="2" fill="{color}"/>',
    }
    # Default fallback for shapes not explicitly defined
    default = f'<circle cx="{cx}" cy="{cy}" r="{hs}" fill="{color}"/>'
    return f'<g opacity="1">{shapes.get(body_shape, default)}</g>'


def attack_particles(attack_type, attack_color, cx, cy, grid_right, grid_bottom, pokemon_idx, anim_begin, pokemon_total):
    """Generate attack particle SVG animation for a given type."""
    particles = []
    num = {"thunder": 8, "fire": 10, "water": 8, "grass": 7,
           "rock": 6, "ghost": 7, "psychic": 9, "fighting": 6,
           "dragon": 10, "ice": 8, "dark": 7, "steel": 6,
           "normal": 5, "flying": 6}.get(attack_type, 7)

    rng = random.Random(pokemon_idx * 97 + 13)
    for i in range(num):
        px = rng.randint(GRID_LEFT, grid_right)
        py = rng.randint(GRID_TOP, grid_bottom)
        dur    = rng.uniform(0.3, 0.9)
        delay  = anim_begin + rng.uniform(0, 0.5)
        radius = rng.randint(2, 6)

        if attack_type == "thunder":
            particles.append(
                f'<line x1="{cx}" y1="{cy-10}" x2="{px}" y2="{py}" '
                f'stroke="{attack_color}" stroke-width="2" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</line>')
        elif attack_type == "fire":
            particles.append(
                f'<circle cx="{px}" cy="{py}" r="{radius}" fill="{attack_color}" opacity="0">'
                f'<animateTransform attributeName="transform" type="translate" '
                f'values="0,0; {rng.randint(-5,5)},{rng.randint(-15,-5)}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animate attributeName="opacity" values="0;0.9;0.9;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animate attributeName="r" values="{radius};{radius*2};0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</circle>')
        elif attack_type == "water":
            particles.append(
                f'<ellipse cx="{px}" cy="{py}" rx="{radius}" ry="{int(radius*0.5)}" '
                f'fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;0.8;0.8;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'values="0,0;{rng.randint(-8,8)},{rng.randint(-8,8)}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</ellipse>')
        elif attack_type == "grass":
            particles.append(
                f'<polygon points="{px},{py-radius} {px+radius},{py+radius} {px-radius},{py+radius}" '
                f'fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="rotate" '
                f'values="0,{px},{py};360,{px},{py}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</polygon>')
        elif attack_type == "psychic":
            particles.append(
                f'<circle cx="{px}" cy="{py}" r="{radius}" fill="none" '
                f'stroke="{attack_color}" stroke-width="2" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animate attributeName="r" values="{radius};{radius*3};{radius*5}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</circle>')
        elif attack_type == "ghost":
            particles.append(
                f'<circle cx="{px}" cy="{py}" r="{radius}" fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;0.7;0;0.7;0" '
                f'dur="{dur*2:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</circle>')
        elif attack_type == "rock":
            particles.append(
                f'<rect x="{px-radius}" y="{py-radius}" width="{radius*2}" height="{radius*2}" '
                f'fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'values="0,0;{rng.randint(-10,10)},{rng.randint(5,15)}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</rect>')
        elif attack_type == "dragon":
            particles.append(
                f'<circle cx="{px}" cy="{py}" r="{radius}" fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;0.5;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animate attributeName="cx" values="{cx};{px}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animate attributeName="cy" values="{cy};{py}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</circle>')
        elif attack_type == "ice":
            particles.append(
                f'<line x1="{px-radius}" y1="{py}" x2="{px+radius}" y2="{py}" '
                f'stroke="{attack_color}" stroke-width="2" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</line>'
                f'<line x1="{px}" y1="{py-radius}" x2="{px}" y2="{py+radius}" '
                f'stroke="{attack_color}" stroke-width="2" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</line>')
        elif attack_type == "dark":
            particles.append(
                f'<circle cx="{px}" cy="{py}" r="{radius}" fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;0.8;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animate attributeName="r" values="0;{radius*2};0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</circle>')
        elif attack_type == "steel":
            particles.append(
                f'<rect x="{px-2}" y="{py-radius}" width="4" height="{radius*2}" '
                f'fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="rotate" '
                f'values="0,{px},{py};45,{px},{py}" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</rect>')
        else:  # normal / flying
            particles.append(
                f'<circle cx="{px}" cy="{py}" r="{radius}" fill="{attack_color}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;0" '
                f'dur="{dur:.2f}s" begin="{delay:.2f}s" fill="freeze"/>'
                f'</circle>')

    return "".join(particles)


def cell_destruction(week, day, anim_begin, attack_color):
    """Flash a contribution cell when attacked."""
    cid = cell_id(week, day)
    return (
        f'<animate href="#{cid}" attributeName="fill" '
        f'values="{attack_color};#161b22" '
        f'dur="0.4s" begin="{anim_begin:.2f}s" fill="freeze"/>'
    )


def build_svg(grid):
    """Build the complete animated SVG."""
    rng = random.Random(42)  # fixed seed for reproducibility

    grid_right  = GRID_LEFT + WEEKS * (CELL_SIZE + CELL_GAP)
    grid_bottom = GRID_TOP  + DAYS  * (CELL_SIZE + CELL_GAP)

    # ── Build roster: Pikachu first, rest randomized ─────────────────────────
    roster = [POKEMON_ROSTER[0]] + rng.sample(POKEMON_ROSTER[1:], len(POKEMON_ROSTER) - 1)

    # Flatten all contribution cells sorted by level desc (most active attacked last = dramatic)
    all_cells = [(w, d) for w in range(WEEKS) for d in range(DAYS)]
    # Assign each Pokémon a slice of cells to "destroy"
    cells_per_pokemon = max(1, len(all_cells) // len(roster))

    # Per-Pokémon timing
    ATTACK_DURATION  = 3.0   # seconds per Pokémon attack phase
    ENTER_DURATION   = 0.8   # enter animation
    EXIT_DURATION    = 0.8   # exit animation
    TURN_DURATION    = ENTER_DURATION + ATTACK_DURATION + EXIT_DURATION
    TOTAL_DURATION   = TURN_DURATION * len(roster)

    lines = []
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  width="{SVG_W}" height="{SVG_H}"
  viewBox="0 0 {SVG_W} {SVG_H}">

  <defs>
    <style>
      .pokemon-name {{ font: bold 11px monospace; fill: #58a6ff; }}
      .attack-name  {{ font: 9px monospace; fill: #ffa657; }}
      .label        {{ font: 10px monospace; fill: #8b949e; }}
      .title        {{ font: bold 13px monospace; fill: #58a6ff; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{SVG_W}" height="{SVG_H}" fill="#0d1117" rx="8"/>

  <!-- Title -->
  <text x="{SVG_W//2}" y="22" class="title" text-anchor="middle">
    ⚔ Pokémon Contribution Battle — chimataraghuram ⚔
  </text>

  <!-- Day labels -->''')

    day_labels = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    for d, lbl in enumerate(day_labels):
        if d % 2 == 1:
            lines.append(f'  <text x="{GRID_LEFT-18}" y="{cell_y(d)+9}" class="label">{lbl}</text>')

    # Month labels
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    today = datetime.date.today()
    start = today - datetime.timedelta(weeks=52)
    prev_month = None
    for w in range(WEEKS):
        week_date = start + datetime.timedelta(weeks=w)
        m = week_date.month
        if m != prev_month:
            lines.append(f'  <text x="{cell_x(w)}" y="{GRID_TOP-10}" class="label">{month_names[m-1]}</text>')
            prev_month = m

    lines.append('\n  <!-- Contribution grid cells -->')
    # Draw cells
    for w in range(WEEKS):
        for d in range(DAYS):
            lvl   = grid[w][d]
            color = LEVEL_COLORS[lvl]
            cid   = cell_id(w, d)
            x     = cell_x(w)
            y     = cell_y(d)
            lines.append(
                f'  <rect id="{cid}" x="{x}" y="{y}" '
                f'width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'rx="2" fill="{color}"/>')

    lines.append('\n  <!-- Pokémon battle animations -->')

    # Flatten cell list and shuffle for attack order
    cell_list = all_cells[:]
    rng.shuffle(cell_list)

    # Progress bar base
    BAR_Y = grid_bottom + 25
    BAR_X = GRID_LEFT
    BAR_W = grid_right - GRID_LEFT
    lines.append(f'  <rect x="{BAR_X}" y="{BAR_Y}" width="{BAR_W}" height="6" rx="3" fill="#21262d"/>')

    for idx, (name, color, body_shape, attack_name, attack_color, attack_type) in enumerate(roster):
        t_start  = idx * TURN_DURATION
        t_enter  = t_start
        t_attack = t_start + ENTER_DURATION
        t_exit   = t_attack + ATTACK_DURATION

        # Pokémon enter from alternating sides
        enter_from_right = (idx % 2 == 0)
        start_x = grid_right + 30 if enter_from_right else GRID_LEFT - 50
        park_x  = grid_right + 15 if enter_from_right else GRID_LEFT - 35
        end_x   = grid_right + 80 if enter_from_right else GRID_LEFT - 80
        poke_y  = GRID_TOP + GRID_H // 2

        gid = f"poke_{idx}"

        # Pokémon sprite group with enter/exit animation
        sprite_svg = pokemon_sprite_path(name, color, body_shape, 0, 0, 20)
        lines.append(f'''
  <!-- Pokémon {idx+1}: {name} -->
  <g id="{gid}" opacity="0">
    {sprite_svg}
    <!-- Name label below sprite -->
    <text x="0" y="18" class="pokemon-name" text-anchor="middle">{name}</text>
    <text x="0" y="30" class="attack-name" text-anchor="middle">{attack_name}</text>

    <!-- Enter: appear + move to park position -->
    <animate attributeName="opacity" values="0;1" dur="0.3s" begin="{t_enter:.2f}s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate"
      values="{start_x},{poke_y}; {park_x},{poke_y}"
      dur="{ENTER_DURATION:.2f}s" begin="{t_enter:.2f}s" fill="freeze"/>

    <!-- Exit: move out + fade -->
    <animateTransform attributeName="transform" type="translate"
      values="{park_x},{poke_y}; {end_x},{poke_y}"
      dur="{EXIT_DURATION:.2f}s" begin="{t_exit:.2f}s" fill="freeze"/>
    <animate attributeName="opacity" values="1;0" dur="0.3s" begin="{t_exit+EXIT_DURATION-0.3:.2f}s" fill="freeze"/>
  </g>''')

        # Attack particles
        attack_cx = park_x
        attack_cy = poke_y
        particles_svg = attack_particles(
            attack_type, attack_color,
            attack_cx, attack_cy,
            grid_right, grid_bottom,
            idx, t_attack, len(roster)
        )
        lines.append(f'  <!-- Attack particles for {name} -->')
        lines.append(f'  {particles_svg}')

        # Cell destruction: destroy a slice of cells during attack
        cell_start_idx = idx * cells_per_pokemon
        cell_end_idx   = min(cell_start_idx + cells_per_pokemon, len(cell_list))
        for ci, (cw, cd) in enumerate(cell_list[cell_start_idx:cell_end_idx]):
            cell_t = t_attack + (ci / max(1, cell_end_idx - cell_start_idx)) * ATTACK_DURATION * 0.8
            lines.append(f'  {cell_destruction(cw, cd, cell_t, attack_color)}')

        # Progress bar fill
        progress = (idx + 1) / len(roster)
        lines.append(
            f'  <rect x="{BAR_X}" y="{BAR_Y}" width="0" height="6" rx="3" fill="{color}" opacity="0">'
            f'<animate attributeName="width" values="0;{int(BAR_W * progress)}" dur="0.5s" begin="{t_exit:.2f}s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="0;1" dur="0.1s" begin="{t_enter:.2f}s" fill="freeze"/>'
            f'</rect>')

    # Infinite loop restart: reset everything after last exit
    # (SVG SMIL doesn't natively loop complex scenes; we use repeatCount="indefinite" on the full SVG via a wrapper)
    # Footer legend
    legend_y = BAR_Y + 25
    for lvl, lc in LEVEL_COLORS.items():
        lx = GRID_LEFT + lvl * 18
        lines.append(f'  <rect x="{lx}" y="{legend_y}" width="11" height="11" rx="2" fill="{lc}"/>')
    lines.append(f'  <text x="{GRID_LEFT + 5*18}" y="{legend_y+9}" class="label">  Less ← More contributions</text>')

    lines.append('</svg>')
    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"Fetching contributions for @{USERNAME}...")
    grid = fetch_contributions()

    print("Building SVG...")
    svg = build_svg(grid)

    # Avoid unnecessary writes: compare hashes
    new_hash = hashlib.md5(svg.encode()).hexdigest()
    old_hash = ""
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, "rb") as f:
            old_hash = hashlib.md5(f.read()).hexdigest()

    if new_hash == old_hash:
        print("SVG unchanged — skipping write.")
    else:
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            f.write(svg)
        size_kb = len(svg.encode()) / 1024
        print(f"Written {OUT_FILE} ({size_kb:.1f} KB)")

    # Verification
    print("\n--- Pokémon Roster Verification ---")
    names = [p[0] for p in POKEMON_ROSTER]
    print(f"Total Pokémon: {len(names)}")
    print(f"Pikachu first: {names[0] == 'Pikachu'}")
    print(f"Raichu absent: {'Raichu' not in names}")
    print(f"Bulbasaur present: {'Bulbasaur' in names}")
    print(f"Onix present: {'Onix' in names}")
    print(f"Unique names: {len(names) == len(set(names))}")
    if len(names) != 50:
        print(f"ERROR: Expected 50, got {len(names)}")
    else:
        print("All 50 Pokémon verified ✓")


if __name__ == "__main__":
    main()
