import sqlite3
from datetime import datetime, timedelta
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations


class WeatherProcessor:
    def __init__(self, db_name="weather_data.db"):
        """
        Initialize the WeatherProcessor with the database name.
        :param db_name: The SQLite database file name.
        """
        self.db_name = db_name
        self.weather_scraper = WeatherScraper()
        self.plotter = PlotOperations(db_name)

    def _get_latest_date_in_db(self):
        """
        Fetch the latest date of weather data available in the database.
        :return: Latest date as a string in the format 'YYYY-MM-DD', or None if no data exists.
        """
        query = "SELECT MAX(sample_date) FROM weather;"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            latest_date = cursor.fetchone()[0]
        return latest_date

    def _save_weather_data_to_db(self, weather_data):
        """
        Save the scraped weather data into the database.
        :param weather_data: Dictionary of weather data to save.
        """
        if not weather_data:
            print("No weather data to save.")
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            for date, data in weather_data.items():
                query = """
                    INSERT OR REPLACE INTO weather (sample_date, max_temp, min_temp, avg_temp)
                    VALUES (?, ?, ?, ?);
                """
                cursor.execute(query, (date, data.get("Max"), data.get("Min"), data.get("Mean")))
            conn.commit()
            print(f"Saved {len(weather_data)} records to the database.")

    def _update_weather_data(self):
        """
        Update the weather database by fetching missing data.
        """
        latest_date = self._get_latest_date_in_db()
        today = datetime.today().date()

        if latest_date:
            latest_date = datetime.strptime(latest_date, "%Y-%m-%d").date()
            if latest_date >= today:
                print("Weather data is already up-to-date.")
                return
            start_date = latest_date + timedelta(days=1)
        else:
            print("No data found in the database. Downloading full dataset.")
            start_date = datetime(2000, 1, 1).date()  # Assuming data starts from 2000

        print(f"Updating weather data from {start_date} to {today}.")
        weather_data = self.weather_scraper.scrape(start_date, today)
        self._save_weather_data_to_db(weather_data)
        print("Weather data update complete.")

    def _download_full_weather_data(self):
        """
        Download a full set of weather data into the database.
        """
        start_date = datetime(2000, 1, 1).date()  # Assuming data starts from 2000
        today = datetime.today().date()
        print(f"Downloading weather data from {start_date} to {today}.")
        weather_data = self.weather_scraper.scrape(start_date, today)
        self._save_weather_data_to_db(weather_data)
        print("Full weather data download complete.")

    def _generate_box_plot(self):
        """
        Prompt the user to enter a year range and generate a box plot.
        """
        try:
            start_year = int(input("Enter the start year (e.g., 2020): "))
            end_year = int(input("Enter the end year (e.g., 2023): "))
            self.plotter.plot_boxplot(start_year, end_year)
        except ValueError:
            print("Invalid input. Please enter valid years.")

    def _generate_line_plot(self):
        """
        Prompt the user to enter a year and month and generate a line plot.
        """
        try:
            year = int(input("Enter the year (e.g., 2023): "))
            month = int(input("Enter the month (1-12): "))
            if 1 <= month <= 12:
                self.plotter.plot_lineplot(year, month)
            else:
                print("Invalid month. Please enter a value between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid year and month.")

    def main_menu(self):
        """
        Present the user with a menu of options and handle user interactions.
        """
        while True:
            print("\nWeather Data Processor Menu")
            print("1. Download full set of weather data")
            print("2. Update weather data")
            print("3. Generate box plot (year range)")
            print("4. Generate line plot (specific year and month)")
            print("5. Exit")
            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == "1":
                self._download_full_weather_data()
            elif choice == "2":
                self._update_weather_data()
            elif choice == "3":
                self._generate_box_plot()
            elif choice == "4":
                self._generate_line_plot()
            elif choice == "5":
                print("Exiting Weather Data Processor. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
