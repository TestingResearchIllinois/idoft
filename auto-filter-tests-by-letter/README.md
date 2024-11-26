# Filter Tests Script

This script filters rows from a CSV file based on specific criteria and writes the results to a new CSV file. It is designed to find repository names starting with a specified letter and having an empty `Status` column.

## Requirements

- Python 3.9 or later
- CSV file with the following columns (at a minimum):
  - A column containing repository URLs name `Project URL`.
  - A column named `Status`.

## Usage

1. Run the script

```
python3 filter_tests_by_letter.py <letter> <file_path>
```

Parameters:
<letter>: The letter that repository names should start with (case-insensitive).
<file_path>: Path to the CSV file to process.

Example:

```
python3 filter_tests_by_letter.py b ../pr-data.csv
```

This will print to the terminal all repositories in pr-data.csv that start with the letter B and have an empty Status column.
