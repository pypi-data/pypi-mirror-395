#!/bin/bash

# Format script for quick-assistant project
# Uses ruff for fast Python formatting

set -e  # Exit on any error

echo "Ä| Running formatter with ruff..."

# Ensure ruff is in dev dependencies
if ! uv tree | grep -q "ruff"; then
    echo "Ä÷ ruff not found in dependencies. Adding..."
    uv add --dev ruff
fi

# Run ruff format
echo "ÅS Formatting code..."
uv run ruff format src/

echo "Ä, Formatting completed successfully!"
