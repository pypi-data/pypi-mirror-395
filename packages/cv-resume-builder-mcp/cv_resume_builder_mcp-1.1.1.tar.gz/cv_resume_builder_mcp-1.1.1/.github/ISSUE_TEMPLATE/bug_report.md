---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure MCP with '...'
2. Run command '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
 - OS: [e.g. macOS, Windows, Linux]
 - Node.js version: [e.g. 18.0.0]
 - MCP Client: [e.g. Claude Desktop, Kiro IDE]
 - MCP Server version: [e.g. 1.0.0]

**Configuration (remove sensitive data):**
```json
{
  "mcpServers": {
    "cv-resume-builder": {
      "command": "node",
      "args": ["..."],
      "env": {
        "REPO_PATH": "...",
        "AUTHOR_NAME": "..."
      }
    }
  }
}
```

**Error messages:**
```
Paste any error messages here
```

**Additional context**
Add any other context about the problem here.
