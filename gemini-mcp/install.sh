#!/bin/bash

set -e

echo "🚀 Installing Gemini MCP for Claude Code..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if Claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI is required but not installed. Please install Claude CLI first."
    echo "   Visit: https://docs.anthropic.com/claude-code/cli-usage"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ask for Gemini API key
echo "Please enter your Gemini API key:"
echo "(Get one at: https://makersuite.google.com/app/apikey)"
read -s GEMINI_API_KEY
echo ""

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ API key cannot be empty"
    exit 1
fi

# Export API key for setup script
export GEMINI_API_KEY

# Run setup script
echo "Running setup..."
bash "$SCRIPT_DIR/setup.sh"

echo ""
echo "✅ Installation complete!"
echo ""
echo "To verify installation, run: claude mcp list"
echo ""
echo "Usage examples:"
echo "  - Ask Gemini: mcp__gemini-collab__ask_gemini"
echo "  - Code review: mcp__gemini-collab__gemini_code_review"
echo "  - Brainstorm: mcp__gemini-collab__gemini_brainstorm"
echo "  - Analyze large content: mcp__gemini-collab__gemini_analyze_large"