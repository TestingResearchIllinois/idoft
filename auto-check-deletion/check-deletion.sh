#!/bin/bash

filtered_tests=$(cat filtered_tests.txt | sed 's/,.*\//,/' | rev | cut -d'.' -f 1,2 | rev);

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
	echo ==== deleted ${test} ? ====;
	if echo "$git_show" | grep -q "^-.*${test_method}"
	then
		echo "$git_show" | grep "^-.*${test_method}";
	else
		echo "Deleted method not found. Finding deleted test class."
		echo "$git_show" | grep "^-.*${class}";
	fi
done