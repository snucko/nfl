# NFL TRMNL Plugin - AI Agent Context

## Overview
This is an automated NFL schedule and scores plugin for TRMNL e-ink displays. It fetches live NFL data from ESPN's API and pushes it to TRMNL devices via webhooks.

## Architecture

### Data Flow
1. **GitHub Actions** runs on a schedule (every 10min Sundays, 15min game nights, hourly otherwise)
2. **nfl_build.py** fetches current NFL data from ESPN API
3. **Webhook** pushes data to TRMNL plugin UUID: `960f3b34-4632-4060-82c7-5847d72175c8`
4. **TRMNL device** renders templates with fresh data

### Key Files

#### Data & Scripts
- `nfl_build.py` - Fetches NFL schedule/scores from ESPN API, writes to `data/schedule.json`
- `data/schedule.json` - Current NFL data (updated by GitHub Actions)
- `docs/schedule.json` - Copy for GitHub Pages (https://snucko.github.io/nfl/schedule.json)

#### Templates (src/)
- `full.liquid` - Full screen layout (800×480), shows 10 games with scores and icons
- `half_horizontal.liquid` - Half horizontal (800×240), shows 4 games
- `half_vertical.liquid` - Half vertical (400×480), shows 8 games
- `quadrant.liquid` - Quadrant (400×240), shows next game with large score

All templates use webhook data with:
- Team abbreviations
- Live scores in black boxes
- Status icons: 🔴 LIVE, ✓ FINAL, 📅 Upcoming

#### Automation
- `.github/workflows/update-nfl-data.yml` - Automated data updates & webhook push
  - Sundays 1pm-9pm EST: Every 10 minutes
  - Thu/Mon nights 7pm-12am EST: Every 15 minutes
  - Other times: Every hour

#### Local Development
- `start-trmnl.sh` - Start local TRMNL development server
- `update-nfl.sh` - Manually update NFL data (static template generation disabled)
- `.trmnlp.yml` - TRMNL local dev configuration

## GitHub Secrets Required
- `TRMNL_WEBHOOK_URL` = `https://usetrmnl.com/api/custom_plugins/960f3b34-4632-4060-82c7-5847d72175c8`

## Common Commands

### Update data manually
```bash
python3 nfl_build.py
```

### Test webhook locally
```bash
curl "https://usetrmnl.com/api/custom_plugins/960f3b34-4632-4060-82c7-5847d72175c8" \
  -H "Content-Type: application/json" \
  -d @data/schedule.json \
  -X POST
```

### Start local TRMNL dev server
```bash
./start-trmnl.sh
# Then visit http://localhost:4567/full
```

## Template Development

Templates receive data via TRMNL webhook with this structure:
```liquid
{{ season.year }}          - 2025
{{ season.type }}          - 2 (regular), 3 (playoffs)
{{ week.number }}          - 1-18
{{ events }}               - Array of games
  {{ event.competitions[0].competitors }}
    {{ competitor.team.abbreviation }}  - NYG, KC, etc.
    {{ competitor.score }}              - Current score
  {{ competition.status.type.state }}   - 'pre', 'in', 'post'
  {{ competition.status.type.completed }} - true/false
```

## Troubleshooting

### Data not updating on TRMNL
1. Check GitHub Actions is running: https://github.com/snucko/nfl/actions
2. Verify webhook secret is set in repo settings
3. Manually trigger workflow from Actions tab

### Templates not showing data
1. Ensure you copied the latest template from `src/` to TRMNL
2. Check TRMNL plugin is using "Webhook" strategy
3. Verify webhook URL in TRMNL matches UUID above

## TRMNL Integration (Direct ESPN Polling)

Using TRMNL's polling strategy to fetch live data directly from ESPN API:

- **Data Source**: TRMNL polls `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard` periodically
- **Full Data**: Complete NFL scoreboard with team logos, records, and live scores
- **No Processing**: Direct API integration, no custom filtering needed
- **Automatic Updates**: TRMNL fetches fresh data on schedule

### Plugin Setup
1. In TRMNL dashboard, set **Strategy** to "Polling"
2. Set **Polling URL** to: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
3. Set **Polling Verb** to "GET" (default)
4. Upload the template from `src/full.liquid`

### Template Features
- **Main Game**: Featured game with large team logos, records, and QR code link
- **Live Scores**: Prominent score display for games currently in progress
- **Grid Layout**: Additional games in a 2-column grid with small logos and live scores
- **Game Status**: Shows current quarter/time for live games, final status for completed
- **Responsive Design**: Optimized for TRMNL's e-ink display

## Notes
- Direct ESPN API integration - no custom data processing needed
- Template uses live ESPN data with team logos and records
- Automatic updates via TRMNL's polling schedule
- ESPN API endpoint: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
