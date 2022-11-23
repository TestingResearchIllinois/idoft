import csv
import sys
import logging
import errorhandler
from pr_checker import check_forked_project
from utils import log_std_error, log_esp_error, log_warning

if __name__ == "__main__":
    filename = "pr-data.csv"
    error_handler = errorhandler.ErrorHandler()
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    log_std_error.tracker = 0
    log_esp_error.tracker = 0
    log_warning.tracker = 0
    checked = []
    auth = (sys.argv[1], sys.argv[2])
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if check_forked_project(filename, row, "", logger, auth):
                checked.append(row)
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, checked[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(checked)



