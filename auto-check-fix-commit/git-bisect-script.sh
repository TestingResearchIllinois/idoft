#!/bin/bash

set -uo pipefail  # Exit on undefined variables and pipe failures

# Parse arguments
test_module="$1"
test_case="$2"
nondex_version="$3"
mvn_options="${4:-}"  # Optional, default to empty

# Log current commit being tested
echo "=== Testing Commit: $(git rev-parse --short HEAD) ==="
echo "Commit: $(git log -1 --oneline)"
echo ""

# Build the project
echo "Starting build..."
if ! mvn clean install -pl "$test_module" -am -DskipTests -Dlicense.skip $mvn_options; then
  echo "Build Failed - Cannot determine if test is flaky"
  exit 125  # Git bisect special code: skip this commit
fi

echo "Build successful"
echo ""

# Run NonDex test
echo "Running NonDex test..."
if ! mvn -pl "$test_module" edu.illinois:nondex-maven-plugin:"$nondex_version":nondex \
     -Dtest="$test_case" -DnondexRuns=5 -Dlicense.skip=true $mvn_options; then
  echo "NonDex Test Failed - Test is FLAKY at this commit"
  exit 0  # Test is flaky (old state)
fi

echo "NonDex Test Passed - Test is NON-FLAKY at this commit"
exit 1  # Test is non-flaky (new state)
