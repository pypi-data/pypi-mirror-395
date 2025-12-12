from git import Repo
from typing import Optional


def get_git_diff(repo: Repo, staged: bool = False, file_path: Optional[str] = None):
    exclude_pattern = ":(exclude)*lock*"
    if staged:
        return repo.git.diff("--staged", file_path, exclude_pattern)
    else:
        return repo.git.diff(file_path, exclude_pattern)


def commit_changes(repo: Repo, commit_message: str):
    repo.git.add(A=True)
    repo.index.commit(commit_message)


def get_commit_diff(repo: Repo, commit_hash: str):
    return repo.git.diff(f"{commit_hash}^!", "--word-diff=color")
