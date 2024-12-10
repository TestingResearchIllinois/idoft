#!/bin/bash

# This script identifies the commit where a specified function was modified,
# starting from a given commit, and handles cases where the function or file
# might have been renamed or moved.

# Usage:
# ./find_moved_or_renamed_commit.sh <FUNCTION_NAME> <FILENAME> <START_COMMIT>

# Parameters:
FUNCTION_NAME="$1"
FILENAME="$2"   # Relative Path
START_COMMIT="$3"

if [ -z "$FUNCTION_NAME" ] || [ -z "$FILENAME" ] || [ -z "$START_COMMIT" ]; then
    echo "Usage: $0 <FUNCTION_NAME> <FILENAME> <START_COMMIT>"
    exit 1
fi

# Ensure we're in the root directory of the repository
cd "$(git rev-parse --show-toplevel)"

METHOD_REGEX="(public|protected|private|static|\s)+\s+.*\s+$FUNCTION_NAME\s*\(.*\)"

echo "Checking for function renames or file renames/moves..."

# Track file renames: See commits where the file was renamed.
# Track function changes: See commits where the function was modified, or removed.
git log "$START_COMMIT"..HEAD \
    --follow \
    --find-renames \
    -G"$METHOD_REGEX" \
    -p \
    --name-status \
    --reverse \
    --color \
    --decorate \
    -- "$FILENAME" | less -R