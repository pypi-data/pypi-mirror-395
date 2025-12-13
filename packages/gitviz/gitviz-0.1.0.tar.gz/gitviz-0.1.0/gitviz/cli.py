import sys
import argparse
from gitviz.api import analyze_repo, visualize_activity, export_dashborad
from gitviz.exporter import export_to_csv, export_to_json, save_dashborad_config, load_dashboard_config


def main():
    """Command-line interface for gitviz."""
    import importlib.metadata
    parser = argparse.ArgumentParser(description="Visualize git activity as an intractive dashboard.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {importlib.metadata.version('gitviz')}", help="Show the version number and exit")
    parser.add_argument("repo_path", help="path to local git repository")
    parser.add_argument("--output", default="git_activity.html", help="Output file HTML")
    parser.add_argument("--theme", default="plotly_white", help="Plotly theme e.g., plotly_dark, plotly_white")
    parser.add_argument("--export-csv", default=None, help="Export commits to CSV")
    parser.add_argument("--export-json", default=None, help="Export commits to JSON")
    parser.add_argument("--save-config", help="")
    parser.add_argument("--load-config", help="")
    parser.add_argument("--title", default="Git Activity Dashboard", help="Dashboard title")
    parser.add_argument("--description", default=None, help="Dashboard discription")
    parser.add_argument("--app-name", default=None, help="Application name for dashboard")
    parser.add_argument("--author", default=None, help="Filter by author name (substring)")

    args = parser.parse_args()

    config = None
    if args.load_config:
        config = load_dashboard_config(args.load_config)
        print(f"Loaded dashboard config from {args.load_config}")

    app_name = args.app_name
    if not app_name:
        import os
        app_name = os.path.basename(os.path.abspath(args.repo_path))



    try:
        print(f"Analyzing repository at {args.repo_path}...")
        df = analyze_repo(args.repo_path)
        if df.empty:
            print("No commits found in the repository.")
            sys.exit(1)

        if args.export_csv:
            export_to_csv(df, args.export_csv)
            print(f"Exported commits to CSV at {args.export_csv}")

        if args.export_json:
            export_to_json(df, args.export_json)
            print(f"Exported commits to JSON at {args.export_json}")

        print("Genrating Visualizations...")
        theme = config.get("theme", args.theme) if config else args.theme
        figs = visualize_activity(df, theme=theme)
        if not figs:
            print("No visualizations generated.")
            sys.exit(1)
        
        print(f"Exporting dashboard...")
        export_dashborad(
            figs,
            args.output,
            theme=theme,
            title=args.title,
            description=args.description,
            author = args.author,
            df=df,
            max_commit=20,
            app_name=app_name)
        
        if args.save_config:
            save_dashborad_config({"theme": theme}, args.save_config)
            print(f"Saved dashboard config to {args.save_config}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()