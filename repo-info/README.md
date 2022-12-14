# Repo Info Helper

This script scans a given .csv file (works on both `pr-data.csv` and `py-data.csv`), and outputs another .csv file, with 3 columns:

* Repo URL
* Months since latest commit to master/main
* Number of stars

... which are sorted in descending order of number of stars and ascending order of months since last commit to master.

The latter 2 values will help us in shortlisting a project to fix flaky tests in. The chances of your PR getting accepted are higher for a repository that is actively maintained and has a high number of stars. This script will only scan URLs that have an empty `Status` column.

## To run:

* Requires a github access token if there are more than 60 requests made (i.e. more than 60 unique repositories in the file), which is highly likely, since both `pr-data.csv` and `py-data.csv` each contain 300+ unique repositories at the time of writing this (Nov 2022).

* Following are the commands to run the script from the root directory. Remember to use a github access token to overcome the rate limit:
    * For `pr-data.csv`: `repo-info/get_repo_info.py -f pr-data.csv -c 'Project URL' -t <github-access-token>`
    * For `py-data.csv`: `repo-info/get_repo_info.py -f py-data.csv -c 'Project URL' -t <github-access-token>`

The new file will be saved with the name `repo_info.csv` inside the `repo-info` directory.