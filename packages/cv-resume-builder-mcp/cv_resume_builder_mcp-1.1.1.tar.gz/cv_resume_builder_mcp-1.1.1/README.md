# CV Resume Builder MCP

> AI-powered CV and resume builder using Model Context Protocol (MCP)

Automatically generate and update your CV/resume from git commits, Jira tickets, Credly certifications, and LinkedIn. Built for developers who want their CV to stay current without manual updates.

[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 📊 **Git commits** - Track your code contributions automatically ✅
- 🎫 **Jira tickets** - Pull completed projects and tasks ⚠️ (requires testing)
- 🏆 **Credly badges** - Sync certifications and achievements ✅
- 💼 **LinkedIn profile** - Not implemented yet 🚧 (authentication required)
- 📄 **PDF parsing** - Extract content from existing CVs ✅
- 🚀 **Enhanced CV generation** - Combine all data sources ✅
- 📝 **LaTeX support** - Generate professional CVs ✅

## Quick Start

### Prerequisites
- Python 3.10+
- `uv` installed (for uvx): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- An MCP-compatible AI assistant (Claude Desktop, Kiro, etc.)

### Installation

**Using uvx (recommended - no installation needed!):**

Just configure your MCP client and uvx handles the rest.

**Or install with pip:**
```bash
pip install cv-resume-builder-mcp
```

### Configuration

#### For Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cv-resume-builder": {
      "command": "uvx",
      "args": ["cv-resume-builder-mcp"],
      "env": {
        "AUTHOR_NAME": "your-git-username",
        "REPOS": "default:/absolute/path/to/your-repo"
      }
    }
  }
}
```

**For multiple repositories:** Change `REPOS` to: `"CompanyA:/path1,CompanyB:/path2,Personal:/path3"`

#### For Kiro IDE

Edit `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "cv-resume-builder": {
      "command": "uvx",
      "args": ["cv-resume-builder-mcp"],
      "env": {
        "AUTHOR_NAME": "your-git-username",
        "REPOS": "default:/absolute/path/to/your-repo"
      }
    }
  }
}
```

**For multiple repositories:** Change `REPOS` to: `"CompanyA:/path1,CompanyB:/path2,Personal:/path3"`

**Important:** Use absolute paths (no `~`). Get it with `pwd` in your repo directory.

### Restart Your AI Assistant

After configuration, restart Claude Desktop or Kiro to load the MCP server.

### Test It

```
"List available MCP tools"
```

You should see tools like `get_git_log`, `read_cv`, `parse_cv_pdf`, etc.

## Usage Examples

```
"Get my git commits from the last 6 months and suggest CV updates"
```

**With multiple repositories:**
```
"List all my configured repositories"
"Get my commits from CompanyA for the last 3 months"
"Show me all my work across all repositories in the last year"
```

### Parse existing CV
```
"Parse my CV at ~/Documents/resume.pdf"
```

### Generate enhanced CV
```
"Generate an enhanced CV using my existing resume.pdf and recent work from the last 3 months"
```

### Get certifications
```
"Get my Credly badges and add them to my CV"
```

### Analyze commit impact (NEW!)
```
"Analyze my commits from the last month and show me what I actually built"
"Get detailed code changes for commit abc123 to understand the impact"
"Show me the stats for my recent commits to highlight achievements"
```

## Optional Integrations

Add these to your MCP configuration's `env` section:

### Jira (⚠️ Requires Testing)
```json
"JIRA_URL": "https://your-company.atlassian.net",
"JIRA_EMAIL": "your-email@example.com",
"JIRA_API_TOKEN": "your-api-token",
"JIRA_USER": "your-email@example.com"
```

Get API token: https://id.atlassian.com/manage-profile/security/api-tokens

**Note:** Jira integration is functional but requires more testing across different Jira configurations. Please report any issues!

### Credly (✅ Fully Tested)
```json
"CREDLY_USER_ID": "your-credly-username"
```

Find your username in your Credly profile URL: `https://www.credly.com/users/YOUR-USERNAME`

### LinkedIn (🚧 Not Implemented)
```json
"LINKEDIN_PROFILE_URL": "https://www.linkedin.com/in/yourprofile"
```

**Note:** LinkedIn integration is not yet implemented due to authentication requirements. The tool currently only returns your profile URL. For now, manually copy your LinkedIn achievements to `wins.md` file. Contributions welcome!

### CV Formatting
```json
"MAX_BULLETS_PER_EXPERIENCE": "5"
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_git_log` | Get your git commits from default repo (excludes merge commits) |
| `list_repos` | List all configured repositories |
| `get_git_log_by_repo` | Get commits from a specific repository |
| `get_git_log_all_repos` | Get commits from all repos, grouped by project |
| `get_commit_details` | **NEW!** Get detailed commit info including code changes (diff) for impact analysis |
| `analyze_commits_impact` | **NEW!** Analyze multiple commits with stats to understand actual work done |
| `read_cv` | Read your current LaTeX CV |
| `read_wins` | Read your wins.md achievements file |
| `get_jira_tickets` | Get completed Jira tickets |
| `get_credly_badges` | Get your certifications from Credly |
| `get_linkedin_profile` | Read your LinkedIn profile summary |
| `parse_cv_pdf` | Extract text from existing CV/resume PDF |
| `generate_enhanced_cv` | Combine all data sources into comprehensive report |
| `get_cv_guidelines` | Get formatting rules and constraints |

## Project Structure

```
cv-resume-builder-mcp/
├── src/cv_resume_builder_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server
├── tests/
│   └── test_server.py     # Unit tests
├── pyproject.toml         # Package configuration
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
├── cv.tex                 # LaTeX CV template
├── wins.md                # Manual achievements tracking
└── README.md              # This file
```

## Development

### Setup
```bash
git clone https://github.com/YOUR-USERNAME/cv-resume-builder-mcp.git
cd cv-resume-builder-mcp
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Format Code
```bash
black src/
ruff check src/
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure no credentials are hardcoded
6. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Troubleshooting

### MCP server not showing up
- Verify absolute paths in config (use `pwd`)
- Restart your AI assistant completely
- Check for typos in configuration

### Git log returns empty
- Check your git author name: `git config user.name`
- Update `AUTHOR_NAME` to match exactly

### "Command not found: uvx"
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Or: `brew install uv`

### Jira/Credly errors
- Verify API tokens are correct
- Check URLs don't have trailing slashes
- Ensure services are accessible

## Security

- All credentials stored in environment variables
- No data sent to external services except configured integrations
- Git history stays local
- Open source - audit the code yourself

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 🐛 **Report bugs** - Open an issue on GitHub
- 💡 **Request features** - Create a feature request issue
- 💬 **Ask questions** - Start a discussion on GitHub

---

**Keywords:** cv builder, resume builder, mcp, model context protocol, ai resume, ai cv, automatic cv, career tracker, latex cv, resume generator, cv generator, developer resume, tech resume

Made with ❤️ for developers who hate updating their CVs manually
