#!/usr/bin/env python3
"""
Generates a Mac-style terminal window SVG displaying the user's top GitHub projects.
"""
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "projects.svg")

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
CARD_BG = "#0d1117"
CARD_BORDER = "#30363d"
TITLE_COLOR = "#58a6ff"
TEXT_COLOR = "#7d8590"
LANG_COLOR_JS = "#f1e05a"
LANG_COLOR_PY = "#3572A5"
MUTED = "#7d8590"

W = 860
PAD = 24
TITLEBAR_H = 30
GAP = 16
CARD_W = (W - 2 * PAD - GAP) // 2

projects = [
    {
        "name": "Automated_CI-CD_Pipeline_Setup",
        "url": "https://github.com/Amogh0786/Automated_CI-CD_Pipeline_Setup",
        "desc": "Demonstration of DevOps best practices using Azure. Features automated Docker image builds via Azure Container Registry (ACR) and seamless deployments to Azure App Service.",
        "lang": "JavaScript",
        "lang_color": LANG_COLOR_JS
    },
    {
        "name": "Enterprise_Agentic_RAG",
        "url": "https://github.com/Amogh0786/Enterprise_Agentic_RAG",
        "desc": "Enterprise-Grade Agentic RAG System featuring dynamic SQL/Vector modality routing, Cross-Encoder reranking with token-overlap deduplication, and an Apple visionOS Spatial UI.",
        "lang": "Python",
        "lang_color": LANG_COLOR_PY
    },
    {
        "name": "Self-Healing-ML-Pipelines",
        "url": "https://github.com/Amogh0786/Self-Healing-ML-Pipelines",
        "desc": "Enterprise-grade Self-Healing MLOps Pipeline with Hybrid Decision Engine (Rules + Contextual Bandits), Automated Drift Monitoring, Airflow, and K8s Zero-Downtime Rollouts.",
        "lang": "Python",
        "lang_color": LANG_COLOR_PY
    },
    {
        "name": "Multi_Agent_Threat_Intel",
        "url": "https://github.com/Amogh0786/Multi_Agent_Threat_Intel",
        "desc": "Multi-Agent Autonomous Threat Intelligence &amp; Tactical SOC Terminal powered by LangGraph, Google Gemini 3.1 Pro, and Vector DBs.",
        "lang": "Python",
        "lang_color": LANG_COLOR_PY
    },
    {
        "name": "RAG_Pipeline",
        "url": "https://github.com/Amogh0786/RAG_Pipeline",
        "desc": "Architected an automated Retrieval-Augmented Generation (RAG) pipeline using Python and LangChain. Implemented local semantic embedding via HuggingFace transformers, vector similarity search with ChromaDB.",
        "lang": "Python",
        "lang_color": LANG_COLOR_PY
    },
    {
        "name": "AI_Agent_Eval_Pipeline",
        "url": "https://github.com/Amogh0786/AI_Agent_Eval_Pipeline",
        "desc": "A production-grade Autonomous AI Agent built with LangGraph and Google Gemini, augmented with an Automated Evaluation (LLM-as-a-Judge) CI/CD Pipeline.",
        "lang": "Python",
        "lang_color": LANG_COLOR_PY
    }
]

def render_projects():
    css = """
@keyframes fadein {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.card {
  opacity: 0;
  animation: fadein 0.4s ease-out forwards;
}
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }
.delay-6 { animation-delay: 0.6s; }
"""

    parts = []
    
    # Calculate card heights and overall height
    cards_html = []
    current_y = TITLEBAR_H + 30
    
    # We will lay them out in 2 columns
    row_heights = []
    for i in range(0, len(projects), 2):
        h1 = 120 # base height
        h2 = 120
        if i < len(projects):
            lines1 = textwrap.wrap(projects[i]["desc"], width=52)
            h1 = 40 + len(lines1) * 20 + 35
        if i + 1 < len(projects):
            lines2 = textwrap.wrap(projects[i+1]["desc"], width=52)
            h2 = 40 + len(lines2) * 20 + 35
        
        row_h = max(h1, h2)
        row_heights.append(row_h)
    
    H = TITLEBAR_H + 30 + sum(row_heights) + len(row_heights) * GAP + PAD
    
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji">'
    )
    parts.append(f'<style>{css}</style>')
    parts.append('<defs>')
    parts.append(f'<linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">')
    parts.append(f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>')
    parts.append('</defs>')
    
    parts.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#abg)"/>')
    parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>')
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>')
    
    # Window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" text-anchor="middle">'
        f'amogh@github: ~/projects</text>'
    )
    
    y = TITLEBAR_H + PAD
    
    for row_idx in range(0, len(projects), 2):
        row_h = row_heights[row_idx // 2]
        
        for col_idx in range(2):
            idx = row_idx + col_idx
            if idx >= len(projects):
                break
                
            p = projects[idx]
            x = PAD + col_idx * (CARD_W + GAP)
            delay = f"delay-{idx + 1}"
            
            parts.append(f'<g class="card {delay}">')
            parts.append(f'<a href="{p["url"]}" target="_blank">')
            
            # Card background
            parts.append(f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{row_h}" rx="6" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1"/>')
            
            # Repo icon (SVG path)
            repo_icon = '<path fill-rule="evenodd" d="M3 1.25A2.25 2.25 0 00.75 3.5v11A2.25 2.25 0 003 16.75h14A2.25 2.25 0 0019.25 14.5v-11A2.25 2.25 0 0017 1.25H3zM2.25 3.5a.75.75 0 01.75-.75h14a.75.75 0 01.75.75v11a.75.75 0 01-.75.75H3a.75.75 0 01-.75-.75v-11z"/><path fill-rule="evenodd" d="M12.75 7.75a.75.75 0 01.75-.75h3a.75.75 0 010 1.5h-3a.75.75 0 01-.75-.75zm0 3a.75.75 0 01.75-.75h3a.75.75 0 010 1.5h-3a.75.75 0 01-.75-.75zM4 6.5A1.5 1.5 0 015.5 5h3A1.5 1.5 0 0110 6.5v3A1.5 1.5 0 018.5 11h-3A1.5 1.5 0 014 9.5v-3zM5.5 6.5v3h3v-3h-3z"/>'
            # Let's use a simpler repo icon
            repo_icon = '<path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>'
            parts.append(f'<g transform="translate({x + 16}, {y + 16})" fill="{MUTED}">{repo_icon}</g>')
            
            # Title
            parts.append(f'<text x="{x + 40}" y="{y + 28}" fill="{TITLE_COLOR}" font-size="14" font-weight="600">{p["name"]}</text>')
            
            # Description
            desc_lines = textwrap.wrap(p["desc"], width=52)
            desc_y = y + 54
            for line in desc_lines:
                parts.append(f'<text x="{x + 16}" y="{desc_y}" fill="{TEXT_COLOR}" font-size="13">{line}</text>')
                desc_y += 20
                
            # Language
            lang_y = y + row_h - 16
            parts.append(f'<circle cx="{x + 22}" cy="{lang_y - 4}" r="6" fill="{p["lang_color"]}"/>')
            parts.append(f'<text x="{x + 36}" y="{lang_y}" fill="{TEXT_COLOR}" font-size="12">{p["lang"]}</text>')
            
            parts.append('</a>')
            parts.append('</g>')
            
        y += row_h + GAP

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg_content = render_projects()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Wrote {OUT_PATH} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    main()
