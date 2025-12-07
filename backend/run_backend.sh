#!/usr/bin/env bash
set -e

echo "Starting Stonebranch UAC backend (FastAPI)..."

# 1) Set UAC_URL if not already set
: "${UAC_URL:=https://atlantacyclic.stonebranchdev.cloud/}"
export UAC_URL

# 2) Ensure UAC_TOKEN exists, but DO NOT hardcode it
if [ -z "$UAC_TOKEN" ]; then
  echo "UAC_TOKEN is not set in the environment."
  # Optional: securely prompt for it
  read -s -p "Enter UAC Personal Access Token (will not be shown): " UAC_TOKEN
  echo
  export UAC_TOKEN
fi

# 3) Install deps (optional, can comment out after first run)
if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies..."
  pip install -r requirements.txt
fi

# 4) Run FastAPI with uvicorn
echo "Using UAC_URL=$UAC_URL"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
