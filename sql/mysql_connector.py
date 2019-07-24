import mysql.connector
from mysql.connector import errorcode


class MySQLConnector:

    @classmethod
    def create_connection(cls, config):
        try:
            cnx = mysql.connector.connect(**config)
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if cnx is not None:
                cnx.close()
                print('Database connection closed.')
