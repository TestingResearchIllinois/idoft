# git blame pr-data.csv | egrep '2022-(08|09|10|11|12)' | sed -e 's/[^(]*(//' -e 's/2022-[^)]*)/,/' | python3 compute-idoft-points.py
# git blame py-data.csv | egrep '2022-(08|09|10|11|12)' | sed -e 's/[^(]*(//' -e 's/2022-[^)]*)/,/' | python3 compute-idoft-points.py
 
# (cd ~/github.com/TestingResearchIllinois/idoft; git pull -r; git blame pr-data.csv) | egrep '2022-(08|09|10|11|12)' | sed -e 's/[^(]*(//' -e 's/2022-[^)]*)/,/' | python3 compute-idoft-points.py | sed 's/Counter(\([^)]*\))/\1/g' | tr -d \' | grep -v no-
 
from collections import Counter
import sys
import math
 
# just copy from Google Sheet (separated by \t)
GIT2NETID = """
yx31    xieyt2000
anantd2 anantdahiya8
pma7    priyanka-28
boyuli4 BoyuLi4
yichen28    tt0suzy
yz97    yannizhou05
bk28    bmk15897
kumbhar2    aditya-kumbhar
zhewenf2    Zhewen
yiweili6    Yiwei Li
sp83    sopan98
bk28    Bharati Kulkarni
kumbhar2    Aditya Kumbhar
bk28    Bharati
kumbhar2    Aditya
frn3    blazyy
yiteng3 Kerr0220
yiteng3 Kerr
sh69-no-flaky-project   sh69
sh69-no-flaky-project   Shan
no-527-1    Philmon
zitongz4-no-flaky-project   zitongzhoueric
no-527-2    Partha
no-527-3    MohsenDehghankar
no-527-4    Talank
kejiawu2-no-flaky-project   kejiawu2
kf14-no-flaky-project   kfadillah
sk117-no-flaky-project  Akshath
sk117-no-flaky-project  akshathsk
anantd2 unknown
sp83    Sopan
zhewenf2    Zhewen
zhewenf2    zhewenf2
yiweili6    Yiwei
yiweili6    yiweili6
no-527-5    Pious
frn3    Faaez
yiweili6    YiweiLi4
"""
PAIRS = {'yiweili6': 'yiweili6/zhewenf2', 'zhewenf2': 'yiweili6/zhewenf2'}
PAIR_DIVIDE = 2
 
 
def is_pair(netid):
    return '/' in netid
 
 
def parse_netid():
    global GIT2NETID
    res = {}
    for line in GIT2NETID.splitlines():
        if not line:
            continue
        netid, git = line.split('\t')
        if netid in PAIRS:
            netid = PAIRS[netid]
        res[git] = netid
    GIT2NETID = res
 
 
PY_DATA = False
STATUS_ID = 5 if PY_DATA else 6
CAT_ID = 4 if PY_DATA else 5
 
DETECTED = 'Detected'  # ''
POINTS = {'Accepted': 5, 'InspiredAFix': 4, 'Opened': 3, 'MovedOrRenamed': 2, 'Deleted': 2, 'DeveloperFixed': 2,
          'RepoDeleted': 1, DETECTED: 1, 'DeveloperWontFix': .33, 'Deprecated': .25, 'RepoArchived': .25,
          'Rejected': -2}
PR_STATUS = {'Accepted', 'InspiredAFix', 'Opened', 'Rejected'}
MAX_NON_PR_STATUS_POINTS = 20
CATEGORY_STATUS = {'Accepted', 'InspiredAFix', 'Opened', 'Rejected', DETECTED, 'DeveloperFixed', 'DeveloperWontFix'}
 
print('points = ' + str(POINTS))
print('max points for non-pr statuses = ' + str(MAX_NON_PR_STATUS_POINTS))
print('bonus for mix of categories = 0% for no mix (1 category), 10% for some mix (2), 40% for high mix (>=3)')
 
 
def parse_lines(lines):
    tests = {}
    projects = {}
    categories = {}
    name_not_netid = set()
    for line in lines:
        splitted = line.rstrip().split(',')
        git_name = splitted[0].split(' ')[0]
        if git_name not in GIT2NETID:
            netid = "no-netid-" + git_name
            name_not_netid.add(git_name)
            continue
        else:
            netid = GIT2NETID[git_name]
        status = splitted[STATUS_ID] if splitted[STATUS_ID] else DETECTED
        if netid not in tests:
            tests[netid] = Counter()
        tests[netid][status] += 1
        project = splitted[1]
        if netid not in projects:
            projects[netid] = Counter()
        projects[netid][project] += 1
        if status in CATEGORY_STATUS:
            category = splitted[CAT_ID]
            if netid not in categories:
                categories[netid] = Counter()
            categories[netid][category] += 1
    print(f"name not in netid: {name_not_netid}")
    return tests, projects, categories
 
 
def get_cat_list(netid, categories):
    return categories.get(netid, [])
 
 
def get_mix_str(netid, categories):
    num_cat = min(len(get_cat_list(netid, categories)), 3)
    return f"{'no' if num_cat <= 1 else 'some' if num_cat == 2 else 'high'} mix: {get_cat_list(netid, categories)}"
 
 
def get_mix_val(netid, categories):
    num_cat = min(len(get_cat_list(netid, categories)), 3)
    return 1 + .1 * (num_cat - 1) * (num_cat - 1)
 
 
def get_result(tests, projects, categories):
    res = []
    point_netid = []
    for netid, statuses in tests.items():
        pr_point = non_pr_point = 0
        for status, num in statuses.items():
            stat_point = num * POINTS[status]
            if status in PR_STATUS:
                pr_point += stat_point
            else:
                non_pr_point += stat_point
        if is_pair(netid):
            non_pr_point = min(non_pr_point, MAX_NON_PR_STATUS_POINTS * PAIR_DIVIDE)
        else:
            non_pr_point = min(non_pr_point, MAX_NON_PR_STATUS_POINTS)
        point = (pr_point + non_pr_point) * get_mix_val(netid, categories)
        if is_pair(netid):
            point /= PAIR_DIVIDE
        point_netid.append((point, netid))
    for (total, netid) in sorted(point_netid, reverse=True):
        line = (f'{int(total):>3} {netid:<8} {tests[netid]}, '
                f'projects={str(len(projects[netid]))}, {get_mix_str(netid, categories)}')
        res.append(line)
    return res
 
 
def main(lines):
    parse_netid()
    tests, projects, categories = parse_lines(lines)
    results = '\n'.join(get_result(tests, projects, categories))
    print(results)
 
 
if __name__ == '__main__':
    main(sys.stdin)
    # with open("./input.txt") as f:
    #     main(f.readlines())