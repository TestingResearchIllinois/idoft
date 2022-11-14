#!/bin/bash

echo "Started Execution"

test_module=$1
test_case=$2

echo "Started Build"
mvn clean install -pl $test_module -am -DskipTests -Dlicense.skip
if [[ "$?" -ne 0 ]]; then
  echo "Build Failed"
  exit 1
else
  mvn -pl $test_module edu.illinois:nondex-maven-plugin:1.1.2:nondex -Dtest=$test_case -DnondexRuns=5 -Dlicense.skip=true
  if [[ "$?" -ne 0 ]]; then
    echo "NonDex Test Failed"
    exit 0
  else
    exit 1
  fi
fi

exit 0
