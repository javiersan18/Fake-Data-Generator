class SQLConnector:

    def __init__(self, host, database, username, password, driver="mysql", port=None, jdbc_url=None):
        # self.jdbc_url = jdbc_url
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
            from .mysql_connector import MySQLConnector
            config['port'] = self.port if self.port is not None else '3306'
            return MySQLConnector(config)
        elif self.driver == "postgres":
            from .postgres_connector import PostgreSQLConnector
            config['port'] = self.port if self.port is not None else '5432'
            return PostgreSQLConnector(config)
        else:
            print("Error: Driver not supported yet.")

    def query_exec(self, query):
        self.conn.exec_query(query)

    def insert_exec(self, query, values):
        self.conn.insert_query(query, values)

    def create_table(self):
        with open('./sql/queries/create_table_' + self.driver + '.sql') as f:
            create_table_query = ""
            for line in f:
                create_table_query += line
            #print(create_table_query)
            self.query_exec(create_table_query)
