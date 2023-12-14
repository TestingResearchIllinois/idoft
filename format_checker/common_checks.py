"""Contains implementations of rules that are common to all dataset files"""

import re
import csv
import subprocess
from utils import (
    get_committed_lines,
    get_uncommitted_lines,
    log_info,
    log_std_error,
    log_esp_error,
)


# Contains regexes for columns that are commmon to pr-data, gr-data and tic-fic-data
common_data = {
    "Project URL": re.compile(r"(https:\/\/github.com)(\/(\w|\.|-)+){2}(?<!\.git)$"),
    "SHA": re.compile(r"\b[0-9a-f]{40}\b"),
    "Module Path": re.compile(r"((\w|\.|-)+(\/|\w|\.|-)*)|^$"),
    "Fully-Qualified Name": re.compile(
        r"((\w|\s)+\.)+(\w+|\d+|\W+)+(\[((\d+)|(\w+|\s)+)\])?"
    ),
}


def check_header(header, valid_dict, filename, log):
    """Validates that the header is correct."""

    if not header == valid_dict["columns"]:

        # Check that columns are properly formatted
        log_esp_error(filename, log, "The header is improperly formatted")


def check_common_rules(filename, row, i, log):
    """
    Checks validity of Project URL, SHA Detected, Module Path,
    Fully-Qualified Test Name (packageName.ClassName.methodName).
    """

    if not common_data["Project URL"].fullmatch(row["Project URL"]):
        log_std_error(filename, log, i, row, "Project URL")
    if not common_data["SHA"].fullmatch(row["SHA Detected"]):
        log_std_error(filename, log, i, row, "SHA Detected")
    if not common_data["Module Path"].fullmatch(row["Module Path"]):
        log_std_error(filename, log, i, row, "Module Path")
    if not common_data["Fully-Qualified Name"].fullmatch(
        row["Fully-Qualified Test Name (packageName.ClassName.methodName)"]
    ) or '#' in row["Fully-Qualified Test Name (packageName.ClassName.methodName)"]:
        log_std_error(
            filename,
            log,
            i,
            row,
            "Fully-Qualified Test Name (packageName.ClassName.methodName)",
        )


def check_row_length(header_len, filename, row, i, log):
    """Checks that each row has the required length."""

    if len(row) != header_len:
        log_esp_error(
            filename,
            log,
            "On row "
            + str(i)
            + ", row length should be "
            + str(header_len)
            + " but is "
            + str(len(row)),
        )


def check_sort(filename, log):
    """Checks order of a file."""

    command = (
        'echo "$(head -n1 '
        + filename
        + " && tail -n +2 "
        + filename
        + ' | LC_ALL=C sort -k1,1 -k4,4 -t, -f)" >  sorted-'
        + filename
        + "; diff "
        + filename
        + " sorted-"
        + filename
        + "; rm sorted-"
        + filename
    )
    diff = subprocess.check_output(command, shell=True).decode("utf-8")
    if diff != "":
        log_esp_error(filename, log, "The file is not properly ordered")
        print("Refer to IDoFT readme for how " + filename + " should be sorted: https://github.com/TestingResearchIllinois/idoft#to-contribute-a-newly-detected-flaky-test")
        print("Differences between current order and expected order:")
        print(diff)


def check_duplication(filename, log):
    """Check for duplicated lines in a file"""

    command = f'sort {filename} | uniq -cd'
    diff = subprocess.check_output(command, shell=True).decode("utf-8")
    if diff != "":
        log_esp_error(filename, log, "The file contains duplicated lines")
        print("Duplicated lines:")
        print(diff)


def run_checks(file, data_dict, log, commit_range, checks):
    """Checks rule compliance for any given dataset file."""

    committed_lines = get_committed_lines(file, commit_range)
    uncommitted_lines = get_uncommitted_lines(file)
    with open(file, newline="") as csvfile:
        info = csv.DictReader(csvfile, data_dict["columns"])
        header = next(info)
        if "1" in uncommitted_lines or "1" in committed_lines:
            check_header(list(header.values()), data_dict, file, log)
        if uncommitted_lines != [] or committed_lines != []:
            for i, row in enumerate(info):
                i += 2
                line = str(i)
                # The line is either:
                # (1) only uncommitted (needs to always bechecked locally),
                # (2) only committed (needs to always be checked in CI) or
                # (3) both in the unpushed commits and uncommitted (which in
                # practice is the same as (1)--the committed one is
                # deprecated--)
                if (line in uncommitted_lines) or (line in committed_lines):
                    params = [file, row, line, log]
                    for check_rule in checks:
                        if check_rule.__name__ == check_row_length.__name__:
                            check_rule(len(header), *params)
                            continue
                        check_rule(*params)
        else:
            log_info(file, log, "There are no changes to be checked")

    with open(file, 'rb') as fp:
        for line in fp:
            if line.endswith(b'\r\n'):
                log_esp_error(file, log, "Incorrect End of Line encoding")
                break
