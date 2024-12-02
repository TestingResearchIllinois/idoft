#!/bin/bash

filtered_tests=$(cat filtered_tests.txt | sed 's/,.*\//,/' | rev | cut -d'.' -f 1,2 | rev)

output_file='check-deletion-output.txt'
rm "$output_file"

echo "$filtered_tests" | while IFS=',' read -r test commit; do
    if [ -z "$test" ] || [ -z "$commit" ]; then
        continue
    fi

    echo "Processing test: $test with commit: $commit"

    class=$(printf "%s" "$test" | cut -d'.' -f 1)
    test_method=$(printf "%s" "$test" | cut -d'.' -f 2)
    git_show=$(git show "${commit::-1}")

    echo "==== deleted ${test} ? ====" 2>&1 | tee -a "$output_file"
    if echo "$git_show" | grep -q "^-.*${test_method}"; then
        echo "$git_show" | grep "^-.*${test_method}" |& tee -a "$output_file"
    else
        echo "Deleted method not found. Finding deleted test class." |& tee -a "$output_file"
        echo "$git_show" | grep "^-.*${class}" |& tee -a "$output_file"
    fi
done

echo "Output written to $output_file"