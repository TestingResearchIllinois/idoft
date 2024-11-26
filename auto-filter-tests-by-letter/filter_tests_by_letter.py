"""
This script filters rows from a CSV file based on specific criteria.

It identifies rows where the project name (extracted from a URL column) 
starts with a given letter and where the "Status" column is empty. 
The filtered rows are saved to a new CSV file.

Usage:
    python3 filter_tests_by_letter.py <letter> <file_path>

Arguments:
    letter: The starting letter of the project name to filter.
    file_path: The path to the input CSV file.
"""

import csv
import argparse
import sys


def filter_tests_by_letter(file_path: str, letter: str) -> tuple[list[str], list]:
    """
    Filters rows from a CSV file where the project name starts with a given letter
    and the "Status" column is empty.

    Args:
        file_path (str): The path to the input CSV file.
        letter (str): The letter to match at the start of project names.

    Returns:
        tuple[list[str], list]: A tuple containing:
            - The header row from the CSV file as a list of strings.
            - A list of rows that match the criteria, where each row is a list of values.
    """

    matching_lines = []
    header = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)
        url_index = header.index("Project URL")
        status_index = header.index("Status")

        for row in reader:
            project_url = row[url_index]
            project_name = project_url.split('/')[4]
            status = row[status_index]
            if project_name.lower().startswith(letter.lower()) and status == '':
                matching_lines.append(row)

    return header, matching_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find unique repos starting with a specific letter.')
    parser.add_argument('letter', type=str,
                        help='The starting letter of the project name')
    parser.add_argument('file_path', type=str, help='The path to the CSV file')

    args = parser.parse_args()

    output_header, filtered_lines = filter_tests_by_letter(
        args.file_path, args.letter)

    writer = csv.writer(sys.stdout)
    writer.writerow(output_header)
    writer.writerows(filtered_lines)
