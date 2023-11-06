#!/bin/bash

# Check if all required arguments are provided
if [ "$#" -ne 4 ]; then
  echo "Ensure that you are running the command from the repo root"
  echo "Usage: $0 <module_name> <commit_hash> <test_name> <test_class>"
  exit 1
fi

# Assign command-line arguments to variables
module_name="$1"
commit_hash="$2"
test_name="$3"
test_class="$4"

echo "Module Name: $module_name"
echo "Commit Hash: $commit_hash"
echo "Test Name: $test_name"
echo "Test Class: $test_class"

echo "Running tests for module '$module_name'"
echo "Executing test '$test_name' in the class '$test_class'."

current_dir="$(pwd)"

base_dir="$current_dir/$target/$test_name/logs"

echo "Running commands for $target:"
echo "base_dir/outdir: $base_dir"

# Create the directory if it doesn't exist
if [ ! -d "$base_dir" ]; then
    mkdir -p "$base_dir"
    echo "Created directory: $base_dir"
fi

echo "Checking out to specific commit"
git reset --hard "$commit_hash"

echo "Cleaning directory"
rm -rf "$base_dir"/*
echo "Doing a clean install"
mvn clean
echo "Installing module"

mvn install -pl "$module_name" -am -DskipTests |& tee "$base_dir/install.log"
if grep -q "BUILD SUCCESS" "$base_dir/install.log"; then
    echo "CHECKPOINT-MVN: mvn install succeeded"
    echo "Running test"

    mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false -Dtest="$test_class#$test_name" |& tee "$base_dir/normal_test_standalone.log"
    if grep -q "BUILD SUCCESS" "$base_dir/normal_test_standalone.log"; then
        echo "CHECKPOINT-TESTSTANDALONE: test passes individually running nondex"
        mvn -pl "$module_name" edu.illinois:nondex-maven-plugin:2.1.1:nondex -Dmaven.test.failure.ignore=false -Dtest="$test_class#$test_name" |& tee "$base_dir/nondex_simple.log"
        if grep -q "BUILD SUCCESS" "$base_dir/nondex_simple.log"; then
            echo "CHECKPOINT-NONDEXPASS: Test success with non-dex running with more runs"
            mvn -pl "$module_name" edu.illinois:nondex-maven-plugin:2.1.1:nondex -Dmaven.test.failure.ignore=false -Dtest="$test_class#$test_name" -DnondexRuns=50 |& tee "$base_dir/nondex_50runs.log"
            if grep -q "BUILD SUCCESS" "$base_dir/nondex_50runs.log"; then
                echo "CHECKPOINT-NONDEXPASS_50_RUNS: Test success with non-dex 50 runs attempting to run the full class for testing OD"

                for ((i = 1; i <= 4; i++)); do
                    mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false -Dtest="$test_class" | tee -a "$base_dir/test_class_4runs.log"
                done
                echo "Class level tests dumped in $base_dir/test_class_4runs.log"
                echo "CHECKPOINT CLASS: If current test fails at class level anytime, then we can conclude it as OD"

                echo "Running module level tests"

                for ((i = 1; i <= 10; i++)); do
                    mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false | tee -a "$base_dir/module_level_10runs.log"
                done
                echo "CHECKPOINT MODULE: Module level tests dumped in $base_dir/module_level_10runs.log"

                echo "Running test individually multiple times"
                for ((i = 1; i <= 10; i++)); do
                    mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false -Dtest="$test_class#$test_name" | tee -a "$base_dir/single_test_10runs.log"
                done
                echo "Individual tests dumped in $base_dir/single_test_10runs.log"
                
                echo "CHECKPOINT FINAL: Nondex has passed with 50 runs. Analyze the module,class and Individual level test logs for conclusion"
                exit 0
            else
                echo "CHECKPOINT FINAL: Failed on non-dex when the number of runs were increased but passed individually and with lower nondex runs. Test is likely ID"
                exit 0
            fi
        else
            echo "CHECKPOINT OD/NOD CHECK: Test passed once individually then failed on non-dex, checking for OD/NOD by running individually 20 times"
            fail_count=0

            for ((i = 1; i <= 20; i++)); do
                mvn -pl "$module_name" test -Dmaven.test.failure.ignorefalse -Dtest="$test_class#$test_name" | tee -a "$base_dir/single_test_20runs_idpath.log"
                if grep -qE "BUILD FAILED|BUILD FAILURE|BUILD FAIL" "$base_dir/single_test_20runs_idpath.log" ; then
                    ((fail_count++))
                    echo "CHECKPOINT OD/NOD STATUS: Failed"
                else
                    echo "CHECKPOINT OD/NOD STATUS: Passed"
                fi
            done

            if [ "$fail_count" -eq 0 ]; then
                echo "CHECKPOINT ID: Test fails non-dex, and passes normally always hence mostly ID"
                exit 0 
            else
                echo "CHECKPOINT OD: Test looks OD as it passes and fails sometimes, running at the class level to check for OD"
                fail_count=0

                for ((i = 1; i <= 4; i++)); do
                    mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false -Dtest="$test_class" | tee -a "$base_dir/test_class_4runs_nonidpath.log"
                done
                echo "Class level tests dumped in $base_dir/test_class_4runs_nonidpath.log"
                echo "CHECKPOINT CLASS: If current test fails at class level anytime, then we can conclude it as OD"

                echo "Running module level tests"
                
                for ((i = 1; i <= 10; i++)); do
                    mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false | tee -a "$base_dir/module_level_10runs.log"
                done

                echo "CHECKPOINT MODULE: module level tests dumped in $base_dir/module_level_10runs.log"
                echo "CHECKPOINT FINAL: Test has failed with Nondex and is failing independently sometimes. Analyze the module and class level test logs for OD/NOD"
            fi
        fi
    else 
        echo "Test fails normally, trying with a few more runs"
        fail_count=0

        for ((i = 1; i <= 10; i++)); do
            mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false -Dtest="$test_class#$test_name" | tee -a "$base_dir/single_test_10runs_nonidpath.log"
            if grep -qE "BUILD FAILED|BUILD FAILURE|BUILD FAIL"  "$base_dir/single_test_10runs_nonidpath.log"; then
                ((fail_count++))
                echo "CHECKPOINT TEST_FAILURE: Failed"
            else
                echo "CHECKPOINT TEST_PASSED: Passed"
            fi
        done

        if [ "$fail_count" -eq 10 ]; then
            echo "CHECKPOINT: Test always fails aborting"
            exit 0
        fi

        echo "Passing and failing sometimes looks NOD, checking at the class level"

        for ((i = 1; i <= 4; i++)); do
            mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false -Dtest="$test_class" | tee -a "$base_dir/test_class_4runs_nonidpath.log"
        done
        echo "Class level tests dumped in $base_dir/test_class_4runs_nonidpath.log"
        echo "CHECKPOINT CLASS: If current test passes at class level always, then we can conclude it as OD else it could be NOD"

        echo "Running Module level tests" 
        for ((i = 1; i <= 10; i++)); do
                mvn -pl "$module_name" test -Dmaven.test.failure.ignore=false | tee -a "$base_dir/module_level_10runs.log"
        done
        echo "Module level tests dumped in $base_dir/module_level_10runs.log"
        echo "CHECKPOINT MODULE: If current test passes at module level always, then we can conclude it as OD else it could be NOD"
    fi
else
    echo "mvn install failed aborting"
fi
