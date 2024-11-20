#!/bin/bash
set -e

# Checking if the git repo url is set
if [ -z "$REPO_URL" ]; then
  echo "Error: REPO_URL is not set. It is a required argument."
  exit 1
fi

echo "Cloning repository: $REPO_URL"
git clone "$REPO_URL" repo

cd repo

echo "Printing java version for reference"
java --version

# Initialize the Maven install command
MVN_INSTALL_CMD="mvn clean install -DskipTests"

# Add the -pl option if MODULE is provided
if [ -n "$MODULE" ]; then
  MVN_INSTALL_CMD="$MVN_INSTALL_CMD -pl $MODULE"
fi

# Output and execute the command
echo "Running 'mvn clean install' with command: $MVN_INSTALL_CMD"
eval $MVN_INSTALL_CMD

# Creating a directory for logs, volume mount to get onto your local
NONDEX_LOG_DIR=/app/nondex_logs
mkdir -p "$NONDEX_LOG_DIR"

# Building nondex command using the various options configured - eg. mvn -pl <module_path> edu.illinois:nondex-maven-plugin:2.1.7:nondex -Dtest="<tests>" --fail-never
NONDEX_CMD="mvn"

if [ -n "$MODULE" ]; then
  NONDEX_CMD="$NONDEX_CMD -pl $MODULE"
fi

NONDEX_CMD="$NONDEX_CMD edu.illinois:nondex-maven-plugin:2.1.7:nondex"

if [ -n "$TESTS" ]; then
  NONDEX_CMD="$NONDEX_CMD -Dtest=\"$TESTS\""
fi

if [ -n "$NONDEX_RUNS" ]; then
  NONDEX_CMD="$NONDEX_CMD -DnondexRuns=$NONDEX_RUNS"
fi

if [ "$RUN_NONDEX_WITH_FN" == "true" ]; then
  NONDEX_CMD="$NONDEX_CMD --fail-never"
fi

echo "Final NonDex command: $NONDEX_CMD"

NONDEX_LOG_FILE="$NONDEX_LOG_DIR/nondex-logs-$(date +%Y%m%d-%H%M%S).log"
NONDEX_FAILURE_FILE="$NONDEX_LOG_DIR/nondex-flaky-tests-$(date +%Y%m%d-%H%M%S).txt"

echo "Running the NonDex plugin. Logs will be saved to $NONDEX_LOG_FILE"
eval $NONDEX_CMD 2>&1 | tee "$NONDEX_LOG_FILE"

if [ ! -f "$NONDEX_LOG_FILE" ]; then
  echo "Error: NonDex log file not found at $NONDEX_LOG_FILE."
  echo "Listing all files in $NONDEX_LOG_DIR:"
  ls -R /app/nondex_logs
  exit 1
fi

# Scraping the nondex file to get flaky tests
echo "Processing NonDex log file: $NONDEX_LOG_FILE"

if grep -q "\[INFO\] Across all seeds:" "$NONDEX_LOG_FILE"; then
  # Extract failing tests
  awk '
  /\[INFO\] Across all seeds:/ { in_section=1; next }
  /\[INFO\] Test results can be found at:/ { in_section=0 }
  in_section && /^\[INFO\]/ { print substr($0, index($0, $5)) }
  ' "$NONDEX_LOG_FILE" | sort -u > "$NONDEX_FAILURE_FILE"
  
  if [ -s "$NONDEX_FAILURE_FILE" ]; then
    echo "Failing tests have been written to: $NONDEX_FAILURE_FILE"
  else
    echo "No failing tests were found in the NonDex log file."
    rm -f "$NONDEX_FAILURE_FILE"
  fi
else
  echo "No 'Across all seeds:' section found in the NonDex log file."
fi

