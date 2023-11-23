import json
import os
import csv
import sys
import errorhandler
import logging
from utils import (
    log_info,
    log_esp_error,
    log_std_error,
    log_warning
)


def combine_csvs(*input_csv_paths):
    combined_data = []

    for input_csv_path in input_csv_paths:
        with open(input_csv_path, "r") as input_file:
            reader = csv.reader(input_file)
            header = next(reader)
            combined_data.extend([row for row in reader])
    return combined_data


def check_csv(forked_data, *csv_file_path):
    project_urls_set = set()
    combined_data = combine_csvs(*csv_file_path)

    for row in combined_data:
        project_url = row[0]
        project_urls_set.add(project_url)

    # Read the forked JSON file
    with open("format_checker/forked-projects.json", "r") as json_file:
        forked_data = json.load(json_file)

    # Check if each entry in forked_projects is present in the set of project URLs
    anamalous_urls = []
    for forked_entry in forked_data:
        project_url = forked_entry
        if project_url not in project_urls_set:
            anamalous_urls.append(project_url)
    return anamalous_urls


def is_fp_sorted(data):
    sorted_data = dict(sorted(data.items()))
    list1 = list(data.items())
    list2 = list(sorted_data.items())
    return list1 == list2

def update_fp(data, file_path):
    sorted_data = dict(sorted(data.items()))

    with open(file_path, "w") as file:
        json.dump(sorted_data, file, indent=2)
        
def check_stale_fp(data, file_path, log):
    urls = check_csv(data, "pr-data.csv", "gr-data.csv", "py-data.csv")
    if len(urls) > 0:
        log_esp_error(file_path, log, "Missing urls in csv:")
        for url in urls:
            log_esp_error(file_path, log, url)
    else:
        log_info(file_path, log, "There are no changes to be checked")
        
    update_fp(data, file_path)


def run_checks_sort_fp(file_path, log):
    with open(file_path, "r") as file:
        data = json.load(file)
    if not is_fp_sorted(data):
        log_esp_error(file_path, log, "Entries are not sorted")
    else:
        log_info(file_path, log, "There are no changes to be checked")


def main():
    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    log_std_error.tracker = 0
    log_esp_error.tracker = 0
    log_warning.tracker = 0
    args = sys.argv[1:]
    file_path="format_checker/forked-projects.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    if "check-sort" in args:
        print(is_fp_sorted(data))
    elif "check-stale" in args:
        check_stale_fp(data,file_path, logger)
    elif "sort" in args:
        update_fp(data,file_path)
    else:
         log_esp_error(file_path, logger, f"{args[0]} is invalid")


if __name__ == "__main__":
    main()
