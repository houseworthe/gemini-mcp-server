# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

1. **Do NOT** open a public issue
2. Email the maintainers directly with details (check repository for contact info)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- Acknowledgment: Within 48 hours
- Initial assessment: Within 1 week
- Fix timeline: Depends on severity
  - Critical: Within 48 hours
  - High: Within 1 week
  - Medium: Within 2 weeks
  - Low: Next regular release

## Security Best Practices for Users

1. **API Key Management**
   - Never commit API keys to version control
   - Use environment variables or secure secret management
   - Rotate API keys regularly
   - Use separate keys for development and production

2. **Access Control**
   - Limit API key permissions to minimum required
   - Review MCP server permissions regularly
   - Use proper file permissions (600) for sensitive files

3. **Updates**
   - Keep the server updated to the latest version
   - Monitor security advisories
   - Review changelog for security fixes

## Security Features

This project includes:
- Secure API key storage using environment variables
- HTTPS-only communication with Gemini API
- Input validation and sanitization
- Error messages that don't expose sensitive information
- Logging that excludes sensitive data

## Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who help improve our security.