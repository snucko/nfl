# NFL Schedule TRMNL Plugin

A dynamic NFL schedule plugin for TRMNL devices that displays current week games, scores, and schedules.

## ✅ Current Status: WORKING

The plugin is now fully functional and displays:
- **NFL Week 5 · 2025 (Regular Season)**
- Current games including 49ers @ Rams, Chiefs @ Jaguars, etc.
- Game times, dates, and venues
- Responsive layouts for all TRMNL screen sizes

## 🏈 Features

### Live Data Integration
- **Production**: Automatically fetches live data from ESPN's NFL API
- **Local Development**: Uses hardcoded current week data for testing
- **Smart Fallback**: Seamlessly switches between data sources

### Multiple Layout Support
- **Full (800×480)**: Complete game information with venues and detailed times
- **Half Horizontal (800×240)**: Compact grid layout showing 6 games
- **Half Vertical (400×480)**: Vertical list format for 8 games  
- **Quadrant (400×240)**: Minimal display showing 3 key games

### Real-time Information
- Current NFL week and season
- Live game scores during games
- Game status (scheduled, live, final)
- Team matchups with abbreviations
- Venue information and game times

## 🚀 Setup Instructions

### For TRMNL Platform (Production)

1. **Create Private Plugin**:
   - Go to [usetrmnl.com](https://usetrmnl.com/) dashboard
   - Navigate to Plugins → Create Private Plugin
   - Name: `NFL Schedule`
   - Description: `Live NFL games, scores, and schedules`

2. **Upload Template Files**:
   Copy the contents of these files from `src/` directory:
   - `full.liquid` - Full screen layout
   - `half_horizontal.liquid` - Half horizontal layout
   - `half_vertical.liquid` - Half vertical layout  
   - `quadrant.liquid` - Quadrant layout
   - `settings.yml` - Plugin metadata

3. **Configure Settings** (Optional):
   - **Data URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
   - **Refresh Rate**: 1-2 hours during game days
   - **Time Zone**: Your local timezone

4. **Deploy**:
   - Save the plugin
   - Add to your TRMNL device
   - Select your preferred layout

### For Local Development

The plugin is designed to work locally with the TRMNL development server:

```bash
# Clone and setup
git clone https://github.com/snucko/nfl
cd nfl

# Run TRMNL development server
docker run --rm -it -p 4567:4567 -v "$(pwd):/plugin" trmnl/trmnlp serve

# View in browser
open http://localhost:4567/full
```

## 📱 Layout Previews

### Full Layout (800×480)
Shows complete game information:
```
NFL Week 5 · 2025 (Regular Season)

San Francisco 49ers at Los Angeles Rams (10/2 - 8:15 PM EDT)
Thu Oct 02, 8:15 PM · SoFi Stadium

Kansas City Chiefs at Jacksonville Jaguars (10/6 - 8:15 PM EDT)  
Mon Oct 06, 8:15 PM · EverBank Stadium
```

### Half Horizontal (800×240)
Compact grid format:
```
NFL Week 5 · 2025

SF@LAR     MIN@CLE    LV@IND
10/2 8:15PM  10/5 9:30AM  10/5 1:00PM
```

### Half Vertical (400×480)
Vertical list:
```
NFL Week 5

SF@LAR
10/2 8:15PM

MIN@CLE  
10/5 9:30AM
```

### Quadrant (400×240)
Minimal display:
```
NFL W5

SF@LAR
Thu

MIN@CLE
Sat
```

## 🔧 Technical Details

### Data Sources
- **Primary**: ESPN NFL API (`https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`)
- **Fallback**: Hardcoded current week data for local development
- **Format**: JSON with team info, scores, schedules, venues

### Template Engine
- **Liquid**: Jekyll-compatible templating
- **Variables**: `{{ trmnl.user.name }}`, `{{ trmnl.plugin_settings.instance_name }}`
- **Filters**: Date formatting, string manipulation
- **Logic**: Conditional rendering based on data availability

### Styling
- **Framework**: System fonts with TRMNL CSS framework
- **Responsive**: Adapts to different screen sizes
- **Themes**: Works with white, black, mint, gray, and wood cases
- **Typography**: Clean, readable fonts optimized for e-ink displays

## 🛠 Development

### File Structure
```
src/
├── full.liquid              # Full screen layout
├── half_horizontal.liquid   # Half horizontal layout  
├── half_vertical.liquid     # Half vertical layout
├── quadrant.liquid          # Quadrant layout
└── settings.yml             # Plugin metadata

data/
└── schedule.json            # Current NFL data (auto-updated)

_data/
└── schedule.json            # Jekyll-style data access
```

### Data Updates
The NFL data is automatically updated using the `nfl_build.py` script:
```bash
# Update current week data
python3 nfl_build.py

# This updates data/schedule.json with latest games
```

### Testing Layouts
```bash
# Test all layouts locally
curl http://localhost:4567/render/full.html
curl http://localhost:4567/render/half_horizontal.html  
curl http://localhost:4567/render/half_vertical.html
curl http://localhost:4567/render/quadrant.html
```

## 📊 Data Format

The plugin handles ESPN's NFL API format:
```json
{
  "season": {"year": 2025, "type": 2},
  "week": {"number": 5},
  "events": [
    {
      "name": "San Francisco 49ers at Los Angeles Rams",
      "date": "2025-10-02T20:15:00Z",
      "competitions": [{
        "competitors": [
          {"homeAway": "away", "team": {"displayName": "San Francisco 49ers", "abbreviation": "SF"}},
          {"homeAway": "home", "team": {"displayName": "Los Angeles Rams", "abbreviation": "LAR"}}
        ],
        "status": {"type": {"shortDetail": "10/2 - 8:15 PM EDT"}},
        "venue": {"fullName": "SoFi Stadium"}
      }]
    }
  ]
}
```

## 🎯 Next Steps

1. **Deploy to TRMNL**: Follow setup instructions above
2. **Customize Styling**: Modify CSS in templates for personal preferences  
3. **Add Features**: Extend with playoff brackets, team records, etc.
4. **Automate Updates**: Set up scheduled data refreshes

## 🐛 Troubleshooting

- **No data showing**: Check internet connection and API availability
- **Wrong week**: Data updates automatically, may need 1-2 hours to reflect new week
- **Layout issues**: Ensure correct template file is uploaded
- **Local testing**: Use `docker run` command with TRMNL development server

## 📄 License

This project is open source. The NFL data is provided by ESPN's public API.