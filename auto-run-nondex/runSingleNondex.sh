#!/bin/bash

DIR="${PWD}"
nondex_version="2.1.1"

if [[ $1 == "" ]] || [[ $2 == "" ]] || [[ $3 == "" ]] || [[ $4 == "" ]] || [[ $5 == "" ]] || [[ $6 == "" ]]; then
    echo "arg1 - Project Path"
    echo "arg2 - Module"
    echo "arg3 - Fully-Qualified Test Name (NOTE: packageName.ClassName#methodName with # before methodName)"
    echo "arg4 - Number of nondex_runs"
    echo "arg5 - Value for nondex_seed"
    echo "arg6 - Number of rounds running the same test"
    exit 1
fi


runsingleNondex () {
    DIR="${PWD}"
    
    PROJ_PATH=$1
    MODULE_PATH=$2
    TEST_NAME=$3
    NONDEX_RUNS=$4
    NONDEX_SEED=$5
    ROUNDS=$6

    ## The parameters below can be uncommented to be used without using CLI.

    # PROJ_PATH=
    # MODULE_PATH="pinot-core"
    # TEST_NAME="org.apache.pinot.queries.ExplainPlanQueriesTest#testSelect"
    # NONDEX_RUNS="1"
    # NONDEX_SEED=""
    # ROUNDS="10"

    error_count=0
    error_message="[ERROR] Tests run:"
    output_file="$DIR/.runNondex/singleLogs/single-run-$TEST_NAME.log"

    cd $PROJ_PATH
    mkdir .runNondex
    mkdir ./.runNondex/singleLogs


    > "$output_file"
    

    for i in {1..{$ROUNDS}}
    do
        temp_log="$DIR/.runNondex/singleLogs/round${i}_$(date +%s).log"
        
        mvn clean install -pl $MODULE_PATH -am -DskipTests | tee "$temp_log"
        mvn -pl $MODULE_PATH edu.illinois:nondex-maven-plugin:$nondex_version:nondex -DnondexRuns=$nondex_runs -DnondexSeed=$nondex_seed -Dtest=$test 2>&1 | tee "$temp_log"

        if grep -q "$error_message" "$temp_log"; then
            echo "Round $i : $(grep "$error_message" "$temp_log")" >> "$output_file"
            echo "Round $i : Instances of found - $(grep -o "$error_message" "$temp_log" | wc -l)" >> "$output_file"
            error_count=$((error_count++))
        else
            echo "Round $i : tests did not fail : $temp_log" >> "$output_file"
        fi

        sleep 1
    done
    
    echo "Total Error Rounds: $error_count" >> "$output_file"
    echo "Total Rounds: $ROUNDS" >> "$output_file"

    if [ $error_count -eq 0 ]; then
        echo "All rounds passed. " >> "$output_file"
    elif [ $error_count -eq $ROUNDS ]; then
        echo "All rounds failed. Likely Implementation Dependent (ID) Flaky test." >> "$output_file"
    else
        echo "Some rounds failed. Likely Not Implementation Dependent (NID) Flaky test." >> "$output_file"
    fi
}

