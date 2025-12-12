# model_registry.py
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Union, Optional
from pandas import DataFrame
import logging

from aiq.churn.algo.feature_selectors.base import BaseFeatureSelector
from aiq.churn.plugin.inputs.DataTransformer import DataTransformer
from aiq.churn.utility import save_artifact, load_artifact, save_data

logger = logging.getLogger(__name__)

class ModelRegistry:

    def __init__(self, registry_path: Union[str, Path]):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)

    def get_next_version(self, service_name: str, algo_name: str) -> str:
        algo_path = self.registry_path / service_name / algo_name
        if not algo_path.exists():
            return "v1"
        versions = [d.name for d in algo_path.iterdir() if d.is_dir() and d.name.startswith("v")]
        if not versions:
            return "v1"
        latest = sorted(versions, key=lambda x: int(x[1:]))[-1]
        next_version = int(latest[1:]) + 1
        return f"v{next_version}"

    def get_latest_version(self, service_name: str, algo_name: str) -> str:
        algo_path = self.registry_path / service_name / algo_name
        if not algo_path.exists():
            return "v1"  # nothing exists → overwrite first version
        versions = [
            d.name for d in algo_path.iterdir()
            if d.is_dir() and d.name.startswith("v")
        ]
        if not versions:
            return "v1"
        latest = sorted(versions, key=lambda x: int(x[1:]))[-1]
        return latest

    def register_model(
            self,
            model: Any,
            service_name: str,
            algo_name: str,
            metrics: Dict[str, Any],
            params: Dict[str, Any] = None,
            version: str = None,
            train_data: DataFrame = None,
            test_data: DataFrame = None,
            transformer: DataTransformer = None,
            featureSelector: BaseFeatureSelector = None
        ):
        if version is None:
            version = self.get_next_version(service_name, algo_name)
        else:
            logger.warning(f"Explicit version '{version}' provided. Will re-register if it exists.")

        model_name = f"{service_name}_{algo_name}_{version}"
        model_path = self.registry_path / service_name / algo_name / version
        model_path.mkdir(parents=True, exist_ok=True)

        # --- 1. Save Core Model Artifact ---
        save_artifact(model, model_path / "model.joblib")

        # --- 2. Save Metadata ---
        metadata = {
            "model_name": model_name,
            "service": service_name,
            "algorithm": algo_name,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "parameters": params or {}
        }
        with open(model_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=4)

        logger.info(f"Registered core model: {model_name} at {model_path}")

        # --- 3. Save Supplementary Artifacts ---
        self.save_supplementary_artifacts(
            base_path=model_path,
            transformer=transformer,
            featureSelector=featureSelector,
            train_data=train_data,
            test_data=test_data
        )
        logger.info(f"Successfully registered model and all artifacts: {model_name}")

    def load_model(self, published_dir: Path) -> Any:
        print(f"load_model from {published_dir}")
        if not published_dir.exists():
            raise FileNotFoundError(f"No models found under : '{published_dir}'")
        model_file = published_dir / "model.joblib"
        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found at: {model_file}")

        logger.info(f"Loading model from '{published_dir}")
        return load_artifact(model_file)

    def save_supplementary_artifacts(
            self,
            base_path: Path,
            transformer: Optional[DataTransformer] = None,
            featureSelector: Optional[BaseFeatureSelector] = None,
            train_data: Optional[DataFrame] = None,
            test_data: Optional[DataFrame] = None
    ):
        logger.info("  Saving supplementary artifacts...")

        if transformer:
            transformer.save_state(base_path / "transformer.joblib")
            logger.info(f"  - Saved transformer.")

        if featureSelector:
            featureSelector.save_state(base_path / "selected_features.joblib")
            logger.info(f"  - Saved feature selector.")

        # Save data
        if train_data is not None or test_data is not None:
            data_path = base_path / "data"
            data_path.mkdir(parents=True, exist_ok=True)

            if train_data is not None:
                save_data(train_data, data_path / "train_data.csv")
                logger.info(f"  - Saved train_data.")

            if test_data is not None:
                save_data(test_data, data_path / "test_data.csv")
                logger.info(f"  - Saved test_data.")


    def get_model_archive_path_old(self, service_name: str, algo_name: str, version: str = None) -> Path:
        if version is None:
            version = self.get_next_version(service_name, algo_name)

        # path structure: registry_path / service / algorithm / version / data
        model_path = self.registry_path / service_name / algo_name / version
        data_archive_path = model_path / "data"
        data_archive_path.mkdir(parents=True, exist_ok=True)

        return data_archive_path

    def get_model_archive_path(self, service_name: str, algo_name: str, version: str, create: bool = True) -> Path:
        """
        Returns the data archive path for a given (service, algo, version).
        Does NOT decide the version; caller must pass it in.
        """
        model_path = self.registry_path / service_name / algo_name / version
        data_archive_path = model_path / "data"
        if create:
            data_archive_path.mkdir(parents=True, exist_ok=True)
        return data_archive_path