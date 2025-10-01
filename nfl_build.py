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

    # Get current NFL season data - let ESPN API determine the current week
    current_date = datetime.date.today()
    
    # First try to get today's data to see what ESPN considers "current"
    today = current_date.strftime("%Y%m%d")
    m = try_fetch(f"{ESPN}?dates={today}")
    if m:
        yr = (m.get("season") or {}).get("year")
        tp = (m.get("season") or {}).get("type")
        wk = (m.get("week") or {}).get("number")
        if yr and tp and wk:
            print(f"[info] ESPN current data: year={yr} type={tp} week={wk}", file=sys.stderr)
            return int(yr), int(tp), int(wk)
    
    # If no current data, try the default API endpoint
    m = try_fetch(ESPN)
    if m:
        yr = (m.get("season") or {}).get("year")
        tp = (m.get("season") or {}).get("type")
        wk = (m.get("week") or {}).get("number")
        if yr and tp and wk:
            print(f"[info] ESPN default data: year={yr} type={tp} week={wk}", file=sys.stderr)
            return int(yr), int(tp), int(wk)
    
    # If we're in the current NFL season (Sept-Feb), use current data
    if current_date.month >= 9 or current_date.month <= 2:
        return current_date.year, 2, 1  # Regular season
    
    # During offseason, fallback to completed 2024 data
    print(f"[info] offseason detected, using 2024 data", file=sys.stderr)
    return 2024, 3, 3  # 2024 playoffs Conference Championship week

def fetch_week_data(year_or_date, seasontype, week):
    # Handle date-based queries (legacy)
    if isinstance(year_or_date, str) and len(year_or_date) == 10:  # YYYY-MM-DD format
        date_str = year_or_date.replace("-", "")
        urls = [f"{ESPN}?dates={date_str}"]
    else:
        # Preferred query for year/season/week
        urls = [
            f"{ESPN}?year={year_or_date}&seasontype={seasontype}&week={week}",
            f"{ESPN}",  # Current data
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

    year_or_date, stype, wk = discover_week()
    
    if isinstance(year_or_date, str):
        print(f"[info] target date -> {year_or_date}", file=sys.stderr)
        # Extract fallback values from the date
        year = int(year_or_date.split("-")[0])
        stype = 3  # playoffs
        wk = 3  # conference championships
    else:
        year = year_or_date
        print(f"[info] target week -> year={year} type={stype} week={wk}", file=sys.stderr)

    data, used_url = fetch_week_data(year_or_date, stype, wk)
    
    # If no events found, try to find the next available week
    if not (data.get("events") or []):
        print(f"[info] no events found, scanning for current week...", file=sys.stderr)
        # Try current year, different weeks
        current_year = datetime.date.today().year
        for guess_week in range(1, 22):  # up to week 21 including playoffs
            for guess_type in [2, 3]:  # regular season, then playoffs
                d2, _ = fetch_week_data(current_year, guess_type, guess_week)
                if d2.get("events"):
                    # Check if games are upcoming or recent
                    has_future_games = False
                    for event in d2["events"]:
                        event_date = datetime.datetime.fromisoformat(event["date"].replace("Z", "+00:00"))
                        if event_date > datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1):
                            has_future_games = True
                            break
                    
                    if has_future_games:
                        data = d2
                        year = current_year
                        stype = guess_type
                        wk = guess_week
                        print(f"[info] found current week with upcoming games -> year={year} type={stype} week={wk}", file=sys.stderr)
                        break
            if data.get("events"):
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
    
    # Also regenerate the Liquid templates with new data
    try:
        import subprocess
        subprocess.run([sys.executable, "-c", """
import json
import datetime as dt

# Read the schedule data
with open('data/schedule.json', 'r') as f:
    data = json.load(f)

def generate_template(template_name, content):
    with open(f'src/{template_name}.liquid', 'w') as f:
        f.write(content)

# Generate full.liquid template
template = '''{% comment %}
NFL Schedule - Full Size TRMNL Plugin
{% endcomment %}

<div class="plugin">
  <h1 class="title">
    NFL Week ''' + str(data['week']['number']) + ''' · ''' + str(data['season']['year']) + '''
    ''' + ('(Regular Season)' if data['season']['type'] == 2 else '(Playoffs)') + '''
  </h1>
  
  <div class="games">'''

for event in data['events']:
    comp = event['competitions'][0]
    status = comp['status']
    
    # Get team info
    away_team = next((c for c in comp['competitors'] if c['homeAway'] == 'away'), None)
    home_team = next((c for c in comp['competitors'] if c['homeAway'] == 'home'), None)
    
    template += '''
    <div class="game-row">
      <div class="teams">'''
    
    if status['type']['completed'] and away_team and home_team:
        template += away_team['team']['displayName'] + ' ' + away_team['score'] + ' - ' + home_team['score'] + ' ' + home_team['team']['displayName']
        template += ' <span class="status">(' + status['type']['shortDetail'] + ')</span>'
    else:
        template += event['name']
        template += ' <span class="status">(' + status['type']['shortDetail'] + ')</span>'
    
    template += '''</div>
      <div class="meta">'''
    
    # Format date
    date_obj = dt.datetime.fromisoformat(event['date'].replace('Z', '+00:00'))
    formatted_date = date_obj.strftime('%a %b %d, %I:%M %p')
    
    template += formatted_date + ' · ' + comp['venue']['fullName']
    template += '''</div>
    </div>'''

template += '''
  </div>
</div>

<style>
  .plugin {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 16px;
    color: #000;
    background: #fff;
    height: 100vh;
    overflow: hidden;
  }
  
  .title {
    font-size: 18px;
    font-weight: bold;
    margin: 0 0 12px 0;
    border-bottom: 2px solid #000;
    padding-bottom: 4px;
  }
  
  .games {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .game-row {
    padding: 8px 0;
    border-bottom: 1px solid #ccc;
  }
  
  .game-row:last-child {
    border-bottom: none;
  }
  
  .teams {
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 2px;
  }
  
  .status {
    font-weight: normal;
    color: #666;
  }
  
  .meta {
    font-size: 11px;
    color: #666;
  }
</style>'''

generate_template('full', template)
print('[ok] regenerated Liquid templates with current data', file=sys.stderr)
"""], cwd=repo)
    except Exception as e:
        print(f"[warn] failed to regenerate templates: {e}", file=sys.stderr)
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

