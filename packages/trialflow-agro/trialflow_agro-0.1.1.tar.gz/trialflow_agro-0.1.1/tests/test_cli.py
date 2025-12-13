from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from trialflow_agro.cli.main import app

runner = CliRunner()


def test_cli_fit_creates_results(demo_config_path: Path, tmp_path: Path):
    out_dir = tmp_path / "cli_results"

    result = runner.invoke(
        app,
        [
            "fit",
            str(demo_config_path),
            "--out",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert (out_dir / "results.json").exists()


def test_cli_report_creates_html(demo_config_path: Path, tmp_path: Path):
    # first run fit
    results_dir = tmp_path / "results"
    fit_result = runner.invoke(
        app,
        [
            "fit",
            str(demo_config_path),
            "--out",
            str(results_dir),
        ],
    )
    assert fit_result.exit_code == 0

    report_path = tmp_path / "report.html"
    result = runner.invoke(
        app,
        [
            "report",
            str(results_dir),
            "--out",
            str(report_path),
        ],
    )

    assert result.exit_code == 0
    assert report_path.exists()
    assert "<html" in report_path.read_text().lower()
