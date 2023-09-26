import csv
import sys
import json
import logging
import requests


def check_existing_project(projects, row, auth):
    proj_url = row["Project URL"]
    if proj_url not in projects:
        splitted_url = proj_url.split("/")
        author = splitted_url[-2]
        repo = splitted_url[-1]

        url = "https://api.github.com/repos/{}/{}".format(author, repo)
        try:
            resp = requests.get(url, auth=auth).json()
            print(resp)
            if resp.get("fork"):
                logging.info("forked project: ", proj_url)
                projects[proj_url] = "forked"
            else:
                projects[proj_url] = "unforked"
        except requests.exceptions.RequestException:
            logging.info("RequestException: ", proj_url)
            return False
    return projects, projects[proj_url] == "unforked"


if __name__ == "__main__":
    filename = "pr-data.csv"
    with open("format_checker/forked-projects.json", "r") as f:
        projects = json.load(f)
    checked = []
    auth = (sys.argv[1], sys.argv[2])
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            projects, unforked = check_existing_project(projects, row, auth)
            if unforked:
                checked.append(row)
    with open("format_checker/forked-projects.json", "w") as f:
        json.dump(projects, f)
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, checked[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(checked)
