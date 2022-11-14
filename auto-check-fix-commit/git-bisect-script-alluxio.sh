#!/bin/bash

echo "Start Execution"

echo "Start Build"
mvn clean install -pl core/server/worker -am -DskipTests -Dlicense.skip
if [[ "$?" -ne 0 ]]; then
  echo "Build Failed"
  exit 1
else
  mvn -pl core/server/worker edu.illinois:nondex-maven-plugin:1.1.2:nondex -Dtest=alluxio.worker.block.BlockLockManagerTest#lockAlreadyReadLockedBlock -DnondexRuns=5 -Dlicense.skip=true
  if [[ "$?" -ne 0 ]]; then
    echo "NonDex Test Failed"
    exit 0
  else
    exit 1
  fi
fi

exit 0
