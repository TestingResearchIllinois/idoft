#!/bin/bash

filtered_tests=$(cat filtered_tests.txt | sed 's/,.*\//,/' | rev | cut -d'.' -f 1,2 | rev);

output_file='check-deletion-output.txt';

# Check the file is exists or not
if [ -f $output_file ]; then
   rm check-deletion-output.txt;
fi

IFS=','

printf "$filtered_tests" | while read line;
do 
	read -a split_line <<< $line
	test=${split_line[0]};
	commit=${split_line[1]};
	commit=$(printf "$commit");
	class=$(printf "$test" | cut -d'.' -f 1);
	test_method=$(printf "$test" | cut -d'.' -f 2);
	git_show=$(git show "${commit::-1}");
	echo ==== deleted ${test} ? ==== |& tee -a $output_file;
	if echo "$git_show" | grep -q "^-.*${test_method}"
	then
		echo "$git_show" | grep "^-.*${test_method}" |& tee -a $output_file;
	else
		echo "Deleted method not found. Finding deleted test class." |& tee -a $output_file;
		echo "$git_show" | grep "^-.*${class}" |& tee -a $output_file;
	fi
done

echo "$output_file";