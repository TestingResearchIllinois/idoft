#!/bin/bash
DIR="${PWD}"
cd $1
mvn install -DskipTests
mvn -Dexec.executable='echo' -Dexec.args='${project.artifactId}' exec:exec -q -fn | tee modnames
mkdir .runNondex
mkdir ./.runNondex/LOGSSS
input="modnames"
while IFS= read -r line
do
    mvn edu.illinois:nondex-maven-plugin:1.1.2:nondex -pl :$line -Dlicense.skip=true | tee ./.runNondex/LOGSSS/$line.log
done < "$input"
grep -rnil "There are test failures" ./.runNondex/LOGSSS/* | tee ./.runNondex/LOGresult
input=".runNondex/LOGresult"
while IFS= read -r line
do
    grep "test_results.html" $line | tee ./.runNondex/htmlOutput
done < "$input"
if [ -e $1/.runNondex/htmlOutput ]
then
    python3 $DIR/showmarkdown.py $1/.runNondex/htmlOutput
else
    echo "No flaky tests detected"
fi
