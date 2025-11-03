# NFL Schedule for TRMNL

Automated NFL schedule and live scores plugin for TRMNL e-ink displays.

## Features

- 🏈 **Live scores** with real-time updates during games
- 📅 **Auto-detects** current NFL season and week
- 🔴 **Live game indicators** with status icons (LIVE/FINAL/Upcoming)
- 📺 **All TRMNL layouts** - full, half horizontal/vertical, quadrant
- ⚡ **Smart updates** - Every 10min on Sundays, 15min on game nights, hourly otherwise
- 🤖 **Fully automated** via GitHub Actions webhooks

## How It Works

TRMNL automatically polls live NFL data from ESPN API and displays it on your device.

- **Direct Polling**: No custom processing needed - TRMNL fetches fresh data directly
- **Live Scores**: Team logos, records, and real-time game status
- **Automatic Updates**: TRMNL handles scheduling and data refresh

## Setup for TRMNL Device

### 1. Create Private Plugin
1. Go to [TRMNL Dashboard](https://usetrmnl.com/)
2. Create a **Private Plugin**
3. Choose **"Polling"** as the data strategy
4. Set **Polling URL** to: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
5. Set **Polling Verb** to "GET" (default)

### 2. Copy Template
Copy the template from `src/` based on your preferred layout:
- **Full screen** → `src/full.liquid`
- **Half horizontal** → `src/half_horizontal.liquid`
- **Half vertical** → `src/half_vertical.liquid`
- **Quadrant** → `src/quadrant.liquid`

Paste into your TRMNL private plugin's template editor.

### 3. Done!
Your TRMNL will now auto-update with live NFL scores directly from ESPN!

## Local Development

### Start TRMNL Dev Server
```bash
./start-trmnl.sh
```

Then visit:
- http://localhost:4567/full
- http://localhost:4567/half_horizontal
- http://localhost:4567/half_vertical
- http://localhost:4567/quadrant

### Update Data Manually
```bash
python3 nfl_build.py
```

## Update Schedule

TRMNL polls the ESPN API according to your device's refresh settings. For live games, set a frequent refresh interval (recommended: 1-4 hours).

## File Structure

```
nfl/
├── .github/workflows/
│   └── update-nfl-data.yml      # Automated updates
├── src/                         # TRMNL templates
│   ├── full.liquid             # Full screen (10 games)
│   ├── half_horizontal.liquid  # Half horizontal (4 games)
│   ├── half_vertical.liquid    # Half vertical (8 games)
│   ├── quadrant.liquid         # Quadrant (next game)
│   └── settings.yml
├── data/
│   └── schedule.json           # Current NFL data
├── docs/
│   └── schedule.json           # GitHub Pages copy
├── nfl_build.py               # ESPN API data fetcher
├── update-nfl.sh              # Manual update script
├── start-trmnl.sh             # Local dev server
└── AGENTS.md                  # AI agent context
```

## Data Source

- **ESPN NFL API**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- **Backup endpoint**: https://snucko.github.io/nfl/schedule.json

## Manual Data Override

Override automatic season/week detection:
```bash
YEAR=2024 TYPE=2 WEEK=18 python3 nfl_build.py
```

Where:
- `TYPE=2` = Regular season, `TYPE=3` = Playoffs
- `WEEK` = Week number (1-18 for regular season, 1-4 for playoffs)

## Display Examples

### Full Layout
- Complete game information
- Team names, scores, dates
- Venue information
- Game status (scheduled, live, final)

### Compact Layouts
- Essential game info only
- Team abbreviations
- Key times and scores
- Optimized for smaller screens

## Deployment to TRMNL

1. **Create polling plugin:**
- In TRMNL dashboard, create a Private Plugin
- Set Strategy to "Polling"
- Polling URL: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`

2. **Upload template:**
- Copy template from `src/` folder
- Paste into TRMNL plugin template editor

3. **Configure display:**
    - Choose your preferred layout size
- Set refresh frequency (recommended: 1-4 hours)

## Development

### Update NFL Data
```bash
python3 nfl_build.py
```

### Test Locally
```bash
# Start TRMNL development server
./start-trmnl.sh

# View at http://localhost:4567
```

### Customize Display
Edit the Liquid templates in `src/` to modify:
- Colors and fonts
- Information displayed
- Layout and spacing

## Troubleshooting

### No Games Showing
- Check if it's NFL offseason
- Verify ESPN API connectivity
- Run `python3 nfl_build.py` manually

### Wrong Week Displayed
- Check system date/time
- Override with environment variables
- Verify ESPN API responses

### Display Issues
- Ensure templates are properly formatted
- Check TRMNL development server logs
- Test with different layout sizes

## Contributing

Feel free to submit issues and pull requests to improve the plugin!

## License

This project is open source. Perfect for TRMNL device owners who want to display NFL schedules!
