import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


class PlotOperations:
    def __init__(self, db_name="weather_data.db"):
        """
        Initialize the PlotOperations with the database name.
        :param db_name: The name of the SQLite database file.
        """
        self.db_name = db_name

    def _fetch_data(self, query, params=None):
        """
        Fetch data from the database based on a query and parameters.
        :param query: SQL query to execute.
        :param params: Parameters for the SQL query.
        :return: Fetched data as a list of tuples.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def plot_boxplot(self, start_year, end_year):
        """
        Generate a boxplot for mean temperatures for each month between the specified years.
        :param start_year: The start year for the data.
        :param end_year: The end year for the data.
        """
        query = """
        SELECT sample_date, avg_temp FROM weather
        WHERE sample_date BETWEEN ? AND ?;
        """
        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        data = self._fetch_data(query, (start_date, end_date))

        # Organize data by month
        monthly_data = {month: [] for month in range(1, 13)}
        for sample_date, avg_temp in data:
            date = datetime.strptime(sample_date, "%Y-%m-%d")
            monthly_data[date.month].append(avg_temp)

        # Create the boxplot
        plt.figure(figsize=(10, 6))
        plt.boxplot([monthly_data[month] for month in range(1, 13)], labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        plt.title("Monthly Mean Temperature Distribution")
        plt.xlabel("Month")
        plt.ylabel("Mean Temperature (\u00b0C)")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.show()

    def plot_lineplot(self, year, month):
        """
        Generate a line plot for daily mean temperatures for a specific month and year.
        :param year: The year for the data.
        :param month: The month for the data (1-12).
        """
        query = """
        SELECT sample_date, avg_temp FROM weather
        WHERE sample_date LIKE ?;
        """
        date_pattern = f"{year}-{month:02d}-%"
        data = self._fetch_data(query, (date_pattern,))

        # Extract days and temperatures
        days = [datetime.strptime(sample_date, "%Y-%m-%d").day for sample_date, _ in data]
        temperatures = [avg_temp for _, avg_temp in data]

        # Create the line plot
        plt.figure(figsize=(10, 6))
        plt.plot(days, temperatures, marker="o", linestyle="-", color="b")
        plt.title(f"Daily Mean Temperatures - {datetime(year, month, 1).strftime('%B %Y')}")
        plt.xlabel("Day of Month")
        plt.ylabel("Mean Temperature (\u00b0C)")
        plt.xticks(range(1, max(days) + 1))
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.show()
