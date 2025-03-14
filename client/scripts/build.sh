#!/bin/bash
set -e  # Exit immediately on error

# Get the script's directory and navigate to the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT/client/src"

GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -o ../builds/alloyupdater-windows-amd64.exe .
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o ../builds/alloyupdater-linux-amd64 .
