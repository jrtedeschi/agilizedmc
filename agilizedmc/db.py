import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Tuple

class DB:
    def __init__(self, host: str, user: str, password: Optional[str], port: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self._connection = None

    @property
    def connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    database=self.database
                )
            except Error as e:
                raise Exception(f"Error connecting to MySQL: {e}")
        return self._connection

    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        """Execute a query without returning results"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        finally:
            cursor.close()

    def query(self, query: str, params: Optional[tuple] = None) -> List[Tuple]:
        """Execute a query and return results"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def close(self) -> None:
        """Close the database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
