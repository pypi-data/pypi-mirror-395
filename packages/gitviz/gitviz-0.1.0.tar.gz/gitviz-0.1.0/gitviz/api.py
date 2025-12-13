"""
python-gitviz API module.
Provides functions to analyze Git repositories, visualize activity, and export dashboards.
Exported Functions:
- analyze_repo(path): Analyze a Git repository at the given path.
- visualize_activity(df, theme="plotly"): Visualize Git activity from a DataFrame.
- export_dashborad(fig, path, theme="plotly", title="GIT Activity Dashboard", description=None, author=None, df=None, max_commit=20, app_name="Application Dashboard"): Export a dashboard with Git activity visualizations.
"""

from .git_analyzer import analyze_repo as _analyze_repo
from .visualizer import visualize_activity as _visualize_activity
from .dashboard import export_dashborad as _export_dashborad
import pandas as pd


def analyze_repo(path: str)-> dict:
    """Analyze a Git repository at the given path."""
    return _analyze_repo(path)


def visualize_activity(df: pd.DataFrame, theme="plotly")-> dict:
    """Visualize Git activity from a DataFrame."""
    return _visualize_activity(df, theme=theme)


def export_dashborad(fig, path: str, theme:str="plotly", title:str="GIT Activity Dashboard", description=None, author=None, df=None, max_commit=20, app_name="Application Dashboard")-> None:
    """Export a dashboard with Git activity visualizations."""
    return _export_dashborad(fig, path, theme=theme, title=title, description=description, author=author, df=df, max_commit=20, app_name=app_name)