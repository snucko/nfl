# NFL TRMNL Plugin - Deployment Guide

## Ready for TRMNL Upload! 🚀

Your NFL plugin is now ready to deploy to your TRMNL device.

### What's Included

✅ **TRMNL Plugin Files** (in `src/` directory):
- `full.liquid` - Full screen layout (800×480)
- `half_horizontal.liquid` - Half horizontal (800×240)  
- `half_vertical.liquid` - Half vertical (400×480)
- `quadrant.liquid` - Quadrant layout (400×240)
- `settings.yml` - Plugin metadata

✅ **Current NFL Data**:
- 2025 Season Week 5 (Regular Season)
- 14 upcoming games with schedules
- Auto-generated templates with embedded data

✅ **Development Tools**:
- Local TRMNL server support
- Automatic data update scripts
- Git repository with clean history

### Deploy to TRMNL Device

#### Method 1: Manual Upload
1. Go to [TRMNL Dashboard](https://usetrmnl.com/)
2. Create a new Private Plugin
3. Copy and paste the contents of each file from `src/`:
   - Copy `src/full.liquid` → Paste into "Full" layout
   - Copy `src/half_horizontal.liquid` → Paste into "Half Horizontal" layout
   - Copy `src/half_vertical.liquid` → Paste into "Half Vertical" layout  
   - Copy `src/quadrant.liquid` → Paste into "Quadrant" layout
   - Copy `src/settings.yml` → Paste into plugin settings

#### Method 2: Git Integration (if available)
1. Push this repository to GitHub
2. Connect your TRMNL to the repository
3. Set up automatic updates

### Keep Data Current

#### Option 1: Manual Updates
Run when you want fresh NFL data:
```bash
./update-nfl.sh
```

#### Option 2: Automated Updates  
Set up a cron job or GitHub Action to run:
```bash
python3 nfl_build.py
```

### Current Plugin Status

🏈 **Season**: 2025 Week 5 (Regular Season)  
📊 **Games**: 14 upcoming games  
📅 **Updated**: Auto-generated with current data  
🎯 **Layouts**: All 4 TRMNL sizes supported  

### What Your TRMNL Will Show

- **Game matchups** with team names
- **Scheduled times** for upcoming games  
- **Live scores** when games are in progress
- **Final scores** for completed games
- **Clean formatting** optimized for e-ink display

### Next Steps

1. **Deploy to TRMNL** using the files in `src/`
2. **Choose your layout** size on the TRMNL dashboard
3. **Set refresh rate** (recommended: 1-4 hours)
4. **Enjoy NFL updates** on your TRMNL device!

The plugin will automatically show current week games and handle different seasons (regular season, playoffs, offseason) gracefully.

---

*Your NFL TRMNL plugin is ready! 🎉*