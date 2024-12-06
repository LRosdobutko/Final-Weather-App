# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta

# class WeatherScraper:
#     def __init__(self):
#         """
#         Initialize the WeatherScraper with the start year and start month.

#         :param start_year: The year to start scraping from.
#         :param start_month: The month to start scraping from (1-12).
#         """
#         current_date = datetime.now()
#         self.start_year = current_date.year
#         self.start_month = current_date.month
#         self.weather_data = {}

#     def _get_html(self, url):
#         """
#         Fetch HTML content from the provided URL.

#         :param url: The URL to fetch the content from.
#         :return: HTML content of the page as a string.
#         """
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         else:
#             raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

#     def _parse_date(self, date_str):
#         """
#         Parse the date from the HTML table and convert it into YYYY-MM-DD format.

#         :param date_str: Date in the format "MM-DD-YYYY" or similar.
#         :return: Date in YYYY-MM-DD format.
#         """
#         try:
#             date = datetime.strptime(date_str, '%B %d, %Y')
#             return date.strftime('%Y-%m-%d')
#         except ValueError:
#             return None

#     def _parse_weather_data(self, row):
#       """
#       Extract temperature data (Max, Min, Mean) from an HTML row.

#       :param row: The HTML row containing weather data.
#       :return: A dictionary of temperature data (Max, Min, Mean), or None if data is invalid.
#       """
#       cells = row.find_all('td')
#       if len(cells) < 4:  # Ensure enough cells exist
#           return None

#       try:
#           # Correctly map the indices to the data
#           max_temp = float(cells[0].text.strip()) if cells[0].text.strip() != "M" else None
#           min_temp = float(cells[1].text.strip()) if cells[1].text.strip() != "M" else None
#           mean_temp = float(cells[2].text.strip()) if cells[2].text.strip() != "M" else None

#           # If all values are None, consider the data invalid
#           if max_temp is None and min_temp is None and mean_temp is None:
#               return None

#           return {'Max': max_temp, 'Min': min_temp, 'Mean': mean_temp}
#       except ValueError:
#           # Return None if conversion to float fails
#           return None


#     def scrape(self):
#         """
#         Scrape the weather data starting from the specified year and month, and continue scraping until no more data is found.
#         """
#         current_date = datetime(self.start_year, self.start_month, 1)
#         url = self._generate_url_for_month(current_date)

#         while True:
#             print(f"Scraping: {url}")

#             # Fetch the page HTML
#             html = self._get_html(url)

#             # Parse the HTML content
#             soup = BeautifulSoup(html, 'html.parser')
#             rows = soup.find_all('tr')

#             # If no weather data is found, stop scraping
#             if not rows:
#                 print("No more data found. Stopping scrape.")
#                 break

#             # Process each row for weather data
#             for row in rows:
#                 date_link = row.find('abbr')
#                 if date_link:
#                     date_str = date_link['title']
#                     date = self._parse_date(date_str)

#                     if date:
#                         weather = self._parse_weather_data(row)
#                         if weather:
#                             self.weather_data[date] = weather

#             # Update the URL to scrape the previous month
#             current_date -= timedelta(days=30)  # Go back one month
#             url = self._generate_url_for_month(current_date)

#         return self.weather_data

#     def _generate_url_for_month(self, date):
#         """
#         Generate the URL for the specified month and year.

#         :param date: The date to base the URL on.
#         :return: The URL for the month’s data.
#         """
#         year = date.year
#         month = date.month
#         day = 1
#         url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day={day}&Year={year}&Month={month}"
#         return url

#     def save_to_file(self, file_name="weather_data.txt"):
#         """
#         Save the scraped weather data to a text file.

#         :param file_name: Name of the file to save the data.
#         """
#         with open(file_name, 'w') as f:
#             for date, data in self.weather_data.items():
#                 f.write(f"{date}: {data}\n")
#             print(f"Weather data saved to {file_name}")


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class WeatherScraper:
    def __init__(self):
        """
        Initialize the WeatherScraper with an empty weather data dictionary.
        """
        self.weather_data = {}

    def _get_html(self, url):
        """
        Fetch HTML content from the provided URL.

        :param url: The URL to fetch the content from.
        :return: HTML content of the page as a string.
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

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
