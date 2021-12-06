input="./flaky_tests.csv"
while IFS=',' read MODULE TEST_CLASS TEST_NAME NONDEX_RUN_TIMES FIRST_FIX_SHA; do
        git checkout "$FIRST_FIX_SHA"
        (git rev-parse HEAD; mvn clean install -pl $MODULE -am -DskipTests; mvn -pl $MODULE edu.illinois:nondex-maven-plugin:1.1.2:nondex -Dtest="$TEST_CLASS#$TEST_NAME" -DnondexRuns=10) | tee first_fix_$TEST_NAME.log;
        git switch -;
        git checkout "$FIRST_FIX_SHA^";
        (git rev-parse HEAD; mvn clean install -pl $MODULE -am -DskipTests; mvn -pl $MODULE edu.illinois:nondex-maven-plugin:1.1.2:nondex -Dtest="$TEST_CLASS#$TEST_NAME" -DnondexRuns=10) | tee last_flaky_$TEST_NAME.log;
        git switch -;
done < $input