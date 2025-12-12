import mysql.connector
from mysql.connector import pooling

class AIQMysqlDBPool:
    __pool = None  # Static variable to hold the pool

    @staticmethod
    def initialize_pool(host, user, password, database, pool_name="AIQPool", pool_size=5, port=None):
        """
        Initialize the MySQL connection pool (only once).
        """
        if AIQMysqlDBPool.__pool is None:
            AIQMysqlDBPool.__pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            print(f"Connection pool '{pool_name}' initialized with size {pool_size}")
        else:
            print("Connection pool already initialized.")

    @staticmethod
    def get_connection():
        """
        Get a connection from the pool.
        """
        if AIQMysqlDBPool.__pool is None:
            raise Exception("Connection pool is not initialized. Call initialize_pool() first.")
        con = AIQMysqlDBPool.__pool.get_connection()
        con.autocommit = False
        return con