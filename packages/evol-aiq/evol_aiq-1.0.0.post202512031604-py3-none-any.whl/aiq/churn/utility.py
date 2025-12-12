import importlib
import sys
import logging
import yaml
import json
import joblib
from pathlib import Path
from typing import Any, Dict, Union

from pandas import DataFrame, Series

logger = logging.getLogger(__name__)
def load_class(class_package: str, class_name: str, class_ref: type):
    try:
        module = importlib.import_module(class_package)
        the_class = getattr(module, class_name)
        the_instance = the_class()
        if isinstance(the_instance, class_ref):
            return the_instance
        else:
            logger.info("unable to load plugin {}, expected {}".format(class_package, class_ref))
    except(ModuleNotFoundError, ImportError) as e:
        logger.error(e)
        logger.info("unable to load plugin {}, as {}".format(class_package, e))
        sys.exit(1)

def load_config(path: Union[str, Path] = 'config/config.yaml') -> Dict:
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    logger.info("Configuration loaded successfully.")
    return config

def save_artifact(obj: Any, path: Union[str, Path]):
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(obj, path)
        logger.info(f"Artifact saved successfully to: {path}")
    except (IOError, PermissionError) as e:
        logger.info(f"Error: Could not save artifact to {path}. Reason: {e}")
        raise

def load_artifact(path: Union[str, Path]) -> Any:
    path = Path(path)
    try:
        obj = joblib.load(path)
        logger.info(f"Artifact loaded successfully from: {path}")
        return obj
    except FileNotFoundError:
        logger.info(f"Error: The file was not found at {path}")
        raise

def save_dict_as_json(data: Dict, path: Union[str, Path]):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON report saved successfully to: {path}")

def save_data(df: DataFrame, path: Union[str, Path]) -> None:
    path = Path(path)
    try:
        # Ensure the parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving data to: {path}")
        df.to_csv(path, index=False)
        logger.info("Data saved successfully.")
    except (IOError, PermissionError) as e:
        logger.info(f"Error: Could not save file to {path}. Reason: {e}")
        raise


def get_data_summary(df: DataFrame) -> None:
    logger.info("=" * 30)
    logger.info("      DATA SUMMARY REPORT      ")
    logger.info("=" * 30)

    logger.info("\n[ DataFrame Info ]")
    df.info()

    logger.info("\n" + "=" * 30)
    logger.info("\n[ Descriptive Statistics (Numerical) ]")
    logger.info(df.describe())

    logger.info("\n" + "=" * 30)
    logger.info("\n[ Missing Values (%) ]")
    missing_values = get_missing_values_summary(df)
    if missing_values.empty:
        logger.info("No missing values found.")
    else:
        logger.info(missing_values)

    logger.info("\n" + "=" * 30)
    logger.info("\n[ Duplicate Rows Count ]")
    logger.info(get_duplicate_count(df))
    logger.info("\n" + "=" * 30)


def get_missing_values_summary(df: DataFrame) -> Series:
    return round((df.isnull().sum() * 100 / df.shape[0]), 2)

def get_duplicate_count(df: DataFrame) -> int:
    return df.duplicated().sum()

def round_double(num: float, precision: int) -> float:
    return round(num, precision)