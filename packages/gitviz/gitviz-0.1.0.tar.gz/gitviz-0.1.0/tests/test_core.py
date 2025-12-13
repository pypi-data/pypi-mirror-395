import os
from git import Repo, InvalidGitRepositoryError
import pytest

from gitviz.core import parse_git_commits, commits_time_series, filter_commits


def test_parse_git_commits_on_current_repo():
    path = os.getcwd()
    try:
        Repo(path)
    except InvalidGitRepositoryError:
        pytest.skip("Not running tests inside a git repo; skipping parse test.")

    df = parse_git_commits(path)
    assert df is not None
    assert 'commit' in df.columns
    ts = commits_time_series(df)
    assert ts is not None


def test_filter_commits_by_message():
    # Construct a minimal DataFrame for filtering
    import pandas as pd
    from datetime import datetime

    data = [
        {"commit":"a","author_name":"Alice","date":datetime(2022,1,1,12,0),"message":"fix bug"},
        {"commit":"b","author_name":"Bob","date":datetime(2022,1,2,12,0),"message":"add feature"},
    ]
    df = pd.DataFrame(data)
    res = filter_commits(df, message_query="fix")
    assert len(res) == 1
    assert res.iloc[0]["author_name"] == "Alice"
