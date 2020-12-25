# Illinois Dataset of Flaky Tests (IDoFT)
This repository contains all of the data used to build the flaky tests website, hosted here: [http://mir.cs.illinois.edu/flakytests](http://mir.cs.illinois.edu/flakytests). Specifically, the [pr-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/pr-data.csv) contains all of the information about the flaky tests detected or fixed in the Illinois Dataset of Flaky Tests (IDoFT).
 
To contribute a newly detected or fixed flaky test to the dataset, please see [Contributing detected flaky test](#contributing-detected-flaky-test) or [Contributing fixed flaky test](#contributing-fixed-flaky-test), respectively.

## Contributing detected flaky test
  
### To contribute a newly detected flaky test:

* Add a new entry to the [pr-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/pr-data.csv) while maintaining the order of the file (i.e., alphabetical order for Project URL, then Fully-Qualified Test Name, then SHA Detected, ...).
  * One recommended way to automatically sort is to run `echo "$(head -n1 pr-data.csv && tail +2 pr-data.csv | LC_ALL=C sort -k1,1 -k4,4 -t, -f)" > pr-data.csv`.
  * The following columns need to be filled in: `Project URL, SHA Detected, Module Path, Fully-Qualified Test Name (packageName.ClassName.methodName), Category`. Detailed information for the columns can be found [here](#detailed-information-for-each-column).
  * Status and PR Link should be left blank. Notes can be provided if applicable, see [here](#adding-notes) for what to provide.
  * If the flaky test being added already exist but has a different SHA Detected, please update the existing row's SHA Detected if the existing SHA is older than the one being added. There should only be one row for each triple of `Project URL, Module Path, Fully-Qualified Test Name`.
    * One recommended way to check if which SHAs may be more recent is to run `[[ $(git show -s --pretty=%at $SHA1) -gt $(git show -s --pretty=%at $SHA2) ]] && echo $SHA1 || echo $SHA2`.

#### Example:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/alibaba/fastjson | e05e9c5e4be580691cc55a59f3256595393203a1 | . | com.alibaba.json.bvt.date.DateTest_tz.test_codec | OD | | |
 
## Contributing fixed flaky test

### To contribute a newly fixed flaky test that has yet to be accepted by developers:

* Edit the same test entry to set the Status as Opened and update the PR link.

Note that to submit the fix to the developers you likely need to reproduce the flaky-test failure in the latest commit of the repository. We expect that the fix you submit (or a very similar fix) would also remove the flakiness at the SHA Detected commit. If your fix does not remove the flaky-test failure at the existing SHA Detected commit, please create a new row with the SHA Detected as the latest commit of the repository.

#### Example:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/alibaba/fastjson | e05e9c5e4be580691cc55a59f3256595393203a1 | . | com.alibaba.json.bvt.date.DateTest_tz.test_codec | OD | Opened | https://github.com/alibaba/fastjson/pull/2148 |


### To contribute a newly accepted flaky test fix:

* Edit the same test entry to set the Status as Accepted.

#### Example:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/alibaba/fastjson | e05e9c5e4be580691cc55a59f3256595393203a1 | . | com.alibaba.json.bvt.date.DateTest_tz.test_codec | OD | Accepted | https://github.com/alibaba/fastjson/pull/2148 |

## Adding notes

To add more information about any test:

* Open an issue in this repository where the title is of the format:
  * Project URL,SHA Detected,Fully-Qualified Test Name (packageName.ClassName.methodName): If the notes are for a particular test.
  * Project URL,SHA Detected,Module Path: If the notes are for a particular module.
  * Project URL,SHA Detected: If the notes are for a particular project.
* Make sure to include any steps to reproduce, any relevant logs, or any relevant information about the test/module in the issue. You may attach relevant files (e.g., log output of NonDex or iDFlakies, `flaky-lists.json` files of iDFlakies) by [attaching the files to the issue](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/file-attachments-on-issues-and-pull-requests).

An example issue can be found [here](https://github.com/TestingResearchIllinois/flaky-test-dataset/issues/1).

#### Example entry in the [pr-data.csv file](https://github.com/TestingResearchIllinois/pr-data/blob/main/pr-data.csv):

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/wso2/carbon-apimgt | a82213e40e7e6aa529341fdd1d1c3de776949e64 | components/apimgt/org.wso2.carbon.apimgt.rest.api.commons | org.wso2.carbon.apimgt.rest.api.commons.util.RestApiUtilTestCase.testConvertYmlToJson | ID | Skipped | | https://github.com/TestingResearchIllinois/flaky-test-dataset/issues/1

## Detailed information for each column

* **Project URL**: The Github project where the flaky test was found.

Example: https://github.com/wso2/carbon-apimgt

* **SHA Detected**: The commit SHA for the project where the flaky test was detected. This may or may not be the latest SHA.

Example: a82213e40e7e6aa529341fdd1d1c3de776949e64
 
* **Module path**: The path of the module within the project that contains the flaky test. Please use ```.``` if the test is located at the base of the repository.

Example: components/apimgt/org.wso2.carbon.apimgt.rest.api.commons
 
* **Fully-Qualified Test Name (packageName.ClassName.methodName)**: The fully-qualified test name of the flaky test in the format of packageName.ClassName.methodName.

Example: org.wso2.carbon.apimgt.rest.api.commons.util.RestApiUtilTestCase.testConvertYmlToJson
 
* **Category**: The category of the detected flaky test. Multiple categories may be supplied, each separated with ```;```, sorted alphabetically, and contains no spaces. Please use ```UD``` if you do not know the category. When adding OD related tests, it is much appreciated if one can provide the passing and failing order of the test (e.g., the `flaky-lists.json` file created by iDFlakies). The accepted categories are:

Category | Description
------------ | -------------
OD | Order-Dependent flaky tests as defined in [iDFlakies](http://mir.cs.illinois.edu/winglam/publications/2019/LamETAL19iDFlakies.pdf)
OD-Brit | Order-Dependent Brittle tests as defined in [iFixFlakies](http://mir.cs.illinois.edu/winglam/publications/2019/ShiETAL19iFixFlakies.pdf)
OD-Vic | Order-Dependent Victim tests as defined in [iFixFlakies](http://mir.cs.illinois.edu/winglam/publications/2019/ShiETAL19iFixFlakies.pdf)
ID | Implementation-Dependent Tests found by [Nondex](http://mir.cs.illinois.edu/marinov/publications/ShiETAL16NonDex.pdf)
NOD | Non-Deterministic tests 
NDOD | Non-Deterministic Order-Dependent tests that fail non-deterministically but with significantly different failure rates in different orders as defined in our [ISSRE’20 work](http://mir.cs.illinois.edu/winglam/publications/2020/LamETAL20ISSRE.pdf)
NDOI | Non-Deterministic Order-Independent tests that fail non-deterministically but similar failure rates in all orders as defined in our [ISSRE’20 work](http://mir.cs.illinois.edu/winglam/publications/2020/LamETAL20ISSRE.pdf)
UD | Unknown Dependency tests that pass and fail in a test suite or in isolation
 
* **Status**: This defines the state the flaky test is in. Only one status may be used at any given time for each flaky test. The accepted status values are:
 
Status | Description
--------- | -----------
Blank | A blank value denotes that a flaky test was detected and is yet to be inspected
Opened | For tests where a PR was opened to fix the flaky test
Accepted | For tests where a PR was accepted to fix the flaky test
InspiredAFix | The work (e.g., issue report, pull request) inspired a fix from the developer, but did not directly change any code. The PR Link should be the one the developer uses to fix the flakiness and some [Notes](#adding-notes) should be added to explain how the work inspired the fix
DeveloperFixed | For tests where a developer fixed the tests before a PR was made
Deleted | For tests that can no longer be fixed as the tests have been removed from the repository after the tests were detected
Rejected | For tests where a PR was rejected/closed as the developers did not think a fix was necessary
Skipped | For test which was inspected and should not be fixed (e.g., test is annotated with @Ignore). To use this status, please provide some [Notes](#adding-notes)

* **PR Link**: Link to the pull request in the repository of the Project URL to fix a given flaky test.

Example: https://github.com/alibaba/fastjson/pull/2148

* **Notes**: Any additional information that one may need to debug the test such as steps to reproduce, any relevant logs, or any relevant information about this test.

Note: The only acceptable values are URLs for this column. For more information about the format please refer to the [Adding notes](#adding-notes) section.

Example: https://github.com/TestingResearchIllinois/flaky-test-dataset/issues/1

# Acknowledgments

[Wing Lam](http://mir.cs.illinois.edu/winglam) is the author of this dataset. He thanks all contributors and the students from the Fall 2020 CS 527 class from the University of Illinois at Urbana-Champaign for their contributions.

For any questions about the dataset, please email [testflaky@gmail.com](mailto:testflaky@gmail.com).
