#!/usr/bin/env python3
"""
Generates a Mac-style terminal window SVG displaying the user's Tech Stack and Links.
This matches the neofetch aesthetic of the other profile cards.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "tech-stack.svg")

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"

W = 860
H = 420
PAD = 24
TITLEBAR_H = 30

def render_tech_stack():
    css = """
@keyframes fadein {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.row {
  opacity: 0;
  animation: fadein 0.4s ease-out forwards;
}
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }
.delay-6 { animation-delay: 0.6s; }
.delay-7 { animation-delay: 0.7s; }
"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#abg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    # Window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
        f'amogh@github: ~/tech-stack --all</text>'
    )

    y = TITLEBAR_H + 30
    x_start = PAD + 10

    # Header prompt
    parts.append(f'<g class="row delay-1">')
    parts.append(f'<text x="{x_start}" y="{y}" fill="#39d353" font-size="14" font-weight="700">&gt; system.get_tech_stack()</text>')
    parts.append(f'</g>')
    
    y += 35

    tech_groups = [
        ("LANGUAGES", ["Python", "TypeScript", "Java", "C++", "C"], "#f2cc60", "delay-2"),
        ("FRONTEND", ["React.js", "Next.js", "HTML", "CSS", "Tailwind", "JavaScript", "Vite"], "#58a6ff", "delay-3"),
        ("BACKEND &amp; DB", ["Node.js", "Express", "PHP", "MySQL", "PostgreSQL", "MongoDB"], "#39d353", "delay-4"),
        ("TOOLS &amp; CLOUD", ["AWS", "Docker", "Kubernetes", "Linux", "Git/GitHub", "VS Code", "Postman", "Figma"], "#a371f7", "delay-5")
    ]

    for label, items, color, delay in tech_groups:
        parts.append(f'<g class="row {delay}">')
        parts.append(f'<text x="{x_start}" y="{y}" fill="{MUTED}" font-size="12" font-weight="700">[{label}]</text>')
        
        curr_x = x_start + 130
        for item in items:
            # Estimate width based on character count (approx 7.5px per char)
            w_box = len(item) * 8 + 16
            parts.append(f'<rect x="{curr_x}" y="{y - 14}" width="{w_box}" height="20" rx="4" fill="{color}" fill-opacity="0.1" stroke="{color}" stroke-opacity="0.5" stroke-width="1"/>')
            parts.append(f'<text x="{curr_x + w_box/2}" y="{y + 0.5}" fill="{color}" font-size="11" font-weight="700" text-anchor="middle">{item}</text>')
            curr_x += w_box + 10
            
        parts.append(f'</g>')
        y += 35

    y += 10
    
    # Links section
    parts.append(f'<g class="row delay-6">')
    parts.append(f'<text x="{x_start}" y="{y}" fill="#39d353" font-size="14" font-weight="700">&gt; system.get_links()</text>')
    parts.append(f'</g>')
    
    y += 35
    
    links = [
        ("LinkedIn", "linkedin.com/in/bala-amogh-raj-4b9722352", "#0077B5", "delay-7"),
        ("Email", "balaamoghraj@gmail.com", "#D14836", "delay-7"),
        ("GitHub", "github.com/Amogh0786", "#ffffff", "delay-7")
    ]

    parts.append(f'<g class="row delay-7">')
    curr_x = x_start
    for label, url, color, delay in links:
        box_w = 260
        parts.append(f'<rect x="{curr_x}" y="{y - 14}" width="{box_w}" height="28" rx="6" fill="#161b22" stroke="{color}" stroke-opacity="0.4" stroke-width="1.5"/>')
        parts.append(f'<text x="{curr_x + 12}" y="{y + 4}" fill="{TEXT}" font-size="12" font-weight="700">{label}</text>')
        parts.append(f'<text x="{curr_x + 75}" y="{y + 4}" fill="{MUTED}" font-size="11">{url}</text>')
        curr_x += box_w + 15
    parts.append(f'</g>')
    
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg_content = render_tech_stack()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Wrote {OUT_PATH} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    main()
