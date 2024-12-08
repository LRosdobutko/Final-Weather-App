import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations
from weather_processor import WeatherProcessor  # Import the WeatherProcessor class

class WeatherApp:
    """
    A user interface for interacting with the weather application.
    Allows users to scrape weather data, save it to a database,
    and visualize the data using plots.
    """

    def __init__(self, root):
        """
        Initialize the WeatherApp UI.

        :param root: The root window of the tkinter application.
        """
        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("600x400")
        self.root.minsize(600, 400)
        self.weather_scraper = WeatherScraper()
        self.db_operations = DBOperations()
        self.plot_operations = PlotOperations()
        self.weather_processor = WeatherProcessor()  # Create an instance of WeatherProcessor
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface.
        """
        # Frame for scraping data inputs
        scrape_frame = ttk.LabelFrame(self.root, text="Scrape Weather Data")
        scrape_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(scrape_frame, text="Action:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.action_choice = ttk.Combobox(scrape_frame, values=["New Weather Data", "Update Weather Data"], state='readonly')
        self.action_choice.grid(row=0, column=1, padx=5, pady=5)
        self.action_choice.set("New Weather Data")

        scrape_button = ttk.Button(scrape_frame, text="Generate", command=self.scrape_data_threaded)
        scrape_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Frame for graph and plotting inputs
        visualize_frame = ttk.LabelFrame(self.root, text="Visualize Data")
        visualize_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(visualize_frame, text="Select Plot:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.plot_type = ttk.Combobox(visualize_frame, values=["Box Plot", "Line Plot"], state='readonly')
        self.plot_type.grid(row=0, column=1, padx=5, pady=5)
        self.plot_type.set("Box Plot")

        ttk.Label(visualize_frame, text="Year: (YYYY or YYYY - YYYY)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.plot_year_entry = ttk.Entry(visualize_frame)
        self.plot_year_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(visualize_frame, text="Month (1-12):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.plot_month_entry = ttk.Entry(visualize_frame)
        self.plot_month_entry.grid(row=2, column=1, padx=5, pady=5)

        plot_button = ttk.Button(visualize_frame, text="Generate Plot", command=self.generate_plot)
        plot_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame for database management
        db_frame = ttk.LabelFrame(self.root, text="Database Management")
        db_frame.pack(fill="x", padx=10, pady=5)

        db_button = ttk.Button(db_frame, text="Purge Database", command=self.purge_database)
        db_button.pack(pady=10)

    def scrape_data_threaded(self):
        """
        Start the data scraping in a separate thread to keep the UI responsive.
        """
        thread = threading.Thread(target=self.scrape_data)
        thread.start()

    def scrape_data(self):
        """
        Scrape weather data based on user input and save it to the database.
        """
        action = self.action_choice.get()

        try:
            if action == "New Weather Data":
                # Use WeatherProcessor to download the full weather data
                self.weather_processor._download_full_weather_data()
                messagebox.showinfo("Success", "Full weather data downloaded successfully.")
            elif action == "Update Weather Data":
                # Use WeatherProcessor to update the weather data
                self.weather_processor._update_weather_data()
                messagebox.showinfo("Success", "Weather data updated successfully.")
            else:
                raise ValueError("Invalid action selected.")

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_plot(self):
        """
        Generate a plot based on user input.
        """
        plot_type = self.plot_type.get()
        year = self.plot_year_entry.get()
        month = self.plot_month_entry.get()

        try:
            if plot_type == "Box Plot":
                start_year = int(year.split("-")[0])
                end_year = int(year.split("-")[1])
                self.plot_operations.plot_boxplot(start_year, end_year)
            elif plot_type == "Line Plot":
                year = int(year)
                month = int(month)
                self.plot_operations.plot_lineplot(year, month)
            else:
                raise ValueError("Invalid plot type selected.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def purge_database(self):
        """
        Purge all data from the database.
        """
        try:
            self.db_operations.purge_data()
            messagebox.showinfo("Success", "Database purged successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
