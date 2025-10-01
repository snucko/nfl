# NFL TRMNL Plugin - Dynamic Data Deployment Guide

## 🚀 Ready for TRMNL Upload with Live Data!

Your NFL plugin now fetches **live, dynamic data** directly from ESPN's API. No more hard-coded game information!

### ✅ **What's New**

- **Dynamic data fetching** - Gets current NFL week automatically
- **Live API calls** - Fresh data every time your TRMNL refreshes
- **Error handling** - Graceful fallbacks when API is unavailable
- **Configurable settings** - Customize API URL and refresh rate
- **No manual updates** - Data updates automatically

### 📁 **Plugin Files Ready**

All files in `src/` are now **dynamic** and ready for TRMNL:

```
src/
├── full.liquid            # Full screen with live API data
├── half_horizontal.liquid # Half horizontal with live API data
├── half_vertical.liquid   # Half vertical with live API data
├── quadrant.liquid        # Quadrant with live API data
└── settings.yml           # Plugin configuration
```

### 🏈 **Deploy to TRMNL Device**

#### **Step 1: Create Private Plugin**
1. Go to [TRMNL Dashboard](https://usetrmnl.com/)
2. Click **"Create Private Plugin"**
3. Name: `NFL Schedule`
4. Description: `Live NFL game schedules and scores`

#### **Step 2: Copy Template Code**

For each layout, copy the **entire contents** from:

**Full Layout:**
```liquid
{% comment %}
NFL Schedule - Full Size TRMNL Plugin
Fetches live NFL data from ESPN API
{% endcomment %}

{% assign api_url = custom_fields.data_url | default: "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard" %}
{% assign nfl_data = api_url | fetch_json %}
<!-- [Rest of src/full.liquid] -->
```

**Half Horizontal:**
```liquid
<!-- Copy complete contents of src/half_horizontal.liquid -->
```

**Half Vertical:**
```liquid
<!-- Copy complete contents of src/half_vertical.liquid -->
```

**Quadrant:**
```liquid
<!-- Copy complete contents of src/quadrant.liquid -->
```

#### **Step 3: Configure Plugin Settings**

In the TRMNL plugin editor:

**Custom Fields:**
- **NFL Data URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard` (default)
- **Refresh Interval**: `60` minutes (recommended)

**Plugin Settings:**
- **Update Frequency**: 1-4 hours
- **Layout**: Choose your preferred size
- **Position**: Select screen placement

### 🎯 **How It Works**

1. **TRMNL calls your plugin** at the configured interval
2. **Plugin fetches live data** from ESPN NFL API using `fetch_json`
3. **Current games display** with real-time information:
   - Current NFL week and season
   - Upcoming game schedules
   - Live scores during games
   - Final scores after completion
   - Team names and venues

### 📊 **What Your TRMNL Will Show**

**During NFL Season:**
- **Live games** with current scores
- **Upcoming games** with schedules
- **Recent games** with final scores
- **Automatic week detection**

**During Offseason:**
- **"No games scheduled"** message
- **Clean error handling**
- **Ready for next season**

### 🔧 **Configuration Options**

**API URL** - Change data source if needed:
```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
```

**Refresh Rate** - How often to fetch new data:
- **60 minutes** - Recommended for general use
- **30 minutes** - During game days
- **15 minutes** - For live game tracking

### 🚨 **Error Handling**

The plugin includes smart error handling:
- **API unavailable** - Shows friendly error message
- **No games** - Shows "No games scheduled"
- **Invalid data** - Falls back to error display
- **Network issues** - Graceful degradation

### 🎉 **Benefits of Dynamic Data**

✅ **Always current** - No manual updates needed  
✅ **Live scores** - Real-time game information  
✅ **Automatic seasons** - Handles regular season, playoffs, offseason  
✅ **Error resilient** - Works even when API has issues  
✅ **Configurable** - Customize refresh rate and data source  

### 🔄 **No More Manual Updates**

Unlike the previous version, you **never need to update templates** again! The plugin automatically:
- Detects current NFL week
- Shows live game scores
- Handles season transitions
- Updates game schedules

### 🚀 **Deploy Now**

Your NFL TRMNL plugin with **live, dynamic data** is ready to deploy! Just copy the template contents from `src/` to your TRMNL private plugin and enjoy automatic NFL updates on your device.

---

*Your TRMNL will now show live NFL data automatically! 🏈📺*