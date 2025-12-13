import plotly.express as px

def visualize_activity(df, theme="plotly"):
    """Visualize Git activity from a DataFrame."""
    figs = []
    if df.empty:
        print("No data available for visualization.")
        return figs
    commits_by_date = df.groupby("date").size().reset_index(name='commits')
    fig1 = px.line(commits_by_date, x="date", y="commits", title="Commits Over Time")
    fig1.update_layout(template=theme)
    figs.append(fig1)

    commits_by_author = df.groupby('author').size().reset_index(name='commits')
    fig2 = px.bar(commits_by_author, x='author', y='commits', title="Commits per Author")
    fig2.update_layout(template=theme)
    figs.append(fig2)

    if "branch" in df.columns:
        commits_by_branch = df.groupby('branch').size().reset_index(name='commits')
        fig3 = px.pie(commits_by_branch, names='branch', values='commits', title="Commits by Branch")
        fig3.update_layout(template=theme)
        figs.append(fig3)
    return figs