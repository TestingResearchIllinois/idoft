## Format Checker

### Run locally

#### 1. Install dependencies

The dependencies for this tool can be installed running the following from the root directory:

```
$ pip install -r format_checker/requirements.txt
```

#### 2. Run the tool

Running this tool locally only requires running `main.py` from the root directory:

```
$ python format_checker/main.py
```

This will check all the implemented rules only for the rows of the `.csv` files that have been modified in some way (including row additions). It can check either for uncommitted changes (e.g. if a row was modified in `pr-data.csv` but the file wasn't committed) or for changes made in the commits related to the push/pull request that triggered the GitHub Actions build, as well as for committed changes that haven't yet been pushed. By default, the tool looks for uncommitted changes as well as committed changes every time it is run locally.

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
- name: Run format checker on pull request
  if: ${{github.event_name == 'pull_request'}}
  env:
    BASE_SHA: ${{github.event.pull_request.base.sha}}
    HEAD_SHA: ${{github.event.pull_request.head.sha}}
  run: |
    commit_list=$(git log --oneline $BASE_SHA..$HEAD_SHA | cut -d " " -f 1)
    python ./format_checker/main.py $commit_list
- name: Run format checker on push
  if: ${{github.event_name == 'push'}}
  env:
    BASE_SHA: ${{github.event.before}}
    HEAD_SHA: ${{github.event.after}}
  run: |
    commit_list=$(git log --oneline $BASE_SHA..$HEAD_SHA | cut -d " " -f 1)
    python ./format_checker/main.py $commit_list
```