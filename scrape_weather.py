"""
This module provides the WeatherScraper class, designed to scrape and process weather data
from the Government of Canada Climate and Weather tracking website.

The WeatherScraper class includes methods to:
- Retrieve HTML content from a specified URL.
- Parse and format dates into a standardized format.
- Extract temperature data (maximum, minimum, and mean) from HTML rows.
- Scrape weather data for a given date range and store it in a dictionary indexed by date.
- Generate URLs dynamically for monthly weather data based on a specified date.
- Save the scraped weather data to a text file for further use or analysis.

This module uses the `requests` library for HTTP requests and
`BeautifulSoup` from `bs4` for parsing HTML.
It also utilizes Python's `datetime` and `timedelta` for date manipulations.
"""


from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

class WeatherScraper:
    """
    A class built to scrape weather from the Government of Canada
    Climate and Weather tracking website.
    """
    def __init__(self):
        """
        Initialize the WeatherScraper with an empty weather data dictionary.
        """
        self.weather_data = {}

    def _get_html(self, url, timeout=10):
        """
        Fetch HTML content from the provided URL.

        :param url: The URL to fetch the content from.
        :param timeout: The maximum time in seconds to wait for a response. Default is 10 seconds.
        :return: HTML content of the page as a string.
        :raises: Exception if the request fails or times out.
        """
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch page: {e}")


    def _parse_date(self, date_str):
        """
        Parse the date from the HTML table and convert it into YYYY-MM-DD format.

        :param date_str: Date in the format "Month Day, Year".
        :return: Date in YYYY-MM-DD format.
        """
        try:
            date = datetime.strptime(date_str, '%B %d, %Y')
            return date.strftime('%Y-%m-%d')
        except ValueError:
            return None

    def _parse_weather_data(self, row):
        """
        Extract temperature data (Max, Min, Mean) from an HTML row.

        :param row: The HTML row containing weather data.
        :return: A dictionary of temperature data (Max, Min, Mean), or None if data is invalid.
        """
        cells = row.find_all('td')
        if len(cells) < 4:  # Ensure enough cells exist
            return None

        try:
            max_temp = float(cells[0].text.strip()) if cells[0].text.strip() != "M" else None
            min_temp = float(cells[1].text.strip()) if cells[1].text.strip() != "M" else None
            mean_temp = float(cells[2].text.strip()) if cells[2].text.strip() != "M" else None

            if max_temp is None and min_temp is None and mean_temp is None:
                return None

            return {'Max': max_temp, 'Min': min_temp, 'Mean': mean_temp}
        except ValueError:
            return None

    def scrape(self, start_date, end_date):
        """
        Scrape weather data for the given date range.

        :param start_date: The start date as a datetime.date object.
        :param end_date: The end date as a datetime.date object.
        :return: A dictionary of weather data indexed by date.
        """
        current_date = end_date
        while current_date >= start_date:
            url = self._generate_url_for_month(current_date)
            print(f"Scraping: {url}")

            html = self._get_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            rows = soup.find_all('tr')

            if not rows:
                print("No more data found. Stopping scrape.")
                break

            for row in rows:
                date_link = row.find('abbr')
                if date_link:
                    date_str = date_link['title']
                    date = self._parse_date(date_str)

                    if date:
                        weather = self._parse_weather_data(row)
                        if weather:
                            self.weather_data[date] = weather

            current_date = (current_date.replace(day=1) - timedelta(days=1))

        return self.weather_data

    def _generate_url_for_month(self, date):
        """
        Generate the URL for the specified month and year.

        :param date: The date to base the URL on.
        :return: The URL for the month’s data.
        """
        year = date.year
        month = date.month
        url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={year}&Month={month}"
        return url

    def save_to_file(self, file_name="weather_data.txt"):
        """
        Save the scraped weather data to a text file.

        :param file_name: Name of the file to save the data.
        """
        with open(file_name, 'w') as f:
            for date, data in self.weather_data.items():
                f.write(f"{date}: {data}\n")
            print(f"Weather data saved to {file_name}")
