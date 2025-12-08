#!/bin/bash
# NFL TRMNL Plugin - Docker Development Server

echo "🏈 Starting NFL TRMNL Plugin with Docker..."
echo ""
echo "🚀 Starting official TRMNL development server..."
echo "   Access your plugin at: http://localhost:4567"
echo ""
echo "📱 Available layouts:"
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