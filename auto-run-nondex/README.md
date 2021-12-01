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
>  A sample command for runNondexUnderAuthor: `./runNondexUnderAuthor.sh https://github.com/orgs/spotify/repositories ~/progress6`



