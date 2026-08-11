import mysql.connector
from mysql.connector import Error


class Database:

    def __init__(self):

        # Always create these first
        self.connection = None
        self.cursor = None

        try:

            # =====================================
            # Connect to MySQL Server
            # =====================================

            self.connection = mysql.connector.connect(

                host="localhost",

                user="root",

                password="Buddu@2112"

            )

            print("MySQL Server Connected Successfully")

            # =====================================
            # Create Database If It Does Not Exist
            # =====================================

            temp_cursor = self.connection.cursor()

            temp_cursor.execute(
                "CREATE DATABASE IF NOT EXISTS resource_management"
            )

            temp_cursor.close()

            self.connection.close()

            # =====================================
            # Connect To Resource Management Database
            # =====================================

            self.connection = mysql.connector.connect(

                host="localhost",

                user="root",

                password="Buddu@2112",

                database="resource_management"

            )

            if self.connection.is_connected():

                self.cursor = self.connection.cursor(
                    dictionary=True
                )

                print(
                    "Database Connected Successfully"
                )

        except Error as e:

            print(
                "Database Connection Error:",
                e
            )

            self.connection = None
            self.cursor = None

    # =====================================
    # CHECK CONNECTION
    # =====================================

    def is_connected(self):

        if self.connection is None:

            return False

        try:

            return self.connection.is_connected()

        except:

            return False

    # =====================================
    # FETCH MULTIPLE RECORDS
    # =====================================

    def fetch_all(self, query, params=None):

        if self.cursor is None:

            print(
                "Database is not connected."
            )

            return []

        try:

            self.cursor.execute(
                query,
                params
            )

            return self.cursor.fetchall()

        except Error as e:

            print(
                "Fetch Error:",
                e
            )

            return []

    # =====================================
    # FETCH SINGLE RECORD
    # =====================================

    def fetch_one(self, query, params=None):

        if self.cursor is None:

            print(
                "Database is not connected."
            )

            return None

        try:

            self.cursor.execute(
                query,
                params
            )

            return self.cursor.fetchone()

        except Error as e:

            print(
                "Fetch Error:",
                e
            )

            return None

    # =====================================
    # INSERT / UPDATE / DELETE
    # =====================================

    def execute(self, query, params=None):

        if self.cursor is None:

            print(
                "Database is not connected."
            )

            return False

        try:

            self.cursor.execute(
                query,
                params
            )

            self.connection.commit()

            return True

        except Error as e:

            print(
                "Execute Error:",
                e
            )

            try:

                self.connection.rollback()

            except:

                pass

            return False

    # =====================================
    # COUNT RECORDS
    # =====================================

    def count(self, table):

        if self.cursor is None:

            print(
                "Database is not connected."
            )

            return 0

        try:

            # Only use this method with your own
            # known table names.

            allowed_tables = [

                "users",
                "departments",
                "roles",
                "projects",
                "resources",
                "resource_types",
                "assignments",
                "leave_types",
                "leave_requests",
                "timesheets"

            ]

            if table not in allowed_tables:

                print(
                    "Invalid table name:",
                    table
                )

                return 0

            query = f"""
                SELECT COUNT(*) AS total
                FROM {table}
            """

            self.cursor.execute(query)

            result = self.cursor.fetchone()

            if result:

                return result["total"]

            return 0

        except Error as e:

            print(
                "Count Error:",
                e
            )

            return 0

    # =====================================
    # CLOSE DATABASE
    # =====================================

    def close(self):

        try:

            if self.cursor is not None:

                self.cursor.close()

            if self.connection is not None:

                if self.connection.is_connected():

                    self.connection.close()

                    print(
                        "Database Closed"
                    )

        except Error as e:

            print(
                "Database Close Error:",
                e
            )