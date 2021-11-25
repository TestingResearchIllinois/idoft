"""Implements rule checks for the pr-data.csv file."""

import re
from utils import log_std_error, log_warning
from common_checks import (
    check_common_rules,
    check_row_length,
    check_sort,
    run_checks,
)


# Contains information and regexes unique to pr-data.csv
pr_data = {
    "columns": [
        "Project URL",
        "SHA Detected",
        "Module Path",
        "Fully-Qualified Test Name (packageName.ClassName.methodName)",
        "Category",
        "Status",
        "PR Link",
        "Notes",
    ],
    "Category": [
        "OD",
        "OD-Brit",
        "OD-Vic",
        "ID",
        "NOD",
        "NDOD",
        "NDOI",
        "NDOI",
        "UD",
    ],
    "Status": [
        "",
        "Opened",
        "Accepted",
        "InspiredAFix",
        "DevelopersDoNotWantFix",
        "DeveloperFixed",
        "RepoArchived",
        "Deleted",
        "Rejected",
        "Skipped",
        "MovedOrRenamed",
    ],
    "PR Link": re.compile(
        r"((https:\/\/github.com\/((\w|\.|-)+\/)+)(pull\/\d+))"
    ),
    "Notes": re.compile(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    ),
}


def check_category(filename, row, i, log):
    """Check validity of Category."""

    if not re.fullmatch(r"(\w+|-|\;)*\w+", row["Category"]) or not all(
        x in pr_data["Category"] for x in row["Category"].split(";")
    ):
        log_std_error(filename, log, i, row, "Category")


def check_status(filename, row, i, log):
    """Check validity of Status."""

    if not row["Status"] in pr_data["Status"]:
        log_std_error(filename, log, i, row, "Status")


def check_status_consistency(filename, row, i, log):
    """Check that the status is consistent with the requirements."""

    # Checks if Status is one of Accepted, Opened, Rejected
    # and checks for required information if so
    if row["Status"] in ["Accepted", "Opened", "Rejected"]:

        # The project apache/incubator-dubbo was renamed to apache/dubbo,
        # so the Project URL name (old) doesn't match the PR Link name
        # (new), despite them being the same project. This if statement is
        # a workaround for that issue.
        if (
            row["Project URL"] == "https://github.com/apache/incubator-dubbo"
            and re.sub(r"\/pull\/\d+", "", row["PR Link"]).casefold()
            == "https://github.com/apache/dubbo"
        ):
            pass
        else:
            check_pr_link(filename, row, i, log)

    if row["Status"] in ["InspiredAFix", "Skipped", "MovedOrRenamed"]:

        # Should contain a note
        if row["Notes"] == "":
            log_warning(
                filename,
                log,
                i,
                "Status " + row["Status"] + " should contain a note",
            )
        # If it contains a note, it should be a valid link
        else:
            check_notes(filename, row, i, log)

        # Should contain a PR Link
        if row["Status"] == "InspiredAFix":
            if row["PR Link"] == "":
                log_warning(
                    filename,
                    log,
                    i,
                    "Status " + row["Status"] + " should have a PR Link",
                )
            # If it contains a PR link, it should be a valid one
            else:
                check_pr_link(filename, row, i, log)

    if row["Status"] == "" and row["PR Link"] != "":
        check_pr_link(filename, row, i, log)
        log_std_error(filename, log, i, row, "Status should not be empty when a PR link is provided.")        

def check_notes(filename, row, i, log):
    """Checks validity of Notes."""

    if not pr_data["Notes"].fullmatch(row["Notes"]):
        log_std_error(filename, log, i, row, "Notes")


def check_pr_link(filename, row, i, log):
    """Checks validity of the PR Link."""

    if not pr_data["PR Link"].fullmatch(row["PR Link"]) or (
        re.sub(r"\/pull\/\d+", "", row["PR Link"]).casefold()
        != row["Project URL"].casefold()
    ):
        log_std_error(filename, log, i, row, "PR Link")


def run_checks_pr(log, commit_range):
    """Checks that pr-data.csv is properly formatted."""

    filename = "pr-data.csv"
    checks = [
        check_row_length,
        check_common_rules,
        check_category,
        check_status,
        check_status_consistency,
    ]
    run_checks(filename, pr_data, log, commit_range, checks)
    check_sort(filename, log)
