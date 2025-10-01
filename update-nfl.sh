#!/bin/bash
# NFL TRMNL Plugin - Update Data and Templates

set -euo pipefail

echo "🏈 NFL TRMNL Plugin - Data Update"
echo "================================"
echo ""

# Update NFL data
echo "📊 Fetching current NFL data..."
python3 nfl_build.py

# Generate all templates with current data
echo "🎨 Regenerating TRMNL templates..."
python3 -c "
import json
import datetime as dt

# Read the schedule data
with open('data/schedule.json', 'r') as f:
    data = json.load(f)

def generate_template(filename, content):
    with open(f'src/{filename}', 'w') as f:
        f.write(content)
    print(f'✅ Generated {filename}')

# Common template parts
season_type = '(Regular Season)' if data['season']['type'] == 2 else '(Playoffs)'
week_title = f\"NFL Week {data['week']['number']} · {data['season']['year']} {season_type}\"

# Generate full.liquid
full_template = '''{% comment %}
NFL Schedule - Full Size TRMNL Plugin - Auto-generated
{% endcomment %}

<div class=\"plugin\">
  <h1 class=\"title\">''' + week_title + '''</h1>
  <div class=\"games\">'''

for event in data['events']:
    comp = event['competitions'][0]
    status = comp['status']
    away_team = next((c for c in comp['competitors'] if c['homeAway'] == 'away'), None)
    home_team = next((c for c in comp['competitors'] if c['homeAway'] == 'home'), None)
    
    full_template += '''
    <div class=\"game-row\">
      <div class=\"teams\">'''
    
    if status['type']['completed'] and away_team and home_team:
        full_template += away_team['team']['displayName'] + ' ' + away_team['score'] + ' - ' + home_team['score'] + ' ' + home_team['team']['displayName']
    else:
        full_template += event['name']
    
    full_template += ' <span class=\"status\">(' + status['type']['shortDetail'] + ')</span></div>'
    
    # Format date
    date_obj = dt.datetime.fromisoformat(event['date'].replace('Z', '+00:00'))
    formatted_date = date_obj.strftime('%a %b %d, %I:%M %p')
    full_template += '<div class=\"meta\">' + formatted_date + ' · ' + comp['venue']['fullName'] + '</div></div>'

full_template += '''
  </div>
</div>

<style>
  .plugin {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 16px; color: #000; background: #fff; height: 100vh; overflow: hidden;
  }
  .title { font-size: 18px; font-weight: bold; margin: 0 0 12px 0; border-bottom: 2px solid #000; padding-bottom: 4px; }
  .games { display: flex; flex-direction: column; gap: 8px; }
  .game-row { padding: 8px 0; border-bottom: 1px solid #ccc; }
  .game-row:last-child { border-bottom: none; }
  .teams { font-weight: bold; font-size: 14px; margin-bottom: 2px; }
  .status { font-weight: normal; color: #666; }
  .meta { font-size: 11px; color: #666; }
</style>'''

generate_template('full.liquid', full_template)

# Generate half_horizontal.liquid
half_h_template = '''{% comment %}
NFL Schedule - Half Horizontal TRMNL Plugin - Auto-generated
{% endcomment %}

<div class=\"plugin half-horizontal\">
  <h2 class=\"title\">NFL Week ''' + str(data['week']['number']) + '''</h2>
  <div class=\"games\">'''

for event in data['events'][:4]:  # Limit for horizontal space
    comp = event['competitions'][0]
    status = comp['status']
    away_team = next((c for c in comp['competitors'] if c['homeAway'] == 'away'), None)
    home_team = next((c for c in comp['competitors'] if c['homeAway'] == 'home'), None)
    
    half_h_template += '<div class=\"game-row\">'
    
    if status['type']['completed'] and away_team and home_team:
        half_h_template += '<div class=\"teams-compact\">' + away_team['team']['abbreviation'] + ' ' + away_team['score'] + ' - ' + home_team['score'] + ' ' + home_team['team']['abbreviation'] + '</div>'
    else:
        half_h_template += '<div class=\"teams-compact\">' + event['shortName'] + '</div>'
    
    date_obj = dt.datetime.fromisoformat(event['date'].replace('Z', '+00:00'))
    formatted_date = date_obj.strftime('%a %I:%M %p')
    half_h_template += '<div class=\"meta-compact\">' + formatted_date + '</div></div>'

half_h_template += '''
  </div>
</div>

<style>
  .plugin.half-horizontal {
    font-family: system-ui, sans-serif; padding: 12px; height: 240px; width: 800px; overflow: hidden;
  }
  .title { font-size: 14px; font-weight: bold; margin: 0 0 8px 0; }
  .game-row { padding: 4px 0; border-bottom: 1px solid #eee; }
  .teams-compact { font-weight: bold; font-size: 12px; }
  .meta-compact { font-size: 10px; color: #666; }
</style>'''

generate_template('half_horizontal.liquid', half_h_template)

# Generate quadrant.liquid (simple version)
first_game = data['events'][0] if data['events'] else None
quadrant_template = '''{% comment %}
NFL Schedule - Quadrant TRMNL Plugin - Auto-generated
{% endcomment %}

<div class=\"plugin quadrant\">
  <h3 class=\"title\">NFL Week ''' + str(data['week']['number']) + '''</h3>'''

if first_game:
    comp = first_game['competitions'][0]
    status = comp['status']
    away_team = next((c for c in comp['competitors'] if c['homeAway'] == 'away'), None)
    home_team = next((c for c in comp['competitors'] if c['homeAway'] == 'home'), None)
    
    quadrant_template += '<div class=\"game\">'
    
    if status['type']['completed'] and away_team and home_team:
        quadrant_template += '<div class=\"score\">' + away_team['score'] + '-' + home_team['score'] + '</div>'
        quadrant_template += '<div class=\"teams-mini\">' + away_team['team']['abbreviation'] + ' @ ' + home_team['team']['abbreviation'] + '</div>'
    else:
        quadrant_template += '<div class=\"teams-mini\">' + first_game['shortName'] + '</div>'
    
    quadrant_template += '<div class=\"status-mini\">' + status['type']['shortDetail'] + '</div></div>'

quadrant_template += '''
</div>

<style>
  .plugin.quadrant {
    font-family: system-ui, sans-serif; padding: 8px; height: 240px; width: 400px; overflow: hidden; text-align: center;
  }
  .title { font-size: 12px; font-weight: bold; margin: 0 0 6px 0; }
  .game { display: flex; flex-direction: column; align-items: center; justify-content: center; height: calc(100% - 20px); }
  .score { font-size: 24px; font-weight: bold; margin-bottom: 4px; }
  .teams-mini { font-size: 10px; font-weight: bold; margin-bottom: 2px; }
  .status-mini { font-size: 8px; color: #666; }
</style>'''

generate_template('quadrant.liquid', quadrant_template)

print(f'')
print(f'📊 Generated templates for:')
print(f'   Season: {data[\"season\"][\"year\"]} Week {data[\"week\"][\"number\"]}')
print(f'   Games: {len(data[\"events\"])}')
print(f'   Type: {\"Regular Season\" if data[\"season\"][\"type\"] == 2 else \"Playoffs\"}')
"

echo ""
echo "✅ Update complete!"
echo ""
echo "📁 Ready for TRMNL deployment:"
echo "   src/ - Contains all TRMNL plugin files"
echo "   data/schedule.json - Current NFL data"
echo ""
echo "🚀 Next steps:"
echo "   1. Copy src/ contents to your TRMNL plugin"
echo "   2. Set up automatic updates (optional)"
echo "   3. Configure your TRMNL display"