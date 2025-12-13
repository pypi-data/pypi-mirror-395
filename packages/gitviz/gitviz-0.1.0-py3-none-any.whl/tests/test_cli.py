import os
from git import Repo, InvalidGitRepositoryError
import pytest
from click.testing import CliRunner
from gitviz.cli import main


def test_cli_write_outputs(tmp_path):
    path = os.getcwd()
    try:
        Repo(path)
    except InvalidGitRepositoryError:
        pytest.skip("Not inside a git repo; skipping CLI output test")

    runner = CliRunner()

    out_html = tmp_path / "dash.html"
    out_csv = tmp_path / "activity.csv"
    out_json = tmp_path / "activity.json"

    result = runner.invoke(main, [path, "--output", str(out_html), "--export-csv", str(out_csv), "--export-json", str(out_json)])
    assert result.exit_code == 0
    assert out_html.exists()
    assert out_csv.exists()
    assert out_json.exists()
