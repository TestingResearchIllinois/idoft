"""Runs the checkers and handles related errors and warnings."""

import sys
import logging
import errorhandler
from tso_iso_checker import run_checks_tso_iso
from tic_fic_checker import run_checks_tic_fic
from pr_checker import run_checks_pr
from utils import log_std_error, log_esp_error, log_warning

if __name__ == "__main__":
    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    log_std_error.tracker = 0
    log_esp_error.tracker = 0
    log_warning.tracker = 0
    commit_range = sys.argv[1:]
    checks = [run_checks_pr, run_checks_tic_fic, run_checks_tso_iso]
    for check in checks:
        check(logger, sys.argv[1:])
    ERROR_COUNT = str(log_std_error.tracker + log_esp_error.tracker)

    if error_handler.fired:
        logger.critical(
            "Failure: Exiting with code 1 due to %s logged %s",
            ERROR_COUNT,
            ("error" if ERROR_COUNT == "1" else "errors"),
        )
        raise SystemExit(1)

    if log_warning.tracker != 0:
        logger.info(
            "%s %s",
            str(log_warning.tracker),
            " warnings generated"
            if log_warning.tracker != 1
            else " warning generated",
        )
    logger.info("Success: Exiting with code 0 due to no logged errors")
