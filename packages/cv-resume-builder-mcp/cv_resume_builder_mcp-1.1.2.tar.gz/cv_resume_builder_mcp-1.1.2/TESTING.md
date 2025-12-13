# Testing Guide

## Quick Test (Easiest)

### Step 1: Update Kiro Config

Edit `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "cv-resume-builder": {
      "command": "python3",
      "args": ["-m", "cv_resume_builder_mcp.server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/cv-resume-builder-mcp/src",
        "AUTHOR_NAME": "your-git-username",
        "REPOS": "default:/absolute/path/to/your-repo",
        "CREDLY_USER_ID": "your-credly-username",
        "LINKEDIN_PROFILE_URL": "https://www.linkedin.com/in/yourprofile"
      }
    }
  }
}
```

**For multiple repositories:** Change `REPOS` to: `"CompanyA:/path1,CompanyB:/path2"`

**Note:** Replace paths with your actual absolute paths. Use `pwd` in each directory to get the full path.

### Step 2: Install Dependencies

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install mcp httpx pypdf

# Keep this terminal open or add to your shell profile
```

### Step 3: Restart Kiro

Close and reopen Kiro IDE.

### Step 4: Test

In Kiro chat:
```
"List available MCP tools"
```

You should see:
- get_git_log
- read_cv
- read_wins
- get_jira_tickets
- get_credly_badges
- get_linkedin_profile
- parse_cv_pdf
- generate_enhanced_cv
- get_cv_guidelines

### Step 5: Try It

```
"Get my git commits from the last month"
```

```
"Get my Credly badges"
```

**With multiple repositories:**
```
"List all my configured repositories"
"Get my commits from CompanyA for the last 3 months"
"Show me all my work across all repositories in the last year"
```

## Alternative: Test with uvx (After Publishing to PyPI)

Once published to PyPI, users can use:

```json
{
  "mcpServers": {
    "cv-resume-builder": {
      "command": "uvx",
      "args": ["cv-resume-builder-mcp"],
      "env": {
        "AUTHOR_NAME": "your-name",
        "REPOS": "default:/path/to/repo"
      }
    }
  }
}
```

**For multiple repositories:** Change `REPOS` to: `"CompanyA:/path1,CompanyB:/path2"`

No installation needed - uvx handles everything!

## Troubleshooting

### "Module not found: mcp"
Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install mcp httpx pypdf
```

### "Module not found: cv_resume_builder_mcp"
Make sure PYTHONPATH is set correctly in your config:
```json
"PYTHONPATH": "/absolute/path/to/poc-mpc-cv/src"
```

### Server not starting
Check Kiro's MCP Server view for error logs.

### Git log returns empty
Make sure AUTHOR_NAME matches your git config:
```bash
git config user.name
```

## Manual Testing (Without Kiro)

You can't easily test MCP servers manually because they use stdio protocol, but you can test the imports:

```bash
python3 -m venv venv
source venv/bin/activate
pip install mcp httpx pypdf

# Test import
PYTHONPATH=src python3 -c "from cv_resume_builder_mcp import server; print('✅ Works!')"
```

## Next Steps

Once testing works:
1. Publish to PyPI
2. Update config to use `uvx`
3. Share with others!
