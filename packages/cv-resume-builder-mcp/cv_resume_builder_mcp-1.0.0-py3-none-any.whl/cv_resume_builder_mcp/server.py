#!/usr/bin/env python3
"""CV Resume Builder MCP Server - Main implementation."""

import os
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import base64

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import httpx
import pypdf


# Configuration from environment variables
AUTHOR_NAME = os.getenv("AUTHOR_NAME", "your-git-username")

# Repository configuration
# Format: "CompanyA:/path/to/repo1,CompanyB:/path/to/repo2"
# Or single: "default:/path/to/repo"
REPOS = os.getenv("REPOS", "")
# Backward compatibility: support old REPO_PATH
REPO_PATH = os.getenv("REPO_PATH", "")

def parse_repos() -> dict:
    """Parse REPOS environment variable into a dictionary."""
    repos = {}
    
    # Parse REPOS if provided
    if REPOS:
        for repo_entry in REPOS.split(","):
            if ":" in repo_entry:
                name, path = repo_entry.split(":", 1)
                repos[name.strip()] = path.strip()
    
    # Backward compatibility: if REPO_PATH is set and no REPOS, use it as default
    if REPO_PATH and not repos:
        repos["default"] = REPO_PATH
    
    # If nothing configured, use current directory as default
    if not repos:
        repos["default"] = os.getcwd()
    
    return repos

REPO_DICT = parse_repos()

# Jira Configuration
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_USER = os.getenv("JIRA_USER")

# Credly Configuration
CREDLY_USER_ID = os.getenv("CREDLY_USER_ID")

# LinkedIn Configuration
LINKEDIN_PROFILE_URL = os.getenv("LINKEDIN_PROFILE_URL")

# CV Configuration
MAX_BULLETS_PER_EXPERIENCE = int(os.getenv("MAX_BULLETS_PER_EXPERIENCE", "5"))


# Initialize MCP server
app = Server("cv-resume-builder-mcp")


def parse_time_range(since: str) -> datetime:
    """Parse time range like '6 months ago' into a datetime."""
    now = datetime.now()
    
    # Simple parser for common patterns
    parts = since.lower().split()
    if len(parts) >= 3 and parts[-1] == "ago":
        try:
            amount = int(parts[0])
            unit = parts[1].rstrip('s')  # Remove plural 's'
            
            if unit == "day":
                return now - timedelta(days=amount)
            elif unit == "week":
                return now - timedelta(weeks=amount)
            elif unit == "month":
                return now - timedelta(days=amount * 30)
            elif unit == "year":
                return now - timedelta(days=amount * 365)
        except (ValueError, IndexError):
            pass
    
    # Default to 6 months
    return now - timedelta(days=180)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="get_git_log",
            description="Get latest git commits by author from default repo (excludes merge commits)",
            inputSchema={
                "type": "object",
                "properties": {
                    "since": {
                        "type": "string",
                        "description": "Time range for commits",
                        "default": "6 months ago"
                    }
                }
            }
        ),
        Tool(
            name="list_repos",
            description="List all configured git repositories",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_git_log_by_repo",
            description="Get git commits from a specific repository by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "Name of the repository (e.g., 'CompanyA', 'Personal')"
                    },
                    "since": {
                        "type": "string",
                        "description": "Time range for commits",
                        "default": "6 months ago"
                    }
                },
                "required": ["repo_name"]
            }
        ),
        Tool(
            name="get_git_log_all_repos",
            description="Get git commits from all configured repositories, grouped by repo",
            inputSchema={
                "type": "object",
                "properties": {
                    "since": {
                        "type": "string",
                        "description": "Time range for commits",
                        "default": "6 months ago"
                    }
                }
            }
        ),
        Tool(
            name="read_cv",
            description="Read current CV (LaTeX)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="read_wins",
            description="Read wins.md achievements file",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_jira_tickets",
            description="Get Jira tickets assigned to or created by user",
            inputSchema={
                "type": "object",
                "properties": {
                    "since": {
                        "type": "string",
                        "description": "Time range for tickets",
                        "default": "6 months ago"
                    },
                    "status": {
                        "type": "string",
                        "description": "Ticket status to filter",
                        "default": "Done"
                    }
                }
            }
        ),
        Tool(
            name="get_credly_badges",
            description="Get Credly badges and certifications",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of badges to retrieve",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="get_linkedin_profile",
            description="Get LinkedIn profile summary (headline, about, experience)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_cv_guidelines",
            description="Get CV formatting guidelines and constraints",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="parse_cv_pdf",
            description="Parse an existing CV PDF file to extract text content and structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdfPath": {
                        "type": "string",
                        "description": "Relative or absolute path to the CV PDF file"
                    }
                },
                "required": ["pdfPath"]
            }
        ),
        Tool(
            name="generate_enhanced_cv",
            description="Generate an enhanced CV by combining existing CV content with data from all sources",
            inputSchema={
                "type": "object",
                "properties": {
                    "existingCvPath": {
                        "type": "string",
                        "description": "Path to existing CV (PDF or LaTeX)"
                    },
                    "since": {
                        "type": "string",
                        "description": "Time range for fetching recent work",
                        "default": "6 months ago"
                    }
                },
                "required": ["existingCvPath"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "get_git_log":
            return await get_git_log(arguments.get("since", "6 months ago"))
        
        elif name == "list_repos":
            return await list_repos_tool()
        
        elif name == "get_git_log_by_repo":
            return await get_git_log_by_repo(
                arguments.get("repo_name"),
                arguments.get("since", "6 months ago")
            )
        
        elif name == "get_git_log_all_repos":
            return await get_git_log_all_repos(arguments.get("since", "6 months ago"))
        
        elif name == "read_cv":
            return await read_cv()
        
        elif name == "read_wins":
            return await read_wins()
        
        elif name == "get_jira_tickets":
            return await get_jira_tickets(
                arguments.get("since", "6 months ago"),
                arguments.get("status", "Done")
            )
        
        elif name == "get_credly_badges":
            return await get_credly_badges(arguments.get("limit", 50))
        
        elif name == "get_linkedin_profile":
            return await get_linkedin_profile()
        
        elif name == "get_cv_guidelines":
            return await get_cv_guidelines()
        
        elif name == "parse_cv_pdf":
            return await parse_cv_pdf(arguments.get("pdfPath"))
        
        elif name == "generate_enhanced_cv":
            return await generate_enhanced_cv(
                arguments.get("existingCvPath"),
                arguments.get("since", "6 months ago")
            )
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def get_git_log(since: str) -> list[TextContent]:
    """Get git commits by author from first/default repo."""
    # Get first repo (usually 'default' or first configured)
    if not REPO_DICT:
        return [TextContent(type="text", text="No repositories configured")]
    
    first_repo_name = list(REPO_DICT.keys())[0]
    first_repo_path = REPO_DICT[first_repo_name]
    
    try:
        cmd = [
            "git", "log",
            f"--author={AUTHOR_NAME}",
            "--no-merges",
            f"--since={since}",
            "--pretty=format:%h - %s (%cr)"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=first_repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout.strip()
        repo_label = f"'{first_repo_name}'" if first_repo_name != "default" else "default repo"
        return [TextContent(
            type="text",
            text=f"Git commits from {repo_label}:\n\n{output if output else 'No commits found'}"
        )]
    
    except subprocess.CalledProcessError as e:
        return [TextContent(type="text", text=f"Git error: {e.stderr}")]


async def list_repos_tool() -> list[TextContent]:
    """List all configured repositories."""
    if not REPO_DICT:
        return [TextContent(
            type="text",
            text="No repositories configured"
        )]
    
    output = "Configured Repositories:\n\n"
    for name, path in REPO_DICT.items():
        output += f"- {name}: {path}\n"
    
    output += f"\nTotal: {len(REPO_DICT)} repository" + ("ies" if len(REPO_DICT) > 1 else "")
    output += "\n\nUsage:\n"
    output += "- Use 'get_git_log_by_repo' to get commits from a specific repo\n"
    output += "- Use 'get_git_log_all_repos' to get commits from all repos"
    
    return [TextContent(type="text", text=output)]


async def get_git_log_by_repo(repo_name: Optional[str], since: str) -> list[TextContent]:
    """Get git commits from a specific repository."""
    if not repo_name:
        return [TextContent(type="text", text="Error: repo_name is required")]
    
    if not REPO_DICT:
        return [TextContent(type="text", text="No repositories configured")]
    
    if repo_name not in REPO_DICT:
        available = ", ".join(REPO_DICT.keys())
        return [TextContent(
            type="text",
            text=f"Repository '{repo_name}' not found.\n\nAvailable repositories: {available}"
        )]
    
    repo_path = REPO_DICT[repo_name]
    
    try:
        cmd = [
            "git", "log",
            f"--author={AUTHOR_NAME}",
            "--no-merges",
            f"--since={since}",
            "--pretty=format:%h - %s (%cr)"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout.strip()
        return [TextContent(
            type="text",
            text=f"Git commits from '{repo_name}' ({repo_path}):\n\n{output if output else 'No commits found'}"
        )]
    
    except subprocess.CalledProcessError as e:
        return [TextContent(type="text", text=f"Git error for '{repo_name}': {e.stderr}")]


async def get_git_log_all_repos(since: str) -> list[TextContent]:
    """Get git commits from all configured repositories."""
    if not REPO_DICT:
        return [TextContent(type="text", text="No repositories configured")]
    
    all_output = f"Git commits from all repositories ({since}):\n\n"
    all_output += "="*60 + "\n\n"
    
    total_commits = 0
    
    for repo_name, repo_path in REPO_DICT.items():
        try:
            cmd = [
                "git", "log",
                f"--author={AUTHOR_NAME}",
                "--no-merges",
                f"--since={since}",
                "--pretty=format:%h - %s (%cr)"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout.strip()
            commit_count = len(output.split('\n')) if output else 0
            total_commits += commit_count
            
            all_output += f"## {repo_name}\n"
            all_output += f"Path: {repo_path}\n"
            all_output += f"Commits: {commit_count}\n\n"
            
            if output:
                all_output += output + "\n\n"
            else:
                all_output += "No commits found\n\n"
            
            all_output += "-"*60 + "\n\n"
        
        except subprocess.CalledProcessError as e:
            all_output += f"## {repo_name}\n"
            all_output += f"Error: {e.stderr}\n\n"
            all_output += "-"*60 + "\n\n"
    
    all_output += f"Total commits across all repositories: {total_commits}"
    
    return [TextContent(type="text", text=all_output)]


async def read_cv() -> list[TextContent]:
    """Read the current CV file."""
    cv_path = Path(REPO_PATH) / "cv.tex"
    
    if not cv_path.exists():
        return [TextContent(type="text", text="CV file not found")]
    
    content = cv_path.read_text()
    return [TextContent(type="text", text=f"Current CV:\n\n{content}")]


async def read_wins() -> list[TextContent]:
    """Read the wins.md file."""
    wins_path = Path(REPO_PATH) / "wins.md"
    
    if not wins_path.exists():
        return [TextContent(type="text", text="No wins.md found")]
    
    content = wins_path.read_text()
    return [TextContent(type="text", text=f"Achievements:\n\n{content}")]


async def get_jira_tickets(since: str, status: str) -> list[TextContent]:
    """Get Jira tickets."""
    if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
        return [TextContent(
            type="text",
            text="Jira credentials not configured. Set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN"
        )]
    
    try:
        # Parse date
        since_date = parse_time_range(since)
        date_str = since_date.strftime("%Y-%m-%d")
        
        # Build JQL query
        jql = f'assignee = "{JIRA_USER or JIRA_EMAIL}" AND status = "{status}" AND updated >= "{date_str}" ORDER BY updated DESC'
        
        # Create auth header
        auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        # Make request
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{JIRA_URL}/rest/api/3/search",
                params={"jql": jql, "maxResults": 100},
                headers={
                    "Authorization": f"Basic {auth_b64}",
                    "Accept": "application/json"
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
        
        # Format tickets
        tickets = []
        for issue in data.get("issues", []):
            key = issue["key"]
            summary = issue["fields"]["summary"]
            issue_type = issue["fields"]["issuetype"]["name"]
            status = issue["fields"]["status"]["name"]
            tickets.append(f"{key} - {summary} [{issue_type}] ({status})")
        
        output = "\n".join(tickets) if tickets else "No tickets found"
        return [TextContent(
            type="text",
            text=f"Jira Tickets ({len(tickets)}):\n\n{output}"
        )]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Jira API Error: {str(e)}")]


async def get_credly_badges(limit: int) -> list[TextContent]:
    """Get Credly badges."""
    if not CREDLY_USER_ID:
        return [TextContent(
            type="text",
            text="Credly user ID not configured. Set CREDLY_USER_ID"
        )]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.credly.com/users/{CREDLY_USER_ID}/badges.json",
                params={"page": 1, "per_page": limit},
                headers={"Accept": "application/json"},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
        
        # Format badges
        badges = []
        for badge in data.get("data", []):
            name = badge["badge_template"]["name"]
            
            # Extract issuer
            issuer = "Unknown Issuer"
            if badge.get("badge_template", {}).get("issuer", {}).get("entities"):
                entities = badge["badge_template"]["issuer"]["entities"]
                if entities and entities[0].get("entity", {}).get("name"):
                    issuer = entities[0]["entity"]["name"]
            
            # Format date
            issued_at = badge.get("issued_at", "")
            if issued_at:
                date_obj = datetime.fromisoformat(issued_at.replace('Z', '+00:00'))
                date_str = date_obj.strftime("%b %Y")
            else:
                date_str = "Unknown"
            
            # Check expiry
            expires_at = badge.get("expires_at")
            expiry_str = ""
            if expires_at:
                exp_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                expiry_str = f" (Expires: {exp_date.strftime('%b %Y')})"
            
            badges.append(f"{name} - {issuer} ({date_str}){expiry_str}")
        
        # Sort by date (newest first)
        badges.sort(reverse=True)
        
        output = "\n".join(badges) if badges else "No badges found"
        return [TextContent(
            type="text",
            text=f"Credly Badges ({len(badges)}):\n\n{output}"
        )]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Credly API Error: {str(e)}")]


async def get_linkedin_profile() -> list[TextContent]:
    """Get LinkedIn profile (limited due to LinkedIn restrictions)."""
    if not LINKEDIN_PROFILE_URL:
        return [TextContent(
            type="text",
            text="LinkedIn profile URL not configured. Set LINKEDIN_PROFILE_URL"
        )]
    
    output = f"""LinkedIn Profile Summary:

Profile URL: {LINKEDIN_PROFILE_URL}

Note: LinkedIn restricts automated access to profiles. For best results:
1. Ensure your profile is set to public
2. Manually copy key achievements to wins.md
3. Or use LinkedIn's official API with proper authentication

Alternative: Create a linkedin.md file with your profile summary, recent posts, and achievements."""
    
    return [TextContent(type="text", text=output)]


async def get_cv_guidelines() -> list[TextContent]:
    """Get CV formatting guidelines."""
    guidelines = f"""CV Formatting Guidelines:

IMPORTANT: When generating or updating CV content, follow these rules:

1. **Maximum Bullet Points**: {MAX_BULLETS_PER_EXPERIENCE} bullet points per experience/role
2. **Focus on Impact**: Prioritize achievements with quantifiable results
3. **Format**: Use \\textbf{{}} for emphasis on key terms
4. **Metrics**: Include specific numbers, percentages, or time savings
5. **Action Verbs**: Start each bullet with strong action verbs (Engineered, Designed, Implemented, etc.)
6. **Relevance**: Select the most impactful and recent achievements

When asked to update a CV:
- Analyze all available data (git commits, Jira tickets, Credly badges, wins)
- Identify the top {MAX_BULLETS_PER_EXPERIENCE} most significant achievements
- Format them as LaTeX bullet points
- Ensure each bullet demonstrates clear business value

Configuration:
- MAX_BULLETS_PER_EXPERIENCE: {MAX_BULLETS_PER_EXPERIENCE}
- This can be customized via MAX_BULLETS_PER_EXPERIENCE environment variable"""
    
    return [TextContent(type="text", text=guidelines)]


async def parse_cv_pdf(pdf_path: Optional[str]) -> list[TextContent]:
    """Parse a PDF CV file."""
    if not pdf_path:
        return [TextContent(type="text", text="Error: pdfPath parameter is required")]
    
    # Resolve path
    if pdf_path.startswith('/'):
        resolved_path = Path(pdf_path)
    else:
        resolved_path = Path(REPO_PATH) / pdf_path
    
    if not resolved_path.exists():
        return [TextContent(type="text", text=f"PDF file not found: {resolved_path}")]
    
    try:
        # Parse PDF
        reader = pypdf.PdfReader(str(resolved_path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        output = f"""PDF CV Parsed Successfully:

File: {pdf_path}
Pages: {len(reader.pages)} pages
Text Length: {len(text)} characters

--- EXTRACTED CONTENT ---

{text}

--- END OF CONTENT ---

This content can now be used to generate an enhanced CV with recent work data."""
        
        return [TextContent(type="text", text=output)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"PDF parsing error: {str(e)}")]


async def generate_enhanced_cv(existing_cv_path: Optional[str], since: str) -> list[TextContent]:
    """Generate enhanced CV combining all data sources."""
    if not existing_cv_path:
        return [TextContent(type="text", text="Error: existingCvPath parameter is required")]
    
    # Resolve path
    if existing_cv_path.startswith('/'):
        resolved_path = Path(existing_cv_path)
    else:
        resolved_path = Path(REPO_PATH) / existing_cv_path
    
    if not resolved_path.exists():
        return [TextContent(type="text", text=f"CV file not found: {resolved_path}")]
    
    try:
        # Step 1: Parse existing CV
        if resolved_path.suffix.lower() == '.pdf':
            reader = pypdf.PdfReader(str(resolved_path))
            existing_content = ""
            for page in reader.pages:
                existing_content += page.extract_text() + "\n"
        else:
            existing_content = resolved_path.read_text()
        
        # Step 2: Gather all data sources
        data_sections = []
        
        # Git commits
        git_result = await get_git_log(since)
        data_sections.append(f"\n## Git Commits ({since}):\n{git_result[0].text}")
        
        # Wins
        wins_result = await read_wins()
        data_sections.append(f"\n## Achievements (wins.md):\n{wins_result[0].text}")
        
        # Jira tickets
        if all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
            jira_result = await get_jira_tickets(since, "Done")
            data_sections.append(f"\n{jira_result[0].text}")
        else:
            data_sections.append("\n## Jira Tickets: Not configured")
        
        # Credly badges
        if CREDLY_USER_ID:
            credly_result = await get_credly_badges(50)
            data_sections.append(f"\n{credly_result[0].text}")
        else:
            data_sections.append("\n## Credly Badges: Not configured")
        
        # LinkedIn
        if LINKEDIN_PROFILE_URL:
            data_sections.append(f"\n## LinkedIn Profile: {LINKEDIN_PROFILE_URL}\n(Manual review recommended)")
        
        # Step 3: Compile report
        truncated_cv = existing_content[:2000]
        if len(existing_content) > 2000:
            truncated_cv += "\n... (truncated, full content available)"
        
        report = f"""# Enhanced CV Generation Report

## Existing CV Content:
{truncated_cv}

## Recent Work & Achievements ({since}):
{''.join(data_sections)}

---

## CV Guidelines:
- Maximum {MAX_BULLETS_PER_EXPERIENCE} bullet points per experience
- Focus on quantifiable impact and results
- Use action verbs (Engineered, Designed, Implemented, Led, etc.)
- Include metrics (percentages, time savings, scale)

## Next Steps:
1. Review the existing CV content above
2. Analyze the recent work data (git commits, Jira tickets, badges)
3. Identify the top {MAX_BULLETS_PER_EXPERIENCE} most impactful achievements
4. Generate enhanced CV bullet points in LaTeX format
5. Ensure each bullet demonstrates clear business value

## Suggested Approach:
Ask the AI to:
"Based on the above data, generate {MAX_BULLETS_PER_EXPERIENCE} enhanced CV bullet points in LaTeX format that highlight my most significant recent achievements with quantifiable results."
"""
        
        return [TextContent(type="text", text=report)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Enhanced CV generation error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
