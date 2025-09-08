#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# 1) Build JSON
./nfl_build.py

# 2) Snap local preview (ensure trmnlp is running)
npm run snap:both || true

# 3) Commit if anything changed
if ! git diff --quiet -- data/schedule.json screenshots/ 2>/dev/null; then
  git add data/schedule.json screenshots/
  git commit -m "auto: schedule + screenshots $(date -Iseconds)"
  git push origin main
else
  echo "[info] no changes to commit"
fi

