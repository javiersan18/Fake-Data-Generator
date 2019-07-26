#!/usr/bin/python
import psycopg2


class PostgreSQLConnector:

    def __init__(self, config):
        """ Connect to the PostgreSQL database server """
        try:
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**config)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def exec_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def insert_query(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()