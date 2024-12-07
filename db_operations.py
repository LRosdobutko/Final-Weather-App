"""
This module provides database operations for managing weather data in an SQLite database.

The `DBOperations` class offers methods to:
- Initialize the database schema.
- Insert weather data into the database while avoiding duplicates.
- Fetch weather data for a specified date range.
- Purge all data from the database while retaining its structure.

It is designed to work with an SQLite database and employs
a context manager for database connections.
"""

from dbcm import DBCM

class DBOperations:
    """
    A class to manage database operations for weather data in an SQLite database.

    The `DBOperations` class provides functionality to:
    - Set up the database schema for weather data storage.
    - Insert and save weather data into the database with duplicate-checking mechanisms.
    - Retrieve weather data records for a specified date range.
    - Clear all data from the database while preserving the schema.

    Attributes:
        db_name (str): The name of the SQLite database file.

    Methods:
        initialize_db():
            Initializes the database schema by creating the required table
              if it doesn't already exist.

        save_data(weather_data):
            Saves weather data to the database, ensuring no duplicate entries.

        fetch_data(start_date, end_date):
            Retrieves weather data from the database within a specified date range.

        purge_data():
            Deletes all records from the database while keeping the schema intact.
    """
    def __init__(self, db_name="weather_data.db"):
        """
        Initialize the DBOperations with the database name.
        :param db_name: The name of the SQLite database file.
        """
        self.db_name = db_name

    def initialize_db(self):
        """
        Initialize the database with the necessary table if it doesn't already exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_date TEXT UNIQUE,
            min_temp REAL,
            max_temp REAL,
            avg_temp REAL
        );
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute(create_table_sql)

    def save_data(self, weather_data):
        """
        Save weather data to the database, ensuring no duplicates.
        :param weather_data: A dictionary containing date and weather data.
        """
        insert_sql = """
        INSERT OR IGNORE INTO weather (sample_date, min_temp, max_temp, avg_temp)
        VALUES (?, ?, ?, ?);
        """
        with DBCM(self.db_name) as cursor:
            for date, data in weather_data.items():
                min_temp = data.get('Min')
                max_temp = data.get('Max')
                avg_temp = data.get('Mean')
                cursor.execute(insert_sql, (date, min_temp, max_temp, avg_temp))

    def fetch_data(self, start_date, end_date):
        """
        Fetch data from the database within the specified date range.
        :param start_date: The start date in YYYY-MM-DD format.
        :param end_date: The end date in YYYY-MM-DD format.
        :return: A tuple of rows containing the fetched records.
        """
        select_sql = """
        SELECT sample_date, min_temp, max_temp, avg_temp FROM weather
        WHERE sample_date BETWEEN ? AND ?;
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute(select_sql, (start_date, end_date))
            rows = cursor.fetchall()
        return rows

    def purge_data(self):
        """
        Purge all data from the database but keep the schema intact.
        """
        delete_sql = "DELETE FROM weather;"
        with DBCM(self.db_name) as cursor:
            cursor.execute(delete_sql)
