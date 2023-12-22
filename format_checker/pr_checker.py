"""Implements rule checks for the pr-data.csv file."""

import re
import json
from utils import log_std_error, log_warning
from common_checks import (
    check_common_rules,
    check_row_length,
    check_sort,
    run_checks,
    check_duplication
)


# Contains information and regexes unique to pr-data.csv and gr-data.csv files
data = {
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
        "ID-HtF",
        "NIO",
        "NOD",
        "NDOD",
        "NDOI",
        "NDOI",
        "UD",
        "OSD"
    ],
    "Status": [
        "",
        "Opened",
        "Accepted",
        "InspiredAFix",
        "DeveloperWontFix",
        "DeveloperFixed",
        "RepoArchived",
        "RepoDeleted",
        "Deprecated",
        "Deleted",
        "Rejected",
        "Skipped",
        "MovedOrRenamed",
        "Claimed",
        "MovedToGradle",
        "FixedOrder",
        "Unmaintained"
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
        x in data["Category"] for x in row["Category"].split(";")
    ):
        log_std_error(filename, log, i, row, "Category")


def check_status(filename, row, i, log):
    """Check validity of Status."""

    if not row["Status"] in data["Status"]:
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

    if row["Status"] in ["InspiredAFix", "Skipped", "MovedOrRenamed", "Deprecated", "Deleted"]:

        # Should contain a note
        if row["Notes"] == "":
            # warning if no note:
            if row["Status"] in ["InspiredAFix", "Skipped", "Deprecated"]:
                log_warning(
                    filename,
                    log,
                    i,
                    "Status " + row["Status"] + " should contain a note",
                )
            # error if no note:
            if row["Status"] in ["MovedOrRenamed", "Deleted"]:
                log_std_error(filename, log, i, row, "Notes")

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
        if row["PR Link"] != "":
            check_pr_link(filename, row, i, log)

    if row["Status"] == "" and row["PR Link"] != "":
        check_pr_link(filename, row, i, log)
        log_std_error(filename, log, i, row, "Status", "Status should not be empty when a PR link is provided.")


def check_notes(filename, row, i, log):
    """Checks validity of Notes."""

    if not data["Notes"].fullmatch(row["Notes"]):
        log_std_error(filename, log, i, row, "Notes")


def check_forked_project(filename, row, i, log):
    """Checks forked project."""
    proj_url = row["Project URL"]
    if proj_url not in projects:
        log_std_error(filename, log, i, row, "Project URL", "Please add the new project to format_checker/forked-projects.json")
    if proj_url in projects and projects[proj_url] == "forked":
        log_std_error(filename, log, i, row, "Project URL", "Forked project")


def check_pr_link(filename, row, i, log):
    """Checks validity of the PR Link."""

    if not data["PR Link"].fullmatch(row["PR Link"]) or (
        re.sub(r"\/pull\/\d+", "", row["PR Link"]).casefold()
        != row["Project URL"].casefold()
    ):
        log_std_error(filename, log, i, row, "PR Link")


def check_tab(filename, row, i, log):
    """Checks that there is no tab in the row."""

    for key, value in row.items():
        if '\t' in value:
            log_std_error(filename, log, i, row, key, "There are TAB characters in this field")


def run_checks_pr(filename, log, commit_range):
    """Checks that the given file is properly formatted."""

    with open("format_checker/forked-projects.json", "r") as f:
        global projects
        projects = json.load(f)
    checks = [
        check_row_length,
        check_common_rules,
        check_category,
        check_status,
        check_status_consistency,
        check_forked_project,
        check_tab,
    ]
    run_checks(filename, data, log, commit_range, checks)
    check_sort(filename, log)
    check_duplication(filename, log)
