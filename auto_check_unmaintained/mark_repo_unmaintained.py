import pandas as pd

py_data_df = pd.read_csv('py-data.csv')
unmaintained_repos_df = pd.read_csv('unmaintained-repos.csv')
last_commit_dict = unmaintained_repos_df.set_index('REPO_URL')['LAST_COMMIT_DATE'].to_dict()


def update_row(row):
    if row['ProjectURL'] in last_commit_dict:
        if pd.isna(row['Status']):  # Check if 'Status' is empty
            row['Status'] = 'Unmaintained'
        else:
            return row

        row['Notes'] = f"{row['Notes']} | {last_commit_dict[row['ProjectURL']]}" if pd.notna(row['Notes']) else f"{last_commit_dict[row['ProjectURL']]}"
    return row


py_data_df = py_data_df.apply(update_row, axis=1)
py_data_df.to_csv('py-data_with_last_commit.csv', index=False)
