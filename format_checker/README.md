## Format Checker

### Run locally

Running this tool locally only requires running `main.py` from the root directory:
```
python format_checker/main.py
```

This will check all the implemented rules only for the rows of the `.csv` files that have been modified in some way (including row additions). It can check either for uncommitted changes (e.g. if a row was modified in `pr-data.csv` but the file wasn't committed) or for changes made in the last commit, so that when one makes a push/pull request it only checks for rows changed in the commit of the push/PR that triggered the action (therefore it is recommended to keep changes to a single commit).

### Run with GitHub Actions

The file `ci.yml` is already set up to run this tool automatically everytime a push is made to a repository that contains it, as well as pull requests to `main`.  

In case you're already working with another GitHub Actions worklflow, you can add support for this tool by adding the following steps:

```yml
- uses: actions/checkout@v2
  with:
    fetch-depth: 0
- name: Install Python 3
  uses: actions/setup-python@v2
  with:
    python-version: 3.9.4
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install errorhandler
- name: Run format checker
  run: |
    python ./format_checker/main.py 
```

