from pathlib import Path
import html
import re

md_path = Path("docs/NRI_MAINTENANCE_EXPLAINER.md")
with open(md_path) as f:
    md_text = f.read()

# Generate styled HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Understanding NRI Matrimonial & Maintenance Calculations (Audited)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090D16;
      --card-bg: #111827;
      --border: #1F2937;
      --gold: #D4AF37;
      --text: #F3F4F6;
      --text-muted: #9CA3AF;
      --accent: #3B82F6;
      --accent-subtle: rgba(59, 130, 246, 0.1);
      --success: #10B981;
      --warning: #F59E0B;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      line-height: 1.65;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
    }}
    header {{
      text-align: center;
      margin-bottom: 3rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }}
    h1 {{
      font-family: 'Cinzel', serif;
      font-size: 2.25rem;
      color: var(--gold);
      margin-bottom: 0.75rem;
      letter-spacing: 0.05em;
    }}
    h2 {{
      font-family: 'Cinzel', serif;
      font-size: 1.5rem;
      color: #E5E7EB;
      margin-top: 2.5rem;
      margin-bottom: 1rem;
      border-left: 4px solid var(--gold);
      padding-left: 0.75rem;
    }}
    h3 {{
      font-size: 1.15rem;
      color: #93C5FD;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
    }}
    p {{ margin-bottom: 1rem; color: #D1D5DB; }}
    strong {{ color: #FFFFFF; }}
    a {{ color: #60A5FA; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .callout {{
      background: var(--accent-subtle);
      border-left: 4px solid var(--accent);
      padding: 1rem 1.25rem;
      border-radius: 0 8px 8px 0;
      margin-bottom: 1.5rem;
      font-size: 0.95rem;
    }}
    .callout-gold {{
      background: rgba(212, 175, 55, 0.1);
      border-left: 4px solid var(--gold);
      padding: 1rem 1.25rem;
      border-radius: 0 8px 8px 0;
      margin-bottom: 1.5rem;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-size: 0.9rem;
      background: var(--card-bg);
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    th, td {{
      padding: 0.75rem 1rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }}
    th {{
      background-color: #1F2937;
      color: var(--gold);
      font-weight: 600;
      letter-spacing: 0.03em;
    }}
    tr:hover td {{
      background-color: rgba(255, 255, 255, 0.02);
    }}
    pre, code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      background: #1F2937;
      padding: 0.2rem 0.4rem;
      border-radius: 4px;
      color: #FBBF24;
    }}
    pre {{
      padding: 1rem;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
    ul, ol {{
      margin-left: 1.5rem;
      margin-bottom: 1rem;
      color: #D1D5DB;
    }}
    li {{ margin-bottom: 0.5rem; }}
    .badge {{
      display: inline-block;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .badge-recip {{ background: rgba(16, 185, 129, 0.2); color: #34D399; }}
    .badge-nonrecip {{ background: rgba(239, 68, 68, 0.2); color: #F87171; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Nyay Guide Legal Explainer</h1>
      <p style="color: var(--gold); font-size: 1.05rem;">Audited Indian Family Law & Transnational NRI Maintenance Scenario-Planning Architecture</p>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">Legal Audit Edition &bull; Primary Judgments &bull; Statutory Transition (BNSS 2023 / BSA 2023) &bull; 27 October 2026</p>
    </header>

    <div class="callout-gold">
      <strong>Practitioner Notice & Legal Disclaimer</strong>: Nyay Guide is a scenario-planning and research tool designed for advocates and litigants. In Indian family law, maintenance awards under Section 125 CrPC / Section 144 BNSS, Section 24 HMA, and Section 20 DV Act represent an exercise of judicial discretion on facts. Formulas (such as living cost deductions and net surplus percentages) are illustrative guidelines grounded in published precedents, not rigid statutory mandates.
    </div>

    <!-- Main Content rendered from markdown -->
    <div class="content">
      {md_text.replace('# Understanding NRI Matrimonial & Maintenance Modeling', '').replace('### A Practical Guide to the Legal Architecture, Primary Precedents, Procedural Transitions (BNSS/BSA), and Cross-Border Enforcement Limitations', '')}
    </div>
  </div>
</body>
</html>
"""

# Write to docs/NRI_MAINTENANCE_EXPLAINER.html
with open("docs/NRI_MAINTENANCE_EXPLAINER.html", "w") as f:
    f.write(html_content)

print("Generated docs/NRI_MAINTENANCE_EXPLAINER.html successfully.")
