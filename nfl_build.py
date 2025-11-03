#!/usr/bin/env python3
"""
NFL Data Fetcher for TRMNL Plugin

Fetches current NFL schedule and scores from ESPN API and formats for TRMNL webhook.
"""

import json
import os
import sys
from datetime import datetime, timezone
import requests

# ESPN API endpoint
ESPN_API_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

def fetch_nfl_data():
    """Fetch NFL data from ESPN API."""
    try:
        response = requests.get(ESPN_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from ESPN: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Allow override via environment variables
    year = os.getenv('YEAR')
    season_type = os.getenv('TYPE')
    week = os.getenv('WEEK')

    print("Fetching NFL data from ESPN...")

    # Fetch data
    data = fetch_nfl_data()

    # Override season/week if specified
    if year:
        data['season']['year'] = int(year)
    if season_type:
        data['season']['type'] = int(season_type)
    if week:
        data['week']['number'] = int(week)

    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('docs', exist_ok=True)

    # Write to data/schedule.json
    with open('data/schedule.json', 'w') as f:
        json.dump(data, f, indent=2)

    # Copy to docs/ for GitHub Pages
    with open('docs/schedule.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"NFL data updated for {data['season']['year']} Season {data['season']['type']}, Week {data['week']['number']}")
    print(f"Found {len(data.get('events', []))} games")

    # Print summary
    for event in data.get('events', [])[:5]:  # Show first 5 games
        competition = event.get('competitions', [{}])[0]
        competitors = competition.get('competitors', [])
        if len(competitors) >= 2:
            home = competitors[0]
            away = competitors[1]
            status = competition.get('status', {}).get('type', {})
            print(f"  {away['team']['abbreviation']} @ {home['team']['abbreviation']}: {status.get('state', 'unknown')}")

if __name__ == "__main__":
    main()
