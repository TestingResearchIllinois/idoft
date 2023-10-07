import requests
from bs4 import BeautifulSoup
import sys
import traceback

AUTHOR_URL_POSTFIX = 'language=java&q=&sort=&type='
AUTHOR_URL = ''
REPO_URL_PREFIX = 'https://github.com'
PR_DATA_CSV_FILE_URL = 'https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/pr-data.csv'
EXISTING_REPO_URL_SET = set()


def load_existing_repo_in_idoft():
    pr_data_file = requests.get(PR_DATA_CSV_FILE_URL).text
    for row in pr_data_file.splitlines():
        repo_url = row.split(',')[0]
        EXISTING_REPO_URL_SET.add(repo_url)


def extract_org_repos_with_pom_file():
    page_number = 1
    url = AUTHOR_URL.format(page_number)
    html_doc = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    repos = soup.find_all('a', class_='d-inline-block', href=True)
    while len(repos) > 3:
        for repo in repos:
            if repo.get('data-hovercard-type') == 'repository':
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


def extract_personal_repos_with_pom_file():
    html_doc = requests.get(AUTHOR_URL).content.decode('utf-8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    repos = soup.find_all('h3', class_='wb-break-all')
    try:
        next_page = soup.find('div', class_='paginate-container').contents[1].contents[1].attrs.get('href')
    except Exception:
        next_page = None

    while repos or next_page:
        for repo in repos:
            full_repo_url = REPO_URL_PREFIX + repo.contents[1].attrs.get('href', '')
            if full_repo_url in EXISTING_REPO_URL_SET:
                # print('Repetitive repo: ' + REPO_URL_PREFIX + repo['href'])
                continue
            repo_url_html_content = requests.get(full_repo_url).content.decode('utf-8')
            if 'pom.xml' in repo_url_html_content:
                print(full_repo_url + '.git')
        if next_page:
            html_doc = requests.get(next_page).content.decode('utf-8')
            soup = BeautifulSoup(html_doc, 'html.parser')
            repos = soup.find_all('h3', class_='wb-break-all')
            try:
                next_page = soup.find('div', class_='paginate-container').contents[1].contents[1].attrs.get('href')
            except Exception:
                next_page = None
        else:
            break


if __name__ == '__main__':
    try:
        load_existing_repo_in_idoft()
        if '/orgs/' in sys.argv[1]:
            # if the input url is an organizational author
            AUTHOR_URL = sys.argv[1] + '?' + AUTHOR_URL_POSTFIX + '&page={}'
            extract_org_repos_with_pom_file()
        else:
            # if the input url is a personal author
            AUTHOR_URL = sys.argv[1] + '&' + AUTHOR_URL_POSTFIX
            extract_personal_repos_with_pom_file()
    except Exception as e:
        print("[ERROR]: {}.{}.{}".format(e.__class__.__name__, e, traceback.format_exc()))
