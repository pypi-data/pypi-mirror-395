import logging
import os
import time
import shutil
from fileinput import filename

import yaml
from mysql.connector import pooling
from enum import Enum



class FileType(Enum):
    RECHARGE = "RECHARGE"
    BILLING = "BILLING"
    MARKETING_COST = "MARKETING_COST"
    UNKNOWN = "UNKNOWN"

class FileDataLoader:
    logger = logging.getLogger(__name__)

    def __init__(self, analytics_config: dict):
        db_cfg = analytics_config['mysql']
        dir_cfg = analytics_config['dirs']
        self.file_dir = dir_cfg['file_dir']
        self.processed_dir = dir_cfg['processed_dir']
        self.pool = pooling.MySQLConnectionPool(
            **db_cfg
        )
        print("FileDataLoader")

    def ensure_dir_exists(self, path):
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    def read_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()

    def process_file(self, file_path, filename):
        print(f"[INFO] Processing file: {filename}")
        ftype = self.get_file_type(filename)
        if ftype == FileType.UNKNOWN:
            print(f"[WARN] Unknown file type: {filename}")
            return
        lines = self.read_file(file_path)
        self.insert_data(lines, ftype, filename)
        self.move_processed(file_path, filename)

    def get_file_type(self, fname):
        fname = fname.upper()
        if "RECHARGE" in fname: return FileType.RECHARGE
        if "BILLING" in fname: return FileType.BILLING
        if "MARKETING" in fname or "MKT" in fname: return FileType.MARKETING_COST
        return FileType.UNKNOWN

    def insert_data(self, lines, ftype, filename):
        if ftype == FileType.RECHARGE:
            self.load_data_to_recharge_db(lines, filename)
        elif ftype == FileType.BILLING:
            self.load_data_to_billing_db(lines, filename)
        elif ftype == FileType.MARKETING_COST:
            self.load_data_to_marketing_cost_db(lines, filename)

    def load_data_to_recharge_db(self, lines, file_name):
        conn = None
        cursor = None

        try:
            conn =  self.pool.get_connection()
            cursor = conn.cursor()

            # SQL to insert into monthly_recharge table
            sql = """
                INSERT INTO monthly_recharge
                    (recharge_id, customerid, recharge_date, recharge_month, recharge_amount, recharge_type, channel)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # skip empty lines / headers

                parts = line.split(",")

                # Validation: must be exactly 5 fields
                if len(parts) != 7:
                    print(f"[WARN] Skipping malformed line: {line}")
                    continue

                recharge_id, customerid, recharge_date, recharge_month, recharge_amount, recharge_type, channel = parts

                # Convert data types
                try:
                    recharge_amount = float(recharge_amount)
                except ValueError:
                    print(f"[WARN] Invalid amount, skipping: {line}")
                    continue

                # Execute insert
                cursor.execute(sql, (
                    recharge_id,
                    customerid,
                    recharge_date,
                    recharge_month,
                    recharge_amount,
                    recharge_type,
                    channel
                ))

            conn.commit()

            print(f"[OK] monthly_recharge entries inserted from file: {file_name}")

        except Exception as e:
            print(f"[ERROR] Failed to load file {file_name}: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_data_to_billing_db(self, lines, file_name):
        conn = None
        cursor = None

        try:
            conn =  self.pool.get_connection()
            cursor = conn.cursor()

            sql = """
                INSERT INTO monthly_billing (
                    billing_id,
                    customerid,
                    billing_month,
                    billing_amount,
                    payment_status,
                    payment_date
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """

            for line in lines:
                line = line.strip()

                # Skip empty or commented lines
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")

                # Header format expected: 6 fields
                if len(parts) != 6:
                    print(f"[WARN] Skipping malformed line (expected 6 fields) found : {len(parts)}, {line}")
                    continue

                (
                    billing_id,
                    customerid,
                    billing_month,
                    billing_amount,
                    payment_status,
                    payment_date
                ) = parts

                # Validate billing amount
                try:
                    billing_amount = float(billing_amount)
                except ValueError:
                    print(f"[WARN] Invalid billing_amount, skipping: {line}")
                    continue

                # Normalize dates
                billing_month = billing_month.strip()
                payment_status = payment_status.strip()

                if payment_date.strip() == "" or payment_date.strip().upper() == "NULL":
                    payment_date = None

                # Insert
                try:
                    cursor.execute(
                        sql,
                        (
                            billing_id.strip(),
                            customerid.strip(),
                            billing_month,
                            billing_amount,
                            payment_status,
                            payment_date
                        )
                    )
                except Exception as e:
                    print(f"[WARN] Failed to insert line: {line} -> {e}")
                    continue

            conn.commit()
            print(f"[OK] monthly_billing entries inserted successfully from file: {file_name}")

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Failed to load file {file_name}: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def load_data_to_marketing_cost_db(self, lines, file_name):
        conn = None
        cursor = None

        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()

            sql = """
                        INSERT INTO acquisition_cost (
                            cost_id,
                            segmentid,
                            channelid,
                            calculation_period,
                            total_marketing_spend,
                            customers_acquired,
                            campaign_details
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

            for line in lines:
                line = line.strip()

                # Skip empty or commented lines
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")

                # Header format expected: 7 fields
                if len(parts) != 7:
                    print(f"[WARN] Skipping malformed line (expected 7 fields) found: {len(parts)}, {line}")
                    continue

                (
                    cost_id,
                    segmentid,
                    channelid,
                    calculation_period,
                    total_marketing_spend,
                    customers_acquired,
                    campaign_details
                ) = parts

                # Insert
                try:
                    cursor.execute(
                        sql,
                        (
                            cost_id,
                            segmentid,
                            channelid,
                            calculation_period,
                            total_marketing_spend,
                            customers_acquired,
                            campaign_details
                        )
                    )
                except Exception as e:
                    print(f"[WARN] Failed to insert line: {line} -> {e}")
                    continue

            conn.commit()
            print(f"[OK] acquisition_cost  entries inserted successfully from file: {file_name}")

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Failed to load file {file_name}: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def move_processed(self, file_path, file_name):
        dest = os.path.join(self.processed_dir, file_name)
        shutil.move(file_path, dest)
        print(f"[OK] File moved to processed folder: {dest}")

    def run_loader(self):
        print("FileDataLoader running...")
        self.ensure_dir_exists(self.processed_dir)
        print("File DataLoader processing files...")
        for filename in os.listdir(self.file_dir):
            if filename.endswith(".csv"):
                path = os.path.join(self.file_dir, filename)
                self.process_file(path, filename)
        print("File DataLoader processed files...")
