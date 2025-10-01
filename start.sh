#!/bin/bash
# NFL TRMNL Plugin Starter - Multiple Methods

echo "🏈 NFL TRMNL Plugin Starter"
echo "=========================="
echo ""

# Update NFL data first
echo "📊 Updating NFL data..."
cd /Users/unknown1/Downloads/nfl
python3 nfl_build.py
echo ""

# Check if Docker is available
if docker info > /dev/null 2>&1; then
    echo "🐳 Docker is running! Starting official TRMNL server..."
    echo ""
    echo "📱 Access your plugin at:"
    echo "   • Full: http://localhost:4567/full"
    echo "   • Half Horizontal: http://localhost:4567/half_horizontal"
    echo "   • Half Vertical: http://localhost:4567/half_vertical" 
    echo "   • Quadrant: http://localhost:4567/quadrant"
    echo ""
    echo "⏹️  Press Ctrl+C to stop"
    echo ""
    
    docker run \
        --rm \
        --interactive \
        --tty \
        --publish 4567:4567 \
        --volume "$(pwd):/plugin" \
        trmnl/trmnlp serve
        
elif command -v trmnlp > /dev/null 2>&1; then
    echo "💎 Using locally installed TRMNL gem..."
    echo ""
    echo "📱 Access your plugin at:"
    echo "   • Full: http://localhost:4567/full"
    echo "   • Half Horizontal: http://localhost:4567/half_horizontal"
    echo "   • Half Vertical: http://localhost:4567/half_vertical"
    echo "   • Quadrant: http://localhost:4567/quadrant"
    echo ""
    echo "⏹️  Press Ctrl+C to stop"
    echo ""
    
    trmnlp serve
    
else
    echo "🌐 Docker not ready. Starting preview server instead..."
    echo ""
    echo "📱 Access your plugin preview at:"
    echo "   • TRMNL Preview: http://localhost:4567/preview.html"
    echo "   • Original HTML: http://localhost:4567/index.html"
    echo "   • Raw Data: http://localhost:4567/data/schedule.json"
    echo ""
    echo "💡 To use the official TRMNL server:"
    echo "   1. Wait for Docker Desktop to fully start (check menu bar)"
    echo "   2. Run this script again"
    echo ""
    echo "⏹️  Press Ctrl+C to stop"
    echo ""
    
    python3 -m http.server 4567
fi