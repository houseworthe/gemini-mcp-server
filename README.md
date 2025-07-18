# Gemini MCP Server for Claude Code

A Model Context Protocol (MCP) server that seamlessly integrates Google's Gemini AI capabilities into Claude Code, enabling powerful AI collaboration.

## Features

This MCP server provides Claude with access to Gemini's capabilities through four powerful tools:

- **Ask Gemini** - Direct question-answering using Gemini's extensive knowledge base
- **Code Review** - Comprehensive code analysis with support for large codebases
- **Brainstorming** - Creative ideation and problem-solving assistance
- **Large Content Analysis** - Analyze extensive documents, logs, or codebases (optimized for 1M+ tokens)

## Use Cases

### Enhanced Code Development
```bash
# Claude can leverage Gemini for specialized tasks:
"Claude, ask Gemini to review this React component for performance optimizations"
"Use Gemini to analyze this entire codebase and identify potential security vulnerabilities"
```

### Collaborative Problem Solving
```bash
# Combine Claude's reasoning with Gemini's knowledge:
"Ask Gemini about the latest best practices for microservices architecture"
"Have Gemini brainstorm solutions for scaling our database"
```

### Large-Scale Analysis
```bash
# Process extensive content that benefits from Gemini's capabilities:
"Use Gemini to analyze these server logs and identify anomaly patterns"
"Ask Gemini to review this 10,000-line legacy codebase and suggest modernization strategies"
```

## Quick Start

### One-Line Installation

```bash
curl -sSL https://raw.githubusercontent.com/houseworthe/gemini-mcp-server/main/gemini-mcp/install.sh | bash
```

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/houseworthe/gemini-mcp-server.git
   cd gemini-mcp-server
   ```

2. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. Run the installer:
   ```bash
   cd gemini-mcp
   ./install.sh
   ```

4. Enter your API key when prompted

## Architecture

The server acts as a bridge between Claude Code and Google's Gemini API:

```
Claude Code <-> MCP Protocol <-> Gemini MCP Server <-> Gemini API
```

### Key Components:
- **Async JSON-RPC Handler**: Processes MCP protocol messages
- **Tool Registry**: Manages available Gemini tools
- **HTTP Client**: Direct API communication with Gemini
- **Error Handling**: Graceful degradation and timeout management

## Configuration

### Environment Variables
Create a `.env` file (see `.env.example`):
```bash
GEMINI_API_KEY=your-api-key-here
```

### Supported Models
- `gemini-1.5-flash` (default) - Fast responses for most queries
- `gemini-1.5-pro` - Automatically used for large content analysis

## Development

### Prerequisites
- Python 3.7+
- Claude CLI
- Gemini API key

### Running Tests
```bash
python test_server.py
```

### Project Structure
```
gemini-mcp-server/
├── server.py           # Main MCP server implementation
├── test_server.py      # Integration tests
├── gemini-mcp/         # Distribution package
│   ├── server.py       # Server for end-user installation
│   ├── install.sh      # Installation script
│   ├── setup.sh        # Claude MCP registration
│   └── requirements.txt
└── README.md
```

## API Documentation

### Available Tools

#### ask_gemini
Basic question-answering interface.
```json
{
  "question": "string"  // Required: Your question for Gemini
}
```

#### gemini_code_review
Comprehensive code review with contextual understanding.
```json
{
  "code": "string",        // Required: Code to review
  "context": "string",     // Optional: Additional context
  "focus_areas": "string"  // Optional: Specific areas to focus on
}
```

#### gemini_brainstorm
Creative ideation and problem-solving.
```json
{
  "topic": "string",       // Required: Topic to brainstorm
  "constraints": "string"  // Optional: Any constraints or requirements
}
```

#### gemini_analyze_large
Analyze extensive content with intelligent summarization.
```json
{
  "content": "string",        // Required: Large content to analyze
  "analysis_type": "string",  // Optional: Type of analysis (default: "general")
  "questions": "string"       // Optional: Specific questions to answer
}
```

## Troubleshooting

### Server Not Listed
If the server doesn't appear in `claude mcp list`:
```bash
claude mcp remove gemini-collab
claude mcp add --scope user gemini-collab python3 ~/.claude-mcp-servers/gemini-collab/server.py
```

### API Key Issues
- Ensure your API key is valid and has the necessary permissions
- Check that the `.env` file is in the correct location
- Verify the key is set: `echo $GEMINI_API_KEY`

### Timeout Errors
The server has a 30-second timeout for API calls. For large content:
- Consider breaking it into smaller chunks
- Use the `gemini_analyze_large` tool which handles content intelligently

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

- API keys are stored locally and never transmitted except to Google's API
- All communication uses HTTPS
- The server runs with minimal permissions
- Regular security audits are performed

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on the [Model Context Protocol](https://github.com/anthropics/mcp) by Anthropic
- Powered by [Google's Gemini AI](https://deepmind.google/technologies/gemini/)
- Inspired by the AI development community

## Support

- **Issues**: [GitHub Issues](https://github.com/houseworthe/gemini-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/houseworthe/gemini-mcp-server/discussions)
- **Documentation**: [Wiki](https://github.com/houseworthe/gemini-mcp-server/wiki)

---

Made with ❤️ by the open source community