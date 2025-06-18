# Gemini MCP for Claude Code

Integrates Google's Gemini AI into Claude Code via Model Context Protocol (MCP).

## Installation

### One-liner install:
```bash
curl -sSL https://raw.githubusercontent.com/houseworthe/gemini-mcp-server/main/gemini-mcp/install.sh | bash
```

### Manual install:
1. Clone this repository
2. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Run `./install.sh` and enter your API key when prompted

## What it does

The installer:
- Checks for Python 3 and Claude CLI
- Installs the Google Gemini Python SDK
- Sets up a local MCP server at `~/.claude-mcp-servers/gemini-collab/`
- Registers it with Claude Code globally

## Usage

In Claude Code, you can use these commands:

- `mcp__gemini-collab__ask_gemini` - Ask Gemini general questions
- `mcp__gemini-collab__gemini_code_review` - Get code reviews from Gemini
- `mcp__gemini-collab__gemini_brainstorm` - Brainstorm ideas with Gemini
- `mcp__gemini-collab__gemini_analyze_large` - Analyze large documents or codebases

Or use natural language:
```
Claude, ask Gemini to review this function for security issues
```

## Verify Installation

Run:
```bash
claude mcp list
```

You should see:
```
☑ gemini-collab  user   python3 ~/.claude-mcp-servers/gemini-collab/server.py
```

## Troubleshooting

If the server isn't listed, try:
```bash
claude mcp remove gemini-collab
claude mcp add --scope user gemini-collab python3 ~/.claude-mcp-servers/gemini-collab/server.py
```

## Requirements

- Python 3.7+
- Claude CLI
- Gemini API key

## License

MIT