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
    run_checks_pr(logger)
    run_checks_tic_fic(logger)
    run_checks_tso_iso(logger)
    error_count = str(log_std_error.tracker + log_esp_error.tracker)
    if error_handler.fired:
        logger.critical(
            'Failure: Exiting with code 1 due to ' +
            error_count +
            ' logged ' + ('error' if error_count == '1' else 'errors'))
        raise SystemExit(1)
    else:
        if log_warning.tracker != 0:
            logger.info(str(log_warning.tracker) +
                        (' warnings generated' if log_warning.tracker != 1 else ' warning generated'))
        logger.info('Success: Exiting with code 0 due to no logged errors')
