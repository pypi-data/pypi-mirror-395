#!/bin/bash

# =============================================================================
# Development Watch Script for Quick Assistant
# =============================================================================
#
# DESCRIPTION:
#   Automatically watches for file changes in the Quick Assistant project and
#   updates the globally installed CLI tool by calling the build.sh script.
#   This enables rapid development by eliminating the need to manually 
#   reinstall the tool after every code change.
#
# FEATURES:
#   • Monitors source files (src/*.py) and configuration (pyproject.toml)
#   • Delegates build operations to dev/build.sh for consistency
#   • Provides clear visual feedback with status icons
#   • Skips initial install if tool is already present
#
# REQUIREMENTS:
#   • fswatch: File system event monitoring tool
#     - macOS: brew install fswatch
#     - Linux: apt-get install fswatch (or equivalent)
#   • dev/build.sh: Build script for CLI installation
#   • uv: Modern Python package manager
#
# USAGE:
#   ./dev/watch.sh
#
# MONITORED PATHS:
#   • src/          - All Python source files
#   • pyproject.toml - Project configuration and dependencies
#
# TROUBLESHOOTING:
#   • All build and installation logic is handled by dev/build.sh
#   • Press Ctrl+C to stop the watch process
#   • Check uv tool list to see current installation status
#
# =============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    echo "󰅖 fswatch is not installed. Please install it first:"
    echo "   macOS: brew install fswatch"
    echo "   Linux: apt-get install fswatch (or equivalent)"
    exit 1
fi

echo "󰍉 Development mode - watching for changes with fswatch..."
echo "󰈙 Monitoring: src/*.py, pyproject.toml"
echo "󰑓 Auto-updating global 'quick' command"
echo "󰜺 Press Ctrl+C to stop"
echo ""

# =============================================================================
# FUNCTION: install_cli
# =============================================================================
# Performs initial installation of the Quick Assistant CLI tool.
# 
# BEHAVIOR:
#   Delegates to the build.sh script which handles:
#   1. Cleanup of any existing installations
#   2. Fresh installation in editable mode
#   3. Retry logic for installation failures
#   4. Clear status reporting with icons
#
# PARAMETERS: None
# RETURNS: None
# =============================================================================
install_cli() {
    ./dev/build.sh
}

# Check if tool is already installed before attempting initial install
if uv tool list | grep -q "quick-assistant"; then
    echo "󰄬 quick-assistant already installed, skipping initial install"
    echo ""
else
    # Initial install
    install_cli
fi


# =============================================================================
# FUNCTION: update
# =============================================================================
# Updates the globally installed CLI tool when file changes are detected.
# This is the core function called by fswatch on every file modification.
#
# BEHAVIOR:
#   Delegates to the build.sh script which handles:
#   1. Cleanup of any corrupted installations
#   2. Fresh installation in editable mode
#   3. Retry logic for installation failures
#   4. Clear status reporting with icons
#
# PARAMETERS: None
# RETURNS: None
# =============================================================================
update() {
    echo "󰈙 Files changed, rebuilding CLI..."
    ./dev/build.sh
}

# =============================================================================
# MAIN WATCH LOOP
# =============================================================================
# Starts the file system monitoring using fswatch and triggers updates
# whenever changes are detected in the monitored paths.
#
# FSWATCH OPTIONS:
#   -o    : Print only the number of events (optimized for scripts)
#
# MONITORED PATHS:
#   src/          : All Python source code files
#   pyproject.toml: Project configuration and dependencies
#
# LOOP BEHAVIOR:
#   • Runs indefinitely until interrupted (Ctrl+C)
#   • Each file change event triggers update()
#   • Events are batched by fswatch to prevent excessive rebuilds
# =============================================================================
fswatch -o src/ pyproject.toml | while read; do
    update
done