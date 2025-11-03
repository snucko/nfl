#!/bin/bash
# Manual NFL data update script

set -e

echo "Updating NFL data..."
python3 nfl_build.py

echo "Data updated successfully!"
echo "Files created:"
echo "  - data/schedule.json"
echo "  - docs/schedule.json"

echo "To test webhook:"
echo "curl -X POST \"YOUR_WEBHOOK_URL\" -H \"Content-Type: application/json\" -d @data/schedule.json"
