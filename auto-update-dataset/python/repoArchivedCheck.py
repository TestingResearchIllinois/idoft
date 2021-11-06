import pandas as pd
import time
from requests_html import HTMLSession


# it takes about 2 minutes to check 200 projects
def main():
    # get unique urls from pr-data.csv, we can also use cmd: `git pull -r ; cut -f1 -d, pr-data.csv | uniq`
    pr_data_url = r"https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/pr-data.csv"
    urls = pd.read_csv(pr_data_url, usecols=["Project URL"])
    urls = list(set([i[0] for i in urls.values.tolist()]))
    print("load data from", pr_data_url)
    data = pd.read_csv(pr_data_url,
                       usecols=["Project URL",
                                "Fully-Qualified Test Name (packageName.ClassName.methodName)",
                                "Status",
                                "Notes"])
    data = data.values  # get an array of array
    my_dict = {}  # {url:[[line_num, url, test_name, status], [...], ...],}
    line_number = 2
    for i in data:
        if i[0] not in my_dict:
            my_dict[i[0]] = []
        line = list(i)
        line.insert(0, line_number)
        my_dict[i[0]].append(line)
        line_number += 1

    # # save urls in file
    # f = open("pandas_reads_results.txt", "w")
    # for i in urls:
    #     f.writelines(i + "\n")
    # f.close()

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
        if "This repository has been archived by the owner. It is now read-only." in r.text:
            archived.append(url)
            print("archived: ", url)
        # if "archived" in r.text[:len(r.text)]:
        #     print(url)
    end = time.time()

    print("\n===========\n[summary]")
    print("1.total time: ", end-begin, "s")
    print("2.repoArchived: ")
    for i in archived:
        print("    ", i)
    update = []
    for i in archived:
        for j in my_dict[i]:
            if j[3] != "RepoArchived":
                update.append(j)
    if not update:
        print("No need to update")
    else:
        print("[!]May need to update the STATUS:[line_number, url, test_name, status, notes]")
        for i in update:
            print("    ", i)
    print("")
    print("3.anomaly[[status_code, url]]:")
    for i in anomaly:
        print("    ", i)
    print("details: [line_number, url, test_name, status, notes]")
    for i in anomaly:
        for j in my_dict[i[1]]:
            print("    ", j)
    print("")


if __name__ == "__main__":
    main()
