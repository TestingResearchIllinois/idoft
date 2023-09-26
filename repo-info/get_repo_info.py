import os
import argparse
import datetime
import pandas as pd
from tqdm import tqdm
from github import Github

tqdm.pandas()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--github_access_token', help='GitHub access token to overcome API rate limitations')
parser.add_argument('-f', '--filepath', help='Filepath of .csv file containing repo data')
parser.add_argument('-c', '--colname', help='Column name in CSV file pertaining to repo URL')
args = parser.parse_args()

GITHUB_API_RATE_LIMIT = 5000
FILEPATH, COLNAME, GITHUB_ACCESS_TOKEN = args.filepath, args.colname, args.github_access_token

data = pd.read_csv(FILEPATH)
data = data[data['Status'].isna()]
REPO_URLS = data[COLNAME].unique()
NUM_REPOS = REPO_URLS.shape[0]


def check_number_repos():
    if NUM_REPOS > GITHUB_API_RATE_LIMIT:
        print(f'You can only make {GITHUB_API_RATE_LIMIT} requests per hour. Your file has {NUM_REPOS} unique repositories. Exiting.')
        exit(0)


def get_diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def get_repo_object(repo_url):
    try:
        repo_name = repo_url.split('github.com/')[1]
        return Github(GITHUB_ACCESS_TOKEN).get_repo(repo_name)
    except Exception as e:
        print(e)
        return None


def get_months_since_last_commit(repo):
    try:
        default_branch = repo.get_branch(repo.default_branch)
        latest_commit_date = default_branch.commit.commit.author.date
        months_since_commit = get_diff_month(datetime.datetime.now(), latest_commit_date)
        return months_since_commit
    except Exception as e:
        print(e)
        return None


def get_maintained_repos():
    check_number_repos()
    print(f'Analyzing {NUM_REPOS} repositories...')
    df = pd.DataFrame()
    df['REPO_URL'] = REPO_URLS
    df['REPO_OBJECT'] = df['REPO_URL'].progress_apply(lambda url: get_repo_object(url))
    df['MONTHS_SINCE_LAST_COMMIT'] = df['REPO_OBJECT'].progress_apply(lambda repo_object: get_months_since_last_commit(repo_object))
    df['STARS'] = df['REPO_OBJECT'].progress_apply(lambda repo_object: repo_object.stargazers_count if repo_object is not None else None)
    df = df.sort_values(by=['MONTHS_SINCE_LAST_COMMIT', 'STARS'], ascending=[True, False]).drop(columns=['REPO_OBJECT', 'Unnamed: 0'], errors='ignore')
    df.to_csv(f'{os.getcwd()}/repo-info/repo-info.csv', index=False)


if __name__ == '__main__':
    get_maintained_repos()
