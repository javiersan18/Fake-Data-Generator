from faker import Faker


class SQLConn():

    def __init__(self, host, database, username, password, driver="mysql", port=None, jdbc_url=None):
        self.jdbc_url = jdbc_url
        self.driver = driver
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.conn = self.create_connection()

    def create_connection(self):
        config = {
            'user': self.username,
            'password': self.password,
            'host': self.host,
            'database': self.database
        }
        if self.driver == "mysql":
            config['port'] = self.port if self.port is not None else '3306'
            return MySQLConnector.create_connection(config)
        elif self.driver == "postgres":
            config['port'] = self.port if self.port is not None else '5432'
            return PostgreSQLConnector.create_connection(config)
        else:
            print("Error: Driver not supported yet.")

    def query_exec(self, query):
        pass
