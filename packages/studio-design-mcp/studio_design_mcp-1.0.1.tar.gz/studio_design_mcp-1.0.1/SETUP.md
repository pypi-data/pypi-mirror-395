# Setup Guide

Complete setup instructions for Studio Design MCP server.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Installation](#2-installation)
3. [Configure MCP](#3-configure-mcp)
4. [Test Setup](#4-test-setup)
5. [Optional Configuration](#5-optional-configuration)
6. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

Check if you already have these installed:

```bash
# Check Git
git --version

# Check UV
uv --version
```

### Install Missing Prerequisites

**Git:**
- macOS: `brew install git`
- Windows: Download from https://git-scm.com/download/win

**UV Package Manager:**
- macOS: `brew install uv`
- Windows:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  ⚠️ After installing, add to PATH and restart terminal:
  ```powershell
  $env:Path = "C:\Users\$env:USERNAME\.local\bin;$env:Path"
  ```

**VS Code (Recommended):** Download from https://code.visualstudio.com/

---

## 2. Installation

### 2.1 Clone Repository

```bash
git clone https://github.com/gim-home/studio-8-design-agent.git
cd studio-8-design-agent
```

### 2.2 Install Dependencies and Playwright

```bash
# Install Python dependencies (creates virtual environment automatically)
uv sync

# Install Playwright browser
uv run playwright install chromium
```

---

## 3. Configure MCP

### 3.1 Create MCP Configuration

Create `.vscode/mcp.json` in the project directory:

```bash
mkdir -p .vscode
```

### 3.2 Add Configuration

Create `.vscode/mcp.json` with:

**macOS/Linux:**
```json
{
  "servers": {
    "studio-design-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        ".",
        "run",
        "-m",
        "src"
      ],
      "env": {}
    }
  }
}
```

**Windows:**
```json
{
  "servers": {
    "studio-design-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        ".",
        "run",
        "-m",
        "src"
      ],
      "env": {}
    }
  }
}
```

### 3.3 Open in VS Code

```bash
code .
```

---

## 4. Test Setup

1. Open VS Code in the project directory: `code .`
2. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
3. Type and select: **MCP: List Servers**
4. Verify "studio-design-mcp" appears in the list and is running

You can also test by opening GitHub Copilot Chat and trying:
```
Search Mobbin for Claude chat flow on web plartform.
```

---

## 5. Troubleshooting

### UV command not found (Windows)

Add UV to PATH and restart terminal:
```powershell
$env:Path = "C:\Users\$env:USERNAME\.local\bin;$env:Path"
```

### Playwright installation fails

Install manually:
```bash
uv run playwright install chromium
```

### MCP Server not connecting

**Checklist:**
- ✅ Restart VS Code after configuration changes
- ✅ Verify the MCP server runs successfully with `uv run -m src`
- ✅ Check VS Code Output panel for error messages

### Permission errors (macOS/Linux)

```bash
chmod +x .venv/bin/activate
```
