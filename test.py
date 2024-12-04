from scrape_weather import WeatherScraper  # Import the WeatherScraper class
from db_operations import DBOperations  # Import the DBOperations class
from datetime import datetime, timedelta

# Example usage:
current_date = datetime.now()

if __name__ == "__main__":
    # Set the start year and month based on current date
    start_year = current_date.year
    start_month = current_date.month

    # Initialize the WeatherScraper
    scraper = WeatherScraper(start_year, start_month, months_to_scrape=2)

    # Scrape the weather data
    weather_data = scraper.scrape()

    # Initialize the database operations class
    db_operations = DBOperations()

    # Initialize the database (create table if it doesn't exist)
    db_operations.initialize_db()

    # Save the scraped weather data to the database
    db_operations.save_data(weather_data)

    # Optionally, fetch and print data from the database to verify it was saved correctly
    print("Data fetched from the database:")
    rows = db_operations.fetch_data("2024-01-01", "2024-01-31")  # Example date range
    for row in rows:
        print(row)

    # Save the weather data to a file as well (if desired)
    scraper.save_to_file("weather_data.txt")
