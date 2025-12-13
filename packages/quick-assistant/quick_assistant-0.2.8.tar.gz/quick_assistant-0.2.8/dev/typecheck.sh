#!/bin/bash

# Type check script for quick-assistant project
# Uses mypy for static type checking

set -e  # Exit on any error

echo "󰅱 Running type checks with mypy..."

# Ensure mypy is in dev dependencies
if ! uv tree | grep -q "mypy"; then
    echo "󰏖 mypy not found in dependencies. Adding..."
    uv add --dev mypy
fi

# Run mypy on the src directory
uv run mypy src/ --ignore-missing-imports

echo "󰄬 Type checking completed successfully!"