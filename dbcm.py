"""
This module provides a context manager class for managing SQLite database connections.

The `DBCM` (Database Context Manager) class simplifies database operations by
automatically handling connection setup, cursor creation, and cleanup upon
completion of a database transaction or operation.
"""

import sqlite3

class DBCM:
    """
    A context manager class for managing SQLite database connections.

    The `DBCM` class automates the management of SQLite database connections,
    including opening a connection, creating a cursor for executing queries,
    committing changes, and closing the connection.

    Attributes:
        db_name (str): The name of the SQLite database file.

    Methods:
        __enter__():
            Establishes the database connection and returns a cursor for executing queries.

        __exit__(exc_type, exc_value, traceback):
            Commits any changes if no exceptions occurred and closes the database connection.
    """
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
