#!/usr/bin/env python3
"""Test script to verify the MCP server installation."""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.10+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   Python 3.10+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import mcp
        print("✅ mcp package installed")
    except ImportError:
        print("❌ mcp package not found")
        print("   Run: pip install mcp")
        return False
    
    try:
        import httpx
        print("✅ httpx package installed")
    except ImportError:
        print("❌ httpx package not found")
        print("   Run: pip install httpx")
        return False
    
    try:
        import pypdf
        print("✅ pypdf package installed")
    except ImportError:
        print("❌ pypdf package not found")
        print("   Run: pip install pypdf")
        return False
    
    return True


def check_git():
    """Check if git is available."""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ git not found")
        print("   Install git: https://git-scm.com/downloads")
        return False


def check_package():
    """Check if the package can be imported."""
    try:
        from cv_resume_builder_mcp import __version__
        print(f"✅ cv-resume-builder-mcp v{__version__} installed")
        return True
    except ImportError:
        print("❌ cv-resume-builder-mcp not installed")
        print("   Run: pip install -e .")
        return False


def main():
    """Run all checks."""
    print("🔍 Checking CV Resume Builder MCP installation...\n")
    
    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Git", check_git),
        ("Package", check_package),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! Installation is ready.")
        print("\nNext steps:")
        print("1. Configure your MCP client (Claude Desktop, Kiro, etc.)")
        print("2. Set environment variables (REPO_PATH, AUTHOR_NAME)")
        print("3. Restart your AI assistant")
        print("4. Test with: 'List available MCP tools'")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
