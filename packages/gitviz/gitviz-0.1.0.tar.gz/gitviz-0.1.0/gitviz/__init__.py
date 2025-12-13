from .api import analyze_repo, visualize_activity
from .dashboard import export_dashborad
from gitviz.exporter import export_to_csv, export_to_json


def run_dashboard_analysis(
        repo_path: str, 
        output: str = 'dashboard.html', 
        theme:str='plotly', 
        app_name:str="Application Dashboard", 
        title:str="Git Activity Dashboard", 
        description:str=None, 
        author:str=None, 
        max_commits:int=20, 
        export_csv:str="activity.csv", 
        export_json:str="activity.json", 
        export_data:list= None
    ) -> None:
    """Run analysis and export dashboard for the given repository path."""
    if export_data is None:
        export_data = []

    df = analyze_repo(repo_path)
    if 'csv' in export_data:
        export_to_csv(df, export_csv)
        print(f"Exported commits to CSV at {export_csv}")

    if'json' in export_data:
        export_to_json(df, export_json)
        print(f"Exported commits to JSON at {export_json}")
    figs = visualize_activity(df, theme=theme)
    export_dashborad(figs, output, theme=theme, title=title, description=description, author=author, df=df, max_commit=max_commits, app_name=app_name)