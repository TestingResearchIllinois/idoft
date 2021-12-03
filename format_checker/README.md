<h1 align="center">IDoFT Format Checker</h1>

<p align="center">A format checking tool to ensure that changes made to files of the dataset do not violate any of the required rules.</p>

## Run Locally

#### 1. Check your Python version

This tool is recommended to be run using Python 3.9, however Python 3.7 and above should also work. You can check your Python version by typing `python -V` on your command line. For example:

```
python -V
Python 3.9.4
```

If doing that tells you you're working with Python 2.7, you should try `python3 -V`. If it's version 3.7 or above, you can run the tool following step number 3. Otherwise, you should consider installing the [latest Python version](https://www.python.org/downloads/).

#### 2. Install dependencies

The dependencies for this tool can be installed running the following from the root directory:

```
$ pip install -r format_checker/requirements.txt
```

#### 3. Run the tool

Running this tool locally only requires running `main.py` from the root directory:

```
$ python format_checker/main.py
```
In case your Python version is 2.7 but your your Python3 version is 3.7 or above (see step 1), you should run it using `python3` instead of `python`. 

This will check all the implemented rules only for the rows of the `.csv` files that have been modified in some way (including row additions). It can check either for uncommitted changes (e.g. if a row was modified in `pr-data.csv` but the file wasn't committed) or for changes made in the commits related to the push/pull request that triggered the GitHub Actions build, as well as for committed changes that haven't yet been pushed. By default, the tool looks for uncommitted changes as well as committed changes every time it is run locally.

## Run with GitHub Actions

The file `ci.yml` is already set up to run this tool automatically everytime a push is made to a repository that contains it, and the same goes for pull requests.  

In case you're already working with another GitHub Actions workflow, and want to integrate this tool into your own workflow, you can do so by adding the following job to your `.yml` file:

```yml
format-checker:
  runs-on: ubuntu-latest
  env:
    # When there is no base commit (e.g., first push to a new branch), 
    # GitHub assigns a string of zeros to event.before. It's necessary to 
    # handle this separately
    NULL_COMMIT: '0000000000000000000000000000000000000000'
  steps:
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
        pip install -r format_checker/requirements.txt
    # Only run this step if the event is a push and event.before shows 
    # that it's the first push to a new branch
    - if: >-
        ${{github.event_name == 'push' && github.event.before ==
        env.NULL_COMMIT}}
      name: Run format checker on new branch
      run: >
        python format_checker/main.py ${{github.event.before}}
        ${{github.event.commits[0].id}} ${{github.event.after}}
    # Only run this step if the event is a pull request
    - if: ${{github.event_name == 'pull_request'}}
      name: Run format checker on pull request
      run: >
        python format_checker/main.py ${{github.event.pull_request.base.sha}}
        ${{github.event.pull_request.head.sha}}
    # Only run this step if the event is a push and it's not the first one
    # to a new branch
    - if: >-
        ${{github.event_name == 'push' && github.event.before !=
        env.NULL_COMMIT}} 
      name: Run format checker on push
      run: >
        python format_checker/main.py ${{github.event.before}}
        ${{github.event.after}}
```

## Usage/Examples

Given the following uncommitted changes to `tso-iso-rates.csv` (the last column changes from 0 to 10):

```Diff
$ git diff tso-iso-rates.csv
diff --git a/tso-iso-rates.csv b/tso-iso-rates.csv
index 387296e..99fba8c 100644
--- a/tso-iso-rates.csv
+++ b/tso-iso-rates.csv
@@ -1,5 +1,5 @@
 Project URL,SHA Detected,Module Path,Fully-Qualified Test Name (packageName.ClassName.methodName),Number Of Test Failures In Test Suite,Number Of Test Runs In Test Suite,P-Value,Is P-Value Less Or Greater Than 0.05,Total Runs In Test Suite,Number of Times Test Passed In Test Suite,Total Runs In Isolation,Number of Times Test Passed In Isolation
-https://github.com/alibaba/fastjson,e05e9c5e4be580691cc55a59f3256595393203a1,.,com.alibaba.json.bvt.issue_1200.Issue1298.test_for_issue,(0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;100;0;100;0;0),(100;100;100;100;100;100;100;100;100;100;100;100;100;100;100;100;100;2000;100;100;100),0,less,4000,3800,4000,0
+https://github.com/alibaba/fastjson,e05e9c5e4be580691cc55a59f3256595393203a1,.,com.alibaba.json.bvt.issue_1200.Issue1298.test_for_issue,(0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;100;0;100;0;0),(100;100;100;100;100;100;100;100;100;100;100;100;100;100;100;100;100;2000;100;100;100),0,less,4000,3800,4000,10
```

Running the tool locally would output:

```
$ python format_checker/main.py
INFO: On file pr-data.csv: There are no changes to be checked
INFO: On file tic-fic-data.csv: There are no changes to be checked
Success: Exiting with code 0 due to no logged errors
```

As you can see, it exits successfully because it is a valid change, and it says that for `pr-data.csv` and `tic-fic-data.csv` there are no changes to be checked (because there aren't any!), however it ignores the file we modified: `tso-iso-rates.csv`; this is because it did have changes to be checked, however there were no errors among those changes—hence why it does not say anything about it—.
If, instead, we made a change that violated some rule, e.g., writing 'ID;' as a category:

```Diff
$ git diff pr-data.csv
diff --git a/pr-data.csv b/pr-data.csv
index 722b306..bf73e92 100644
--- a/pr-data.csv
+++ b/pr-data.csv
@@ -419,7 +419,7 @@ 
-https://github.com/apache/hive,90fa9064f2c6907fbe6237cb46d5937eebd8ea31,standalone-metastore/metastore-server,org.apache.hadoop.hive.common.TestStatsSetupConst.testStatColumnEntriesCompat,ID,InspiredAFix,https://github.com/apache/hive/pull/1024,
+https://github.com/apache/hive,90fa9064f2c6907fbe6237cb46d5937eebd8ea31,standalone-metastore/metastore-server,org.apache.hadoop.hive.common.TestStatsSetupConst.testStatColumnEntriesCompat,ID;,InspiredAFix,,

```

Running the tool locally would output:

```
$ python format_checker/main.py
ERROR: On file pr-data.csv, row 423:
Invalid Category: "ID;"
WARNING: On file pr-data.csv, row 423: 
Status InspiredAFix should contain a note
WARNING: On file pr-data.csv, row 423: 
Status InspiredAFix should have a PR Link
INFO: On file tic-fic-data.csv: There are no changes to be checked
INFO: On file tso-iso-rates.csv: There are no changes to be checked
Failure: Exiting with code 1 due to 1 logged error
```

Here, the category `ID;` is considered a rule violation and therefore the tool ends in `Failure`. Note as well that it gives 2 warnings: the first one is because we also deleted the note link from the row, and given that its status is `InspiredAFix`, the tool *recommends* (not *enforces*) that it should have a note. The second one is a similar scenario, except that it is recommending a pull request link if the status is `InspiredAFix` (it was deleted for this example).
