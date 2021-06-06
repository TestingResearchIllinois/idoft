import re
import csv
import subprocess

# Contains regexs for columns that are commmon to pr-data and tic-fic-data

common_data = {
    'Project URL': re.compile(r'(https:\/\/github.com)(\/(\w|\.|-)+){2}'),
    'SHA': re.compile(r'\b[0-9a-f]{40}\b'),
    'Module Path': re.compile(r'((\w|\.|-)+(\/|\w|\.|-)*)|^$'),
    'Fully-Qualified Name': re.compile(r'((\w|\s)+\.)+(\w+|\d+|\W+)+(\[((\d+)|(\w+|\s)+)\])?')
}

# Computes which lines have been modified in the last commit


def get_committed_lines(filename, commit_range):
    if commit_range == []:
        commit_range = subprocess.check_output(
            "git log --oneline origin/$(git branch | grep \'\\* *\' | cut -d \" \" -f 2)..$(git rev-parse --short HEAD) | cut -d \" \" -f 1",
            shell=True).decode("utf-8").split('\n')[:-1]
    commit_range = "\\|".join(commit_range)
    command = "git blame " + filename + \
        " | grep -n \'" + commit_range + "\' | cut -f1 -d:"
    committed_lines = subprocess.check_output(command, shell=True)
    committed_lines = committed_lines.decode("utf-8").split('\n')[:-1]
    return committed_lines

# Computes which lines have been modified in filename but not yet committed


def get_uncommitted_lines(filename):
    command = "git blame " + filename + " | grep -n '^0\\{8\\} ' | cut -f1 -d:"
    uncommitted_lines = subprocess.check_output(command, shell=True)
    uncommitted_lines = uncommitted_lines.decode("utf-8").split('\n')[:-1]
    return uncommitted_lines

# Logs a merely informational message


def log_info(filename, log, message):
    log.info("INFO: On file " + filename + ": " + message)

# Logs a standard error


def log_std_error(filename, log, line, row, key):
    log_std_error.tracker += 1
    log.error("ERROR: On file " + filename + ", row " + str(line) +
              ":\n" + "Invalid " + key + ": \"" + row[key] + "\"")

# Logs a special error


def log_esp_error(filename, log, message):
    log_esp_error.tracker += 1
    log.error("ERROR: On file " + filename + ": " + message)


def log_warning(filename, log, line, message):
    log_warning.tracker += 1
    log.warning(
        "WARNING: On file " +
        filename +
        ", row " +
        str(line) +
        ": \n" +
        message)

# Validates that the header is correct


def check_header(header, valid_dict, filename, log):
    if not header == valid_dict['columns']:
        # Check that columns are properly formatted
        log_esp_error(filename, log, "The header is improperly formatted")

# Checks validity of Project URL, SHA Detected, Module Path,
# Fully-Qualified Test Name (packageName.ClassName.methodName)


def check_common_rules(filename, row, i, log):
    if not common_data['Project URL'].fullmatch(row['Project URL']):
        log_std_error(filename, log, i, row, 'Project URL')
    if not common_data['SHA'].fullmatch(row['SHA Detected']):
        log_std_error(filename, log, i, row, 'SHA Detected')
    if not common_data['Module Path'].fullmatch(row['Module Path']):
        log_std_error(filename, log, i, row, 'Module Path')
    if not common_data['Fully-Qualified Name'].fullmatch(
            row['Fully-Qualified Test Name (packageName.ClassName.methodName)']):
        log_std_error(
            filename,
            log,
            i,
            row,
            'Fully-Qualified Test Name (packageName.ClassName.methodName)')

# Checks that each row has the required length


def check_row_length(filename, row, i, log, header_len):
    if len(row) != header_len:
        log_std_error(filename, log, i, 'row length', str(row))

# Check order of a file


def check_sort(filename, log):
    command = "echo \"$(head -n1 " + filename + " && tail +2 " + filename + " | LC_ALL=C sort -k1,1 -k4,4 -t, -f)\" >  sorted-" + \
        filename + "; diff " + filename + " sorted-" + filename + "; rm sorted-" + filename
    diff = subprocess.check_output(command, shell=True).decode("utf-8")
    if diff != "":
        log_esp_error(filename, log, "The file is not properly ordered")
