"""Contains helper functions used in other modules."""

import re
import subprocess


def get_commit_list(commit_range):
    """
    Turns the commit range into a useful list of commits (the ones
    contained in the push/PR).
    """

    # If there is no commit range, it must be because the tool is running
    # locally, so get the list of commits from origin/<current-branch> to the
    # last commit made
    if commit_range == []:
        commit_range = (
            subprocess.check_output(
                "git log --oneline origin/"
                + '$(git branch | grep "\\* *" | cut -d " " -f 2)..'
                + '$(git rev-parse --short HEAD) | cut -d " " -f 1',
                shell=True,
            )
            .decode("utf-8")
            .split("\n")[:-1]
        )

    # If it's the first push to a new branch, the event.before commit
    # will consist of 40 zeroes. This needs to be handled separately
    elif len(commit_range) >= 3 and re.fullmatch(r"0{40}", commit_range[0]):
        commit_range = [commit_range[1][:7]] + subprocess.check_output(
            "git log --oneline "
            + str(commit_range[1])
            + ".."
            + str(commit_range[2])
            + ' | cut -d " " -f 1',
            shell=True,
        ).decode("utf-8").split("\n")[:-1]
    else:
        commit_range = (
            subprocess.check_output(
                "git log --oneline "
                + str(commit_range[0])
                + ".."
                + str(commit_range[1])
                + ' | cut -d " " -f 1',
                shell=True,
            )
            .decode("utf-8")
            .split("\n")[:-1]
        )
    return commit_range


def get_committed_lines(filename, commit_range):
    """
    Computes which lines have been modified in the commits contained in the
    push/PR.
    """

    commit_list = get_commit_list(commit_range)
    if commit_list != []:
        commit_list = "\\|".join(commit_list)
        command = (
            "git blame "
            + filename
            + " | grep -n '"
            + commit_list
            + "' | cut -f1 -d:"
        )
        committed_lines = subprocess.check_output(command, shell=True)
        committed_lines = committed_lines.decode("utf-8").split("\n")[:-1]
        return committed_lines
    return commit_list


def get_uncommitted_lines(filename):
    """
    Computes which lines have been modified in filename
    but not yet committed.
    """

    command = "git blame " + filename + " | grep -n '^0\\{8\\} ' | cut -f1 -d:"
    uncommitted_lines = subprocess.check_output(command, shell=True)
    uncommitted_lines = uncommitted_lines.decode("utf-8").split("\n")[:-1]
    return uncommitted_lines


def log_info(filename, log, message):
    """Logs a merely informational message."""

    log.info("INFO: On file " + filename + ": " + message)


def log_std_error(filename, log, line, row, key, message="Unspecified"):
    """Logs a standard error."""

    log_std_error.tracker += 1
    log.error(
        "ERROR: On file "
        + filename
        + ", row "
        + line
        + ":\n"
        + "Invalid "
        + key
        + ': "'
        + row[key]
        + '", Reason: '
        + message
    )


def log_esp_error(filename, log, message):
    """Logs a special error."""

    log_esp_error.tracker += 1
    log.error("ERROR: On file " + filename + ": " + message)


def log_warning(filename, log, line, message):
    """Logs a warning."""

    log_warning.tracker += 1
    log.warning(
        "WARNING: On file " + filename + ", row " + line + ": \n" + message
    )
