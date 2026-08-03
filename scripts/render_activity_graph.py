#!/usr/bin/env python3
"""
Render data/contributions.json as a high-tech GitHub-style Activity Graph SVG:
a smooth area & line chart of weekly contributions over the past year, with peak dots,
grid lines, and animated draw-in effect.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "activity-graph.svg")

# Color palette matching amogh-ascii2 / neofetch dark theme
BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
ACCENT = "#22d3ee"
GREEN = "#39d353"
GREEN_DARK = "#26a641"
GOLD = "#f2cc60"

W = 860
H = 250
PAD = 24
TITLEBAR_H = 30
CHART_LEFT = 55
CHART_RIGHT = W - 25
CHART_TOP = TITLEBAR_H + 30
CHART_BOTTOM = H - 38
CHART_W = CHART_RIGHT - CHART_LEFT
CHART_H = CHART_BOTTOM - CHART_TOP


def group_by_week(days):
    weeks = []
    current_week = []
    for d in days:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append({
                "date": current_week[0]["date"],
                "total": sum(x["count"] for x in current_week),
                "end_date": current_week[-1]["date"]
            })
            current_week = []
    if current_week:
        weeks.append({
            "date": current_week[0]["date"],
            "total": sum(x["count"] for x in current_week),
            "end_date": current_week[-1]["date"]
        })
    return weeks


def format_num(n):
    return f"{n:,}"


def render_activity_graph(data):
    days = data.get("days", [])
    if not days:
        print("No days found in contributions.json", file=sys.stderr)
        return ""

    weeks = group_by_week(days)
    n_weeks = len(weeks)
    if n_weeks < 2:
        return ""

    max_val = max(w["total"] for w in weeks)
    if max_val < 10:
        max_val = 10
    # Round max_val up to a nice even number
    y_max = ((max_val + 4) // 5) * 5

    points = []
    for i, w in enumerate(weeks):
        x = CHART_LEFT + i * (CHART_W / (n_weeks - 1))
        y = CHART_BOTTOM - (w["total"] / y_max) * CHART_H
        points.append((x, y, w))

    # Build smooth polyline / area path
    line_path_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
    area_path_d = f"M {points[0][0]:.1f},{CHART_BOTTOM} L " + " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points) + f" L {points[-1][0]:.1f},{CHART_BOTTOM} Z"

    css = """
@keyframes draw {
  from { stroke-dashoffset: 3000; }
  to { stroke-dashoffset: 0; }
}
@keyframes fadein {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
.curve-line {
  stroke-dasharray: 3000;
  stroke-dashoffset: 0;
  animation: draw 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}
.area-fill {
  opacity: 0;
  animation: fadein 1s ease-out 0.25s both;
}
.point-dot {
  opacity: 0;
  animation: fadein 0.4s ease-out 0.7s both;
}
"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
        f'<linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{GREEN_DARK}" stop-opacity="0.35"/>'
        f'<stop offset="1" stop-color="{GREEN_DARK}" stop-opacity="0.02"/>'
        f'</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#abg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    # Window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    # Header text & totals
    username = data.get("username", "Amogh0786")
    total_contribs = data.get("total_contributions", 0)
    best_day = data.get("best_day", {"count": 0, "date": "N/A"})

    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
        f'{username.lower()}@github: ~/activity --graph</text>'
    )
    parts.append(
        f'<text x="{CHART_LEFT}" y="{TITLEBAR_H + 18}" fill="{TEXT}" font-size="13" font-weight="700">'
        f'Contribution Activity Graph</text>'
    )
    parts.append(
        f'<text x="{CHART_RIGHT}" y="{TITLEBAR_H + 18}" fill="{MUTED}" font-size="12" text-anchor="end">'
        f'Total: <tspan fill="{GREEN}" font-weight="700">{format_num(total_contribs)}</tspan> in last year  |  '
        f'Peak Day: <tspan fill="{ACCENT}" font-weight="700">{best_day["count"]}</tspan> on {best_day["date"]}</text>'
    )

    # Grid lines & Y-axis labels
    for k in range(5):
        val = int(y_max * (4 - k) / 4)
        y = CHART_TOP + k * (CHART_H / 4)
        parts.append(
            f'<line x1="{CHART_LEFT}" y1="{y:.1f}" x2="{CHART_RIGHT}" y2="{y:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.18" stroke-dasharray="3,3"/>'
        )
        parts.append(
            f'<text x="{CHART_LEFT - 10}" y="{y + 4:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">{val}</text>'
        )

    # X-axis month labels
    seen_months = set()
    for x, y, w in points:
        dt = datetime.date.fromisoformat(w["date"])
        mk = (dt.year, dt.month)
        if mk not in seen_months and dt.day <= 7:
            seen_months.add(mk)
            mon_name = dt.strftime("%b")
            parts.append(
                f'<line x1="{x:.1f}" y1="{CHART_TOP}" x2="{x:.1f}" y2="{CHART_BOTTOM}" '
                f'stroke="{FRAME}" stroke-opacity="0.12"/>'
            )
            parts.append(
                f'<text x="{x:.1f}" y="{CHART_BOTTOM + 18}" fill="{MUTED}" font-size="10" text-anchor="middle">{mon_name}</text>'
            )

    # Draw Area and Line
    parts.append(
        f'<path class="area-fill" d="{area_path_d}" fill="url(#area-grad)"/>'
    )
    parts.append(
        f'<polyline class="curve-line" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" '
        f'stroke-linejoin="round" points="{line_path_pts}"/>'
    )

    # Draw circular dots on active weeks
    for x, y, w in points:
        if w["total"] > 0:
            color = ACCENT if w["total"] == max_val else GREEN
            r = "4" if w["total"] == max_val else "2.5"
            parts.append(
                f'<circle class="point-dot" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" stroke="{BG}" stroke-width="1.2">'
                f'<title>Week of {w["date"]}: {w["total"]} contributions</title>'
                f'</circle>'
            )

    # Footer
    rng = data.get("range", {"start": "", "end": ""})
    parts.append(
        f'<text x="{CHART_LEFT}" y="{H - 12}" fill="{MUTED}" font-size="10">'
        f'Generated dynamically from real GitHub contribution data ({rng.get("start")} to {rng.get("end")})</text>'
    )
    parts.append(
        f'<text x="{CHART_RIGHT}" y="{H - 12}" fill="{MUTED}" font-size="10" text-anchor="end">'
        f'Auto-refreshed daily via GitHub Actions</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if not os.path.exists(IN_PATH):
        print(f"Input file not found: {IN_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    svg_content = render_activity_graph(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Wrote {OUT_PATH} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
