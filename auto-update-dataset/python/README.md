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
![image](https://user-images.githubusercontent.com/46290389/142753068-c5234bb5-d037-49c5-bf6a-b238f650eb3f.png)
