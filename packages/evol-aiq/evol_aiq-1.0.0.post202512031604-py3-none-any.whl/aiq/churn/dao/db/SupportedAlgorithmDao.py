import mysql.connector

from aiq.churn.dao.db.AIQMysqlDBPool import AIQMysqlDBPool


class SupportedAlgorithmDao:

    def __init__(self, config: dict):
        host = config['aiq_core']["mysql"]["host"]
        port = config['aiq_core']["mysql"]["port"]
        user = config['aiq_core']["mysql"]["user"]
        password = config['aiq_core']["mysql"]["password"]
        database = config['aiq_core']["mysql"]["database"]
        pool_name = config['aiq_core']["mysql"]["pool_name"]
        pool_size = config['aiq_core']["mysql"]["pool_size"]
        AIQMysqlDBPool.initialize_pool(host=host, user=user, password=password, database=database, pool_name=pool_name, pool_size=pool_size, port=port)
        self.algos_cache = None

    def _get_connection(self):
        conn = AIQMysqlDBPool.get_connection()
        return conn

    def get_algo_by_id(self, algo_id):
        if self.algos_cache is None:
            self.get_all_active_algorithms()

        for algo in self.algos_cache:
            if algo.get('id') == algo_id:  # Adjust key name if it's different
                return algo

        return None

    def get_all_active_algorithms(self):
        if self.algos_cache is not None:
            return self.algos_cache
        """Fetch all active algorithms"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_supported_algorithm WHERE status = 1"
            cursor.execute(query)
            result = cursor.fetchall()
            self.algos_cache = result  # Cache the result
            return result
        finally:
            cursor.close()
            conn.close()

    def get_algo_by_name(self, algo_name):
        """Fetch algorithm details by name"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM t1_supported_algorithm WHERE algorithm = %s"
            cursor.execute(query, (algo_name,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()