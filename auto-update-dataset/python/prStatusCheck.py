import os
import sys
import argparse
import pandas as pd
import requests
import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pr-status-update.log")
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file at repo root
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, "../.."))
dotenv_path = os.path.join(repo_root, ".env")
load_dotenv(dotenv_path)

# Set up request headers
HEADERS = {}
if os.getenv("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {os.getenv('GITHUB_TOKEN')}"
else:
    logger.warning("GITHUB_TOKEN not set. Rate limits will be strict.")

# Regular expression to match GitHub URLs
GITHUB_URL_PATTERN = re.compile(r"github\.com/([^/]+)/([^/]+)/(?:issues|pull)/(\d+)")

# Cache for PR status lookups to avoid redundant API calls. Key: PR URL, Value: fetched status
pr_status_cache = {}

# Data Source URLs
DATA_URLS = {
    'py-data.csv': "https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/py-data.csv",
    'pr-data.csv': "https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/pr-data.csv",
    'gr-data.csv': "https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/gr-data.csv"
}

# File paths
IGNORE_PATH = os.path.abspath(os.path.join(script_dir, "../ignore.csv"))
REPORT_PATH = os.path.join(script_dir, "accepted.log")
MANUAL_CHECK_PATH = os.path.join(script_dir, "manual-check.log")

def fetch_status(url, original_status):    
    """
    Fetch PR status from GitHub API with caching.
    """
    
    def cache_and_return(url, result):
        """Cache the result and return it."""
        pr_status_cache[url] = result
        return result
    
    if url in pr_status_cache:
        logger.debug(f"Cache hit for {url}")
        return pr_status_cache[url] 
    match = GITHUB_URL_PATTERN.search(url)
    if not match:
        return cache_and_return(url, "Invalid URL")
    owner, repo, number = match.groups()
    pull_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"
    try:
        response = requests.get(pull_url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            state = data.get("state")
            if state == "open":
                result = "Opened"
            elif state == "closed":
                merged = data.get("merged", False)
                result = "Accepted" if merged else "Unknown"
            else:
                result = original_status
            return cache_and_return(url, result)
        elif response.status_code == 404:
            return cache_and_return(url, "PR Not Found")
        else:
            return "Fetch Error"
    except Exception as e:
        logger.warning(f"Exception fetching PR {url}: {e}.")
        return "Fetch Error"

def process_row(filename, index, row):
    """
    Only check for updates when the PR is in 'Opened' status.
    Other statuses (Accepted, Rejected, etc.) are treated as final and not re-checked.
    """
    url = row['PR Link']
    original_status = row['Status']
    csv_row = index + 2
    msg = ""
    if pd.isna(url) or "github.com" not in str(url):
        msg = f"[{filename}] Row {csv_row}: Invalid URL, Status: {original_status} ({url})"
        logger.info(msg)
        return index, original_status, False, url, msg
    new_status = fetch_status(url, original_status)
    changed = new_status != original_status
    if changed:
        if new_status == "Accepted":
            msg = f"[{filename}] Row {csv_row}: Status changed {original_status} -> {new_status} ({url})"
        elif new_status == "Invalid URL":
            msg = f"[{filename}] Row {csv_row}: Invalid URL, Status remains {original_status} ({url})"
        elif new_status == "PR Not Found":
            msg = f"[{filename}] Row {csv_row}: PR not found, Status remains {original_status} ({url})"
        elif new_status == "Fetch Error":
            msg = f"[{filename}] Row {csv_row}: Fetch error, Status remains {original_status} ({url}.)"
        else:
            msg = f"[{filename}] Row {csv_row}: Status changed but could not be determined, remains {original_status} ({url}. Please check manually.)"
    else:
        msg = f"[{filename}] Row {csv_row}: Status remained {new_status} ({url})"
    logger.info(msg)
    return index, new_status, changed, url, msg

def parse_range(range_str):
    if not range_str:
        return None, None
    try:
        parts = range_str.split('-')
        if len(parts) == 2:
            start_idx = int(parts[0])
            end_idx = int(parts[1])
            if start_idx > end_idx:
                logger.error(f"Invalid range: {range_str} (Start > End)")
                sys.exit(1)
            return start_idx, end_idx
        else:
            logger.error(f"Invalid range format: {range_str}. Use start-end.")
            sys.exit(1)
    except ValueError:
        logger.error(f"Invalid range values: {range_str}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Update PR statuses in CSV files.")
    parser.add_argument("--prrange", type=str,
                        help="Range of CSV rows for pr-data.csv (e.g., 100-200). If not specified, processes all rows. Uses actual CSV row numbers (header=row 1, first data=row 2). Inclusive.")
    parser.add_argument("--grrange", type=str,
                        help="Range of CSV rows for gr-data.csv (e.g., 100-200). If not specified, processes all rows. Uses actual CSV row numbers (header=row 1, first data=row 2). Inclusive.")
    parser.add_argument("--pyrange", type=str,
                        help="Range of CSV rows for py-data.csv (e.g., 100-200). If not specified, processes all rows. Uses actual CSV row numbers (header=row 1, first data=row 2). Inclusive.")
    parser.add_argument("--threads", type=int, default=10,
                        help="Number of threads to use for parallel processing.")
    args = parser.parse_args()
    file_ranges = {
        'pr-data.csv': parse_range(args.prrange),
        'gr-data.csv': parse_range(args.grrange),
        'py-data.csv': parse_range(args.pyrange),
    }
    ignored_paths = set()
    if os.path.exists(IGNORE_PATH):
        logger.info(f"Loading ignore list from {IGNORE_PATH}")
        try:
            ignore_df = pd.read_csv(IGNORE_PATH)
            if not ignore_df.empty:
                ignored_paths = set(ignore_df.iloc[:, 0].astype(str).tolist())
        except Exception as e:
            logger.warning(f"Failed to load ignore list: {e}")
    with open(REPORT_PATH, "w") as f:
        f.write(f"Accepted updates - {time.ctime()}\n")
    with open(MANUAL_CHECK_PATH, "w") as f:
        f.write(f"Please manually check - {time.ctime()}\n")
    any_range_specified = any(r[0] is not None for r in file_ranges.values())
    for filename, url in DATA_URLS.items():
        start_idx, end_idx = file_ranges.get(filename, (None, None))
        if any_range_specified and (start_idx is None or end_idx is None):
            continue
        logger.info(f"--- Processing {filename} ---")
        local_path = os.path.abspath(os.path.join(script_dir, f"../../{filename}"))
        if os.path.exists(local_path):
            logger.info(f"Loading data from local file: {local_path}")
            try:
                df = pd.read_csv(local_path)
            except Exception as e:
                logger.error(f"Failed to load local file {local_path}: {e}")
                continue
        else:
            logger.info(f"Local file not found, loading from remote: {url}")
            try:
                df = pd.read_csv(url)
            except Exception as e:
                logger.error(f"Failed to load data from URL {url}: {e}")
                continue
        line_cache = {}
        if os.path.exists(local_path):
            with open(local_path, 'r', newline='', encoding='utf-8') as f:
                line_cache = {i: line for i, line in enumerate(f, start=1)}
        test_name_col = "Fully-Qualified Test Name (packageName.ClassName.methodName)"
        if filename == "py-data.csv":
            test_name_col = "Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod)"
        tasks = []
        num_threads = args.threads
        file_report_lines = []
        manual_check_lines = []
        lines_to_restore = set()
        if start_idx is None or end_idx is None:
            pandas_start = 0
            pandas_end = len(df) - 1
            logger.info(f"No range specified, processing all {len(df)} rows")
        else:
            pandas_start = start_idx - 2
            pandas_end = end_idx - 2
            if pandas_start < 0:
                logger.error(f"Invalid range: CSV rows must be >= 2 (row 1 is header). Got {start_idx}")
                continue
            logger.info(f"Processing CSV rows {start_idx}-{end_idx}")
        rows_to_process = df.iloc[pandas_start: pandas_end + 1]
        if rows_to_process.empty:
            logger.info(f"No rows to process for {filename}")
            continue
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for index, row in rows_to_process.iterrows():
                csv_row = index + 2
                status = str(row['Status'])
                if test_name_col in df.columns:
                    test_name = str(row[test_name_col])
                    if test_name in ignored_paths:
                        lines_to_restore.add(csv_row)
                        continue
                if "Opened" not in status:
                    lines_to_restore.add(csv_row)
                    continue
                tasks.append(executor.submit(process_row, filename, index, row))
            logger.info(f"Queued {len(tasks)} tasks for {filename}.")
            updated_count = 0
            changed_count = 0
            still_open_count = 0
            for future in as_completed(tasks):
                try:
                    idx, new_status, changed, pr_url, log_msg = future.result()
                    csv_row = idx + 2
                    if changed:
                        if new_status == "Accepted":
                            df.at[idx, 'Status'] = new_status
                            updated_count += 1
                            file_report_lines.append(log_msg)
                        else:
                            lines_to_restore.add(csv_row)
                            manual_check_lines.append(log_msg)
                            changed_count += 1
                    else:
                        lines_to_restore.add(csv_row)
                        still_open_count += 1
                except Exception as e:
                    logger.error(f"Task failed: {e}")
        logger.info(f"summary for {filename}: {updated_count} statuses updated, {changed_count} changed but need manual check, {still_open_count} still open.")
        if updated_count > 0:
            df.to_csv(local_path, index=False)
            if lines_to_restore and line_cache:
                with open(local_path, 'r', newline='', encoding='utf-8') as f:
                    lines = f.readlines()
                for ln in lines_to_restore:
                    if ln <= len(lines) and ln in line_cache:
                        lines[ln - 1] = line_cache[ln]
                with open(local_path, 'w', newline='', encoding='utf-8') as f:
                    f.writelines(lines)
                logger.info(f"Restored {len(lines_to_restore)} unchanged lines")
        if file_report_lines:
            with open(REPORT_PATH, "a") as f:
                for line in file_report_lines:
                    f.write(line + "\n")
            logger.info(f"Accepted log updated for {filename}")
        if manual_check_lines:
            with open(MANUAL_CHECK_PATH, "a") as f:
                for line in manual_check_lines:
                    f.write(line + "\n")
            logger.info(f"Manual check log updated for {filename}")

if __name__ == "__main__":
    main()