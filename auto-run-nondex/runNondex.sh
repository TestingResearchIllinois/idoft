#!/bin/bash
DIR="${PWD}"
nondex_version="2.1.1" #LST version

runNondex () {
    #get the modules
    cd $1
    mvn install -DskipTests
    mvn -Dexec.executable='echo' -Dexec.args='${project.artifactId}' exec:exec -q -fn | tee modnames
    if grep -q "[ERROR]" modnames; then
        echo "ERROR: There are errors in the project"
        exit 1
    else
        echo "No errors detected"
    fi

    mkdir .runNondex
    mkdir ./.runNondex/modulelog


    # run nondex on each module
    input="modnames"
    while IFS= read -r line
    do
        mvn edu.illinois:nondex-maven-plugin:$nondex_version:nondex -pl :$line -Dlicense.skip -Drat.skip --fail-at-end | tee ./.runNondex/modulelog/$line.log
    done < "$input"
    grep -rnil "There are test failures" ./.runNondex/modulelog/* | tee ./.runNondex/result

    # format the result
    input=".runNondex/result"
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
