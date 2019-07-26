import mysql.connector
from mysql.connector import errorcode


class MySQLConnector:

    def __init__(self, config):
        try:
            print('Connecting to the PostgreSQL database...')
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def exec_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def insert_query(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()