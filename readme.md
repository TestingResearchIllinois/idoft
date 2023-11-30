# International Dataset of Flaky Tests (IDoFT)
This repository contains all the data used to build the flaky tests' website, hosted here: [http://mir.cs.illinois.edu/flakytests](http://mir.cs.illinois.edu/flakytests). While the website is only for Java tests for now, this repository includes flaky tests in both Java and Python. Specifically, the [pr-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/pr-data.csv) for **Java** projects using **Maven**, [gr-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/gr-data.csv) for **Java** projects using **Gradle** and [py-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/py-data.csv) for **Python** contain all the information about the flaky tests detected or fixed in the International Dataset of Flaky Tests (IDoFT).
 
To contribute a newly detected or fixed flaky test to the dataset, please see [Contributing detected flaky test](#contributing-detected-flaky-test) or [Contributing fixed flaky test](#contributing-fixed-flaky-test), respectively.

## Contributing detected flaky test
  
### To contribute a newly detected flaky test:

* Add a new entry to the [pr-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/pr-data.csv) for **Java** projects using **Maven** or [gr-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/gr-data.csv) for **Java** projects using **Gradle** or the [py-data.csv file](https://github.com/TestingResearchIllinois/idoft/blob/main/py-data.csv) for **Python** while maintaining the order of the file (i.e., alphabetical order for Project URL, then Fully-Qualified Test Name, then SHA Detected, ...).
  * One recommended way to automatically sort is to run `echo "$(head -n1 pr-data.csv && tail +2 pr-data.csv | LC_ALL=C sort -k1,1 -k4,4 -t, -f)" > pr-data.csv` for **Java Maven**, `echo "$(head -n1 gr-data.csv && tail +2 gr-data.csv | LC_ALL=C sort -k1,1 -k4,4 -t, -f)" > gr-data.csv` for **Java Gradle**  and `echo "$(head -n1 py-data.csv && tail +2 py-data.csv | LC_ALL=C sort -k1,1 -k3,3 -t, -f)" > py-data.csv` for **Python**.
  * The following columns need to be filled in: `Project URL, SHA Detected, Module Path, Fully-Qualified Test Name (packageName.ClassName.methodName), Category` for **Java** and `Project URL,SHA Detected,Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod),Category` for **Python**. Detailed information for the columns can be found [here](#detailed-information-for-each-column). Note that for **Python**, we do not have the `Module Path` column. Please note that in the `Pytest Test Name` column, the notion of `TestClass` does not always apply (depending on how developers write tests). We expect the Python testing framework `pytest` can directly run the test with `pytest $Pytest_Test_Name`. The documentation of `pytest` can be found [here](https://docs.pytest.org/en/latest/how-to/usage.html).
  * Status and PR Link should be left blank. Notes can be provided if applicable, see [here](#adding-notes) for what to provide.
  * Please mark the project as "forked" or "unforked" in `format_checker/forked_projects.json` if the project does not exist.
  * If the flaky test being added already exist but has a different SHA Detected, please update the existing row's SHA Detected if the existing SHA is older than the one being added. There should only be one row for each tuple of `Project URL, Module Path, Fully-Qualified Test Name` for **Java** and `Project URL,Pytest Test Name` for **Python**.
    * One recommended way to check if which SHAs may be more recent is to run `[[ $(git show -s --pretty=%at $SHA1) -gt $(git show -s --pretty=%at $SHA2) ]] && echo $SHA1 || echo $SHA2`.
  * Please add some notes describing how you detected the new tests (e.g., commands that were run) and any necessary data to reproduce the detection (e.g., including the NonDex seed or `flaky-list.json` file for ID and OD tests, respectively). The specific format for the notes is described in [Adding notes](#adding-notes).

#### Example:
For Java:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/alibaba/fastjson | e05e9c5e4be580691cc55a59f3256595393203a1 | . | com.alibaba.json.bvt.date.DateTest_tz.test_codec | OD | | |

For Python:

Project URL | SHA Detected | Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/AguaClara/aguaclara | 9ee3d1d007bc984b73b19520d48954b6d81feecc | tests/core/test_cache.py::test_ac_cache | NIO | | |
 
## Contributing fixed flaky test

### To contribute a newly fixed flaky test that has yet to be accepted by developers:

* Edit the same test entry to set the Status as Opened and update the PR link.

Note that to submit the fix to the developers you likely need to reproduce the flaky-test failure in the latest commit of the repository. We expect that the fix you submit (or a very similar fix) would also remove the flakiness at the SHA Detected commit. If your fix does not remove the flaky-test failure at the existing SHA Detected commit, please create a new row with the SHA Detected as the latest commit of the repository.

#### Example:
For Java:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/alibaba/fastjson | e05e9c5e4be580691cc55a59f3256595393203a1 | . | com.alibaba.json.bvt.date.DateTest_tz.test_codec | OD | Opened | https://github.com/alibaba/fastjson/pull/2148 |

For Python:

Project URL | SHA Detected | Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/drtexx/volux | c41339aceeab4295967ea88b2edd05d0d456b2ce | tests/test_operator.py::Test_operator::test_add_module | NIO | Opened | https://github.com/DrTexx/Volux/pull/37 |

### To contribute a newly accepted flaky test fix:

* Edit the same test entry to set the Status as Accepted.

#### Example:
For Java:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/alibaba/fastjson | e05e9c5e4be580691cc55a59f3256595393203a1 | . | com.alibaba.json.bvt.date.DateTest_tz.test_codec | OD | Accepted | https://github.com/alibaba/fastjson/pull/2148 |

For Python:

Project URL | SHA Detected | Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/chaosmail/python-fs | 2567922ced9387e327e65f3244caff3b7af35684 | fs/tests/test_touch.py::test_touch_on_new_file | NIO | Accepted | https://github.com/chaosmail/python-fs/pull/9 |

## Adding notes

To add more information about any test:

* Open an issue for **Java** in this repository where the title is of the format:
  * Project URL,SHA Detected,Fully-Qualified Test Name (packageName.ClassName.methodName): If the notes are for a particular test.
  * Project URL,SHA Detected,Module Path: If the notes are for a particular module.
  * Project URL,SHA Detected: If the notes are for a particular project.
* Open an issue for **Python** in this repository where the title is of the format:
  * Project URL,SHA Detected,Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod): If the notes are for a particular test.
  * Project URL,SHA Detected: If the notes are for a particular project.
* Make sure to include any steps to reproduce, any relevant logs, or any relevant information about the test/module in the issue. You should attach relevant files (e.g., log output of NonDex or iDFlakies) by [attaching the files to the issue](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/file-attachments-on-issues-and-pull-requests). E.g., 
  * for tests detected by iDFlakies, you should include `flaky-list.json` and `original-order` located under the `.dtfixingtools` directory generated by iDFlakies. Note that GitHub requires that these files be of `.txt` format (e.g., upload `flaky-list.txt` and `original-order.txt`, respectively).
  * for tests detected by NonDex, you should include `nondexMode` and `nondexSeed` from the `.nondex/{testid}/config` file generated by NonDex in the comments of the issue. You may also include the whole `config` file instead of adding a comment.

An example issue can be found [here](https://github.com/TestingResearchIllinois/idoft/issues/88).

#### Example entry in the [pr-data.csv file](https://github.com/TestingResearchIllinois/pr-data/blob/main/pr-data.csv):
For Java:

Project URL | SHA Detected | Module Path | Fully-Qualified Test Name (packageName.ClassName.methodName) | Category | Status | PR Link | Notes
---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ----------
https://github.com/wso2/carbon-apimgt | a82213e40e7e6aa529341fdd1d1c3de776949e64 | components/apimgt/org.wso2.carbon.apimgt.rest.api.commons | org.wso2.carbon.apimgt.rest.api.commons.util.RestApiUtilTestCase.testConvertYmlToJson | ID | Skipped | | https://github.com/TestingResearchIllinois/flaky-test-dataset/issues/1

For Python:
We do not have an example yet. If someone wants to open an issue for a Python test, the only two differences from Java are that (1) Python tests do not have the column of `Module Path`, and (2) the `Test Name` is `Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod)`.

## Detailed information for each column

* **Project URL**: The GitHub project where the flaky test was found.

Example: https://github.com/wso2/carbon-apimgt

* **SHA Detected**: The commit SHA for the project where the flaky test was detected. This may or may not be the latest SHA.

Example: a82213e40e7e6aa529341fdd1d1c3de776949e64
 
* **Module path**: The path of the module within the project that contains the flaky test. Please use ```.``` if the test is located at the base of the repository.

Example: components/apimgt/org.wso2.carbon.apimgt.rest.api.commons
 
* **Fully-Qualified Test Name (packageName.ClassName.methodName)**: The test description of the flaky test. This column is typically the fully-qualified test name in the format of packageName.ClassName.methodName. In some cases, such as Cucumber or parameterized tests, please include all relevant test description (e.g., ```lv.ctco.cukes.plugins.RunCukesTest.Given wait for 1 second```).

Example: org.wso2.carbon.apimgt.rest.api.commons.util.RestApiUtilTestCase.testConvertYmlToJson
 
* **Category**: The category of the detected flaky test. Multiple categories may be supplied, each separated with ```;```, sorted alphabetically, and contains no spaces. Please use ```UD``` if you do not know the category. When adding OD related tests, it is much appreciated if one can provide the passing and failing order of the test (e.g., the `flaky-lists.json` file created by iDFlakies). The accepted categories are:

Category | Description
------------ | -------------
OD | Order-Dependent flaky tests as defined in [iDFlakies](http://mir.cs.illinois.edu/winglam/publications/2019/LamETAL19iDFlakies.pdf)
OD-Brit | Order-Dependent Brittle tests as defined in [iFixFlakies](http://mir.cs.illinois.edu/winglam/publications/2019/ShiETAL19iFixFlakies.pdf)
OD-Vic | Order-Dependent Victim tests as defined in [iFixFlakies](http://mir.cs.illinois.edu/winglam/publications/2019/ShiETAL19iFixFlakies.pdf)
ID | Implementation-Dependent Tests found by [Nondex](http://mir.cs.illinois.edu/marinov/publications/ShiETAL16NonDex.pdf)
ID-HtF | Implementation-Dependent tests that are hard to fix. Brief description given in https://github.com/kaiyaok2/ID-HtF.
NIO | Non-Idempotent-Outcome Tests as defined in [ICSE’22 work](https://cs.gmu.edu/~winglam/publications/2022/WeiETAL22NIO.pdf). Tests that pass in the first run but fail in the second.
NOD | Non-Deterministic tests 
NDOD | Non-Deterministic Order-Dependent tests that fail non-deterministically but with significantly different failure rates in different orders as defined in our [ISSRE’20 work](http://mir.cs.illinois.edu/winglam/publications/2020/LamETAL20ISSRE.pdf)
NDOI | Non-Deterministic Order-Independent tests that fail non-deterministically but similar failure rates in all orders as defined in our [ISSRE’20 work](http://mir.cs.illinois.edu/winglam/publications/2020/LamETAL20ISSRE.pdf)
UD | Unknown Dependency tests that pass and fail in a test suite or in isolation
OSD | Operating System Dependent tests that pass and fail depending on the operating system
 
* **Status**: This defines the state the flaky test is in. Only one status may be used at any given time for each flaky test. The accepted status values are:
 
Status | Description
--------- | -----------
Blank | A blank value denotes that a flaky test was detected and is yet to be inspected
Opened | For tests where a PR was opened to fix the flaky test
Accepted | For tests where a PR was accepted to fix the flaky test
InspiredAFix | The work (e.g., issue report, pull request) inspired a fix from the developer, but did not directly change any code. The PR Link should be the link of the PR that the developer merged to fix the flakiness and some [Notes](#adding-notes) should be added to explain how the work inspired the fix
DeveloperWontFix | For tests where developers claimed that they do not want a fix
DeveloperFixed | For tests where a developer fixed the tests before a PR was made
Deleted | For tests that can no longer be fixed as the tests have been removed from the repository after the tests were detected
Rejected | For tests where a PR was rejected/closed as the developers did not think a fix was necessary
Skipped | For test which was inspected and should not be fixed (e.g., test is annotated with @Ignore). To use this status, please provide some [Notes](#adding-notes) on why the test should be skipped
MovedOrRenamed | For test that has a different fully-qualified name on two different shas. This status should be added only to the row with the older sha. To use this status, please also provide some [Notes](#adding-notes) on what the test is renamed to
RepoArchived | For test that is in an archived repo, which is indicated by GitHub in messages such as "This repository has been archived by the owner. It is now read-only."
Deprecated | For test that is in a deprecated repository, which is usually indicated in the project README or description as "Deprecated" or a similar message. To use this status, please also provide some [Notes](#adding-notes) that contain a link to the commit that marks the repository as deprecated. 
RepoDeleted | For tests that are in repository that does not exist anymore and the link to the repository throws a 404 status code error.
MovedToGradle | For tests that are in repository that moved from Maven to Gradle.
FixedOrder | The test has a fixed order, e.g., using `@Order` in JUnit 5.
Unmaintained | For tests that are in a repository that does not have any commits to main/master in the past 2 years. To use this status, please also provide some [Notes](#adding-notes) that contain the last commit date.

* **PR Link**: Link to the pull request in the repository of the Project URL to fix a given flaky test.

Example: https://github.com/alibaba/fastjson/pull/2148

* **Notes**: Any additional information that one may need to debug the test such as steps to reproduce, any relevant logs, or any relevant information about this test. Note: The only acceptable values are URLs for this column. For more information about the format please refer to the [Adding notes](#adding-notes) section.

Example: https://github.com/TestingResearchIllinois/flaky-test-dataset/issues/1

# FAQ

## How to indicate that a test is renamed or moved to a different location?
If the test method body is the same between two versions (e.g., if in ```old_sha```, ```some.test.name``` has the same test method body as ```some.other.test.name``` in ```new_sha```), we consider the two different versions of the test to be the same test. For the row with the older sha, please change the Status to ```MovedOrRenamed``` and add [Notes](#adding-notes) describing which version the test is found to be renamed/moved. 

If the test method body is different, we consider the two different versions of the test to be two different tests. For the row with the older sha, please change the Status to ```Deleted``` and add [Notes](#adding-notes) describing which version the test is found to be renamed/moved and how the test method body differs between the two versions.

For either case, please also add a new row for the newer sha and test name. Once the preceding changes are made, all future pull request updates should only be made to the row with the newer sha.

## How to indicate that a repository has changed owner or is renamed?
Please update all rows of the old repository owner and name with the new repository owner and name.


# Acknowledgments

If you use the dataset, please cite this website and our original dataset:
```
@misc{InternationalDatasetofFlakyTests,
    title = {{International Dataset of Flaky Tests (IDoFT)}},
    author = {Lam, Wing},
    year = {2020},
    url = {http://mir.cs.illinois.edu/flakytests}
}
@inproceedings{LamETAL19iDFlakies,
    author      = "Wing Lam and Reed Oei and August Shi and Darko Marinov and Tao Xie",
    title       = "{iDF}lakies: {A} framework for detecting and partially classifying flaky tests",
    booktitle   = "ICST 2019: 12th IEEE International Conference on Software Testing, Verification and Validation",
    month       = "April",
    year 	= "2019",
    address 	= "Xi'an, China",
    pages       = "312--322"
}
```

[Wing Lam](http://mir.cs.illinois.edu/winglam) is the author of this dataset. He thanks all contributors and the students from the Fall 2020 CS 527 class from the University of Illinois at Urbana-Champaign for their contributions.

For any questions about the dataset, please email [testflaky@gmail.com](mailto:testflaky@gmail.com).
