# NFL Schedule for TRMNL

A TRMNL app that displays current NFL game schedules and scores.

## Features

- 🏈 Shows current NFL week games with live scores
- 📅 Automatically detects current NFL season and week
- 🎯 Displays upcoming games with dates and times
- 📺 Optimized for all TRMNL screen sizes (full, half, quadrant)
- ⚡ Auto-updates with fresh NFL data

## TRMNL Integration

This plugin is designed for the [TRMNL](https://usetrmnl.com/) platform. It includes:

- **Liquid templates** for all TRMNL layout sizes
- **Automatic data fetching** from ESPN's NFL API
- **Smart season detection** (regular season, playoffs, offseason)
- **Clean display formatting** optimized for e-ink screens

## Quick Start

### For TRMNL Device
Upload this plugin directly to your TRMNL device:

1. Go to your [TRMNL dashboard](https://usetrmnl.com/)
2. Create a new private plugin
3. Copy the contents of `src/` directory
4. Set up automatic updates (optional)

### For Local Development

1. **Install dependencies:**
   ```bash
   # Option 1: Docker (recommended)
   docker pull trmnl/trmnlp
   
   # Option 2: Ruby gem
   gem install trmnl_preview
   ```

2. **Start development server:**
   ```bash
   # With Docker
   ./start-trmnl.sh
   
   # With Ruby gem
   trmnlp serve
   ```

3. **View in browser:**
   - Full: http://localhost:4567/full
   - Half Horizontal: http://localhost:4567/half_horizontal
   - Half Vertical: http://localhost:4567/half_vertical
   - Quadrant: http://localhost:4567/quadrant

## How It Works

### Data Source
- Fetches live data from ESPN's NFL API
- Automatically detects current NFL week
- Shows upcoming games with schedules
- Displays completed games with scores

### Smart Week Detection
```python
# The script automatically:
# 1. Queries ESPN for current NFL week
# 2. Falls back to scanning for active games
# 3. Handles offseason gracefully
# 4. Updates templates with current data
```

### Template Generation
The plugin dynamically generates Liquid templates with embedded NFL data, ensuring:
- Fast loading on TRMNL devices
- No external API calls during display
- Consistent formatting across all layouts

## Files Structure

```
nfl/
├── src/                     # TRMNL plugin files
│   ├── full.liquid         # Full screen layout (800×480)
│   ├── half_horizontal.liquid # Half horizontal (800×240)
│   ├── half_vertical.liquid   # Half vertical (400×480)
│   ├── quadrant.liquid     # Quadrant layout (400×240)
│   └── settings.yml        # Plugin metadata
├── data/
│   └── schedule.json       # Current NFL data
├── nfl_build.py           # Data fetcher script
├── .trmnlp.yml            # TRMNL development config
└── README.md
```

## Configuration

### Environment Variables
Override automatic detection:
```bash
YEAR=2024 TYPE=2 WEEK=18 python3 nfl_build.py
```

Where:
- `TYPE=2` = Regular season, `TYPE=3` = Playoffs
- `WEEK` = Week number (1-18 for regular season, 1-4 for playoffs)

### Automatic Updates
The plugin can be configured to update automatically:

1. **GitHub Actions** - Set up workflows to run `nfl_build.py`
2. **TRMNL Webhooks** - Trigger updates via TRMNL's webhook system
3. **Cron Jobs** - Schedule regular updates

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

1. **Copy plugin files:**
   ```bash
   # Copy these files to your TRMNL plugin:
   src/full.liquid
   src/half_horizontal.liquid
   src/half_vertical.liquid
   src/quadrant.liquid
   src/settings.yml
   ```

2. **Set up data updates:**
   - Use TRMNL's scheduling features
   - Or set up external triggers to run `nfl_build.py`

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
