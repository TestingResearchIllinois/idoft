#!/bin/bash

# This script takes a batch of (FUNCTION_NAME, FILENAME, START_COMMIT) sets from a file
# and identifies the commit where each function was modified.

# Usage:
# ./find_moved_or_renamed_commit_batch.sh <BATCH_FILE>
#
# The batch file should have one set of parameters per line, in the following format:
# FUNCTION_NAME FILENAME START_COMMIT

BATCH_FILE="$1"

if [ -z "$BATCH_FILE" ]; then
    echo "Usage: $0 <BATCH_FILE>"
    exit 1
fi

if [ ! -f "$BATCH_FILE" ]; then
    echo "Error: File '$BATCH_FILE' not found!"
    exit 1
fi

# Ensure we're in the root directory of the repository
cd "$(git rev-parse --show-toplevel)" || exit 1

echo "Processing batch input from $BATCH_FILE ..."
echo

while IFS= read -r line; do
    # Skip empty lines or lines starting with '#'
    if [[ -z "$line" || "$line" =~ ^# ]]; then
        continue
    fi
    
    # Extract parameters from line
    FUNCTION_NAME=$(echo "$line" | awk '{print $1}')
    FILENAME=$(echo "$line" | awk '{print $2}')
    START_COMMIT=$(echo "$line" | awk '{print $3}')

    if [ -z "$FUNCTION_NAME" ] || [ -z "$FILENAME" ] || [ -z "$START_COMMIT" ]; then
        echo "Skipping malformed line: $line"
        continue
    fi

    echo "----------------------------------------"
    echo "Checking for function renames or file renames/moves for:"
    echo "FUNCTION_NAME: $FUNCTION_NAME"
    echo "FILENAME:      $FILENAME"
    echo "START_COMMIT:  $START_COMMIT"
    echo "----------------------------------------"

    METHOD_REGEX="(public|protected|private|static|\\s)+\\s+.*\\s+$FUNCTION_NAME\\s*\\(.*\\)"

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

    echo
done < "$BATCH_FILE"
