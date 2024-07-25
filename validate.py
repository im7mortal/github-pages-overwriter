import os
import sys
import fnmatch
from github import Github

# Authenticate to GitHub
g = Github(os.getenv('GITHUB_TOKEN'))


def get_ignored_files(path):
    ignored_files = []
    gitignore_path = os.path.join(path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    ignored_files.append(line.strip())
    return ignored_files


def is_ignored(file_path, ignored_patterns):
    for pattern in ignored_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def compare_files(local_path, repo, branch):
    ignored_patterns = get_ignored_files(local_path)
    for root, dirs, files in os.walk(local_path):
        # Skip the .git directory
        if '.git' in dirs:
            dirs.remove('.git')

        for file_name in files:
            file_path = os.path.relpath(os.path.join(root, file_name), local_path)
            if is_ignored(file_path, ignored_patterns):
                continue

            try:
                remote_file_content = repo.get_contents(file_path, ref=branch).decoded_content
                with open(os.path.join(local_path, file_path), 'rb') as local_file:
                    local_file_content = local_file.read()

                if local_file_content != remote_file_content:
                    print(f'{file_path} does not match the remote content.')
                    return False
            except Exception as e:
                print(f'Error comparing {file_path}: {e}')
                return False

    print('All files match the remote content.')
    return True


def main():
    if len(sys.argv) < 3:
        print('Usage: script.py <repo> <branch> <path>')
        exit(1)

    repo_name = sys.argv[1]
    branch_name = sys.argv[2]
    local_path = sys.argv[3]
    if local_path == ".":
        local_path = os.getcwd()
    else:
        local_path = os.path.abspath(local_path)

    repo = g.get_repo(repo_name)  # Use the provided repo details

    if not compare_files(local_path, repo, branch_name):
        exit(1)


if __name__ == '__main__':
    main()
