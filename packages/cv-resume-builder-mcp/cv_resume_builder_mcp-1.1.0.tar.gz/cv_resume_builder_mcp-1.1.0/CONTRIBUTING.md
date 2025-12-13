# Contributing

Thanks for your interest in contributing to CV Resume Builder MCP!

## How to Contribute

### Reporting Bugs
1. Check if the bug already exists in [Issues](https://github.com/YOUR-USERNAME/cv-resume-builder-mcp/issues)
2. If not, create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, MCP client)

### Suggesting Features
Create an issue describing:
- The problem you're solving
- Your proposed solution
- Any alternatives considered

### Code Contributions

1. **Fork and clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/cv-resume-builder-mcp.git
   cd cv-resume-builder-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make changes**
   - Follow PEP 8 style guide
   - Add type hints
   - Add docstrings
   - Keep functions focused

5. **Test**
   ```bash
   pytest
   black src/
   ruff check src/
   ```

6. **Commit and push**
   ```bash
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings for functions
- Format with `black`
- Lint with `ruff`

### Security
- Never commit credentials
- Use environment variables for sensitive data
- Validate inputs
- Handle errors gracefully

### Testing
- Test with an MCP client before submitting
- Add unit tests for new features
- Ensure all tests pass

## Ideas for Contributions

- Add more integrations (GitHub, GitLab, Stack Overflow)
- Support more CV formats (Markdown, HTML, Word)
- Improve PDF parsing
- Add CV templates
- Better error messages
- Documentation improvements

## Questions?

Open an issue or discussion on GitHub.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

Thank you for contributing! 🎉
