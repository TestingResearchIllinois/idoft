"""Implements rule checks for the tic-fic-data.csv file."""

import re
from utils import log_std_error
from common_checks import (
    common_data,
    check_common_rules,
    check_row_length,
    run_checks,
)


# Contains information and regexes unique to tic-fic-data.csv
tic_fic_data = {
    "columns": [
        "Project URL",
        "SHA Detected",
        "Module Path",
        "Fully-Qualified Test Name (packageName.ClassName.methodName)",
        "TIC = FIC",
        "Test-Introducing Commit SHA",
        "Test-Introducing Commit Fully-Qualified Test Name",
        "Test-Introducing Commit Module Path",
        "Flakiness-Introducing Commit SHA",
        "Flaky Test File Modified",
        "Other Test Files Modified",
        "Code Under Test Files Modified",
        "Build Related Files Modified",
        "Commits Between TIC-FIC Modifying Flaky Test Class",
        "Commits Between TIC-FIC Modifying Other Test Files",
        "Commits Between TIC-FIC Modifying Code Under Test Files",
        "Commits Between TIC-FIC Modifying Build Related Files",
        "Commits Between TIC-FIC",
        "Days Between TIC-FIC",
    ],
    "TIC = FIC": re.compile(r"(TRUE)|(FALSE)"),
    "Modified": re.compile(r"(TRUE)|(FALSE)|^$"),
    "Commits Between": re.compile(r"\d+|^$"),
    "Days Between TIC-FIC": re.compile(r"(\d+\.\d+)|^$"),
}


def check_days_between(filename, row, i, log):
    """Checks validity of Days Between TIC-FIC."""

    if not tic_fic_data["Days Between TIC-FIC"].fullmatch(
        row["Days Between TIC-FIC"]
    ):
        log_std_error(filename, log, i, row, "Days Between TIC-FIC")


def check_mods(filename, row, i, log):
    """
    Checks validity of Flaky Test File Modified, Other Test Files Modified,
    Code Under Test Files Modified and Build Related Files Modified.
    """

    keys = [
        "Flaky Test File Modified",
        "Other Test Files Modified",
        "Code Under Test Files Modified",
        "Build Related Files Modified",
    ]
    for key in keys:
        if not tic_fic_data["Modified"].fullmatch(row[key]):
            log_std_error(filename, log, i, row, key)


def check_fic_sha(filename, row, i, log):
    """Checks of Flakiness-Introducing Commit SHA."""

    if not common_data["SHA"].fullmatch(
        row["Flakiness-Introducing Commit SHA"]
    ):
        log_std_error(
            filename, log, i, row, "Flakiness-Introducing Commit SHA"
        )


def check_tic_mp(filename, row, i, log):
    """Checks validity of Test-Introducing Commit Module Path."""

    if not common_data["Module Path"].fullmatch(
        row["Test-Introducing Commit Module Path"]
    ):
        log_std_error(
            filename, log, i, row, "Test-Introducing Commit Module Path"
        )


def check_tic_fqn(filename, row, i, log):
    """Checks validity of Test-Introducing Commit Fully-Qualified Test Name."""

    if not common_data["Fully-Qualified Name"].fullmatch(
        row["Test-Introducing Commit Fully-Qualified Test Name"]
    ):
        log_std_error(
            filename,
            log,
            i,
            row,
            "Test-Introducing Commit Fully-Qualified Test Name",
        )


def check_tic_sha(filename, row, i, log):
    """Checks validity of Test-Introducing Commit SHA."""

    if not common_data["SHA"].fullmatch(row["Test-Introducing Commit SHA"]):
        log_std_error(filename, log, i, row, "Test-Introducing Commit SHA")


def check_tic_eq_fic(filename, row, i, log):
    """Checks validity of TIC = FIC."""

    if not tic_fic_data["TIC = FIC"].fullmatch(row["TIC = FIC"]):
        log_std_error(filename, log, i, row, "TIC = FIC")


def run_checks_tic_fic(log, commit_range):
    """Checks that tic-fic-data.csv is properly formatted."""

    checks = [
        check_row_length,
        check_common_rules,
        check_tic_eq_fic,
        check_tic_sha,
        check_tic_fqn,
        check_tic_mp,
        check_fic_sha,
        check_mods,
        check_days_between,
    ]
    run_checks("tic-fic-data.csv", tic_fic_data, log, commit_range, checks)
