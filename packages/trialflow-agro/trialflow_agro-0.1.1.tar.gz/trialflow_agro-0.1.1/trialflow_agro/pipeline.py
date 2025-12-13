"""
Pipeline orchestrator for trialflow-agro.

Ties together:
- config loading (YAML + Pydantic)
- data loading and validation
- summary "inference"
- diagnostics
- writing results.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from trialflow_agro.config.schema import ConfigLoader, TrialflowConfig
from trialflow_agro.data.loaders import TrialDataLoader
from trialflow_agro.inference.diagnostics import compute_diagnostics
from trialflow_agro.inference.fit import TrialInference
from trialflow_agro.models.hierarchical import TrialModel


class Pipeline:
    """
    High-level runner for a single trialflow-agro analysis.

    - Reads YAML config
    - Loads data from config.data.path
    - Builds TrialModel and runs TrialInference
    - Computes basic diagnostics
    - Writes results.json under the chosen output directory
    """

    def __init__(self, config_path: Path, output_dir: Optional[Path] = None) -> None:
        self.config_path = config_path
        # Optional CLI override; if None we use config.output.directory
        self._output_dir_override = output_dir
        self._output_dir: Optional[Path] = None

    @property
    def output_dir(self) -> Path:
        """
        Final output directory used for this run.
        Valid only after `run()` has been called.
        """
        if self._output_dir is None:
            raise RuntimeError("Pipeline.run() has not been executed yet.")
        return self._output_dir

    def run(self) -> None:
        # Load config
        cfg: TrialflowConfig = ConfigLoader().load(self.config_path)

        # Load data based purely on config (config-driven workflow)
        data_path = cfg.data.path
        df = TrialDataLoader().load(data_path)

        # Build model spec & run inference
        model = TrialModel(cfg.model)
        inference_engine = TrialInference(
            groups=model.spec.groups,
            min_records_per_group=model.spec.min_records_per_group,
        )
        inference_result = inference_engine.run(df)

        # Diagnostics
        diagnostics = compute_diagnostics(df)

        # Decide output directory: CLI override or config default
        out_dir = self._output_dir_override or cfg.output.directory
        self._output_dir = out_dir

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "results.json").write_text(
            json.dumps(
                {
                    "config": cfg.model_dump(mode="json"),
                    "inference": inference_result.model_dump(mode="json"),
                    "diagnostics": diagnostics,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
