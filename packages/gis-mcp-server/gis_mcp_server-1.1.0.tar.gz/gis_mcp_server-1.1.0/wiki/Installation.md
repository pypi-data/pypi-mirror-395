# Installation

This guide will help you install the GIS MCP Server on your system.

## Prerequisites

Before installing the GIS MCP Server, ensure you have the following:

- **Python 3.11 or higher**: The server requires Python 3.11+. You can check your Python version with:
  ```bash
  python --version
  ```

- **pip or uv**: A package manager for Python packages
  - `pip` is usually included with Python
  - `uv` is a faster alternative package manager (recommended for Claude Desktop integration)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

The easiest way to install the GIS MCP Server is directly from PyPI:

```bash
pip install gis-mcp-server
```

This will install the latest stable release along with all required dependencies.

### Method 2: Install from Source

If you want to contribute to development or use the latest unreleased features:

1. Clone the repository:
   ```bash
   git clone https://github.com/matbel91765/gis-mcp-server
   cd gis-mcp-server
   ```

2. Install in editable mode:
   ```bash
   pip install -e .
   ```

This installs the package in development mode, allowing you to make changes to the source code that will be immediately reflected without reinstalling.

### Method 3: Using uvx for Claude Desktop

For Claude Desktop users, the recommended approach is to use `uvx`, which provides better integration and automatic environment management:

1. First, ensure you have `uv` installed:
   ```bash
   pip install uv
   ```

2. Configure Claude Desktop to use the GIS MCP Server by adding to your Claude Desktop configuration:
   ```json
   {
     "mcpServers": {
       "gis-mcp-server": {
         "command": "uvx",
         "args": ["gis-mcp-server"]
       }
     }
   }
   ```

3. Restart Claude Desktop to activate the server.

The `uvx` command will automatically manage the Python environment and dependencies, ensuring a clean installation isolated from your system Python.

## Verify Installation

After installation, verify that the GIS MCP Server is properly installed:

```bash
python -m gis_mcp_server --version
```

Or if installed via pip/uvx:

```bash
gis-mcp-server --version
```

You should see the version number displayed, confirming successful installation.

## Common Installation Issues and Solutions

### Issue: Python Version Too Old

**Error**: `Python 3.11 or higher is required`

**Solution**: Upgrade your Python installation to version 3.11 or higher. Download the latest version from [python.org](https://www.python.org/downloads/).

### Issue: pip Not Found

**Error**: `pip: command not found`

**Solution**:
- On Windows: Reinstall Python and ensure "Add Python to PATH" is checked
- On Linux/Mac: Install pip with `python -m ensurepip --upgrade`

### Issue: Permission Denied

**Error**: `Permission denied` or `Access is denied`

**Solution**:
- Install in user space: `pip install --user gis-mcp-server`
- Or use a virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install gis-mcp-server
  ```

### Issue: Dependency Conflicts

**Error**: Conflicts with existing packages

**Solution**: Use a virtual environment to isolate dependencies:
```bash
python -m venv gis-env
source gis-env/bin/activate  # On Windows: gis-env\Scripts\activate
pip install gis-mcp-server
```

### Issue: Module Not Found After Installation

**Error**: `ModuleNotFoundError: No module named 'gis_mcp_server'`

**Solution**:
- Ensure you're using the same Python environment where you installed the package
- Check installation with: `pip list | grep gis-mcp-server`
- Reinstall if necessary: `pip install --force-reinstall gis-mcp-server`

### Issue: uvx Command Not Found

**Error**: `uvx: command not found`

**Solution**:
- Install uv first: `pip install uv`
- Ensure your PATH includes the directory where uv is installed
- On Windows, you may need to restart your terminal

### Issue: Claude Desktop Not Detecting the Server

**Problem**: Server doesn't appear in Claude Desktop

**Solution**:
- Verify the configuration file syntax is correct (valid JSON)
- Check the configuration file location:
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Linux: `~/.config/Claude/claude_desktop_config.json`
- Restart Claude Desktop completely (quit and reopen)
- Check Claude Desktop logs for error messages

## Next Steps

After successful installation, proceed to the [Configuration](Configuration.md) guide to set up your GIS MCP Server for your specific use case.

For usage examples and available tools, see the [Usage Guide](Usage.md).
