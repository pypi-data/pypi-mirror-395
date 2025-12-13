import plotly.io as pio
import pandas as pd


def export_dashborad(fig, path, theme="plotly", title="GIT Activity Dashboard", description=None, author=None, df=None, max_commit=20, app_name="Application Dashboard"):
    """Export dashboard with given visualizations to HTML file."""
    if isinstance(fig, list):
        fig = fig[0]
    fig.update_layout(
        title=title,
        template=theme
    )
    annotations = []
    if description:
        annotations.append(
            dict(
                text=F"</b> Description:</b> {description}",
                xref="paper",
                yref="paper",
                x=0,
                y=1.13,
                showarrow=False,
                align="left",
                font=dict(size=14)
            )
        )
    if author:
        annotations.append(
            dict(
                text=f"<b>Author:</b> {author}",
                xref="paper",
                yref="paper",
                x=0,
                y=-1.08,
                showarrow=False,
                align="left",
                font=dict(size=12)
            )
        )
    if annotations:
        fig.update_layout(annotations=annotations)

    fig_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    table_html = ""
    PAGE_SIZE = 50
    if df is not None and not df.empty:
        df_sorted = df.sort_values(by=["date"] , ascending=False)
        columns = [col for col in ['Sr No','hash', 'author', 'date', 'message', 'type', 'branch'] if col in df_sorted.columns]
        num_pages = (len(df_sorted) + PAGE_SIZE - 1) // PAGE_SIZE
        tables = []
        for page in range(num_pages):
            start = page * PAGE_SIZE
            end = start + PAGE_SIZE
            page_df = df_sorted.iloc[start:end]
            table = page_df[columns].to_html(classes=f'commit-table page-{page+1}', border=1, justify='center', table_id=f'commit-table-{page+1}')
            tables.append(table)
            nav_html = ""
            if num_pages > 1:
                nav_html += '<div id="pagination" style="margin:20px 0;">'
                for i in range(num_pages):
                    nav_html += f'<button onclick="showPage({i+1})" id="btn-page-{i+1}"> Page {i+1}</button>'
                nav_html += '</div>'

            search_html = '''
        <div style="margin:20px 0;">
            <input type="text" id="commit-search" placeholder="Search commits.." style="padding:5px; width:300px;">
        </div>
        '''
            table_html = f'<h2 class="app-name">All Commits</h2>{nav_html}{search_html}'.format(table)
            for i, table in enumerate(tables):
                display = "" if i == 0 else "style='display:none;'"
                table_html += f"<div id='table-page-{i+1}' {display}>{table}</div>"
            if num_pages >1:
                table_html += '''
<script>
function showPage(page) {
    var numPages = ''' + str(num_pages) + ''';
    for (var i = 1; i <= numPages; i++) {
        document.getElementById('table-page-' + i).style.display = (i === page) ? '' : 'none';
        document.getElementById('btn-page-' + i).style.fontWeight = (i === page) ? 'bold' : 'normal';
    }
}
document.getElementById('btn-page-1').style.fontWeight = 'bold';
</script>
'''
            table_html += '''
<script>
document.getElementById('commit-search').addEventListener('keyup', function() {
var filter = this.value.toLowerCase();
var numPages = ''' + str(num_pages) + ''';
for (var p = 1; p <= numPages; p++) {
    var tableDiv = document.getElementById('table-page-' + p);
    if (tableDiv.style.display === 'none') continue;
    var table = tableDiv.querySelector('table');
    var trs = table.getElementsByTagName('tr');
    for (var i = 1; i < trs.length; i++) {
    var row = trs[i];
    var txt = row.textContent.toLowerCase();
    row.style.display = txt.indexOf(filter) > -1 ? '' : 'none';
    }
}
});
</script>
'''
    html = f"""
    <html>
    <head>
        <title>{title} - Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
        <style>
            body {{
                font-family: 'Roboto', Arial, sans-serif;
                margin: 0;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #222;
                padding: 20px;
            }}
            .watermark {{
                position: fixed;
                left:0; top:0; width:100vw; height:100vh;
                z-index:-1;
                pointer-events:none;
                display:flex;
                align-items:center;
                justify-content:center;
                opacity:0.10;
                font-size:5em;
                font-weight:bold;
                color:#ccc;
                user-select:none;
                white-space: nowrap;
                transform: rotate(-30deg);
                letter-spacing: 0.2em;
            }}
            .dashborad-header{{
                background: liner-gradient(90deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                padding: 32px 0 24px 0;
                text-align: center;
                box-shadow: 0 2px 8px rgba(58, 141, 222, 0.08);
                margin-bottom: 0;
                position: relative;
            }}
            .dashborad-header .logo {{
                width: 54px;
                height: 54px;
                border-radius: 50px;
                background: #fff;
                display: inline-flex;
                align-items: center;
                margin-right: 12px;
                box-shadow: 0 2px 8px rgba(58, 141, 222, 0.2);
                animation: popin 0.7s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            }}
            .dashborad-header .logo svg {{ width: 36px; height: 36px; }}
            @keyframes popin {{
                0% {{ transform: scale(0); opacity: 0; }}
                80% {{ transform: scale(1.1); opacity: 1; }}
                100% {{ transform: scale(1); }}
            }}
            .accent-bar {{
            height: 7px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            margin-bottom: 32px;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
            box-shadow: 0 2px 8px rgba(58, 141, 222, 0.2);
            animation: slidein 1s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            }}
            @keyframes slidein {{
                0% {{ width: 0; opacity: 0; }}
                100% {{ width: 100%; opacity: 1; }}
            }}
            .app_name {{
                font-size: 1.12em;
                font-weight: 700;
                letter-spacing: 0.05em;
                margin-top: 8px;
                opacity: 0.85;
                text-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .dasbhoard-header h1 {{ font-size:2.5rem; margin: 0 0 10px 0; font-weight: 700; letter-spacing: 1px; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .dashboard-header p {{ font-size:1.1rem; margin: 0; font-weight: 400; }}
            .dashboard-meta {{ 
                max-width: 1200px;
                margin: 0 auto 24px auto;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                padding: 12px 24px;
                display: flex;
                gap: 32px;
                align-items: center;
                justify-content: center;
                animation: fadein 1s ease-in-out;
            }}
            @keyframes fadein {{
                0% {{ opacity: 0; }}
                100% {{ opacity: 1; }}
            }}
            .dashboard-meta p {{ margin: 0; font-size: 0.95rem; color: #555; }}
            .dashboard-content {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
                    padding: 24px;
                    animation: fadein 1s ease-in-out;
            }}
            .sticky-controls {{
                    position: sticky;
                    top: 0;
                    background: #fff;
                    z-index: 10;
                    padding: 12px 0 8px 0;
                    border-bottom: 1px solid #eee;
            }}
            .commit-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 16px;
            }}
            .commit-table th, .commit-table td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            .commit-table th {{
                background-color: #f4f4f4;
            }}
            .commit-table tr:nth-child(even) {{ background : #f7f9fb;}}
            .commit-table tr:hover {{ background : #d6ecfa; transition: backgrounf 0.2s}}
            .commit-table td {{ font-size: 0.98rem;}}
            .pagination-bns button {{
                background: #667eea;
                color: #fff;
                border: none;
                padding: 8px 12px;
                margin: 0 4px;
                border-radius: 4px;
                cursor: pointer;
            }}
            .pagination-bns button:hover, .peginstion-btns buttom.active {{
                background: #764ba2;
                color: #fff;
                font-weight: bold;
            }}
            #commit-search {{
                border: 1px solid #ccc;
                border-radius: 4px;
            }} 
            @media (max-width: 768px) {{
                .dashboard-meta, .dashboard-content {{
                    padding: 16px;
                }}
                .dashborad-header h1 {{ font-size: 1.8rem; }}
            }}
            .app-name {{
                font-size: 1.2em;
                font-weight: 600;
                margin-bottom: 8px;
                text-shadow: 0 1px 2px rgba(0,0,0,0.1);
                leatter-spacing: 0.03em;
                opacity: 0.9;
                text-shadow: 0 1px 3px rgba(0,0,0,0.1);
                color:#667eea
            }}
        </style>
    </head>
    <body>
        <div class="watermark">gitviz</div>
        <div class="dashborad-header">
            <div class="app-name">Application Name: {app_name}</div>
            <h1 class="app-name">{title}</h1>
            {f'<p>{description}</p>' if description else ''}
        </div>
        <div class="accent-bar"></div>
        <div class="dashboard-meta">
            {f'<p><b>Author:</b> {author}</p>' if author else ''}
            <p><b>Generated on:</b> {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        <div class="dashboard-content">
            {fig_html}
            <div class="sticky-controls">
            </div>
            {table_html}
        </div>
    </body>
    </html>
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
