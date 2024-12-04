import sqlite3

class DBCM:
    def __init__(self, db_name):
        """
        Initialize the context manager with the database name.
        :param db_name: The name of the SQLite database.
        """
        self.db_name = db_name

    def __enter__(self):
        """
        Establish the database connection and return a cursor for querying.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Commit any changes and close the connection when the context ends.
        """
        if exc_type is None:
            self.connection.commit()  # Commit if no exceptions
        self.connection.close()

