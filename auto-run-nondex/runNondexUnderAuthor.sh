#!/bin/bash
DIR="${PWD}"

repos=$(python3 valid_repo_extractor.py $1)
echo $repos

for repo in $repos
    do
        echo $repo
        repo_name=$(echo $repo | rev | cut -d'/' -f 1 | rev | cut -d'.' -f 1)
        git clone $repo $2/$repo_name
        echo $repo_name

        ./runNondex.sh $2/$repo_name

        if [ -e $2/$repo_name/.runNondex/htmlOutput ]
        then
            echo "Flaky tests detected"
        else
            rm -rf $2/$repo_name
            echo "Repo [$2/$repo_name] removed..."
        fi

    done

