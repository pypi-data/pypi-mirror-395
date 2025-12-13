from __future__ import annotations

from pathlib import Path

from trialflow_agro.config.schema import ConfigLoader
from trialflow_agro.data.loaders import TrialDataLoader


def test_config_loader_round_trip(demo_config_path: Path):
    cfg = ConfigLoader().load(demo_config_path)

    # We only assert on fields your code actually uses:
    # - cfg.data.path
    # - cfg.output.directory
    assert cfg.data.path.exists()
    assert hasattr(cfg.output, "directory")


def test_trial_data_loader_basic(demo_data: Path):
    df = TrialDataLoader().load(demo_data)

    assert not df.empty
    # Must at least include all REQUIRED_COLUMNS
    for col in ["field_id", "farm_id", "region", "year", "product", "yield"]:
        assert col in df.columns
