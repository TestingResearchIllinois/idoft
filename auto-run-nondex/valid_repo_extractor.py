import requests
from bs4 import BeautifulSoup
import sys

AUTHOR_URL_POSTFIX = '?language=java&page={}&q=&sort=&type='
AUTHOR_URL = ''
REPO_URL_PREFIX = 'https://github.com'
PR_DATA_CSV_FILE_URL = 'https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/pr-data.csv'
EXISTING_REPO_URL_SET = set()


def load_existing_repo_in_idoft():
    pr_data_file = requests.get(PR_DATA_CSV_FILE_URL).text
    for row in pr_data_file.splitlines():
        repo_url = row.split(',')[0]
        EXISTING_REPO_URL_SET.add(repo_url)


def extract_repos_with_pom_file():
    page_number = 1
    url = AUTHOR_URL.format(page_number)
    html_doc = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    repos = soup.find_all('a', class_='d-inline-block', href=True)
    while len(repos) > 3:
        for repo in repos:
            if repo.has_attr('data-hovercard-type') and repo.get('data-hovercard-type') == 'repository':
                if REPO_URL_PREFIX + repo['href'] in EXISTING_REPO_URL_SET:
                    # print('Repetitive repo: ' + REPO_URL_PREFIX + repo['href'])
                    continue
                repo_url_html_content = requests.get(REPO_URL_PREFIX + repo['href']).content.decode('utf-8')
                if 'pom.xml' in repo_url_html_content:
                    print(REPO_URL_PREFIX + repo['href'] + '.git')

        page_number += 1
        url = AUTHOR_URL.format(page_number)
        html_doc = requests.get(url).content.decode('utf-8')
        soup = BeautifulSoup(html_doc, 'html.parser')
        repos = soup.find_all('a', class_='d-inline-block', href=True)


if __name__ == '__main__':
    AUTHOR_URL = sys.argv[1] + AUTHOR_URL_POSTFIX
    load_existing_repo_in_idoft()
    extract_repos_with_pom_file()
