#!/bin/bash
DIR="${PWD}"
nondex_version="2.1.1"
java_version=$(java -version 2>&1 | sed -n ';s/.* version "\(.*\)\.\(.*\)\..*".*/\1\2/p;')
echo java_version "$java_version"
if [[ "$java_version" -ge 90 ]]; then
    echo java version is more than 1.9
else         
    echo java version is less than 1.9
fi
runNondex () {
    cd $1
    mvn install -DskipTests
    mvn -Dexec.executable='echo' -Dexec.args='${project.artifactId}' exec:exec -q -fn | tee modnames
    if grep -q "[ERROR]" modnames; then
        echo !!!!!
        exit 1
    else
        echo OK
    fi
    mkdir .runNondex
    mkdir ./.runNondex/LOGSSS_nondex:1.1.2
    input="modnames"
    while IFS= read -r line
    do
        mvn edu.illinois:nondex-maven-plugin:$nondex_version:nondex -pl :$line -Dlicense.skip=true | tee ./.runNondex/LOGSSS/$line.log
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
}

if [ ! "$2" ]
then
    runNondex $1
else
    for file in $1/$2/*
        do
            echo "start running nondex in module: $file"
            if test -d $file
            then
                runNondex.sh $file
            fi
        done
fi
