#!/usr/bin/env python3
"""
Render data/contributions.json as a high-tech GitHub-style Profile Summary Card SVG:
a 2-column neofetch-inspired stats card with user highlights and a 3x2 grid of metric badges.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "profile-summary-card.svg")

# Color palette matching amogh-ascii2 / neofetch dark theme
BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
INK = "#c9d1d9"
ACCENT = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"
PURPLE = "#a371f7"
BLUE = "#58a6ff"
PINK = "#f778ba"

W = 860
H = 260
PAD = 24
TITLEBAR_H = 30


def format_num(n):
    return f"{n:,}"


def render_profile_card(data):
    username = data.get("username", "Amogh0786")
    total_contribs = data.get("total_contributions", 0)
    active_days = data.get("active_days", 0)
    avg_per_day = data.get("avg_per_active_day", 0.0)
    cur_streak = data.get("current_streak", {}).get("length", 0)
    long_streak = data.get("longest_streak", {}).get("length", 0)
    best_day_count = data.get("best_day", {}).get("count", 0)
    best_day_date = data.get("best_day", {}).get("date", "N/A")

    css = """
@keyframes card-pop {
  0% { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
.stat-box {
  opacity: 0;
  animation: card-pop 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.d0 { animation-delay: 0.1s; }
.d1 { animation-delay: 0.2s; }
.d2 { animation-delay: 0.3s; }
.d3 { animation-delay: 0.4s; }
.d4 { animation-delay: 0.5s; }
.d5 { animation-delay: 0.6s; }
.d6 { animation-delay: 0.7s; }
"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#pbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    # Window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
        f'{username.lower()}@github: ~/profile-summary --stats</text>'
    )

    # LEFT COLUMN: User Identity Panel
    left_x = PAD
    left_y = TITLEBAR_H + 18
    left_w = 250
    left_h = 188
    parts.append(
        f'<g class="stat-box d0">'
        f'<rect x="{left_x}" y="{left_y}" width="{left_w}" height="{left_h}" rx="10" fill="#111722" stroke="#21262d" stroke-width="1"/>'
        f'<circle cx="{left_x + 36}" cy="{left_y + 36}" r="20" fill="#161b22" stroke="{GREEN}" stroke-width="2"/>'
        f'<text x="{left_x + 36}" y="{left_y + 42}" fill="{GREEN}" font-size="16" font-weight="700" text-anchor="middle">&gt;_</text>'
        f'<text x="{left_x + 70}" y="{left_y + 32}" fill="{TEXT}" font-size="13" font-weight="700">GANTA BALA AMOGH RAJ</text>'
        f'<text x="{left_x + 70}" y="{left_y + 48}" fill="{ACCENT}" font-size="11">@{username}</text>'
        f'<line x1="{left_x + 16}" y1="{left_y + 68}" x2="{left_x + left_w - 16}" y2="{left_y + 68}" stroke="#21262d" stroke-width="1"/>'
        f'<text x="{left_x + 16}" y="{left_y + 92}" fill="{INK}" font-size="11">&#183; B.Tech CSE (AIML) Student</text>'
        f'<text x="{left_x + 16}" y="{left_y + 112}" fill="{INK}" font-size="11">&#183; Sreyas Inst. of Technology</text>'
        f'<text x="{left_x + 16}" y="{left_y + 132}" fill="{INK}" font-size="11">&#183; Full-Stack &amp; AI Developer</text>'
        f'<rect x="{left_x + 20}" y="{left_y + 148}" width="{left_w - 40}" height="24" rx="12" fill="#0d1f17" stroke="{GREEN}" stroke-width="1" stroke-opacity="0.8"/>'
        f'<circle cx="{left_x + 36}" cy="{left_y + 160}" r="4" fill="{GREEN}"/>'
        f'<text x="{left_x + left_w/2 + 6}" y="{left_y + 164}" fill="{GREEN}" font-size="11" font-weight="700" text-anchor="middle">ACTIVE CONTRIBUTOR</text>'
        f'</g>'
    )

    # RIGHT COLUMN: 3x2 Grid of Stat Metric Boxes
    right_x = left_x + left_w + 16
    right_w = W - right_x - PAD
    card_w = (right_w - 28) / 3
    card_h = 87
    gap_x = 14
    gap_y = 14

    metrics = [
        {
            "label": "TOTAL CONTRIBUTIONS",
            "val": format_num(total_contribs),
            "sub": "In the last year",
            "color": GREEN,
            "delay": "d1"
        },
        {
            "label": "CURRENT STREAK",
            "val": f"{cur_streak} Days",
            "sub": "Active contribution run",
            "color": ACCENT,
            "delay": "d2"
        },
        {
            "label": "LONGEST STREAK",
            "val": f"{long_streak} Days",
            "sub": "Personal record",
            "color": GOLD,
            "delay": "d3"
        },
        {
            "label": "BEST SINGLE DAY",
            "val": str(best_day_count),
            "sub": f"on {best_day_date}",
            "color": PURPLE,
            "delay": "d4"
        },
        {
            "label": "ACTIVE DAYS",
            "val": f"{active_days} Days",
            "sub": f"{round((active_days/365)*100, 1)}% of the year",
            "color": BLUE,
            "delay": "d5"
        },
        {
            "label": "DAILY AVERAGE",
            "val": str(avg_per_day),
            "sub": "Per active day",
            "color": PINK,
            "delay": "d6"
        }
    ]

    for idx, m in enumerate(metrics):
        col = idx % 3
        row = idx // 3
        cx = right_x + col * (card_w + gap_x)
        cy = left_y + row * (card_h + gap_y)

        parts.append(
            f'<g class="stat-box {m["delay"]}">'
            f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{card_w:.1f}" height="{card_h:.1f}" rx="8" fill="#111722" stroke="#21262d" stroke-width="1"/>'
            f'<path d="M {cx + 4:.1f} {cy + 1:.1f} L {cx + card_w - 4:.1f} {cy + 1:.1f}" stroke="{m["color"]}" stroke-width="3" stroke-linecap="round"/>'
            f'<text x="{cx + 14:.1f}" y="{cy + 22:.1f}" fill="{MUTED}" font-size="9" font-weight="700">{m["label"]}</text>'
            f'<text x="{cx + 14:.1f}" y="{cy + 52:.1f}" fill="{m["color"]}" font-size="22" font-weight="700">{m["val"]}</text>'
            f'<text x="{cx + 14:.1f}" y="{cy + 74:.1f}" fill="{INK}" font-size="10">{m["sub"]}</text>'
            f'</g>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if not os.path.exists(IN_PATH):
        print(f"Input file not found: {IN_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    svg_content = render_profile_card(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Wrote {OUT_PATH} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
