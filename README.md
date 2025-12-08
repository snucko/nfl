# NFL Schedule for TRMNL

Automated NFL schedule and live scores plugin for TRMNL e-ink displays.

## Features

- 🏈 **Live scores** with real-time updates during games
- 📅 **Auto-detects** current NFL season and week
- 🔴 **Live game indicators** with status icons (LIVE/FINAL/Upcoming)
- 📺 **All TRMNL layouts** - full, half horizontal/vertical, quadrant
- ⚡ **Smart updates** - Automatic updates every 6 hours via GitHub Actions
- 🤖 **Optimized payload** - Filtered data ~20KB (below TRMNL's 100KB limit)

## How It Works

GitHub Actions fetches live NFL data from ESPN every 6 hours, filters it to minimal JSON, and serves it via GitHub Pages. TRMNL polls this filtered data to display live scores.

- **Filtered Payload**: ESPN data (~210KB) reduced to ~20KB via `nfl_build.py`
- **Live Scores**: Team logos, records, and real-time game status
- **Automatic Updates**: GitHub Actions updates data every 6 hours

## Setup for TRMNL Device

### 1. Create Private Plugin
1. Go to [TRMNL Dashboard](https://usetrmnl.com/)
2. Create a **Private Plugin**
3. Choose **"Polling"** as the data strategy
4. Set **Polling URL** to: `https://snucko.github.io/nfl/schedule.json`
5. Set **Polling Verb** to "GET" (default)

### 2. Copy Template
Copy the template from `src/` based on your preferred layout:
- **Full screen** → `src/full.liquid`
- **Half horizontal** → `src/half_horizontal.liquid`
- **Half vertical** → `src/half_vertical.liquid`
- **Quadrant** → `src/quadrant.liquid`

Paste into your TRMNL private plugin's template editor.

### 3. Done!
Your TRMNL will auto-update with live NFL scores every 6 hours. Data is kept under 100KB to avoid TRMNL payload limits.

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

## File Structure

```
nfl/
├── src/                         # TRMNL templates
│   ├── full.liquid             # Full screen (10 games)
│   ├── half_horizontal.liquid  # Half horizontal (4 games)
│   ├── half_vertical.liquid    # Half vertical (8 games)
│   └── quadrant.liquid         # Quadrant (next game)
├── data/
│   └── schedule.json           # Current NFL data (generated)
├── docs/
│   └── schedule.json           # GitHub Pages copy (served to TRMNL)
├── nfl_build.py                # Fetches ESPN data, filters to <100KB
├── .github/workflows/
│   └── update-nfl-data.yml     # GitHub Actions automation (every 6 hours)
├── .trmnlp.yml                 # TRMNL dev configuration
├── start-trmnl.sh              # Local dev server
└── AGENTS.md                   # AI agent context
```

## Data Flow

1. **GitHub Actions** (every 6 hours) runs `nfl_build.py`
2. **nfl_build.py** fetches ESPN API (~210KB) and filters to essential data (~20KB)
3. Filtered data saved to `data/` and `docs/schedule.json`
4. **TRMNL** polls `https://snucko.github.io/nfl/schedule.json` (GitHub Pages)
5. **Device** displays updated NFL information

## Data Source

- **ESPN NFL API** (source): `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- **Served to TRMNL** (filtered): `https://snucko.github.io/nfl/schedule.json` (~20KB)

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
   - Polling URL: `https://snucko.github.io/nfl/schedule.json`

2. **Upload template:**
   - Copy template from `src/` folder
   - Paste into TRMNL plugin template editor

3. **Configure display:**
   - Choose your preferred layout size
   - Set refresh frequency (recommended: 1-6 hours)

## Manual Updates

Update NFL data locally:
```bash
./update-nfl.sh
```

## Customization

Edit the Liquid templates in `src/` to modify:
- Colors and fonts
- Information displayed
- Layout and spacing

## Troubleshooting

### No Games Showing
- Check if it's NFL offseason
- Verify GitHub Pages is working: `https://snucko.github.io/nfl/schedule.json`
- Check TRMNL device refresh settings

### Payload Too Large Error
- This repo auto-filters ESPN data to <100KB
- If you see "Large payload" errors, check that polling URL is the GitHub Pages version (not ESPN direct)

### Wrong Week Displayed
- Check your system date/time
- Run `./update-nfl.sh` to manually refresh data

### Display Issues
- Ensure templates are properly formatted
- Check TRMNL development server logs
- Test with different layout sizes

## Contributing

Feel free to submit issues and pull requests to improve the plugin!

## License

This project is open source. Perfect for TRMNL device owners who want to display NFL schedules!
