#!/bin/bash

# Lint script for quick-assistant project
# Uses ruff for fast Python linting and formatting

set -e  # Exit on any error

echo "󰃘 Running linting with ruff..."

# Ensure ruff is in dev dependencies
if ! uv tree | grep -q "ruff"; then
    echo "󰏖 ruff not found in dependencies. Adding..."
    uv add --dev ruff
fi

# Run ruff check for linting
echo "󰑓 Checking code style and potential issues..."
uv run ruff check src/

echo "󰄬 Linting completed successfully!"