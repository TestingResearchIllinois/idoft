# `runNondex`

This script runs individual modules in the specified project with the `Nondex` tool and shows results automatically in the `markdown` format.

Output file is located inside the project folder and called `report_md.md` The output would only contain tests that are detected by the nondex tool as flaky, and the result includes the seeds used for the test and the status of the test result.




# `runNondexUnderAuthor`

This script runs all the valid repos under a given author using the `runNondex` script above. 

The valid repo is defined as:

1. This repo has not appeared in the latest `pr-data.csv`
2. This repo contains pom.xml file.




### Usage:
```bash
./runNondex.sh <project_folder_path>
./runNondexUnderAuthor.sh <author_repository_url> <path_where_you_want_to_clone_those repos>
```



>  To find the author_repository_url, find the author that you want to run Nondex with, and get this author's repository overview url (e.g., https://github.com/orgs/spotify/repositories). Note that you don't need to provide the url with other parameters, as the script will automatically add the parameters needed.
>
>  There are two types of account in the github: personal account and organizational account, and their repo's url is slightly different:
> 
>  1. Organizational Account: https://github.com/orgs/HubSpot/repositories
>  2. Personal Account: https://github.com/Anuken?tab=repositories
> 
>  You don't need to worry about the account type that you want to run Nondex with. This script will automatically handle both cases. 
> 
>  Two sample commands for runNondexUnderAuthor:
>  
>  1. Organizational Account: `./runNondexUnderAuthor.sh https://github.com/orgs/spotify/repositories ~/progress6`
>  2. Personal Account: `./runNondexUnderAuthor.sh https://github.com/Anuken?tab=repositories ~/progress6`
>  
>  After running the `runNondexUnderAuthor.sh` command, you could go to your `progress6` directory (the directory you indicate in the command) and run the command below to get an overview of your findings (`./progress_stats.md`)!
> 
>  `find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' &&  git rev-parse HEAD && git config --get remote.origin.url | rev | cut -c5- | rev  && cat .runNondex/htmlOutput && cat report_md.md" \; &> progress_stats.md`


