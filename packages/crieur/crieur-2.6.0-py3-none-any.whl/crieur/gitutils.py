import os
import shutil
import subprocess
from pathlib import Path


def sparse_git_checkout(
    repo_url, source_path, dest_dir, temp_dir="tmp-checkout", branch="main", quiet=False
):
    """
    Perform a sparse git checkout to extract a specific directory from a repository.

    :repo_url: URL of the git repository
    :source_path: Path within the repo to extract
    :dest_dir: Local destination directory
    :temp_dir: Temporary directory name
    :branch: Branch to checkout (default: main)
    :quiet: If True, skip all prompts and automatically confirm actions
    """

    def confirm_action(prompt):
        """Prompt user for confirmation if not in quiet mode."""
        if quiet:
            return True
        response = input(f"{prompt} [y/N]: ")
        return response.lower().strip() in ["y", "yes"]

    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "Git is not available on this system. "
            "Please install Git and ensure it's in the PATH."
        )
        exit(1)

    cwd = Path.cwd()
    temp_path = cwd / temp_dir
    dest_path = cwd / dest_dir / source_path

    if dest_path.exists():
        if not confirm_action(
            f"Destination '{dest_path}' exists and will be overridden with content from"
            " the remote repository. Continue?"
        ):
            print("Operation cancelled by user.")
            exit(1)
        try:
            shutil.rmtree(dest_path)
        except OSError as e:
            print(f"Failed to remove destination directory: {e}")
            exit(1)

    # Initialize a new git repository in temp directory (without fetching).
    try:
        subprocess.run(["git", "init", temp_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to init git repo: {e}")
        exit(1)

    os.chdir(temp_path)

    try:
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to add remote origin: {e}")
        exit(1)

    print(f"Fetching data from {repo_url}/{source_path}")
    try:
        subprocess.run(["git", "fetch", "--depth=1", "origin"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to fetch repository: {e}")
        exit(1)

    # Enable and configure sparse checkout (to avoid downloading the full repo).
    try:
        subprocess.run(["git", "config", "core.sparseCheckout", "true"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable sparse checkout: {e}")
        exit(1)

    sparse_checkout = temp_path / ".git" / "info" / "sparse-checkout"
    sparse_checkout.parent.mkdir(parents=True, exist_ok=True)
    try:
        sparse_checkout.write_text(f"{source_path}\n")
    except Exception as e:
        print(f"Failed to configure sparse-checkout: {e}")
        exit(1)

    # Finally checkout branch with the specified `source_path` dir only.
    try:
        subprocess.run(["git", "checkout", branch], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to checkout branch '{branch}': {e}")
        exit(1)

    os.chdir(cwd)

    source_full = temp_path / source_path
    if source_full.exists():
        try:
            shutil.move(str(source_full), str(dest_path))
        except Exception as e:
            print(f"Failed to move '{source_path}' to '{dest_dir}': {e}")
            exit(1)
    else:
        print(f"Source path '{source_path}' does not exist in the repository.")
        exit(1)

    try:
        shutil.rmtree(temp_path)
    except OSError as e:
        print(f"Failed to remove temporary directory: {e}")
        exit(1)
