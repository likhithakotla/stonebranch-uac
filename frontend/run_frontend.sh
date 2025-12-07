#!/usr/bin/env bash
set -e

echo "Starting frontend (static HTML/JS)..."

PORT=9000

# Optionally install nothing: frontend is pure static files.
# Just run Python's built-in HTTP server:
python -m http.server "$PORT" --bind 127.0.0.1
