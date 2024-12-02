#!/bin/bash

input_file="test.txt"
output_file="output.txt"

if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' does not exist."
    exit 1
fi

> "$output_file"

while IFS= read -r line || [[ -n "$line" ]]; do
    echo "Processing line: $line" | tee -a "$output_file"

    IFS=',' read -r project_url sha module_path package_class_path _ <<< "$line"

    class_name=$(echo "$package_class_path" | awk -F '.' '{print $(NF-1)}')
    package_path=$(echo "$package_class_path" | awk -F '.' '{for (i=1; i<NF-1; i++) printf "%s/", $i; print ""}')
    current_file_path="$module_path/src/test/java/$package_path$class_name.java"

    # get the commit history of the file
    commits=$(git log --follow --format=%H -- "$current_file_path" 2>/dev/null)

    if [ -z "$commits" ]; then
        echo "No moved or rename found for Line: $line" | tee -a "$output_file"
        continue
    fi

    # for each commit, check if the file was moved
    found_moved_commit=false
    for commit in $commits; do
        rename_info=$(git show --name-status "$commit" | grep "^R" | grep "$current_file_path")

        if [ -n "$rename_info" ]; then
            new_path=$(echo "$rename_info" | awk '{print $3}')

            # ensure the new path exists in the commit, and it is different from the current path
            if [[ "$new_path" != "$current_file_path" ]] && git show "$commit:$new_path" &>/dev/null; then
                echo "File '$current_file_path' was moved or renamed in commit $commit:" | tee -a "$output_file"
                echo "From: $current_file_path" | tee -a "$output_file"
                echo "To: $new_path" | tee -a "$output_file"
                echo "Found moved or renamed for line: $line" | tee -a "$output_file"
                current_file_path=$new_path
                found_moved_commit=true
                break
            fi
        fi
    done

    if [ "$found_moved_commit" = false ]; then
        echo "No moved or rename found for Line: $line" | tee -a "$output_file"
    fi

    echo | tee -a "$output_file"

done < "$input_file"
