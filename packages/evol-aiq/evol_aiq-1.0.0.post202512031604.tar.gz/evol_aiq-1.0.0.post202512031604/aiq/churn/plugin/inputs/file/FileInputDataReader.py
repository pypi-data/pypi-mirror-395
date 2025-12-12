from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import DataFrame
import shutil
import os
from aiq.churn.plugin.inputs.InputDataReader import InputDataReader

class FileInputDataReader(InputDataReader):
    input_file: str = None
    raw_file_type: str = None
    archive_path: Optional[str] = None

    def __init__(self):
        super().__init__()

    def load_configs(self, config: dict, final_archive_path: Path = None):
        src_cfg = config['data_source']
        file_cfg = src_cfg.get('file', {})

        self.input_file = file_cfg.get("path")
        self.raw_file_type = file_cfg.get("type")
        #self.archive_path = file_cfg.get("archive_path")
        if final_archive_path:
            self.archive_path = str(final_archive_path)
        else:
            self.archive_path = file_cfg.get("archive_path")

    def read_data(self):
        if self.input_file is None:
            self.logger.info("Input file path is None. Skipping read.")
            return

        if not os.path.exists(self.input_file):
            self.logger.error(f"Input file not found at: {self.input_file}")
            return

        try:
            if self.raw_file_type == 'csv':
                self.dataframe = pd.read_csv(self.input_file)
            else:
                self.dataframe = pd.read_json(self.input_file, lines=True)
            self.logger.info(f"Successfully read data from {self.input_file}")

        except Exception as e:
            self.logger.error(f"Failed to read data from {self.input_file}: {e}")
            return

        if self.archive_path:
            original_filename = os.path.basename(self.input_file)
            dest_path = os.path.join(self.archive_path, original_filename)
            try:
                #dest_dir = os.path.dirname(dest_path)
                #os.makedirs(self.archive_path, exist_ok=True)

                # Move the file
                self.logger.info(f"Moving processed file {self.input_file} to {dest_path}")
                shutil.move(self.input_file, dest_path)
                self.logger.info(f"File moved successfully to {dest_path}")

            except Exception as e:
                self.logger.warning(f"Failed to move file {self.input_file} to {self.archive_path}: {e}")
        else:
            self.logger.info("No archive_path provided. File will not be moved.")

    def get_data(self) -> DataFrame:
        return self.dataframe
