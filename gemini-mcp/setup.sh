#!/bin/bash

set -e

echo "📦 Setting up Gemini MCP server..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create server directory in ~/.claude-mcp-servers
SERVER_DIR="$HOME/.claude-mcp-servers/gemini-collab"
mkdir -p "$SERVER_DIR"

# Copy server files
echo "Copying server files..."
cp "$SCRIPT_DIR/server.py" "$SERVER_DIR/"
cp "$SCRIPT_DIR/requirements.txt" "$SERVER_DIR/"

# Save API key to environment file
echo "GEMINI_API_KEY=$GEMINI_API_KEY" > "$SERVER_DIR/.env"
chmod 600 "$SERVER_DIR/.env"

# Install dependencies
echo "Installing dependencies..."
cd "$SERVER_DIR"
pip3 install -r requirements.txt

# Remove any existing gemini-collab server
claude mcp remove gemini-collab 2>/dev/null || true

# Register with Claude CLI
echo "Registering with Claude CLI..."
claude mcp add --scope user gemini-collab python3 "$SERVER_DIR/server.py"

echo "✅ Setup complete!"