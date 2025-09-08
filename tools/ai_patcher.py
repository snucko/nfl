#!/usr/bin/env python3
import os, re, base64, pathlib, subprocess, sys
from typing import List
from openai import OpenAI

REPO = pathlib.Path(__file__).resolve().parents[1]
SCREEN_CANDIDATES = [
    REPO / "screenshots" / "latest-hires.png",
    REPO / "screenshots" / "latest.png",
]
SOURCE_FILES: List[pathlib.Path] = [
    REPO / "src" / "full.liquid",
    REPO / "src" / "half_horizontal.liquid",
    REPO / "src" / "half_vertical.liquid",
    REPO / "src" / "quadrant.liquid",
    REPO / ".trmnlp.yml",
    REPO / "data" / "schedule.json",
]
MODEL = "gpt-4o-mini"

PROMPT = """You are a UI engineer for a TRMNL plugin.

You are given:
1) A fresh screenshot of the current render (e-ink style, 800×480 or a hi-res variant).
2) Key source files for the plugin (Liquid templates + YAML config).

GOAL — “Finished” visual spec (target):
- Header bar:
  - Full-width dark bar at the top.
  - Left: small NFL logo (or placeholder).
  - Center: bold title “NFL Week {{ weeknum }}”.
  - Right: small date range for the week (e.g., “Sep 7–9, 2025”).
- Main body:
  - Two-column table layout with clear separators.
  - Each row = one game.
  - Left column: kickoff short time (e.g., “Sun 1:00 PM”).
  - Right column: matchup “Cowboys @ Eagles” (bold), venue below in smaller/lighter text.
  - Comfortable row spacing; readable on 800×480.
- Styling:
  - White background; dark text; thin gray separators.
  - Medium-weight fonts suitable for e-ink.
- Empty state:
  - If no games, show centered: “No games scheduled this week.”
- Scaling:
  - Must read well at 800×480 and hi-res (e.g., 1600×960).
  - Long venue names may wrap; no overflow.

Data shape in Liquid (do NOT change):
- IDX_0.season.year, IDX_0.season.type
- IDX_0.week.number
- IDX_0.events[] (sorted by date), each event has:
  - e.date (ISO8601)
  - e.competitions[0].competitors[] (homeAway, team.abbreviation, team.shortDisplayName)
  - e.competitions[0].venue.fullName

TASK:
- Compare the screenshot to the GOAL.
- Make minimal, surgical edits to achieve it:
  - Prefer editing src/full.liquid and small inline CSS compatible with TRMNL classes.
  - Keep TRMNL classes: .layout, .columns, .column, .table, .label, .title, .title_bar.
  - Use Liquid date filter for time (e.g., "%a %I:%M %p").
  - Add explicit empty state when events.size == 0.
  - If you alter half/vertical/quadrant layouts, mirror improvements safely.

CONSTRAINTS:
- Do NOT change the JSON shape.
- Do NOT remove the title bar; center week title and show a small date range at right.
- Keep changes minimal and reversible.

OUTPUT FORMAT:
- Return a single UNIFIED DIFF between these markers exactly:

<<<PATCH
*** unified diff starts here ***
PATCH>>>

Notes:
- Use paths relative to repo root (e.g., src/full.liquid, .trmnlp.yml).
- Inline tiny <style> in full.liquid if needed.
- If multiple files change, include them all in one diff.
"""

def _b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode("ascii")

def _run(*cmd: str) -> None:
    subprocess.run(list(cmd), check=True)

def main() -> int:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY missing; skipping.", file=sys.stderr)
        return 0

    shot = next((p for p in SCREEN_CANDIDATES if p.exists()), None)
    if not shot:
        print("No screenshot found; skipping.", file=sys.stderr)
        return 0

    content = [
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{_b64(shot)}"}},
    ]
    for p in SOURCE_FILES:
        if p.exists():
            content.append({
                "type": "text",
                "text": f"--- FILE: {p.relative_to(REPO)} ---\n{p.read_text(encoding='utf-8', errors='ignore')}"
            })

    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": content}],
        temperature=0.2,
    )
    text = resp.choices[0].message.content or ""
    m = re.search(r"<<\<PATCH\s*(.*?)\s*PATCH>>>", text, re.S)
    if not m:
        print("No patch block found; nothing to apply.", file=sys.stderr)
        return 0

    patch = m.group(1).strip()
    patch_file = REPO / "tools" / "ai.patch"
    patch_file.write_text(patch, encoding="utf-8")
    print(f"[info] received patch -> {patch_file}")

    try:
        _run("git", "apply", "--index", str(patch_file))
    except subprocess.CalledProcessError:
        _run("git", "apply", "--index", "-p1", str(patch_file))

    print("[ok] patch applied and staged.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

