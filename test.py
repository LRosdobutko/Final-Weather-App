from scrape_weather import WeatherScraper  # Import the WeatherScraper class

from datetime import datetime, timedelta

# Example usage:
current_date = datetime.now()

if __name__ == "__main__":
     start_year = current_date.year
     start_month = current_date.month
     scraper = WeatherScraper(start_year, start_month, months_to_scrape=2)
     scraper.scrape()
     scraper.save_to_file("weather_data.txt")