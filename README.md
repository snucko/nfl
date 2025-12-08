# NFL Schedule for TRMNL

Automated NFL schedule and live scores plugin for TRMNL e-ink displays.

## Features

- 🏈 **Live scores** with real-time updates during games
- 📅 **Auto-detects** current NFL season and week
- 🔴 **Live game indicators** with status icons (LIVE/FINAL/Upcoming)
- 📺 **All TRMNL layouts** - full, half horizontal/vertical, quadrant
- ⚡ **Smart updates** - TRMNL polls ESPN API automatically
- 🤖 **Zero processing** - Direct ESPN API polling from TRMNL device

## How It Works

TRMNL automatically polls live NFL data from ESPN API and displays it on your device.

- **Direct Polling**: TRMNL fetches fresh data directly from ESPN API
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

## File Structure

```
nfl/
├── src/                         # TRMNL templates
│   ├── full.liquid             # Full screen (10 games)
│   ├── half_horizontal.liquid  # Half horizontal (4 games)
│   ├── half_vertical.liquid    # Half vertical (8 games)
│   └── quadrant.liquid         # Quadrant (next game)
├── .trmnlp.yml                 # TRMNL dev configuration
├── start-trmnl.sh              # Local dev server
└── AGENTS.md                   # AI agent context
```

## Data Source

**ESPN NFL API**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`

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

## Customization

Edit the Liquid templates in `src/` to modify:
- Colors and fonts
- Information displayed
- Layout and spacing

## Troubleshooting

### No Games Showing
- Check if it's NFL offseason
- Verify ESPN API connectivity at: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`

### Wrong Week Displayed
- Check your system date/time

### Display Issues
- Ensure templates are properly formatted
- Check TRMNL development server logs
- Test with different layout sizes

## Contributing

Feel free to submit issues and pull requests to improve the plugin!

## License

This project is open source. Perfect for TRMNL device owners who want to display NFL schedules!
