import psycopg2
from psycopg2.extensions import connection as pg_connection

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
    
class Database:
    def __init__(self, dbname="saverbot_db", user="saverbot_db_user", password="QgLON8WtRCH5WZIcrLgZkme0EFZCumtv", host="dpg-cpj7926ct0pc7384ua1g-a.oregon-postgres.render.com", port="5432"):
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    @property
    def connection(self) -> pg_connection:
        return psycopg2.connect(**self.connection_params)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        logger(cursor.mogrify(sql, parameters).decode('utf-8'))  # Log the exact SQL statement with parameters
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        cursor.close()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL UNIQUE,
            Name VARCHAR(255) NOT NULL,
            active INTEGER DEFAULT 1
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = %s" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def stat(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def add_user(self, user_id: int, name: str, active: int):
        sql = """
        INSERT INTO Users(user_id, Name, active) VALUES(%s, %s, %s)
        """
        self.execute(sql, parameters=(user_id, name, active), commit=True)

    def is_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_users(self):
        sql = """
        SELECT user_id, active FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def set_active(self, user_id, active):
        sql = "UPDATE Users SET active = %s WHERE user_id = %s"
        self.execute(sql, parameters=(active, user_id), commit=True)

    def update_user_email(self, email, id):
        sql = """
        UPDATE Users SET email=%s WHERE id=%s
        """
        self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def create_table_files(self):
        sql = """
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            type TEXT,
            file_id TEXT,
            caption TEXT,
            user_id INTEGER
        );
        """
        self.execute(sql, commit=True)

    def add_files(self, type: str=None, file_id: str=None, caption: str = None, user_id: str =None):
        sql = """
        INSERT INTO files(type, file_id, caption, user_id) VALUES(%s, %s, %s, %s)
        """
        self.execute(sql, parameters=(type, file_id, caption, user_id), commit=True)

    def select_files(self, **kwargs):
        sql = " SELECT * FROM files WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Admins (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE,
            full_name VARCHAR(255) NOT NULL
            );
        """
        self.execute(sql, commit=True)

    def add_admin(self, user_id: int, full_name: str):
        sql = """
        INSERT INTO Admins(user_id, full_name) VALUES(%s, %s)
        """
        self.execute(sql, parameters=(user_id, full_name), commit=True)

    def is_admin(self, **kwargs):
        sql = "SELECT * FROM Admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_admins(self):
        sql = """
        SELECT * FROM Admins
        """
        return self.execute(sql, fetchall=True)

    def stat_admins(self):
        return self.execute("SELECT COUNT(*) FROM Admins;", fetchone=True)

    def delete_admin(self, admin_id):
        self.execute("DELETE FROM Admins WHERE user_id=%s", (admin_id,), commit=True)

    def create_table_channel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels (
            id SERIAL PRIMARY KEY,
            channel TEXT
        );
        """
        self.execute(sql, commit=True)

    def add_channel(self, channel: str):
        sql = """
        INSERT INTO Channels(channel) VALUES(%s)
        """
        self.execute(sql, parameters=(channel,), commit=True)

    def check_channel(self, channel):
        return self.execute("SELECT channel FROM Channels WHERE channel=%s", (channel,), fetchone=True)

    def select_channels(self):
        return self.execute("SELECT * FROM Channels WHERE TRUE", fetchall=True)

    def delete_channel(self, channel):
        return self.execute("DELETE FROM Channels WHERE channel=%s", (channel,), commit=True)
        
    def delete_table(self, table_name=None):
        # Assuming 'db' is an instance of your database class
        self.execute(f"DROP TABLE IF EXISTS {table_name};", commit=True)

        
    def close(self):
        self.cur.close()
        self.conn.close()
    
