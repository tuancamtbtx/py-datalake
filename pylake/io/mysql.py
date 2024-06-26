
import mysql.connector.pooling

class MysqlIO():
    def __init__(self):
        self.pool = None

    def connect(self, host, user, password, database):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host=host,
            user=user,
            password=password,
            database=database
        )

    def execute_query(self, query):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result