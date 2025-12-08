#!/usr/bin/env python3
"""
NFL Schedule Builder - Fetches ESPN NFL data and filters to minimal JSON
Serves filtered data (~20KB) via GitHub Pages to avoid TRMNL's 100KB payload limit
"""

import requests
import json
import os
from datetime import datetime

def fetch_nfl_data():
    """Fetch live NFL data from ESPN API"""
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching ESPN data: {e}")
        return None

def filter_payload(data):
    """Filter ESPN payload to minimal JSON (~20KB instead of 210KB)"""
    if not data or 'events' not in data:
        return None
    
    filtered_events = []
    for event in data.get('events', []):
        try:
            comp = event.get('competitions', [{}])[0]
            competitors = comp.get('competitors', [])
            
            filtered_event = {
                'id': event.get('id'),
                'name': event.get('name'),
                'date': event.get('date'),
                'links': event.get('links', []),
                'season': event.get('season', {}),
                'week': event.get('week', {}),
                'competitions': [{
                    'status': comp.get('status', {}),
                    'competitors': [
                        {
                            'homeAway': c.get('homeAway'),
                            'score': c.get('score'),
                            'records': c.get('records', []),
                            'team': {
                                'abbreviation': c.get('team', {}).get('abbreviation'),
                                'displayName': c.get('team', {}).get('displayName'),
                                'logo': c.get('team', {}).get('logo')
                            }
                        }
                        for c in competitors
                    ]
                }]
            }
            filtered_events.append(filtered_event)
        except Exception as e:
            print(f"Error filtering event: {e}")
            continue
    
    return {
        'season': data.get('season', {}),
        'week': data.get('week', {}),
        'events': filtered_events,
        'lastUpdated': datetime.utcnow().isoformat() + 'Z'
    }

def save_schedule(data, filepath):
    """Save filtered schedule to file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"Saved {filepath} ({size_kb:.1f} KB)")

def main():
    print("Fetching NFL schedule from ESPN...")
    raw_data = fetch_nfl_data()
    
    if not raw_data:
        print("Failed to fetch data")
        return
    
    print(f"Raw ESPN payload: {len(json.dumps(raw_data))/1024:.1f} KB")
    
    filtered_data = filter_payload(raw_data)
    if not filtered_data:
        print("Failed to filter data")
        return
    
    filtered_size = len(json.dumps(filtered_data))/1024
    print(f"Filtered payload: {filtered_size:.1f} KB")
    
    if filtered_size > 100:
        print(f"Warning: Filtered payload still {filtered_size:.1f} KB (max 100 KB)")
    
    # Save to both data/ and docs/ for GitHub Pages
    save_schedule(filtered_data, 'data/schedule.json')
    save_schedule(filtered_data, 'docs/schedule.json')

if __name__ == '__main__':
    main()
