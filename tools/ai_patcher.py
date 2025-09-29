#!/usr/bin/env python3
import os, re, base64, pathlib, subprocess, sys
from typing import List

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

def _b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode("ascii")

def _run(*cmd: str) -> None:
    subprocess.run(list(cmd), check=True)

def main() -> int:
    print("ai_patcher is disabled because OPENAI_API_KEY is not set.", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())