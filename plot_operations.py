import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dbcm import DBCM
from datetime import datetime

class PlotOperations:
    def __init__(self, db_name="weather_data.db"):
        """
        Initialize the PlotOperations class with the database name.

        :param db_name: Name of the SQLite database file.
        """
        self.db_name = db_name

    def _fetch_monthly_data(self, start_year, end_year):
        """
        Fetch mean temperature data grouped by month and year for box plotting.

        :param start_year: Starting year for data.
        :param end_year: Ending year for data.
        :return: A dictionary with months as keys and lists of mean temperatures as values.
        """
        monthly_data = {month: [] for month in range(1, 13)}
        query = """
        SELECT strftime('%m', sample_date) as month, avg_temp
        FROM weather
        WHERE strftime('%Y', sample_date) BETWEEN ? AND ?
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute(query, (str(start_year), str(end_year)))
            for row in cursor.fetchall():
                month = int(row[0])  # Convert month to integer
                if row[1] is not None:
                    monthly_data[month].append(row[1])
        return monthly_data

    def _fetch_daily_data(self, year, month):
        """
        Fetch daily mean temperatures for a specific month and year.

        :param year: Year for the data.
        :param month: Month for the data.
        :return: A tuple of days and mean temperatures.
        """
        days = []
        temperatures = []
        query = """
        SELECT sample_date, avg_temp
        FROM weather
        WHERE strftime('%Y', sample_date) = ? AND strftime('%m', sample_date) = ?
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute(query, (str(year), f"{int(month):02d}"))
            for row in cursor.fetchall():
                date = datetime.strptime(row[0], '%Y-%m-%d')
                days.append(date)
                temperatures.append(row[1])
        return days, temperatures

    def create_boxplot(self, start_year, end_year):
        """
        Create a boxplot of mean temperatures grouped by month.

        :param start_year: Starting year for the data range.
        :param end_year: Ending year for the data range.
        """
        monthly_data = self._fetch_monthly_data(start_year, end_year)

        # Prepare data for plotting
        data = [monthly_data[month] for month in range(1, 13)]
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Create the boxplot
        plt.figure(figsize=(10, 6))
        plt.boxplot(data, labels=labels)
        plt.title(f"Monthly Mean Temperatures ({start_year}-{end_year})")
        plt.ylabel("Temperature (°C)")
        plt.xlabel("Month")
        plt.grid(True)
        plt.show()

    def create_lineplot(self, year, month):
        """
        Create a line plot of daily mean temperatures for a specific month and year.

        :param year: Year for the data.
        :param month: Month for the data.
        """
        days, temperatures = self._fetch_daily_data(year, month)

        # Create the line plot
        plt.figure(figsize=(10, 6))
        plt.plot(days, temperatures, marker='o')
        plt.title(f"Daily Mean Temperatures ({datetime(year, month, 1).strftime('%B %Y')})")
        plt.ylabel("Temperature (°C)")
        plt.xlabel("Day")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.grid(True)
        plt.show()
