#!/bin/bash

mvn_options=""
nondex_version=""
flaky_commit=""
fixed_commit=""
test_module=""
test_case=""

while [[ $# -gt 0 ]]; do
  case "$1" in
  '--flaky') flaky_commit="$2"; shift 2 ;;
  '--fixed') fixed_commit="$2"; shift 2 ;;
  '--module') test_module="$2"; shift 2 ;;
  '--test') test_case="$2"; shift 2 ;;
  '--nondex-version') nondex_version="$2"; shift 2 ;;
  '--mvn-install') mvn_options="$2"; shift 2 ;;
  *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

echo "Flaky Commit: $flaky_commit"
echo "Fixed Commit: $fixed_commit"
echo "Test Module: $test_module"
echo "Test Case: $test_case"
echo "NonDex Version: $nondex_version"
echo "Maven Options: $mvn_options"

if [[ -z "$flaky_commit" || -z "$fixed_commit" || -z "$test_module" || -z "$test_case" || -z "$nondex_version" ]]; then
  echo "Error: Missing required argument(s)."
  exit 1
fi

git checkout $fixed_commit

git bisect start

git bisect bad

git checkout $flaky_commit

git bisect good

git bisect run ./git-bisect-script.sh $test_module $test_case "$nondex_version" "$mvn_options"
