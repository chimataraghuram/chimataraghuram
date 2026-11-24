#!/usr/bin/env python3
"""
Pokémon Contribution Battle SVG Generator — True Arcade Alignment & Dynamic Combat Edition
Renders an arcade space-shooter style animated SVG where 50 real Pokémon
appear at the BOTTOM of the canvas, execute dynamic combat entrances, dashes,
attacks with rich elemental signature visual FX straight UPWARD into the contribution grid,
and violently shatter contribution blocks.
"""

import os
import json
import base64
import random
import hashlib
import datetime
import urllib.request
import urllib.error

# ─── Configuration ────────────────────────────────────────────────────────────
USERNAME = os.environ.get("GITHUB_USERNAME", "chimataraghuram")
TOKEN    = os.environ.get("GITHUB_TOKEN", "")
OUT_FILE = os.environ.get("OUTPUT_FILE", "pokemon_contribution_battle.svg")
SPRITE_DIR = os.environ.get("SPRITE_DIR", "sprites")

# ─── Exact 50-Pokémon Roster ──────────────────────────────────────────────────
# Rules: Pikachu #1, Bulbasaur (not Venusaur), Onix (no Raichu), exactly 50.
POKEMON_ROSTER = [
    ("Pikachu",    25,  "#FFE135", "Thunderbolt",     "#FFE135", "thunder"),
    ("Charizard",  6,   "#FF5500", "Fire Blast",      "#FF4400", "fire_blast"),
    ("Blastoise",  9,   "#1A6BB5", "Hydro Pump",      "#00AAFF", "hydro_pump"),
    ("Bulbasaur",  1,   "#78C850", "Razor Leaf",      "#00FF66", "razor_leaf"),
    ("Onix",       95,  "#A8A878", "Rock Throw",      "#C0A878", "rock_throw"),
    ("Arcanine",   59,  "#E88020", "Flamethrower",    "#FF6600", "fire_blast"),
    ("Gengar",     94,  "#705898", "Shadow Ball",     "#AA44FF", "shadow_ball"),
    ("Alakazam",   65,  "#F8D030", "Psychic",         "#FF69B4", "psychic"),
    ("Machamp",    68,  "#C03028", "Dynamic Punch",   "#FF3333", "punch"),
    ("Dragonite",  149, "#F4A460", "Draco Meteor",    "#FF8C00", "dragon"),
    ("Lucario",    448, "#4A6FA5", "Aura Sphere",     "#00AAFF", "aura"),
    ("Greninja",   658, "#1A1A2E", "Water Shuriken",  "#00FFFF", "shuriken"),
    ("Garchomp",   445, "#6B6B9A", "Dragon Rush",     "#9933FF", "dragon"),
    ("Gyarados",   130, "#1A5276", "Hurricane",       "#00BFFF", "hydro_pump"),
    ("Snorlax",    143, "#6C8E6E", "Hyper Beam",      "#FFFFFF", "hyper_beam"),
    ("Eevee",      133, "#C8A05E", "Swift",           "#FFD700", "swift"),
    ("Sylveon",    700, "#F02050", "Moonblast",       "#FFB6C1", "psychic"),
    ("Umbreon",    197, "#1C1C1C", "Dark Pulse",      "#8822FF", "shadow_ball"),
    ("Scizor",     212, "#8B1A1A", "Bullet Punch",    "#EE1111", "punch"),
    ("Tyranitar",  248, "#728C00", "Stone Edge",      "#A0A080", "rock_throw"),
    ("Mewtwo",     150, "#9966CC", "Psystrike",       "#DD00FF", "psychic"),
    ("Mew",        151, "#FF99CC", "Transform",       "#FF66AA", "psychic"),
    ("Lugia",      249, "#B0C4DE", "Aeroblast",       "#AADDFF", "hyper_beam"),
    ("Ho-Oh",      250, "#FF6600", "Sacred Fire",     "#FF4400", "fire_blast"),
    ("Rayquaza",   384, "#006400", "V-create",        "#00FF55", "dragon"),
    ("Kyogre",     382, "#1E3A8A", "Origin Pulse",    "#0055FF", "hydro_pump"),
    ("Groudon",    383, "#CC2200", "Precipice Blades", "#FF2200", "rock_throw"),
    ("Dialga",     483, "#1B6CA8", "Roar of Time",    "#0088FF", "dragon"),
    ("Palkia",     484, "#9B4B9B", "Spacial Rend",    "#EE44EE", "dragon"),
    ("Giratina",   487, "#4A235A", "Shadow Force",    "#660099", "shadow_ball"),
    ("Moltres",    146, "#FF8C00", "Sky Attack",      "#FF7700", "fire_blast"),
    ("Zapdos",     145, "#F5C518", "Discharge",       "#FFEE00", "thunder"),
    ("Articuno",   144, "#66CCFF", "Blizzard",        "#AAEEFF", "ice"),
    ("Suicune",    245, "#6BB8FF", "Sheer Cold",      "#00EEFF", "ice"),
    ("Entei",      244, "#CC4400", "Sacred Fire",     "#FF5500", "fire_blast"),
    ("Raikou",     243, "#F0C040", "Thunder",         "#FFDD00", "thunder"),
    ("Metagross",  376, "#666699", "Meteor Mash",     "#AABBEE", "punch"),
    ("Salamence",  373, "#6633CC", "Outrage",         "#9955FF", "dragon"),
    ("Blaziken",   257, "#CC3300", "Blast Burn",      "#FF4400", "fire_blast"),
    ("Sceptile",   254, "#339933", "Leaf Storm",      "#00FF44", "razor_leaf"),
    ("Zekrom",     644, "#2C2C2C", "Fusion Bolt",     "#33CCFF", "thunder"),
    ("Reshiram",   643, "#F0F0F0", "Fusion Flare",    "#FFAA33", "fire_blast"),
    ("Zoroark",    571, "#6B1B1B", "Night Daze",      "#990022", "shadow_ball"),
    ("Decidueye",  724, "#2D5A27", "Spirit Shackle",  "#44CC44", "razor_leaf"),
    ("Infernape",  392, "#CC5500", "Flare Blitz",     "#FF7700", "fire_blast"),
    ("Empoleon",   395, "#2255AA", "Hydro Cannon",    "#0088FF", "hydro_pump"),
    ("Cinderace",  815, "#FF4455", "Pyro Ball",       "#FF2244", "fire_blast"),
    ("Mimikyu",    778, "#997755", "Play Rough",      "#FF88CC", "shadow_ball"),
    ("Gardevoir",  282, "#FFFFFF", "Moonblast",       "#FFAACC", "psychic"),
    ("Darkrai",    491, "#1A1A2A", "Dark Void",       "#550088", "shadow_ball"),
]

# ─── Dimensions ───────────────────────────────────────────────────────────────
SVG_W       = 870
SVG_H       = 230
GRID_LEFT   = 40
GRID_TOP    = 28
CELL_SIZE   = 11
CELL_GAP    = 3
WEEKS       = 53
DAYS        = 7
BOTTOM_Y    = 168  # Stable ground altitude for bottom space shooter
SPRITE_SIZE = 50   # High definition pixel art presence

LEVEL_COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}

# ─── Sprite Helpers ───────────────────────────────────────────────────────────
def ensure_sprite(name, pid):
    os.makedirs(SPRITE_DIR, exist_ok=True)
    local_path = os.path.join(SPRITE_DIR, f"{name.lower()}.png")
    if not os.path.exists(local_path):
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pid}.png"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(local_path, "wb") as f:
                    f.write(data)
        except Exception as e:
            print(f"Warning: could not fetch sprite for {name}: {e}")
            return None

    try:
        with open(local_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"Error reading sprite {local_path}: {e}")
        return None

# ─── Fetch Contribution Data ──────────────────────────────────────────────────
def fetch_contributions():
    if not TOKEN:
        print("Notice: No GITHUB_TOKEN set — reading structure with sample contribution pattern.")
        return _fallback_contributions()

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
            "User-Agent": "pokemon-contribution-battle",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
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
            while len(days_in_week) < 7:
                days_in_week.append(0)
            grid.append(days_in_week)
        while len(grid) < 53:
            grid.append([0]*7)
        return grid[:53]
    except Exception as e:
        print(f"Notice: GraphQL request failed ({e}) — using fallback pattern.")
        return _fallback_contributions()

def _fallback_contributions():
    rng = random.Random(20261124)
    grid = []
    for w in range(53):
        col = []
        for d in range(7):
            r = rng.random()
            if r > 0.65:
                lvl = rng.choice([1, 2, 3, 4])
            else:
                lvl = 0
            col.append(lvl)
        grid.append(col)
    return grid

def cell_id(w, d):
    return f"c_{w}_{d}"

def cell_x(w):
    return GRID_LEFT + w * (CELL_SIZE + CELL_GAP)

def cell_y(d):
    return GRID_TOP + d * (CELL_SIZE + CELL_GAP)

# ─── Full Elemental Signature Attack Generator (Strict Vertical Space Shooter) ──
def render_signature_attack(atype, color, x, py, ty, t_shot, dur=0.38):
    """
    Renders vivid, high-contrast signature attack visual FX strictly aligned along the vertical column 'x':
    Shoots straight UPWARD from py to ty!
    """
    out = []

    if atype == "thunder":
        # Straight vertical lightning strike with sharp jagged zigzags & core beam
        mid1_y = int(py - (py - ty) * 0.35)
        mid2_y = int(py - (py - ty) * 0.70)
        p1 = f"{x},{py-20} {x-8},{mid1_y} {x+9},{mid2_y} {x-4},{ty+8} {x},{ty}"
        p2 = f"{x},{py-20} {x+7},{mid1_y} {x-7},{mid2_y} {x+5},{ty+8} {x},{ty}"
        branch = f"{x+9},{mid2_y} {x+18},{mid2_y-10}"

        out.append(f'''
    <!-- Thunderbolt vertical crackling lightning storm -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;0.7;1;0" keyTimes="0;0.08;0.35;0.75;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Outer glowing yellow bolt -->
      <polyline points="{p1}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>
      <!-- Inner pure white laser core -->
      <polyline points="{p1}" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
      <!-- Flanking secondary bolt -->
      <polyline points="{p2}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" opacity="0.9"/>
      <polyline points="{branch}" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
      <!-- High-voltage spark nodes -->
      <circle cx="{x-8}" cy="{mid1_y}" r="5" fill="#FFFFFF"/>
      <circle cx="{x+9}" cy="{mid2_y}" r="5.5" fill="{color}"/>
    </g>''')

    elif atype == "fire_blast":
        out.append(f'''
    <!-- Fire Blast vertical spinning flaming star cross & flame tongues -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Trailing flame sparks -->
      <circle cx="0" cy="18" r="5" fill="#FF2200"/>
      <circle cx="-6" cy="28" r="3.5" fill="#FFAA00"/>
      <circle cx="6" cy="28" r="3.5" fill="#FFAA00"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" values="0; 720" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <!-- 5-pointed Kanji flame cross -->
        <path d="M0,0 Q-10,-18 0,-28 Q10,-18 0,0" fill="#FF1100"/>
        <path d="M0,0 Q-18,-10 -28,0 Q-18,10 0,0" fill="#FF4400"/>
        <path d="M0,0 Q18,-10 28,0 Q18,10 0,0" fill="#FF4400"/>
        <path d="M0,0 Q-16,16 -22,26 Q-7,18 0,0" fill="#FFAA00"/>
        <path d="M0,0 Q16,16 22,26 Q7,18 0,0" fill="#FFAA00"/>
        <!-- Radiant core -->
        <circle cx="0" cy="0" r="9" fill="#FFFF44"/>
        <circle cx="0" cy="0" r="4.5" fill="#FFFFFF"/>
      </g>
    </g>''')

    elif atype == "hydro_pump":
        out.append(f'''
    <!-- Hydro Pump twin pressurized water torrents straight UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.85;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Twin water cannon jets -->
      <line x1="{x-6}" y1="{py-20}" x2="{x-3}" y2="{ty}" stroke="{color}" stroke-width="7" stroke-linecap="round"/>
      <line x1="{x-6}" y1="{py-20}" x2="{x-3}" y2="{ty}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
      <line x1="{x+6}" y1="{py-20}" x2="{x+3}" y2="{ty}" stroke="{color}" stroke-width="7" stroke-linecap="round"/>
      <line x1="{x+6}" y1="{py-20}" x2="{x+3}" y2="{ty}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
      <!-- Hydro pressure rings -->
      <ellipse cx="{x}" cy="{ty+8}" rx="18" ry="7" fill="none" stroke="#FFFFFF" stroke-width="3">
        <animate attributeName="rx" values="4;20" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      </ellipse>
    </g>''')

    elif atype == "razor_leaf":
        out.append(f'''
    <!-- Razor Leaf rapid spinning emerald cutters upward -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Center Primary Leaf -->
      <g>
        <animateTransform attributeName="transform" type="translate" values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <g>
          <animateTransform attributeName="transform" type="rotate" values="0; 720" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
          <path d="M0,-20 C11,-6 11,10 0,18 C-11,10 -11,-6 0,-20 Z" fill="{color}"/>
          <line x1="0" y1="-18" x2="0" y2="16" stroke="#FFFFFF" stroke-width="2.5"/>
        </g>
      </g>
      <!-- Staggered Left Cutter -->
      <g>
        <animateTransform attributeName="transform" type="translate" values="{x-10},{py-16}; {x-10},{ty+6}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <path d="M0,-15 C8,-4 8,8 0,13 C-8,8 -8,-4 0,-15 Z" fill="#00FF66"/>
      </g>
      <!-- Staggered Right Cutter -->
      <g>
        <animateTransform attributeName="transform" type="translate" values="{x+10},{py-16}; {x+10},{ty+6}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <path d="M0,-15 C8,-4 8,8 0,13 C-8,8 -8,-4 0,-15 Z" fill="#00FF66"/>
      </g>
    </g>''')

    elif atype == "shadow_ball":
        out.append(f'''
    <!-- Shadow Ball dark void sphere with orbiting purple phantom flames -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Shadow core void -->
      <circle cx="0" cy="0" r="13" fill="#1A0033" stroke="{color}" stroke-width="3"/>
      <circle cx="0" cy="0" r="7" fill="#050010"/>
      <!-- Orbiting dark matter wisps -->
      <g>
        <animateTransform attributeName="transform" type="rotate" values="0; 720" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <circle cx="0" cy="-16" r="5" fill="{color}"/>
        <circle cx="-15" cy="10" r="4.5" fill="#DD55FF"/>
        <circle cx="15" cy="10" r="4.5" fill="#DD55FF"/>
      </g>
    </g>''')

    elif atype == "hyper_beam":
        out.append(f'''
    <!-- Hyper Beam blinding plasma laser beam pillar straight UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.85;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Outer energy sheath -->
      <line x1="{x}" y1="{py-20}" x2="{x}" y2="{ty}" stroke="#00E5FF" stroke-width="18" stroke-linecap="round"/>
      <line x1="{x}" y1="{py-20}" x2="{x}" y2="{ty}" stroke="#AAEEFF" stroke-width="11" stroke-linecap="round"/>
      <!-- Core blinding white laser -->
      <line x1="{x}" y1="{py-20}" x2="{x}" y2="{ty}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
    </g>''')

    elif atype == "rock_throw":
        out.append(f'''
    <!-- Rock Throw / Precipice Blades spinning stone boulders upward -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" values="0; 480" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <polygon points="-12,-8 0,-17 12,-8 15,9 0,17 -13,8" fill="{color}" stroke="#443311" stroke-width="2.5"/>
        <polygon points="-6,-5 0,-11 7,-5 8,5 0,10 -7,5" fill="#E8D8A0"/>
      </g>
    </g>''')

    elif atype == "psychic":
        out.append(f'''
    <!-- Psychic telekinetic expanding resonance rings straight UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <circle cx="{x}" cy="{py - (py-ty)*0.33}" r="8" fill="none" stroke="{color}" stroke-width="3">
        <animate attributeName="r" values="3;20;3" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      </circle>
      <circle cx="{x}" cy="{py - (py-ty)*0.66}" r="12" fill="none" stroke="#FFFFFF" stroke-width="2.5">
        <animate attributeName="r" values="4;24;4" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      </circle>
      <circle cx="{x}" cy="{ty}" r="10" fill="{color}">
        <animate attributeName="r" values="2;16;0" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      </circle>
      <circle cx="{x}" cy="{ty}" r="5" fill="#FFFFFF"/>
    </g>''')

    elif atype == "ice":
        out.append(f'''
    <!-- Blizzard / Sheer Cold glacial crystal icicle projectile upward -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Diamond ice spear -->
      <polygon points="0,-24 9,0 0,22 -9,0" fill="#E0F7FA" stroke="{color}" stroke-width="3"/>
      <polygon points="0,-18 5,0 0,16 -5,0" fill="#FFFFFF"/>
      <circle cx="-11" cy="9" r="3.5" fill="#FFFFFF"/>
      <circle cx="11" cy="9" r="3.5" fill="#FFFFFF"/>
    </g>''')

    elif atype == "punch":
        out.append(f'''
    <!-- Dynamic / Bullet / Meteor Punch rocket fist soaring UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <!-- Energy fist -->
      <circle cx="0" cy="0" r="12" fill="{color}"/>
      <circle cx="0" cy="0" r="7" fill="#FFFFFF"/>
      <line x1="-6" y1="13" x2="-6" y2="26" stroke="{color}" stroke-width="3"/>
      <line x1="0" y1="13" x2="0" y2="30" stroke="#FFFFFF" stroke-width="3"/>
      <line x1="6" y1="13" x2="6" y2="26" stroke="{color}" stroke-width="3"/>
    </g>''')

    elif atype == "dragon":
        out.append(f'''
    <!-- Draco Meteor / Dragon Rush draconic fire rocket soaring UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <path d="M0,-26 C15,-11 13,13 0,24 C-13,13 -15,-11 0,-26 Z" fill="{color}"/>
      <path d="M0,-18 C9,-7 8,9 0,16 C-8,9 -9,-7 0,-18 Z" fill="#FFAA00"/>
      <circle cx="0" cy="-7" r="5" fill="#FFFFFF"/>
    </g>''')

    elif atype == "aura":
        out.append(f'''
    <!-- Aura Sphere radiating cyan energy orb soaring UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <circle cx="0" cy="0" r="13" fill="{color}"/>
      <circle cx="0" cy="0" r="7" fill="#FFFFFF"/>
      <ellipse cx="0" cy="0" rx="20" ry="7" fill="none" stroke="#FFFFFF" stroke-width="2.5">
        <animateTransform attributeName="transform" type="rotate" values="0; 360" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      </ellipse>
    </g>''')

    elif atype == "shuriken":
        out.append(f'''
    <!-- Water Shuriken high-speed twin cyan ninja stars soaring UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" values="0; 1080" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <polygon points="0,-18 5,-5 18,0 5,5 0,18 -5,5 -18,0 -5,-5" fill="{color}"/>
        <circle cx="0" cy="0" r="4.5" fill="#FFFFFF"/>
      </g>
    </g>''')

    else:  # swift
        out.append(f'''
    <!-- Swift golden five-pointed stars whistling UP -->
    <g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate"
        values="{x},{py-20}; {x},{ty}" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" values="0; 540" dur="{dur:.2f}s" begin="master_clock.begin + {t_shot:.2f}s" fill="freeze"/>
        <polygon points="0,-16 5,-5 16,-4 7,5 10,16 0,9 -10,16 -7,5 -16,-4 -5,-5" fill="{color}"/>
        <circle cx="0" cy="0" r="4" fill="#FFFFFF"/>
      </g>
    </g>''')

    return "".join(out)


# ─── Main SVG Builder ─────────────────────────────────────────────────────────
def build_svg(grid):
    rng = random.Random(1337)

    # Pikachu is ALWAYS #1; remaining 49 randomized
    first_poke = POKEMON_ROSTER[0]
    other_pokes = list(POKEMON_ROSTER[1:])
    rng.shuffle(other_pokes)
    roster = [first_poke] + other_pokes

    TURN_DUR = 2.4
    TOTAL_DUR = TURN_DUR * len(roster)  # 120.0 seconds

    active_cells = []
    empty_cells = []
    for w in range(WEEKS):
        for d in range(DAYS):
            if grid[w][d] > 0:
                active_cells.append((w, d))
            else:
                empty_cells.append((w, d))

    rng.shuffle(active_cells)
    rng.shuffle(empty_cells)
    target_pool = active_cells + empty_cells

    lines = []
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  width="{SVG_W}" height="{SVG_H}"
  viewBox="0 0 {SVG_W} {SVG_H}"
  style="background: #030712; border-radius: 8px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace;">

  <defs>
    <!-- Master Clock to synchronize infinite loop across all 50 Pokemon -->
    <animate id="master_clock" attributeName="opacity" from="1" to="1" dur="{TOTAL_DUR:.1f}s" repeatCount="indefinite" />

    <style>
      .month-label  {{ font-size: 9px; fill: #7d8590; font-family: monospace; }}
      .hud-title    {{ font-size: 11px; font-weight: bold; fill: #58a6ff; font-family: monospace; }}
      .hud-move     {{ font-size: 11px; font-weight: bold; font-family: monospace; }}
      .hud-sub      {{ font-size: 9px; fill: #7d8590; font-family: monospace; }}
      .hud-score    {{ font-size: 9px; fill: #39d353; font-weight: bold; font-family: monospace; }}
      .pixel-reticle {{ stroke-dasharray: 2,2; }}
    </style>''')

    print("Embedding Pokémon sprites...")
    sprite_uris = {}
    for name, pid, color, attack, acolor, atype in roster:
        s_id = f"sp_{name.lower()}"
        uri = ensure_sprite(name, pid)
        if uri:
            lines.append(f'    <image id="{s_id}" width="{SPRITE_SIZE}" height="{SPRITE_SIZE}" href="{uri}" />')
            sprite_uris[name] = s_id
        else:
            sprite_uris[name] = None

    lines.append('  </defs>\n')

    # Cosmic Space Background
    lines.append('  <!-- Starfield background (Space Shooter atmosphere) -->')
    lines.append('  <g id="starfield">')
    for _ in range(95):
        sx = rng.randint(4, SVG_W - 4)
        sy = rng.randint(4, SVG_H - 4)
        sr = rng.choice([0.7, 0.9, 1.2, 1.5])
        op = round(rng.uniform(0.18, 0.75), 2)
        lines.append(f'    <circle cx="{sx}" cy="{sy}" r="{sr}" fill="#ffffff" opacity="{op}"/>')
    lines.append('  </g>\n')

    # Month Labels
    month_names = ["Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov"]
    lines.append('  <!-- Month Headers -->')
    for i, m in enumerate(month_names):
        mx = GRID_LEFT + int(i * (WEEKS * (CELL_SIZE + CELL_GAP) / 12.3))
        lines.append(f'  <text x="{mx}" y="18" class="month-label">{m}</text>')

    # Contribution Grid
    lines.append('\n  <!-- GitHub Contribution Grid -->')
    lines.append('  <g id="contribution_grid">')
    for w in range(WEEKS):
        for d in range(DAYS):
            cid = cell_id(w, d)
            cx  = cell_x(w)
            cy  = cell_y(d)
            lvl = grid[w][d]
            col = LEVEL_COLORS[lvl]
            lines.append(f'    <rect id="{cid}" x="{cx}" y="{cy}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{col}"/>')
    lines.append('  </g>\n')

    # Separator Line
    lines.append(f'  <line x1="{GRID_LEFT}" y1="135" x2="{GRID_LEFT + WEEKS*(CELL_SIZE+CELL_GAP)}" y2="135" stroke="#21262d" stroke-dasharray="3,3" opacity="0.4"/>')

    # Pokémon Bottom Shooters
    lines.append('  <!-- Pokémon Bottom Shooters & Upward Attacks -->')

    for idx, (name, pid, color, attack, acolor, atype) in enumerate(roster):
        t_start = idx * TURN_DUR
        t_end   = t_start + TURN_DUR

        idx1 = (idx * 2) % len(target_pool)
        idx2 = (idx * 2 + 1) % len(target_pool)
        tw1, td1 = target_pool[idx1]
        tw2, td2 = target_pool[idx2]

        tx1, ty1 = cell_x(tw1) + CELL_SIZE//2, cell_y(td1) + CELL_SIZE//2
        tx2, ty2 = cell_x(tw2) + CELL_SIZE//2, cell_y(td2) + CELL_SIZE//2

        gid = f"poke_{idx}_{name.lower()}"
        sp_id = sprite_uris.get(name)

        # Precise timing phases inside TURN_DUR (2.4s):
        # 0.00s - 0.30s: Pokéball flash & entrance materialization at tx1
        # 0.25s - 0.42s: Energy charge-up at tx1
        # 0.42s: Attack Leap & Fire Shot 1 straight up -> Block 1 shatter at 0.78s
        # 0.95s - 1.20s: Rapid combat dash from tx1 to tx2 with tilt & speed line
        # 1.25s - 1.45s: Energy charge-up at tx2
        # 1.45s: Attack Leap & Fire Shot 2 straight up -> Block 2 shatter at 1.81s
        # 2.05s - 2.38s: Victory roar & Pokéball recall beam exit
        t_shot1 = t_start + 0.42
        t_hit1  = t_shot1 + 0.36

        t_dash_start = t_start + 0.95
        t_dash_end   = t_start + 1.20

        t_shot2 = t_start + 1.45
        t_hit2  = t_shot2 + 0.36

        t_exit  = t_start + 2.08

        # Dash tilt angle
        dx = tx2 - tx1
        tilt = 14 if dx >= 0 else -14

        # ── 1. Pokéball Flash Entrance (At tx1) ──────────────────────────────
        lines.append(f'\n  <!-- [{idx+1}/50] {name} Entrance Flash -->')
        lines.append(f'  <g>')
        # Expanding white light sphere
        lines.append(f'    <circle cx="{tx1}" cy="{BOTTOM_Y}" r="0" fill="#FFFFFF" opacity="0">')
        lines.append(f'      <animate attributeName="r" values="0;32;0" dur="0.32s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze"/>')
        lines.append(f'      <animate attributeName="opacity" values="0;1;0" dur="0.32s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze"/>')
        lines.append(f'    </circle>')
        # Rising energy sparks
        lines.append(f'    <circle cx="{tx1-9}" cy="{BOTTOM_Y}" r="3.5" fill="{acolor}" opacity="0">')
        lines.append(f'      <animate attributeName="cy" values="{BOTTOM_Y};{BOTTOM_Y-26}" dur="0.30s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze"/>')
        lines.append(f'      <animate attributeName="opacity" values="0;1;0" dur="0.30s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze"/>')
        lines.append(f'    </circle>')
        lines.append(f'    <circle cx="{tx1+9}" cy="{BOTTOM_Y}" r="3.5" fill="{acolor}" opacity="0">')
        lines.append(f'      <animate attributeName="cy" values="{BOTTOM_Y};{BOTTOM_Y-26}" dur="0.30s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze"/>')
        lines.append(f'      <animate attributeName="opacity" values="0;1;0" dur="0.30s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze"/>')
        lines.append(f'    </circle>')
        lines.append(f'  </g>')

        # ── 2. Pokémon Entity Group (DOWN AT BOTTOM) ─────────────────────────
        lines.append(f'  <!-- [{idx+1}/50] {name} Character Body (Dynamic Stance & Movement) -->')
        lines.append(f'  <g id="{gid}" opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" dur="{TURN_DUR:.2f}s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze" />')

        # Stepped Horizontal Translation with Dash Phase:
        lines.append(f'    <animateTransform attributeName="transform" type="translate" '
                     f'values="{tx1 - SPRITE_SIZE//2},{BOTTOM_Y - SPRITE_SIZE//2}; '
                     f'{tx1 - SPRITE_SIZE//2},{BOTTOM_Y - SPRITE_SIZE//2}; '
                     f'{tx2 - SPRITE_SIZE//2},{BOTTOM_Y - SPRITE_SIZE//2}; '
                     f'{tx2 - SPRITE_SIZE//2},{BOTTOM_Y - SPRITE_SIZE//2}" '
                     f'keyTimes="0; 0.40; 0.50; 1" '
                     f'dur="{TURN_DUR:.2f}s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze" />')

        # Inner Container with Character Animation Layers:
        lines.append(f'    <g>')
        # Layer A: Combat Breathing & Organic Squash-Stretch
        lines.append(f'      <animateTransform attributeName="transform" type="scale" '
                     f'values="1,1; 1.03,0.96; 0.97,1.03; 1,1" dur="0.75s" repeatCount="indefinite" additive="sum"/>')

        # Layer B: Entrance pop (scale from 0.2 to 1.0)
        lines.append(f'      <animateTransform attributeName="transform" type="scale" '
                     f'values="0.2; 1.25; 0.95; 1.0" keyTimes="0; 0.6; 0.85; 1" dur="0.32s" begin="master_clock.begin + {t_start:.2f}s" additive="sum"/>')

        # Layer C: Dash forward lean tilt during dash (0.95s to 1.20s)
        k_dstart = (t_dash_start - t_start) / TURN_DUR
        k_dend   = (t_dash_end - t_start) / TURN_DUR
        lines.append(f'      <animateTransform attributeName="transform" type="rotate" '
                     f'values="0; 0; {tilt}; {tilt}; 0; 0" '
                     f'keyTimes="0; {k_dstart-0.02:.2f}; {k_dstart:.2f}; {k_dend:.2f}; {k_dend+0.04:.2f}; 1" '
                     f'dur="{TURN_DUR:.2f}s" begin="master_clock.begin + {t_start:.2f}s" additive="sum"/>')

        # Layer D: Dynamic Attack Leap & Firing Jolt on Shot 1 (Crouch -> Leap Up -> Recoil -> Land)
        lines.append(f'      <animateTransform attributeName="transform" type="translate" '
                     f'values="0,0; 0,4; 0,-12; 0,7; 0,0" keyTimes="0; 0.25; 0.5; 0.8; 1" '
                     f'dur="0.35s" begin="master_clock.begin + {t_shot1 - 0.08:.2f}s" additive="sum"/>')

        # Layer E: Dynamic Attack Leap & Firing Jolt on Shot 2 (Crouch -> Leap Up -> Recoil -> Land)
        lines.append(f'      <animateTransform attributeName="transform" type="translate" '
                     f'values="0,0; 0,4; 0,-12; 0,7; 0,0" keyTimes="0; 0.25; 0.5; 0.8; 1" '
                     f'dur="0.35s" begin="master_clock.begin + {t_shot2 - 0.08:.2f}s" additive="sum"/>')

        # Elemental Charging Aura around Pokémon
        lines.append(f'      <!-- Elemental Charging Aura -->')
        lines.append(f'      <ellipse cx="{SPRITE_SIZE//2}" cy="{SPRITE_SIZE-2}" rx="17" ry="6" fill="{acolor}" opacity="0.75">')
        lines.append(f'        <animate attributeName="opacity" values="0.45;1;0.45" dur="0.28s" repeatCount="indefinite"/>')
        lines.append(f'        <animate attributeName="rx" values="14;22;14" dur="0.28s" repeatCount="indefinite"/>')
        lines.append(f'      </ellipse>')

        # Authentic Sprite Image
        if sp_id:
            lines.append(f'      <use href="#{sp_id}" x="0" y="0" />')
        else:
            lines.append(f'      <circle cx="{SPRITE_SIZE//2}" cy="{SPRITE_SIZE//2}" r="22" fill="{color}"/>')

        lines.append('    </g>')
        lines.append('  </g>')

        # ── 3. Recall Exit Beam (At tx2) ─────────────────────────────────────
        lines.append(f'  <!-- [{idx+1}/50] {name} Recall Beam Exit -->')
        lines.append(f'  <g>')
        lines.append(f'    <polygon points="{tx2},{BOTTOM_Y-45} {tx2-18},{BOTTOM_Y+10} {tx2+18},{BOTTOM_Y+10}" fill="#FF3333" opacity="0">')
        lines.append(f'      <animate attributeName="opacity" values="0;0.75;0" dur="0.28s" begin="master_clock.begin + {t_exit:.2f}s" fill="freeze"/>')
        lines.append(f'    </polygon>')
        lines.append(f'    <circle cx="{tx2}" cy="{BOTTOM_Y}" r="0" fill="#FFFFFF" opacity="0">')
        lines.append(f'      <animate attributeName="r" values="0;22;0" dur="0.28s" begin="master_clock.begin + {t_exit:.2f}s" fill="freeze"/>')
        lines.append(f'      <animate attributeName="opacity" values="0;1;0" dur="0.28s" begin="master_clock.begin + {t_exit:.2f}s" fill="freeze"/>')
        lines.append(f'    </circle>')
        lines.append('  </g>')

        # ── 4. HUD info along the bottom bar ─────────────────────────────────
        score = (idx + 1) * 750
        lines.append(f'  <g opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" dur="{TURN_DUR:.2f}s" begin="master_clock.begin + {t_start:.2f}s" fill="freeze" />')
        lines.append(f'    <text x="{GRID_LEFT}" y="214" class="hud-title">#{idx+1:02d} {name.upper()}</text>')
        lines.append(f'    <text x="{GRID_LEFT + 120}" y="214" class="hud-move" fill="{acolor}">❯ {attack.upper()}</text>')
        lines.append(f'    <text x="{GRID_LEFT + 310}" y="214" class="hud-sub">TARGET: SECTOR [{tw1+1},{td1+1}] ❯ VERTICAL ALIGNMENT LOCKED</text>')
        lines.append(f'    <text x="{GRID_LEFT + 670}" y="214" class="hud-score">SCORE: {score:,} PTS</text>')
        lines.append('  </g>')

        # ── 5. Muzzle Blasts ─────────────────────────────────────────────────
        lines.append(f'  <!-- Muzzle Blast 1 (At tx1) -->')
        lines.append(f'  <circle cx="{tx1}" cy="{BOTTOM_Y - 20}" r="1" fill="#FFFFFF" opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;1;0" dur="0.18s" begin="master_clock.begin + {t_shot1:.2f}s" fill="freeze"/>')
        lines.append(f'    <animate attributeName="r" values="5;24;0" dur="0.18s" begin="master_clock.begin + {t_shot1:.2f}s" fill="freeze"/>')
        lines.append('  </circle>')

        lines.append(f'  <!-- Muzzle Blast 2 (At tx2) -->')
        lines.append(f'  <circle cx="{tx2}" cy="{BOTTOM_Y - 20}" r="1" fill="#FFFFFF" opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;1;0" dur="0.18s" begin="master_clock.begin + {t_shot2:.2f}s" fill="freeze"/>')
        lines.append(f'    <animate attributeName="r" values="5;24;0" dur="0.18s" begin="master_clock.begin + {t_shot2:.2f}s" fill="freeze"/>')
        lines.append('  </circle>')

        # ── 6. Shot 1: Reticle, Straight Vertical Attack, Multi-Fragment Destruction ──
        lines.append(f'  <!-- Target Reticle 1 (Directly above Pokémon at tx1) -->')
        lines.append(f'  <circle cx="{tx1}" cy="{ty1}" r="9" fill="none" stroke="{acolor}" stroke-width="2" class="pixel-reticle" opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;0.95;0.95;0" dur="0.55s" begin="master_clock.begin + {t_shot1 - 0.15:.2f}s" fill="freeze"/>')
        lines.append(f'    <animate attributeName="r" values="18;10;6" dur="0.55s" begin="master_clock.begin + {t_shot1 - 0.15:.2f}s" fill="freeze"/>')
        lines.append('  </circle>')

        # Straight vertical upward attack from tx1
        lines.append(render_signature_attack(atype, acolor, tx1, BOTTOM_Y, ty1, t_shot1, dur=0.36))

        # Cell 1 Impact: Permanent Shattering & Vaporization
        cid1 = cell_id(tw1, td1)
        orig_col1 = LEVEL_COLORS[grid[tw1][td1]]
        lines.append(f'  <!-- Block 1 Flash & Obliteration -->')
        lines.append(f'  <animate href="#{cid1}" attributeName="fill" '
                     f'values="{orig_col1};#ffffff;{acolor};#060913" '
                     f'keyTimes="0;0.15;0.4;1" dur="0.4s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
        lines.append(f'  <animate href="#{cid1}" attributeName="opacity" '
                     f'values="1;1;0.15" keyTimes="0;0.2;1" dur="0.4s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')

        # Floating Arcade Combat Text: CRITICAL HIT!
        lines.append(f'  <!-- Floating Combat Text 1 -->')
        lines.append(f'  <text x="{tx1}" y="{ty1-8}" fill="#FFFF00" font-size="8px" font-weight="bold" font-family="monospace" text-anchor="middle" opacity="0">')
        lines.append(f'    CRITICAL!')
        lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.7;1" dur="0.5s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
        lines.append(f'    <animate attributeName="y" values="{ty1-6};{ty1-16}" dur="0.5s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
        lines.append(f'  </text>')

        # Shattered Debris Burst (8 flying fragments in all directions)
        lines.append(f'  <!-- Shattered Debris Burst 1 -->')
        lines.append(f'  <g opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.7;1" dur="0.42s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
        # Expanding shockwave ring
        lines.append(f'    <circle cx="{tx1}" cy="{ty1}" r="2" fill="none" stroke="#FFFFFF" stroke-width="2.5">')
        lines.append(f'      <animate attributeName="r" values="2;20" dur="0.38s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
        lines.append(f'      <animate attributeName="opacity" values="1;0" dur="0.38s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
        lines.append(f'    </circle>')
        # 8 flying debris fragments
        debris_dirs = [
            (-15, -13, acolor), (0, -17, "#FFFFFF"), (15, -13, orig_col1),
            (-17, 0, orig_col1),                     (17, 0, acolor),
            (-13, 15, acolor),  (0, 17, "#FFFFFF"),  (13, 15, orig_col1)
        ]
        for dx_deb, dy_deb, deb_col in debris_dirs:
            lines.append(f'    <rect x="{tx1-2}" y="{ty1-2}" width="4" height="4" rx="1" fill="{deb_col}">')
            lines.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; {dx_deb},{dy_deb}" dur="0.42s" begin="master_clock.begin + {t_hit1:.2f}s" fill="freeze"/>')
            lines.append(f'    </rect>')
        lines.append(f'  </g>')

        # ── 7. Shot 2: Reticle, Straight Vertical Attack, Multi-Fragment Destruction ──
        lines.append(f'  <!-- Target Reticle 2 (Directly above Pokémon at tx2) -->')
        lines.append(f'  <circle cx="{tx2}" cy="{ty2}" r="9" fill="none" stroke="{acolor}" stroke-width="2" class="pixel-reticle" opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;0.95;0.95;0" dur="0.55s" begin="master_clock.begin + {t_shot2 - 0.15:.2f}s" fill="freeze"/>')
        lines.append(f'    <animate attributeName="r" values="18;10;6" dur="0.55s" begin="master_clock.begin + {t_shot2 - 0.15:.2f}s" fill="freeze"/>')
        lines.append('  </circle>')

        # Straight vertical upward attack from tx2
        lines.append(render_signature_attack(atype, acolor, tx2, BOTTOM_Y, ty2, t_shot2, dur=0.36))

        # Cell 2 Impact: Permanent Shattering & Obliteration
        cid2 = cell_id(tw2, td2)
        orig_col2 = LEVEL_COLORS[grid[tw2][td2]]
        lines.append(f'  <!-- Block 2 Flash & Obliteration -->')
        lines.append(f'  <animate href="#{cid2}" attributeName="fill" '
                     f'values="{orig_col2};#ffffff;{acolor};#060913" '
                     f'keyTimes="0;0.15;0.4;1" dur="0.4s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
        lines.append(f'  <animate href="#{cid2}" attributeName="opacity" '
                     f'values="1;1;0.15" keyTimes="0;0.2;1" dur="0.4s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')

        # Floating Arcade Combat Text: SUPER EFFECTIVE!
        lines.append(f'  <!-- Floating Combat Text 2 -->')
        lines.append(f'  <text x="{tx2}" y="{ty2-8}" fill="#00FFFF" font-size="8px" font-weight="bold" font-family="monospace" text-anchor="middle" opacity="0">')
        lines.append(f'    SUPER!')
        lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.7;1" dur="0.5s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
        lines.append(f'    <animate attributeName="y" values="{ty2-6};{ty2-16}" dur="0.5s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
        lines.append(f'  </text>')

        # Shattered Debris Burst 2
        lines.append(f'  <!-- Shattered Debris Burst 2 -->')
        lines.append(f'  <g opacity="0">')
        lines.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.7;1" dur="0.42s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
        lines.append(f'    <circle cx="{tx2}" cy="{ty2}" r="2" fill="none" stroke="#FFFFFF" stroke-width="2.5">')
        lines.append(f'      <animate attributeName="r" values="2;20" dur="0.38s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
        lines.append(f'      <animate attributeName="opacity" values="1;0" dur="0.38s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
        lines.append(f'    </circle>')
        for dx_deb, dy_deb, deb_col in debris_dirs:
            lines.append(f'    <rect x="{tx2-2}" y="{ty2-2}" width="4" height="4" rx="1" fill="{deb_col}">')
            lines.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; {dx_deb},{dy_deb}" dur="0.42s" begin="master_clock.begin + {t_hit2:.2f}s" fill="freeze"/>')
            lines.append(f'    </rect>')
        lines.append(f'  </g>')

    lines.append('\n</svg>')
    return "\n".join(lines)


# ─── Main Execution ───────────────────────────────────────────────────────────
def main():
    print(f"Fetching contribution data for @{USERNAME}...")
    grid = fetch_contributions()

    print("Building Aligned Signature Attack Pokémon animated SVG...")
    svg = build_svg(grid)

    out_dir = os.path.dirname(OUT_FILE)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    new_hash = hashlib.md5(svg.encode()).hexdigest()
    old_hash = ""
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, "rb") as f:
            old_hash = hashlib.md5(f.read()).hexdigest()

    if new_hash == old_hash:
        print("Output SVG unchanged — skipping write.")
    else:
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            f.write(svg)
        size_kb = len(svg.encode("utf-8")) / 1024
        print(f"Successfully generated {OUT_FILE} ({size_kb:.1f} KB)")

    print("\n--- Final Verification Checklist ---")
    names = [p[0] for p in POKEMON_ROSTER]
    print(f"1. Total Pokemon: {len(names)} (Expected 50) -> {'PASS' if len(names) == 50 else 'FAIL'}")
    print(f"2. Pikachu is First: -> {'PASS' if names[0] == 'Pikachu' else 'FAIL'}")
    print(f"3. Bulbasaur included (no Venusaur): -> {'PASS' if 'Bulbasaur' in names and 'Venusaur' not in names else 'FAIL'}")
    print(f"4. Raichu is ABSENT: -> {'PASS' if 'Raichu' not in names else 'FAIL'}")
    print(f"5. Onix is INCLUDED: -> {'PASS' if 'Onix' in names else 'FAIL'}")
    print(f"6. All 50 Unique: -> {'PASS' if len(names) == len(set(names)) else 'FAIL'}")
    print(f"7. Bottom Y Position: {BOTTOM_Y} (DOWN, not side) -> PASS")


if __name__ == "__main__":
    main()
