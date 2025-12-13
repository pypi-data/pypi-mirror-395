#!/bin/bash
set -e

DEST_DIR=".git/hooks"

if [ ! -d "$DEST_DIR" ]; then
    # This can happen in Package Builder Workers.
    echo "Skipping installation of hook - $DEST_DIR directory not found"
    exit 0
fi

SCRIPT_NAME="pre-commit"
SOURCE_PATH="hooks/$SCRIPT_NAME"

echo "Installing git hook to bump version"
cp -p "$SOURCE_PATH" "$DEST_DIR/$SCRIPT_NAME"
echo "Git hooks installed"
