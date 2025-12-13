from __future__ import annotations

from pathlib import Path

from trialflow_agro.pipeline import Pipeline


def test_pipeline_run_creates_results_json(demo_config_path: Path, tmp_path: Path):
    out_dir = tmp_path / "results_override"
    pipeline = Pipeline(config_path=demo_config_path, output_dir=out_dir)

    pipeline.run()

    assert pipeline.output_dir == out_dir
    results_path = out_dir / "results.json"
    assert results_path.exists()
    text = results_path.read_text()
    assert '"inference"' in text
    assert '"diagnostics"' in text
