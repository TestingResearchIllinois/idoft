"""Implements rule checks for the tso-iso-rates.csv file."""

import re
from utils import log_std_error
from common_checks import (
    check_common_rules,
    check_row_length,
    run_checks,
)

# Contains information and data unique to tso-iso-rates.csv
tso_iso_rates = {
    "columns": [
        "Project URL",
        "SHA Detected",
        "Module Path",
        "Fully-Qualified Test Name (packageName.ClassName.methodName)",
        "Number Of Test Failures In Test Suite",
        "Number Of Test Runs In Test Suite",
        "P-Value",
        "Is P-Value Less Or Greater Than 0.05",
        "Total Runs In Test Suite",
        "Number of Times Test Passed In Test Suite",
        "Total Runs In Isolation",
        "Number of Times Test Passed In Isolation",
    ],
    "Failures/Runs": re.compile(r"\((\d+\;)+\d+\)"),
    "P-Value": re.compile(r"\d(\.\d+(E-\d+)?)?"),
    "Less/Greater": re.compile(r"(less)|(greater)"),
    "Last 4": re.compile(r"\d+"),
}


def check_totals(filename, row, i, log):
    """
    Checks validity of Total Runs In Test Suite, Number of Times Test
    Passed In Test Suite, Total Runs In Isolation and Number of Times
    Test Passed In Isolation.
    """

    keys = [
        "Total Runs In Test Suite",
        "Number of Times Test Passed In Test Suite",
        "Total Runs In Isolation",
        "Number of Times Test Passed In Isolation",
    ]
    for key in keys:
        if not tso_iso_rates["Last 4"].fullmatch(row[key]):
            log_std_error(filename, log, i, row, key)


def check_less_greater(filename, row, i, log):
    """Checks validity of Is P-Value Less Or Greater Than 0.05."""

    if not tso_iso_rates["Less/Greater"].fullmatch(
        row["Is P-Value Less Or Greater Than 0.05"]
    ):
        log_std_error(
            filename, log, i, row, "Is P-Value Less Or Greater Than 0.05"
        )


def check_pvalue(filename, row, i, log):
    """Checks validity of P-Value."""

    if not tso_iso_rates["P-Value"].fullmatch(row["P-Value"]):
        log_std_error(filename, log, i, row, "P-Value")


def check_num_runs(filename, row, i, log):
    """Checks validity of Number Of Test Runs In Test Suite."""

    if not tso_iso_rates["Failures/Runs"].fullmatch(
        row["Number Of Test Runs In Test Suite"]
    ):
        log_std_error(
            filename, log, i, row, "Number Of Test Runs In Test Suite"
        )


def check_num_failures(filename, row, i, log):
    """Checks validity of Number Of Test Failures In Test Suite."""

    if not tso_iso_rates["Failures/Runs"].fullmatch(
        row["Number Of Test Failures In Test Suite"]
    ):
        log_std_error(
            filename, log, i, row, "Number Of Test Failures In Test Suite"
        )


def run_checks_tso_iso(log, commit_range):
    """Checks that tso-iso-data.csv is properly formatted."""

    checks = [
        check_row_length,
        check_common_rules,
        check_num_failures,
        check_num_runs,
        check_pvalue,
        check_less_greater,
        check_totals,
    ]
    run_checks("tso-iso-rates.csv", tso_iso_rates, log, commit_range, checks)
    