import subprocess
import pandas as pd
import re
import shutil

GIT_PATH = shutil.which("git")
import sys
if not GIT_PATH:
    print("Git executable not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
    sys.exit(1)

print(f"[INFO] Using Git executable at: {GIT_PATH}")

def analyze_repo(repo_path="."):
    """Analyze a Git repository at the given path and return a DataFrame of commits."""
    branches = subprocess.run([GIT_PATH, "-C", repo_path, "branch", "--format=%(refname:short)"], capture_output=True, text=True, check=True).stdout.strip().splitlines()
    all_commits = []
    for branch in branches:
        log_cmd = [GIT_PATH, "-C", repo_path, "log", branch, "--pretty=format:%H|%an|%ad|%s", "--date=short"]
        log = subprocess.run(log_cmd, capture_output=True, text=True, check=True).stdout.strip()
        for line in log.splitlines():
            if not line:
                continue
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            commit_hash, author, date, message = parts
            ctype = "merge" if re.match(r"^Merge ", message) else "commit"
            all_commits.append({
                "hash": commit_hash,
                "author": author,
                "date": date,
                "message": message,
                "type": ctype,
                "branch": branch
            })
    df = pd.DataFrame(all_commits)
    if not df.empty:
        df = df.drop_duplicates(subset=["hash", "branch"])
    return df