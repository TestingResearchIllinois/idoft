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

OUTPUT_FILE="batch_output.log"
> "$OUTPUT_FILE" # Clear the file at the start of each run

echo "Processing batch input from $BATCH_FILE ..." | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"

while IFS= read -r line; do
    # Skip empty lines or lines starting with '#'
    if [[ -z "$line" || "$line" =~ ^# ]]; then
        continue
    fi
    
    # Extract parameters from the line
    FUNCTION_NAME=$(echo "$line" | awk '{print $1}')
    FILENAME=$(echo "$line" | awk '{print $2}')
    START_COMMIT=$(echo "$line" | awk '{print $3}')

    if [ -z "$FUNCTION_NAME" ] || [ -z "$FILENAME" ] || [ -z "$START_COMMIT" ]; then
        echo "Skipping malformed line: $line" | tee -a "$OUTPUT_FILE"
        continue
    fi

    echo "----------------------------------------" | tee -a "$OUTPUT_FILE"
    echo "Checking for function renames or file renames/moves for:" | tee -a "$OUTPUT_FILE"
    echo "FUNCTION_NAME: $FUNCTION_NAME" | tee -a "$OUTPUT_FILE"
    echo "FILENAME:      $FILENAME" | tee -a "$OUTPUT_FILE"
    echo "START_COMMIT:  $START_COMMIT" | tee -a "$OUTPUT_FILE"
    echo "----------------------------------------" | tee -a "$OUTPUT_FILE"

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
        -- "$FILENAME" >> "$OUTPUT_FILE"

    echo | tee -a "$OUTPUT_FILE"
done < "$BATCH_FILE"

echo "All results have been logged to $OUTPUT_FILE."