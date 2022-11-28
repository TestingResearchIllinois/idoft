# Repo Info Helper

This script scans a given .csv file (works on both `pr-data.csv` and `py-data.csv`), specifically, just a single column inside, and outputs another .csv file, with 3 columns:

* Repo URL
* Months since latest commit to master/main
* Number of stars

... which are sorted in descending order of number of stars and ascending order of months since last commit to master.

The latter 2 values will help us in shortlisting a project to fix flaky tests in. The chances of your PR getting accepted are higher for a repository that is actively maintained and has a high number of stars.

## To run:

* Required libraries to install: `pandas`, `tqdm`, `pygithub`

* Requires a github access token if there are more than 60 requests made (i.e. more than 60 unique repositories in the file), which is highly likely, since both `pr-data.csv` and `py-data.csv` each contain 300+ unique repositories at the time of writing this (Nov 2022).

* To run: `python3 get_repo_info.py -t <GITHUB_ACCESS_TOKEN> -f '<CSV_FILEPATH>' -c '<COLUMN_NAME_CONTAINING_REPO_URL>'`

The new file will be saved with the name `repo_info.csv` in the same directory as the script.