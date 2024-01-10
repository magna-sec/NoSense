from .Menu import DatabaseInputMenu

from os import path
from sqlite3 import connect as dbconnect
from collections import namedtuple

class Database():
    def __init__(self) -> None:
        """Initialises the object.

        Args:
          None.
        """
        self.DATABASE = "settings.db"
        self.DEBUG = False


    def __init_DB(self) -> None:
        """Used to first create the database

        Args:
            self:
                Self object

        Returns:
            None

        """
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()

        # SQL statements to create four tables
        createAttacker = """
        CREATE TABLE attacker (
            id INTEGER PRIMARY KEY,
            ip TEXT NOT NULL,
            iplong TEXT,
            iphex TEXT
        );
        """

        createFirewalls = """
        CREATE TABLE firewalls (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ip TEXT,
            url TEXT,
            pfippath TEXT,
            username TEXT, 
            password TEXT
        );
        """

        createWebshells = """
        CREATE TABLE webshells (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            path TEXT NOT NULL,
            level TEXT NOT NULL,
            arguments TEXT
        );
        """

        createRevshells = """
        CREATE TABLE revshells (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            path TEXT NOT NULL,
            level TEXT NOT NULL,
            arguments TEXT
        );
        """

        createSshkeys = """
        CREATE TABLE sshkeys (
            id INTEGER PRIMARY KEY,
            ip TEXT NOT NULL,
            user TEXT NOT NULL,
            private_key TEXT NOT NULL
        );
        """

        # Execute the SQL statements to create tables
        cursor.execute(createAttacker)
        cursor.execute(createFirewalls)
        cursor.execute(createWebshells)
        cursor.execute(createRevshells)
        cursor.execute(createSshkeys)


        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def get_row(self, table:str, col:str, value:str) -> str:
        """
        """
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()

        # Execute the SELECT query to fetch all values from a particular column
        cursor.execute(f"SELECT * FROM {table} WHERE {col} = '{value}'")

        # Fetch all the results (values in the column)
        row = cursor.fetchone()
    
        # Commit the changes and close the connection
        conn.close()

        return row
    
    def get_sshkey(self, ip:str, user:str) -> str:
        """
        """
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()

        # Execute the SELECT query to fetch all values from a particular column
        cursor.execute(f"SELECT private_key FROM sshkeys WHERE ip = '{ip}' AND user = '{user}'")

        # Fetch all the results (values in the column)
        row = cursor.fetchone()
    
        # Commit the changes and close the connection
        conn.close()

        return row


    def get_all_rows_where(self, col:str, table:str, col_where:str, value:str) -> str:
        """
        """
        col_data = []

        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()

        # Execute the SELECT query to fetch all values from a particular column
        cursor.execute(f"SELECT {col} FROM {table} WHERE {col_where} = '{value}'")

        # Fetch all the results (values in the column)
        column_values = cursor.fetchall()

        # tuple -> array
        for value in column_values:
            col_data.append(value[0])

        # Commit the changes and close the connection
        conn.close()

        return col_data
    
    def get_all_rows(self, col:str, table:str) -> str:
        """
        """
        col_data = []

        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()

        # Execute the SELECT query to fetch all values from a particular column
        cursor.execute(f"SELECT {col} FROM {table}")

        # Fetch all the results (values in the column)
        column_values = cursor.fetchall()

        # tuple -> array
        for value in column_values:
            col_data.append(value[0])

        # Commit the changes and close the connection
        conn.close()

        return col_data


    def get_attacker(self) -> tuple:
        atkTup = namedtuple("attacker", ['ip', 'iplong', 'iphex'])

        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()
        
        # Remove exisiting attacker
        select_query = "SELECT * FROM attacker;"
        cursor.execute(select_query)

        result = cursor.fetchone()
        attacker = atkTup(ip=result[1], iplong=result[2], iphex=result[3])

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return attacker


    def set_attacker(self, data: list) -> None:
        """Remove attacker entry then add a new one

        Args:
            self:
                Self object
            data:
                Attacker information in a list

        Returns:
            None

        """
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()
        
        # Remove exisiting attacker
        del_query = "DELETE FROM attacker;"
        cursor.execute(del_query)


        insert_query = "INSERT INTO attacker (ip, iplong, iphex) VALUES (?, ?, ?);"

        # Execute the SQL statement to insert data
        cursor.execute(insert_query, data)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def set_shell(self, data:list, shellType:str):
        conn = dbconnect("settings.db")
        cursor = conn.cursor()
        
        insert_query = f"INSERT INTO {shellType} (name, url, path, level, arguments) VALUES (?, ?, ?, ?, ?);"
        # Execute the SQL statement to insert data
        cursor.execute(insert_query, data)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def get_firewall(self, id:str) -> tuple:
        firewallTup = namedtuple("firewall", ["id", "name", "ip", "url", "pfippath", "username", "password"])
        
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()
        
        # Remove exisiting attacker
        select_query = f"SELECT * FROM firewalls WHERE id = {id};"
        cursor.execute(select_query)

        result = cursor.fetchone()
        firewall = firewallTup(id=result[0], name=result[1], ip=result[2], url=result[3], pfippath=result[4], username=result[5], password=result[6])
        if(self.DEBUG): print(f"[+] Database->Firewall: {firewall}")
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return firewall
    
    def del_firewall(self, id:str) -> tuple:
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()
        
        # Remove exisiting attacker
        select_query = f"DELETE FROM firewalls WHERE id={id};"
        cursor.execute(select_query)

        result = cursor.fetchone()

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def set_firewall(self, data: list) -> None:
        """Add one firewall entry to the database

        Args:
            self:
                Self object
            data:
                Firewall information in a list

        Returns:
            None

        """
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()
        insert_query = "INSERT INTO firewalls (name, ip, url, pfippath, username, password) VALUES (?, ?, ?, ?, ?, ?);"

        # Execute the SQL statement to insert data
        cursor.execute(insert_query, data)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def change_row(self, table, entry, entryValue, conditionEntry, conditionEntryValue):
        conn = dbconnect(self.DATABASE)
        cursor = conn.cursor()

        # Construct and print the SQL query (for debugging)
        sqlQuery = f'UPDATE {table} SET "{entry}" = ? WHERE {conditionEntry} = ?'
        if(self.DEBUG): print(f"SqlQuery: {sqlQuery}")

        try:
            # Execute the UPDATE query
            cursor.execute(sqlQuery, (entryValue, conditionEntryValue))

            # Commit the changes
            conn.commit()
        except Exception as e:
            if(self.DEBUG): print(f"Error executing query: {e}")

        # Close the connection
        conn.close()

    def set_key(self, data:list):
        conn = dbconnect("settings.db")
        cursor = conn.cursor()
        
        insert_query = f"INSERT INTO sshkeys (ip, user, private_key) VALUES (?, ?, ?);"
        # Execute the SQL statement to insert data
        cursor.execute(insert_query, data)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def fill_db(self, amtFws:int) -> None:
        """Fills database with initial firewalls.

        Args:
            self: Self object
            amtFws (int): Amount of firewalls we need to request

        Returns:
            None
        """    
        # Attacker information
        new_input = DatabaseInputMenu()
        self.__init_DB()
        data = new_input.get_attacker()

        self.set_attacker(data)

        # Firewall information
        for firewall in range(amtFws):
            data = new_input.get_firewall()
            self.set_firewall(data)


    def check_db(self) -> bool:
        """Check that database exists

        Args:
            self: Self object

        Returns:
            bool: Will return true if file found was requested.

        """
        # Create database file if it doesn't exist
        if not path.exists(self.DATABASE):
            return False
        else:
            return True

