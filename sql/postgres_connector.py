#!/usr/bin/python
import psycopg2


class PostgreSQLConnector:

    def __init__(self, config):
        """ Connect to the PostgreSQL database server """
        try:
            print('Connecting to the MySQL database...')
            self.connection = psycopg2.connect(**config)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def exec_query(self, query):
        self.cursor.execute()
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()