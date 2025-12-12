import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
from pandas import DataFrame
import shutil

from aiq.churn.plugin.inputs.InputDataReader import InputDataReader

class DirectoryInputDataReader(InputDataReader):
    directory: Path = None
    archive_dir: Optional[Path] = None
    max_workers: int = None
    required_schema: dict = None
    required_column_names: list = None

    def __init__(self):
        super().__init__()

    def load_configs(self, config: dict, final_archive_path: Path = None):
        src_cfg = config['data_source']
        dir_cfg = src_cfg.get("directory", {})

        self.directory = Path(dir_cfg["path"])

        if final_archive_path:
            self.archive_dir = final_archive_path
        else:
            archive_path_str = dir_cfg.get("archive_path")
            if archive_path_str:
                self.archive_dir = Path(archive_path_str)

        self.max_workers = dir_cfg.get("max_workers", os.cpu_count() or 1)
        self.required_schema = config.get("required_columns", {})

        self.required_column_names = list(self.required_schema.keys())
        print(f"Required Columns (Keys extracted): {self.required_column_names}")

    def read_data(self):
        print(f"Starting parallel ingestion from directory: {self.directory}")

        if not self.directory.is_dir():
            raise NotADirectoryError(f"Directory not found: {self.directory}")

        csv_files = self.find_csv_files()
        if not csv_files:
            print(f"No CSV files found in directory: {self.directory}")
            self.dataframe = pd.DataFrame()
            return

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tmp_dfs = list(executor.map(self.load_single_file, csv_files))

        dfs = []
        success_files = []
        failed_files = []

        for file_path, df in tmp_dfs:
            if df is not None:
                dfs.append(df)
                success_files.append(file_path)
            else:
                failed_files.append(file_path.name)

        if failed_files:
            print(f"Warning: Failed to load {len(failed_files)} files: {failed_files}")

        if not dfs:
            print("No files were successfully loaded. Empty DataFrame.")
            self.dataframe = pd.DataFrame()
            return

        try:
            final_df = pd.concat(dfs, ignore_index=True)
            self.validate_schema(final_df)
        except Exception as e:
            self.logger.error(f"Failed to concatenate DataFrames or validate final schema: {e}")
            self.logger.error("Files will NOT be archived.")
            return

        elapsed_time = time.time() - start_time
        print(f"Loaded and combined {len(dfs)}/{len(csv_files)} files in {elapsed_time:.2f} seconds.")
        print(f"Final DataFrame shape: {final_df.shape}")

        self.dataframe = final_df
        self.logger.info("data read done")

        if self.archive_dir:
            self.archive_files(success_files)
        else:
            print("No archive_dir provided. Files will not be moved.")

    def get_data(self) -> DataFrame:
        return self.dataframe


    def find_csv_files(self) -> List[Path]:
        csv_files = list(self.directory.glob('*.csv'))  # Use .glob('*.csv') for non-recursive or .rglob('*.csv') for recursive search
        return csv_files

    def load_single_file(self, file_path: Path) -> Tuple[Path, Optional[pd.DataFrame]]:
        try:
            print(f"Reading file in thread: {file_path.name}")
            df = pd.read_csv(file_path, dtype=self.required_schema)
            self.validate_schema(df)
            #df['__source_file'] = file_path.name
            return file_path, df
        except Exception as e:
            print(f"Failed to read file {file_path.name} (Check file content/encoding/schema): {e}")
            return file_path, None


    def validate_schema(self, df: pd.DataFrame):
        if not self.required_column_names:
            print("No required columns defined for schema validation.")
            return

        missing_columns = [col for col in self.required_column_names if col not in df.columns]
        if missing_columns:
            error_msg = f"Schema Validation Failed: Missing critical columns: {missing_columns}"
            print(error_msg)
            raise ValueError(error_msg)

        #print("Schema completeness validation successful: All required columns are present.")

    def archive_files(self, file_paths: List[Path]):
        if not self.archive_dir:
            return

        print(f"Archiving {len(file_paths)} successfully processed files to {self.archive_dir}...")
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        for file_path in file_paths:
            try:
                dest_path = self.archive_dir / file_path.name
                shutil.move(str(file_path), str(dest_path))
            except Exception as e:
                self.logger.warning(f"Warning: Failed to move file {file_path.name} to {self.archive_dir}: {e}")

