import duckdb

class DB:
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.connection = duckdb.connect(database=':memory:', read_only=False)

        #check if mysql is installed
        # if not, install mysql

        self.connection.execute('INSTALL mysql; LOAD mysql;')

        if password is None:
            self.connection.execute(f'ATTACH \'host={self.host} user={self.user} port={self.port} database={self.database}\' AS mysqldb (TYPE mysql) ; USE mysqldb;')
        else:
            self.connection.execute(f'ATTACH \'host={self.host} user={self.user} password={self.password} port={self.port} database={self.database}\' AS mysqldb (TYPE mysql) ; USE mysqldb;')

    def get_tables(self):
        tables = self.connection.execute('SHOW TABLES').fetchall()
        return tables

    def get_table_schema(self, table_name):
        schema = self.connection.execute(f'DESCRIBE {table_name}').fetchall()
        return schema


    def get_table_schemas(self):
        tables = self.get_tables()
        schemas = {}
        for table in tables:
            table_name = table[0]
            table_schema = self.get_table_schema(table_name)
            table_schema = [{'column_name': x[0], 'data_type': x[1], 'null' : x[2], 'key' : x[3], 'default_varchar' : x[4],'extra_varchar' : x[5] } for x in table_schema]
            schemas[table_name] = table_schema
        return schemas
    



if __name__ == "__main__":
    db = DB('localhost', 'root', None, '3306', 'osticketdb')
    print(db.get_tables())



