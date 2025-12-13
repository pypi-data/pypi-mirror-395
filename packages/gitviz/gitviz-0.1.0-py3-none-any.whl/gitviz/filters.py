import pandas as pd

def filter_by_date(df, start_date=None, end_date=None, date_column='date'):
    """Filter DataFrame by date range."""
    if start_date:
        df = df[df[date_column] >= start_date]
    if end_date:
        df = df[df[date_column] <= end_date]
    return df

def filter_by_author(df, author, author_col='author_name'):
    """Filter DataFrame by author name."""
    if isinstance(author, str):
        authors = [author]
    return df[df[author_col].isin(authors)]

def filter_by_branch(df, branches, branch_col='branch'):
    """Filter DataFrame by branch name."""
    if isinstance(branches, str):
        branches = [branches]
    return df[df[branch_col].isin(branches)]

def filter_by_commit_type(df, types, type_col='type'):
    """Filter DataFrame by commit type (e.g., 'merge', 'regular')."""
    if isinstance(types, str):
        types=[types]
    return df[df[type_col].isin(types)]

def compare_repos(dfs, labels=None):
    """Compare multiple repositories' DataFrames."""
    if labels is None:
       labels = [f"Repo {i+1}" for i in range(len(dfs))]
    return {label: df.describe(include='all') for label, df in zip(labels, dfs)}