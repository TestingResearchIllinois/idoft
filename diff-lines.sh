#!/bin/bash
#Bash Program that takes in the output of git diff and extracts the line numbers of the differences
#Taken from https://stackoverflow.com/questions/8259851/using-git-diff-how-can-i-get-added-and-modified-lines-numbers

path=
line=
while read; do
    esc=$'\033'
    if [[ $REPLY =~ ---\ (a/)?.* ]]; then
        continue
    elif [[ $REPLY =~ \+\+\+\ (b/)?([^[:blank:]$esc]+).* ]]; then
        path=${BASH_REMATCH[2]}
    elif [[ $REPLY =~ @@\ -[0-9]+(,[0-9]+)?\ \+([0-9]+)(,[0-9]+)?\ @@.* ]]; then
        line=${BASH_REMATCH[2]}
    elif [[ $REPLY =~ ^($esc\[[0-9;]*m)*([\ +-]) ]]; then
        echo "$line"
        if [[ ${BASH_REMATCH[2]} != - ]]; then
            ((line++))
        fi
    fi
done
