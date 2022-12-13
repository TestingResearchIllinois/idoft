#!/bin/bash
DIR="${PWD}"
echo $JAVA_Home
version="1.1.2"
read -p "Enter the nondex version you want run:(press 1 for nondex:1.1.2, press 2 for nondex:2.1.1)" name
case $name in
  1)
    version="1.1.2"
    echo "Chosen nondex:1.1.2"
    ;;
  2)
    version="2.1.1"
    echo "Chosen nondex:2.1.1"
    ;;
  *)
    echo "Default version is nondex:1.1.2"
esac

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
    mkdir ./.runNondex/LOGSSS
    input="modnames"
    while IFS= read -r line
    do
        mvn edu.illinois:nondex-maven-plugin:$version:nondex -pl :$line -Dlicense.skip=true | tee ./.runNondex/LOGSSS/$line.log
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
