import requests
from html.parser import HTMLParser

class ScrapeWeather(HTMLParser):
    def __init__(self, output_file):
        super().__init__()
        self.inside_table = False  # Track if inside a <table> tag
        self.inside_thead = False
        self.inside_th = False
        self.inside_tbody = False
        self.current_header = None  # Store the current header
        self.output_file = output_file  # File to write the output

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.inside_table = True  # Inside a <table>
        if tag == "thead":
            self.inside_thead = True
        if tag == "th":
            self.inside_th = True
        if tag == "tbody":
            self.inside_tbody = True

    def handle_endtag(self, tag):
        if tag == "table":
            self.inside_table = False  # Leaving a <table>
        if tag == "thead":
            self.inside_thead = False
        if tag == "th":
            self.inside_th = False
        if tag == "tbody":
            self.inside_tbody = True

    def handle_data(self, header):
        if self.inside_thead and self.inside_th and header.strip():  # Ensure data is inside <thead> and not empty
            header = header.strip()
            # Exclude unnecessary content like definitions
            if "Definition" not in header:
                if "Heat" not in header:
                  # Check if the header contains "day" or "temp" (case insensitive)
                  if "day" in header.lower() or "temp" in header.lower():
                      # If we already have a current header and the data is not a unit, print it
                      if self.current_header:
                          # If it's a unit, print it after the header
                          if header in ["°C", "mm", "cm", "km/h", "10's deg"]:
                              self.output_file.write(f"{self.current_header} {header}\n")
                              self.current_header = None  # Reset header after printing with unit
                          else:
                              # If it's another label, update the current header
                              self.output_file.write(f"{self.current_header}\n")
                              self.current_header = header
                      else:
                          # For the first header, set it
                          self.current_header = header

# Fetch HTML from a URL
url = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5#"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    response.encoding = 'utf-8'  # Explicitly set the encoding to UTF-8
    html_content = response.text

    # Open a text file to write the output
    with open("output99.txt", "w", encoding="utf-8") as output_file:
        # Parse the fetched HTML and write to the file
        scraper = ScrapeWeather(output_file)
        scraper.feed(html_content)

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the URL: {e}")
