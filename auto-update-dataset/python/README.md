# Introduction 
We can use ``repoArchivedCheck.py`` to find archived projects in [pr-data.csv](https://github.com/TestingResearchIllinois/idoft/blob/main/pr-data.csv), [py-data.csv](https://github.com/TestingResearchIllinois/idoft/blob/main/py-data.csv), and [gr-data.csv](https://github.com/TestingResearchIllinois/idoft/blob/main/gr-data.csv).

It uses multithreading to speed up the process of checking multiple repositories in parallel.


# Environment & Requirements:
    | **Requirement**    | **Details**               |
    |--------------------|---------------------------|
    | **Python Version** | **Python 3.10 or higher** |
    | Libraries          | pandas                    |
    |                    | requests-html[html_clean] |
    |                    | lxml_html_clean           |

# Installation
You can install in one of two ways. A clean Python virtual environment (venv) is recommended.

### Option A: Install Directly (Using requirements.txt)
This installs the dependencies needed to run the script directly via python3.
```
# 1. Navigate to the project's python directory
cd ./idoft/auto-update-dataset/python

# 2. Install dependencies
pip install -r requirements.txt
```

### Option B: Install as Package (Using setup.py)
This installs the script as a system-wide executable command (auto-update-dataset).
```
# 1. Navigate to the project's python directory
cd ./idoft/auto-update-dataset/python

# 2. Install the package
pip install .
```

# Usage:
The script is used to find archived projects within the dataset CSV files and update their status.

- Directly run the script
    ```
    python3 repoArchivedCheck.py <filename.csv> [max_workers]
    ```
- If installed as package:
    ```
    auto-update-dataset <filename.csv> [max_workers]
    ```
- Note: [max_workers] is optional, default is 4

# The example results in console:  
- if no update on ```status``` is needed, it'll print ```No need to update```, otherwise ```Need to Update``` with the contents which user can copy to replace the corresesponding line in ```<filename.csv>``` file;
- Example output:
    ```
    [!]Need to Update (Copy the following contents and replace the corresponding line in pr-data.csv)
    line_number 6830:
    https://github.com/spinn3r/noxy,d53a49421f385c70b5abe7e8cda84ff3a7b59c71,noxy-reverse,com.spinn3r.noxy.reverse.ReverseProxyServiceTest.testRequestMetaForSuccessfulRequest,ID,Opened,https://github.com/spinn3r/noxy/pull/21,RepoDeleted
    ```

## prStatusCheck.py
### Overview
`prStatusCheck.py` is a script for automatically checking and updating pull request statuses in the IDoFT dataset. It queries the GitHub API to retrieve PR status information and updates the corresponding test records.

```bash
python prStatusCheck.py --help
  usage: prStatusCheck.py [-h] [--prrange PRRANGE] [--grrange GRRANGE] [--pyrange PYRANGE] [--threads THREADS]
  
  Update PR statuses in CSV files.
  
  options:
    -h, --help         show this help message and exit
    --prrange PRRANGE  Range of CSV rows for pr-data.csv (e.g., 100-200). If not specified, processes all rows. Uses actual CSV row
                       numbers (header=row 1, first data=row 2). Inclusive.
    --grrange GRRANGE  Range of CSV rows for gr-data.csv (e.g., 100-200). If not specified, processes all rows. Uses actual CSV row
                       numbers (header=row 1, first data=row 2). Inclusive.
    --pyrange PYRANGE  Range of CSV rows for py-data.csv (e.g., 100-200). If not specified, processes all rows. Uses actual CSV row
                       numbers (header=row 1, first data=row 2). Inclusive.
    --threads THREADS  Number of threads to use for parallel processing
```

### Setup 
```
cd ~/idoft
cd auto-update-dataset/python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Features

#### 1. Query by GitHub API

It reads the GitHub token from the .env file. To obtain and use your own token, go to https://github.com/settings/tokens and paste it at a file named as `.env` under `idoft` project root directory. Example:
```
GITHUB_TOKEN=<Your github token here>
```

#### 2. Per-File Independent Row Range Processing

Specify row ranges for each CSV file via command-line arguments

- **Arguments**:

  - `--prrange`: Row range for pr-data.csv (e.g., `3802-3804`)

    ```bash
    python prStatusCheck.py --prrange 3802-3804 
      2025-12-09 20:44:18,978 - INFO - --- Processing pr-data.csv ---
      2025-12-09 20:44:18,978 - INFO - Loading data from local file: $HOME/idoft/pr-data.csv
      2025-12-09 20:44:18,991 - INFO - Queued 3 tasks for pr-data.csv.
      2025-12-09 20:44:19,397 - INFO - [pr-data.csv] Row 3802: Status changed but could not be determined, remains Opened (https://github.com/apache/tinkerpop/pull/1658. Please check manually.)
      2025-12-09 20:44:19,410 - INFO - [pr-data.csv] Row 3803: Status changed but could not be determined, remains Opened (https://github.com/apache/tinkerpop/pull/1658. Please check manually.)
      2025-12-09 20:44:19,968 - INFO - [pr-data.csv] Row 3804: Status changed but could not be determined, remains Opened (https://github.com/apache/tinkerpop/pull/1658. Please check manually.)
      2025-12-09 20:44:19,968 - INFO - summary for pr-data.csv: 0 statuses updated, 3 changed but need manual check, 0 still open.
      2025-12-09 20:44:19,969 - INFO - Manual check log updated for pr-data.csv
    ```

  - `--grrange`: Row range for gr-data.csv (e.g., `107-108`)

    ```bash
    python prStatusCheck.py --grrange 107-108
      2025-12-09 20:43:43,978 - INFO - --- Processing gr-data.csv ---
      2025-12-09 20:43:43,978 - INFO - Loading data from local file: $HOME/idoft/gr-data.csv
      2025-12-09 20:43:43,983 - INFO - Queued 2 tasks for gr-data.csv.
      2025-12-09 20:43:44,574 - INFO - [gr-data.csv] Row 107: Status changed but could not be determined, remains Opened (https://github.com/apache/ignite-3/pull/4557. Please check manually.)
      2025-12-09 20:43:44,726 - INFO - [gr-data.csv] Row 108: Status remained Opened (https://github.com/apache/ignite-3/pull/4836)
      2025-12-09 20:43:44,726 - INFO - summary for gr-data.csv: 0 statuses updated, 1 changed but need manual check, 1 still open.
      2025-12-09 20:43:44,726 - INFO - Manual check log updated for gr-data.csv
    ```

  - `--pyrange`: Row range for py-data.csv (e.g., `43-43`)

    ```bash
    python prStatusCheck.py --pyrange 43-43  
      2025-12-09 20:43:21,857 - INFO - --- Processing py-data.csv ---
      2025-12-09 20:43:21,857 - INFO - Loading data from local file: $HOME/idoft/py-data.csv
      2025-12-09 20:43:21,862 - INFO - Queued 1 tasks for py-data.csv.
      2025-12-09 20:43:22,394 - INFO - [py-data.csv] Row 43: Status changed Opened -> Accepted (https://github.com/jazzband/docopt-ng/pull/20)
      2025-12-09 20:43:22,395 - INFO - summary for py-data.csv: 1 statuses updated, 0 changed but need manual check, 0 still open.
      2025-12-09 20:43:22,404 - INFO - Accepted log updated for py-data.csv
    ```

  - Or use all of them together

    ```bash
    python prStatusCheck.py --pyrange 43-43 --grrange 107-108 --prrange 3802-3804 
      2025-12-09 20:44:54,560 - INFO - --- Processing py-data.csv ---
      2025-12-09 20:44:54,560 - INFO - Loading data from local file: $HOME/idoft/py-data.csv
      2025-12-09 20:44:54,564 - INFO - Queued 1 tasks for py-data.csv.
      2025-12-09 20:44:55,044 - INFO - [py-data.csv] Row 43: Status changed Opened -> Accepted (https://github.com/jazzband/docopt-ng/pull/20)
      2025-12-09 20:44:55,044 - INFO - summary for py-data.csv: 1 statuses updated, 0 changed but need manual check, 0 still open.
      2025-12-09 20:44:55,050 - INFO - Accepted log updated for py-data.csv
      2025-12-09 20:44:55,050 - INFO - --- Processing pr-data.csv ---
      2025-12-09 20:44:55,050 - INFO - Loading data from local file: $HOME/idoft/pr-data.csv
      2025-12-09 20:44:55,081 - INFO - Queued 3 tasks for pr-data.csv.
      2025-12-09 20:44:55,493 - INFO - [pr-data.csv] Row 3802: Status changed but could not be determined, remains Opened (https://github.com/apache/tinkerpop/pull/1658. Please check manually.)
      2025-12-09 20:44:55,516 - INFO - [pr-data.csv] Row 3804: Status changed but could not be determined, remains Opened (https://github.com/apache/tinkerpop/pull/1658. Please check manually.)
      2025-12-09 20:44:55,584 - INFO - [pr-data.csv] Row 3803: Status changed but could not be determined, remains Opened (https://github.com/apache/tinkerpop/pull/1658. Please check manually.)
      2025-12-09 20:44:55,584 - INFO - summary for pr-data.csv: 0 statuses updated, 3 changed but need manual check, 0 still open.
      2025-12-09 20:44:55,584 - INFO - Manual check log updated for pr-data.csv
      2025-12-09 20:44:55,584 - INFO - --- Processing gr-data.csv ---
      2025-12-09 20:44:55,584 - INFO - Loading data from local file: $HOME/idoft/gr-data.csv
      2025-12-09 20:44:55,595 - INFO - Queued 2 tasks for gr-data.csv.
      2025-12-09 20:44:56,177 - INFO - [gr-data.csv] Row 107: Status changed but could not be determined, remains Opened (https://github.com/apache/ignite-3/pull/4557. Please check manually.)
      2025-12-09 20:44:56,416 - INFO - [gr-data.csv] Row 108: Status remained Opened (https://github.com/apache/ignite-3/pull/4836)
      2025-12-09 20:44:56,417 - INFO - summary for gr-data.csv: 0 statuses updated, 1 changed but need manual check, 1 still open.
      2025-12-09 20:44:56,417 - INFO - Manual check log updated for gr-data.csv
    ```

- **Behavior**:

  - If any range is specified: Only files with specified ranges are processed; others are skipped
  - If no range is specified: All three files are processed in full
  - Row numbers use actual CSV row numbers (header = row 1, first data = row 2)

#### 3. PR Status Query

There are three status mappings defined in this script:

- `state == "open"` → "Opened"
- `state == "closed" && merged == true` → "Accepted"
- `state == "closed" && merged == false` → "Unknown"

A pull request can be closed without being merged for various reasons. For example, it may be marked as *DeveloperFixed*, *Rejected*, or fall into other flaky test statuses defined in IDoFT. In some cases, the changes are actually merged through an alternative workflow. Since these situations cannot be reliably distinguished automatically, such pull requests are classified as unknown and logged to `manual-check.log` for further inspection.

##### Output File Description

| File                        | Description                                                 |
| --------------------------- | ----------------------------------------------------------- |
| `accepted.log`              | Records successfully updated to Accepted                    |
| `manual-check.log`          | Records requiring manual check (Unknown or other anomalies) |
| `pr-status-update.log`      | Complete runtime log                                        |
| `../../{pr,gr,py}-data.csv` | Updated data files                                          |

---

#### 4. Ignore List Support

To exclude specific tests, create a `ignore.csv` file under `idoft/auto-update-dataset`. Ignored Python and Java tests can coexist in the same file.

* Example `ignore.csv`

  ```csv
  name
  tk.mybatis.mapper.mapperhelper.FieldHelperTest.testUser
  tests/test_converter.py::TestConverter::test_to_idna_multiple_urls
  ```

##### 4.1 Example For Java

Assume that the 4th and 5th lines of `pr-data.csv` are as follows:

```csv
https://github.com/abel533/Mapper,1764748eedb2f320a0d1c43cb4f928c4ccb1f2f5,core,tk.mybatis.mapper.mapperhelper.FieldHelperTest.testComplex,ID,Accepted,https://github.com/abel533/Mapper/pull/896,Accepted in the PR https://github.com/abel533/Mapper/pull/666 but later reverted in the commit https://github.com/abel533/Mapper/commit/79d313a7ca6cba6c5d5323746fb83ed5744180a1
https://github.com/abel533/Mapper,1764748eedb2f320a0d1c43cb4f928c4ccb1f2f5,core,tk.mybatis.mapper.mapperhelper.FieldHelperTest.testUser,ID,Opened,https://github.com/abel533/Mapper/pull/896,Accepted in the PR https://github.com/abel533/Mapper/pull/666 but later reverted in the commit https://github.com/abel533/Mapper/commit/79d313a7ca6cba6c5d5323746fb83ed5744180a1
```

The output should match the following. Test on the 5th line is not processed.

```bash
python prStatusCheck.py --prrange 4-5
  2025-12-09 21:07:20,243 - INFO - Loading ignore list from $HOME/idoft/auto-update-dataset/ignore.csv
  2025-12-09 21:07:20,245 - INFO - --- Processing pr-data.csv ---
  2025-12-09 21:07:20,245 - INFO - Loading data from local file: $HOME/idoft/pr-data.csv
  2025-12-09 21:07:20,255 - INFO - Processing CSV rows 4-5
  2025-12-09 21:07:20,256 - INFO - Queued 1 tasks for pr-data.csv.
  2025-12-09 21:07:20,776 - INFO - [pr-data.csv] Row 4: Status changed Opened -> Accepted (https://github.com/abel533/Mapper/pull/896)
  2025-12-09 21:07:20,777 - INFO - summary for pr-data.csv: 1 statuses updated, 0 changed but need manual check, 0 still open.
  2025-12-09 21:07:20,796 - INFO - Accepted log updated for pr-data.csv
```

##### 4.2 Example for Python

Assume that rows between 1022 and 1024 of `pr-data.csv` are as follows:

```csv
https://github.com/PyFunceble/domain2idna,39a1c4e1ebb877ed511e53b618fbe437a685c970,tests/test_converter.py::TestConverter::test_to_idna_multiple,OD-Vic,Opened,https://github.com/PyFunceble/domain2idna/pull/4,
https://github.com/PyFunceble/domain2idna,39a1c4e1ebb877ed511e53b618fbe437a685c970,tests/test_converter.py::TestConverter::test_to_idna_multiple_urls,OD-Vic,Opened,https://github.com/PyFunceble/domain2idna/pull/4,
https://github.com/PyFunceble/domain2idna,39a1c4e1ebb877ed511e53b618fbe437a685c970,tests/test_converter.py::TestConverter::test_to_idna_single,OD-Vic,Opened,https://github.com/PyFunceble/domain2idna/pull/4,
```

The output should match the following. Test on 1023 line is not processed.

```bash
python prStatusCheck.py --pyrange 1022-1024
  2025-12-09 21:59:08,624 - INFO - Loading ignore list from $HOME/idoft/auto-update-dataset/ignore.csv
  2025-12-09 21:59:08,626 - INFO - --- Processing py-data.csv ---
  2025-12-09 21:59:08,626 - INFO - Loading data from local file: $HOME/idoft/py-data.csv
  2025-12-09 21:59:08,629 - INFO - Processing CSV rows 1022-1024
  2025-12-09 21:59:08,630 - INFO - Queued 2 tasks for py-data.csv.
  2025-12-09 21:59:09,000 - INFO - [py-data.csv] Row 1022: Status changed Opened -> Accepted (https://github.com/PyFunceble/domain2idna/pull/4)
  2025-12-09 21:59:09,018 - INFO - [py-data.csv] Row 1024: Status changed Opened -> Accepted (https://github.com/PyFunceble/domain2idna/pull/4)
  2025-12-09 21:59:09,018 - INFO - summary for py-data.csv: 2 statuses updated, 0 changed but need manual check, 0 still open.
  2025-12-09 21:59:09,023 - INFO - Accepted log updated for py-data.csv
```

#### 5. Data Source

- Prefers local CSV files if they exist (`../../{filename}` relative to script, i.e., `~/idoft/*.csv`)
- Falls back to GitHub remote repository if local file not found
- Writes updates to local files

---
