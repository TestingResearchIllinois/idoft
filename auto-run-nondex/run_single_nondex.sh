#!/bin/bash

output_file="logs/test1/single-run-final-output.log"
nondex_runs="1"
nondex_seed="974622"
test="cn.crane4j.core.util.ObjectUtilsTest#get"
error_message="Failed tests:   get(cn.crane4j.core.util.ObjectUtilsTest): expected"
module="crane4j-core"

> "$output_file"

for i in {1..10}
do
   temp_log="logs/test1/test1_log_${i}_$(date +%s).log"
   mvn -pl $module edu.illinois:nondex-maven-plugin:2.1.1:nondex -DnondexRuns=$nondex_runs -DnondexSeed=$nondex_seed -Dtest=$test 2>&1 | tee "$temp_log"

   if grep -q "$error_message" "$temp_log"; then
       echo "Run $i : $(grep "$error_message" "$temp_log")" >> "$output_file"
   else
       echo "Run $i : tests did not fail : $temp_log" >> "$output_file"
   fi

   sleep 1
done

# chmod +x run_single.sh
# ./run_single.sh
