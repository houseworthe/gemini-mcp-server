#!/bin/bash

set -e

echo "🚀 Installing Gemini MCP Server for Claude Code..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip3 and try again."
    exit 1
fi

# Check if Claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI is required but not installed. Please install Claude CLI first."
    echo "   Visit: https://docs.anthropic.com/claude-code/cli-usage"
    exit 1
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Clone the repository
echo "📥 Downloading Gemini MCP Server..."
REPO_URL="https://github.com/houseworthe/gemini-mcp-server.git"
git clone --quiet --depth 1 "$REPO_URL" gemini-mcp-server

# Run the setup from the distribution folder
cd gemini-mcp-server/gemini-mcp
bash install.sh

# Cleanup
cd /
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 Installation complete!"