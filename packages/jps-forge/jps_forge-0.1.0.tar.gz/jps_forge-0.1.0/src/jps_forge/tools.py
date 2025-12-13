# tools.py
from langchain_core.tools import tool
from git import Repo
from pathlib import Path
import os
import yaml

from .constants import DEFAULT_CONFIG_FILE_PATH


with open(DEFAULT_CONFIG_FILE_PATH) as f:
    config = yaml.safe_load(f)


@tool
def list_dirty_repos() -> str:
    """
    Return all Git repositories that contain uncommitted or untracked files.

    Use this tool when:
        - The user asks which repositories have pending changes.
        - The user wants to know which repos are dirty, modified, or not clean.
        - The user asks for a summary of repositories that need attention.

    Do NOT use this tool when:
        - The user wants the git status of a single repository (use git_status()).
        - The user wants the git status of the current working directory (use current_repo_status()).
        - The user asks to list *all* repos regardless of clean/dirty state.

    Returns:
        A newline-separated string of directory paths for repositories that are dirty.
        If no repositories are dirty, returns: "All repositories are clean!".
    """
    dirty = []
    for root in [Path(os.path.expanduser(p)) for p in config.get("project_roots", ["~/projects"])]:
        for repo_path in root.rglob(".git"):
            repo_dir = repo_path.parent
            try:
                repo = Repo(repo_dir)
                if repo.is_dirty(untracked_files=True):
                    dirty.append(str(repo_dir))
            except:
                pass
    return "\n".join(dirty) if dirty else "All repositories are clean!"


@tool
def git_status(repo_path: str = ".") -> str:
    """
    Get detailed git status for a specific Git repository.

    Use this tool when:
        - The user references a specific repository (path-based request).
        - The user asks for the git status of a repository other than the current directory.
        - The user provides a repo path, name, or folder explicitly.

    Do NOT use this tool when:
        - The user refers to the "current repo", "this repo", or "here".
          (Use current_repo_status() instead.)
        - The user wants to find all dirty repositories (use list_dirty_repos()).

    Args:
        repo_path:  
            Path to the git repository to inspect.  
            Use "." for the current directory or provide an absolute or
            shell-expandable path (e.g., "~/projects/tooling").

    Returns:
        A formatted string containing:
            - The resolved repository path.
            - The full output of `git status`.

        Returns an error string if the path is not a valid git repository.
    """
    try:
        # Expand and resolve the path
        if repo_path == ".":
            repo_path = os.getcwd()
        else:
            repo_path = os.path.expanduser(repo_path)

        repo = Repo(repo_path)
        status_output = repo.git.status()
        return f"Repository: {repo_path}\n\n{status_output}"
    except Exception as e:
        return f"Error accessing repository at '{repo_path}': {e}"


@tool
def current_repo_status() -> str:
    """
    Get the git status of the current working directory.

    Use this tool when:
        - The user refers to “this repo”, “current repo”, “the repo here”, or “here”.
        - The user asks for the git status without specifying a path.
        - The user is likely referring to the shell’s working directory context.

    Do NOT use this tool when:
        - The user provides a path to another repository (use git_status()).
        - The user wants to scan *all* repos for dirtiness (use list_dirty_repos()).

    Returns:
        A formatted string containing:
            - The current working directory.
            - The full output of `git status`.

        Returns an error string if the current directory is not a git repository.
    """
    try:
        cwd = os.getcwd()
        repo = Repo(cwd)
        status_output = repo.git.status()
        return f"Repository: {cwd}\n\n{status_output}"
    except Exception as e:
        return f"Error: The current directory ({os.getcwd()}) is not a git repository or has an error: {e}"
