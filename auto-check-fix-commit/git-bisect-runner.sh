#!/bin/bash

set -euo pipefail  # Exit on error, undefined variables, and pipe failures

# Default values
flaky_commit=""
fixed_commit=""
test_module=""
test_case=""
nondex_version=""
mvn_options=""

# Usage function
usage() {
  cat << EOF
Usage: $0 --flaky <COMMIT> --fixed <COMMIT> --module <PATH> --test <TEST> --nondex-version <VERSION> [--mvn-install <OPTIONS>]

Required arguments:
  --flaky           Commit hash where the test was flaky
  --fixed           Commit hash where the test was fixed
  --module          Maven module path
  --test            Test case name
  --nondex-version  NonDex version to use

Optional arguments:
  --mvn-install     Additional Maven options (e.g., "-Dlicense.skip")

Example:
  $0 --flaky ecf41be2ecd007853c2db19e1c6a038cf356cb9e \
  --fixed f69557e325c5bb9e4e250bb0ec2db12d85298211 \
  --module pinot-core \
  --test org.apache.pinot.queries.ForwardIndexHandlerReloadQueriesTest#testSelectQueries \
  --nondex-version "2.1.7" \
  --mvn-install "-Dspotless.skip"
EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --flaky) flaky_commit="$2"; shift 2 ;;
    --fixed) fixed_commit="$2"; shift 2 ;;
    --module) test_module="$2"; shift 2 ;;
    --test) test_case="$2"; shift 2 ;;
    --nondex-version) nondex_version="$2"; shift 2 ;;
    --mvn-install) mvn_options="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Error: Unknown argument: $1"; usage ;;
  esac
done

# Validate required arguments and report missing ones
missing_args=()
[[ -z "$flaky_commit" ]] && missing_args+=("--flaky")
[[ -z "$fixed_commit" ]] && missing_args+=("--fixed")
[[ -z "$test_module" ]] && missing_args+=("--module")
[[ -z "$test_case" ]] && missing_args+=("--test")
[[ -z "$nondex_version" ]] && missing_args+=("--nondex-version")

if [[ ${#missing_args[@]} -gt 0 ]]; then
  echo "Error: Missing required argument(s): ${missing_args[*]}"
  echo ""
  usage
fi

# Display configuration
echo "=== Git Bisect Configuration ==="
echo "Flaky Commit:    $flaky_commit"
echo "Fixed Commit:    $fixed_commit"
echo "Test Module:     $test_module"
echo "Test Case:       $test_case"
echo "NonDex Version:  $nondex_version"
echo "Maven Options:   ${mvn_options:-<none>}"
echo "================================"
echo ""

# Verify git bisect script exists
if [[ ! -f "./git-bisect-script.sh" ]]; then
  echo "Error: git-bisect-script.sh not found in current directory"
  exit 1
fi

# Verify commits exist
if ! git rev-parse "$flaky_commit" >/dev/null 2>&1; then
  echo "Error: Flaky commit '$flaky_commit' not found"
  exit 1
fi

if ! git rev-parse "$fixed_commit" >/dev/null 2>&1; then
  echo "Error: Fixed commit '$fixed_commit' not found"
  exit 1
fi

# Clean up any previous bisect session
if git bisect log >/dev/null 2>&1; then
  echo "Warning: Previous bisect session found. Resetting..."
  git bisect reset
fi

# Start bisect process
echo "Starting git bisect..."

git checkout "$fixed_commit" || {
  echo "Error: Failed to checkout fixed commit"
  exit 1
}

git bisect start --term-old=flaky --term-new=non-flaky || {
  echo "Error: Failed to start bisect"
  exit 1
}

git bisect non-flaky || {
  echo "Error: Failed to mark commit as non-flaky"
  git bisect reset
  exit 1
}

git checkout "$flaky_commit" || {
  echo "Error: Failed to checkout flaky commit"
  git bisect reset
  exit 1
}

git bisect flaky || {
  echo "Error: Failed to mark commit as flaky"
  git bisect reset
  exit 1
}

# Run bisect with the test script
echo "Running bisect to find the fix commit..."
git bisect run ./git-bisect-script.sh "$test_module" "$test_case" "$nondex_version" "$mvn_options"

# Capture bisect result
bisect_exit_code=$?

echo ""
echo "=== Bisect Complete ==="
if [[ $bisect_exit_code -eq 0 ]]; then
  echo "Successfully identified the commit that fixed the flaky test"
else
  echo "Bisect completed with exit code: $bisect_exit_code"
fi

# Show bisect log
echo ""
echo "=== Bisect Log ==="
git bisect log

# Reset bisect
echo ""
echo "Resetting bisect session..."
git bisect reset

exit $bisect_exit_code
