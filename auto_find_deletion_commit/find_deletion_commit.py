import subprocess
import os
import sys


def clone_repo(repo_url, clone_dir):
    try:
        if not os.path.exists(clone_dir):
            subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        else:
            print(f"Repository already exists in {clone_dir}.")
    except Exception as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)


def find_deleted_test_function(repo_path, file_path, test_function_name):
    try:
        result = subprocess.run(
            [
                "git", "log", "-S", test_function_name,
                "--pickaxe-regex", "--diff-filter=D", "--", file_path
            ],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0 or not result.stdout:
            print("No deletion found for test function")
            return None
        lines = result.stdout.splitlines()
        for line in lines:
            if line.startswith("commit "):
                commit_hash = line.split()[1]
                print(commit_hash)
                return commit_hash

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python find_deleted_test_function.py <repository_url_or_path> <file_path> <test_function_name>")
    else:
        repo_input = sys.argv[1]
        file_path = sys.argv[2]
        test_function_name = sys.argv[3]

        if repo_input.startswith("http://") or repo_input.startswith("https://"):
            repo_dir = os.path.basename(repo_input).replace(".git", "")
            clone_repo(repo_input, repo_dir)
            repo_path = repo_dir
        else:
            repo_path = repo_input

        find_deleted_test_function(repo_path, file_path, test_function_name)
