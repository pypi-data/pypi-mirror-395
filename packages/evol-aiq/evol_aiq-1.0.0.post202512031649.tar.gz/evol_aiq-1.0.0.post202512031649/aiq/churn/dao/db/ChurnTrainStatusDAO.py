import time

from aiq.churn.dao.db.AIQMysqlDBPool import AIQMysqlDBPool
import json


class ChurnTrainStatusDAO:
    def __init__(self, config: dict):
        host = config['aiq_core']["mysql"]["host"]
        port = config['aiq_core']["mysql"]["port"]
        user = config['aiq_core']["mysql"]["user"]
        password = config['aiq_core']["mysql"]["password"]
        database = config['aiq_core']["mysql"]["database"]
        pool_name = config['aiq_core']["mysql"]["pool_name"]
        pool_size = config['aiq_core']["mysql"]["pool_size"]
        AIQMysqlDBPool.initialize_pool(host=host, user=user, password=password, database=database, pool_name=pool_name, pool_size=pool_size, port=port)
        self.published_state_cache = None


    def _get_connection(self):
        conn = AIQMysqlDBPool.get_connection()
        return conn

    def create(self, algorithm_id, model_version, status, triggered_by="AUTO", hyperparams: dict = None):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO t1_churn_train_status (
                algorithm_id, model_version, status, triggered_by, start_time, hyperparams
            ) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
            """
            values = (algorithm_id, model_version, status, triggered_by, json.dumps(hyperparams))
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, id):
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_churn_train_status WHERE id = %s"
            cursor.execute(query, (id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_to_publish_by_id(self, run_id):
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_churn_train_status WHERE id = %s and status = 'COMPLETED' AND published = FALSE"
            cursor.execute(query, (run_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_loaded_and_published_state(self):
        if self.published_state_cache is not None:
            return self.published_state_cache

        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_churn_train_status WHERE  status = 'COMPLETED' AND published = TRUE"
            cursor.execute(query, )
            result = cursor.fetchone()
            self.published_state_cache = result  # Cache the result
            return result
        finally:
            cursor.close()
            conn.close()

    def publish_by_id(self, run_id):
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            # Step 1: Set all other records to published = FALSE
            update_others_query = """
                        UPDATE t1_churn_train_status
                        SET published = FALSE;
                    """
            cursor.execute(update_others_query)

            update_query = """
                        UPDATE t1_churn_train_status
                        SET published = TRUE
                        WHERE id = %s
                    """
            cursor.execute(update_query, (run_id,))
            conn.commit()

            self.published_state_cache = None

            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def is_a_job_running(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_churn_train_status WHERE status = %s LIMIT 1"
            cursor.execute(query, ("RUNNING",))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def last_unpublished_state(self, algorithm_id: str):
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_churn_train_status WHERE algorithm_id = %s and published = FALSE order by id desc LIMIT 1"
            cursor.execute(query, (algorithm_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def complete_running_status(self, error_message=None):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            UPDATE t1_churn_train_status
            SET status = %s, end_time = CURRENT_TIMESTAMP, error_message = %s
            WHERE status = %s
            """
            cursor.execute(query, ('COMPLETED', error_message, 'RUNNING'))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    def complete(self, run_id, model_version, records_trained, accuracy, precision, recall, f1_score,
                 model_artifact_path, error_message=None):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE t1_churn_train_status
            SET model_version = %s,
                status = %s,
                end_time = CURRENT_TIMESTAMP,
                records_trained = %s,
                accuracy = %s,
                `precision` = %s,
                recall = %s,
                f1_score = %s,
                model_artifact_path = %s,
                error_message = %s
            WHERE id = %s
            """

            values = (
                model_version,
                'COMPLETED',
                records_trained,
                accuracy,
                precision,
                recall,
                f1_score,
                model_artifact_path,
                error_message,
                run_id
            )

            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount  # Number of rows updated
        finally:
            cursor.close()
            conn.close()

    def fail_running_status(self, error_message=None):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = """
            UPDATE t1_churn_train_status
            SET status = %s, end_time = CURRENT_TIMESTAMP, error_message = %s
            WHERE status = %s
            """
            cursor.execute(query, ('FAILED', error_message, 'RUNNING'))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    def list_all(self):
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_churn_train_status ORDER BY created_at DESC"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def delete(self, id):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM t1_churn_train_status WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()