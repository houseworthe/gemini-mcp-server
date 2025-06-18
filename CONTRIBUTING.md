# Contributing to Gemini MCP Server

First off, thank you for considering contributing to Gemini MCP Server! It's people like you that make this tool better for everyone.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct (see CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Why this enhancement would be useful
- Examples of how it would be used

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Issue that pull request!

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/gemini-mcp.git
   cd gemini-mcp
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Guidelines

### Code Style

- We use Black for code formatting (line length: 88)
- We use Ruff for linting
- Type hints are encouraged where appropriate
- Follow PEP 8 conventions

### Testing

- Write tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Use pytest for testing

Run tests with:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=server --cov-report=html
```

### Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in the imperative mood (e.g., "Add", "Fix", "Update")
- Keep the first line under 50 characters
- Reference issues and pull requests where relevant

### Documentation

- Update README.md if you change functionality
- Add docstrings to new functions and classes
- Update usage examples if relevant

## Review Process

1. A maintainer will review your PR
2. They may request changes or ask questions
3. Once approved, your PR will be merged
4. Your contribution will be included in the next release!

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing!