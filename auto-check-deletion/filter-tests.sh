#!/bin/bash

cd ..

pr_data=$(<pr-data.csv);

cd auto-check-deletion/

for item in "$@"; do
	pr_data=$(printf "$pr_data" | grep "$item");
done

formatted_data=$(printf "$pr_data" | cut -d',' -f 4,8)

echo "${formatted_data}"; 

printf "$formatted_data" > filtered_tests.txt;