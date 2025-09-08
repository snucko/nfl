#!/usr/bin/env python3
"""
Builds data/schedule.json in the flattened shape TRMNL expects:
{
  "season": { "year": 2025, "type": 2 },
  "week":   { "number": 1 },
  "events": [ ... ]
}

ENV overrides supported:
  YEAR=2025 TYPE=2 WEEK=1 ./nfl_build.py
"""

import os, sys, json, datetime, urllib.request, urllib.error, pathlib, tempfile, shutil

ESPN = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

def fetch(url, timeout=30):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def try_fetch(url):
    try:
        return fetch(url)
    except Exception as e:
        print(f"[warn] fetch failed: {url} :: {e}", file=sys.stderr)
        return None

def discover_week():
    # Allow pinning via env
    y = os.getenv("YEAR"); t = os.getenv("TYPE"); w = os.getenv("WEEK")
    if y and t and w:
        return int(y), int(t), int(w)

    # Ask "today" board for meta
    today = datetime.date.today().strftime("%Y%m%d")
    m = try_fetch(f"{ESPN}?dates={today}")
    if m:
        yr = (m.get("season") or {}).get("year")
        tp = (m.get("season") or {}).get("type")
        wk = (m.get("week") or {}).get("number")
        if yr and tp and wk:
            return int(yr), int(tp), int(wk)

    # Fallback guess: current calendar year, regular season week 1
    return datetime.date.today().year, 2, 1

def fetch_week_data(year, seasontype, week):
    # Preferred query
    urls = [
        f"{ESPN}?year={year}&seasontype={seasontype}&week={week}",
        f"{ESPN}?dates={year}&seasontype={seasontype}&week={week}",
        f"{ESPN}?dates={datetime.date.today().strftime('%Y%m%d')}"
    ]
    for u in urls:
        data = try_fetch(u)
        if data and data.get("events") is not None:
            return data, u
    return {}, urls[-1]

def flatten_payload(data, fallback_year, fallback_type, fallback_week):
    # Ensure top-level keys exist
    season = data.get("season") or {"year": fallback_year, "type": fallback_type}
    week   = data.get("week")   or {"number": fallback_week}
    events = data.get("events") or []

    # (Optional) sort by kickoff time
    events = sorted(events, key=lambda e: e.get("date", ""))

    return {"season": {"year": season.get("year"), "type": season.get("type")},
            "week":   {"number": (week or {}).get("number")},
            "events": events}

def main():
    repo = pathlib.Path(__file__).resolve().parent
    out_dir = repo / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkstemp(prefix="sched_", suffix=".json")[1])

    year, stype, wk = discover_week()
    print(f"[info] target week -> year={year} type={stype} week={wk}", file=sys.stderr)

    data, used_url = fetch_week_data(year, stype, wk)
    # If no events, auto-scan a few weeks forward (regular season) to avoid blanks
    if not (data.get("events") or []):
        for guess in range(1, 22):  # up to week 21 including playoffs
            d2, _ = fetch_week_data(year, 2, guess)  # prefer regular season
            if d2.get("events"):
                data = d2
                stype = (d2.get("season") or {}).get("type", 2)
                wk    = (d2.get("week") or {}).get("number", guess)
                print(f"[info] fallback to first non-empty week -> type={stype} week={wk}", file=sys.stderr)
                break

    flat = flatten_payload(data, year, stype, wk)

    with open(tmp, "w") as f:
        json.dump(flat, f, indent=2)

    # Atomic replace if changed
    out_file = out_dir / "schedule.json"
    if out_file.exists() and out_file.read_text() == tmp.read_text():
        print("[info] no changes to schedule.json", file=sys.stderr)
        tmp.unlink(missing_ok=True)
        return 0

    shutil.move(str(tmp), str(out_file))
    print(f"[ok] wrote {out_file} (source: {used_url})", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

