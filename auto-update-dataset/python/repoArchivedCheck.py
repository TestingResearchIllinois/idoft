import pandas as pd
import time
from requests_html import HTMLSession
import sys

# Mapping of file names to URLs
data_urls = {
    'py-data.csv': "https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/py-data.csv",
    'pr-data.csv': "https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/pr-data.csv",
    'gr-data.csv': "https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/gr-data.csv"
}


# it takes about 2 minutes to check 200 projects
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in data_urls:
        print("Usage: python script.py [py-data.csv | pr-data.csv | gr-data.csv]")
        sys.exit(1)
    # get unique urls from passed filename, we can also use cmd: `git pull -r ; cut -f1 -d,  `filename` | uniq`
    file_name = sys.argv[1]
    pr_data_url = data_urls[file_name]
    urls = pd.read_csv(pr_data_url, usecols=["Project URL"])
    urls = list(set([i[0] for i in urls.values.tolist()]))
    print("load data from", pr_data_url)

    # copy the first line of raw cvs.file here:
    csv_first_line = "Project URL,SHA Detected,Module Path,Fully-Qualified Test Name (packageName.ClassName.methodName),Category,Status,PR Link,Notes"
    if file_name == "py-data.csv":
        csv_first_line = "Project URL,SHA Detected,Pytest Test Name (PathToFile::TestClass::TestMethod or PathToFile::TestMethod),Category,Status,PR Link,Notes"
    cols = csv_first_line.split(",")
    status_idx = cols.index("Status") + 1  # we add linenumber into the cols later
    notes = cols.index("Notes") + 1
    data = pd.read_csv(pr_data_url, usecols=cols)

    data = data.values  # get an array of array
    my_dict = {}  # {url:[[line_num, url, sha, path, ...], [...], ...],}
    line_number = 2
    for i in data:
        if i[0] not in my_dict:  # i[0] == project_url
            my_dict[i[0]] = []
        line = list(i)
        line.insert(0, line_number)
        my_dict[i[0]].append(line)
        line_number += 1

    archived = []
    anomaly = []
    begin = time.time()
    cnt = 1
    t1 = begin
    for url in urls:
        session = HTMLSession()
        r = session.get(url)
        if r.status_code != 200 and r.status_code != 429:  # no need to report 429("Too Many Requests response"), 200("OK")
            anomaly.append([r.status_code, url])
            print("anomaly[status_code, url]:", r.status_code, url)
        if cnt % 10 == 0:  # print every 10 repos
            print("count: ", str(cnt)),
            print("time used: ", time.time() - t1, "s")
            t1 = time.time()
        cnt += 1
        div = r.html.find('#js-repo-pjax-container > div.flash.flash-warn.flash-full.border-top-0.text-center.text-bold.py-2', first=True)
        if div and "This repository has been archived by the owner" in div.text:
            archived.append(url)
            print("archived: ", url)
    end = time.time()

    print("\n===========\n[summary]")
    print("1.total time: ", end-begin, "s")
    print("")

    print("2.repoArchived: ")
    for i in archived:
        print("    ", i)
    update = []
    for i in archived:
        for j in my_dict[i]:
            if j[status_idx] != "RepoArchived" and j[notes] != "RepoArchived":
                if pd.isna(j[status_idx]) or j[status_idx] == "":
                    j[status_idx] = "RepoArchived"
                else:
                    j[notes] = "RepoArchived"
                update.append(j)
    if not update:
        print("No need to update")
    else:
        print("[!]Need to Update (Copy the following contents and replace the corresponding line in csv.file)")
        for i in update:
            print("line_number " + str(i[0]) + ":")  # line_number
            print(str(i[1:]).replace("[", "").replace("]", "").replace("\'", "").replace(", ", ",").replace("nan", "").replace("\"", ""))
            print("")
    print("")

    print("3.anomaly:")
    for i in anomaly:
        print("status code: " + str(i[0])),
        print("url:", i[1])
        print("[!]details: ")
        updates = []
        if str(i[0]) == '404':
            for record in my_dict[i[1]]:
                if record[status_idx] != "RepoDeleted" and record[notes] != "RepoDeleted":
                    # should mark deleted archived repo as deleted
                    if pd.isna(record[status_idx]) or record[status_idx] == "" or record[status_idx] == "RepoArchived":
                        record[status_idx] = "RepoDeleted"
                    else:
                        record[notes] = "RepoDeleted"
                    updates.append(record)
            if not updates:
                print("No need to update")
                print("")
            else:
                print("[!]Need to Update (Copy the following contents and replace the corresponding line in csv.file)")
                for update in updates:
                    print("line_number " + str(update[0]) + ":")
                    print(str(update[1:]).replace("[", "").replace("]", "").replace("\'", "").replace(", ", ",").replace("nan", "").replace("\"", ""))
                    print("")
                print("")
        else:
            for record in my_dict[i[1]]:
                print("line_number " + str(record[0]) + ":")
                print(str(record[1:]).replace("[", "").replace("]", "").replace("\'", "").replace(", ", ",").replace("nan", "").replace("\"", ""))
                print("")
            print("")


if __name__ == "__main__":
    main()
