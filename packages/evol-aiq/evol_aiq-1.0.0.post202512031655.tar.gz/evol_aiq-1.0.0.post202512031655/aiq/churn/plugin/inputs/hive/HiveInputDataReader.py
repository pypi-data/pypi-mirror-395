from pathlib import Path

import pandas as pd
from pandas import DataFrame
from pyhive import hive
import time
import os

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:
    pa = None
    pq = None

from aiq.churn.plugin.inputs.InputDataReader import InputDataReader

class HiveInputDataReader(InputDataReader):

    def __init__(self):
        super().__init__()

    def load_configs(self, config: dict, final_archive_path: Path = None):
        src_cfg = config['data_source']
        hive_cfg = src_cfg["hive"]

        self.host = hive_cfg["host"]
        self.port = hive_cfg.get("port", 10000)
        self.database = hive_cfg.get("database", "default")
        self.query = hive_cfg.get("query")
        self.auth = hive_cfg.get("auth", "NONE")
        self.username = hive_cfg.get("username")
        self.password = hive_cfg.get("password")
        self.chunk_size = hive_cfg.get("chunk_size", 50000)
        self.max_retries = hive_cfg.get("max_retries", 3)
        self.connect_timeout = hive_cfg.get("connect_timeout", 30)
        self.output_file = hive_cfg.get("output_file")
        self.output_format = hive_cfg.get("output_format")

    def _get_connection(self):
        args = {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "auth": self.auth or "NONE",
            #"connect_timeout": self.connect_timeout,
        }
        if self.username:
            args["username"] = self.username
        if self.password:
            args["password"] = self.password
        self.logger.info(f"Connecting to Hive with: {args}")
        return hive.Connection(**args)

    def read_data(self):
        attempt = 0
        while attempt < self.max_retries:
            try:
                conn = self._get_connection()
                self.logger.info(f"Connected to Hive at {self.host}:{self.port}, database: {self.database}")
                start_time = time.time()
                chunks = []
                total_rows = 0

                # Prepare Parquet writer if needed
                if self.output_file and self.output_format == "parquet":
                    if pa is None or pq is None:
                        raise ImportError("pyarrow is required for Parquet output.")
                    if os.path.exists(self.output_file):
                        os.remove(self.output_file)
                    writer = None

                for chunk in pd.read_sql(self.query, conn, chunksize=self.chunk_size):
                    nrows = len(chunk)
                    total_rows += nrows
                    self.logger.info(f"Fetched chunk with {nrows} rows (total fetched: {total_rows})")
                    # Always collect chunk for DataFrame return
                    chunks.append(chunk)
                    if self.output_file:
                        if self.output_format == "csv":
                            chunk.to_csv(self.output_file, mode="a", header=(total_rows == nrows), index=False)
                        elif self.output_format == "parquet":
                            table = pa.Table.from_pandas(chunk)
                            if writer is None:
                                writer = pq.ParquetWriter(self.output_file, table.schema)
                            writer.write_table(table)
                        else:
                            raise ValueError(f"Unknown output format: {self.output_format}")

                if self.output_file and self.output_format == "parquet" and writer is not None:
                    writer.close()

                conn.close()
                elapsed = time.time() - start_time
                self.logger.info(f"Query finished: {total_rows} rows in {elapsed:.1f} seconds.")

                if chunks:
                    df = pd.concat(chunks, ignore_index=True)
                    df.columns = [col.split('.')[-1] for col in df.columns]     # for ADM -- remove tablename prefix from column name -- churntbla.customerid to customerid
                else:
                    df = pd.DataFrame()
                self.logger.info(f"Final DataFrame shape: {df.shape}")
                print(df.head())
                self.dataframe = df

            except Exception as ex:
                self.logger.error(f"Hive ingestion failed (attempt {attempt+1} of {self.max_retries}): {str(ex)}")
                attempt += 1
                time.sleep(2 ** attempt)
                if attempt >= self.max_retries:
                    self.logger.critical("All retries failed.")
                    raise ex

    
    def get_data(self) -> DataFrame:
        return self.dataframe

