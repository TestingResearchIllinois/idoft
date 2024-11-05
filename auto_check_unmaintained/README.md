# Find Unmaintained Repos
`check_unmaintained.py` scans the `data.csv` file (e.g., `py-data.csv`, only tested on `py-data.csv`, should work the same for `pr-data.csv`) and outputs `unmaintained-repos.csv`, containing:
* Repository URL
* Months since the latest commit to the master/main branch
* Date of the latest commit

# Update Unmaintained Status in data.csv
`mark_repo_unmaintained.py` matches URLs in both `py-data.csv` and `unmaintained-repos.csv` to produce a new file, `py-data_with_last_commit.csv`, updating:
* The status to **Unmaintained** (if the current status is empty)
* The date of the latest commit in the notes
(could work for `pr-data.csv` but is not tested)

# To Run
## Produce unmaintained-repos.csv:
```bash
python check_unmaintained.py -t your_github_access_token -f py-data.csv -c 'Project URL'
```

## Update py-data.csv:
```bash
python mark_repo_unmaintained.py
```

## Acknowledgments

I would like to thank [blazyy](https://github.com/blazyy) for their work on the [repo-info](https://github.com/TestingResearchIllinois/idoft/tree/main/repo-info). Their project provided invaluable resources that helped create this tool.