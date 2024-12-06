from plot_operations import PlotOperations

def main():
    """
    Main method to test the functionality of PlotOperations with user input.
    """
    print("Welcome to Weather Data Visualization!")
    plotter = PlotOperations()

    while True:
        print("\nSelect an option:")
        print("1. Generate a boxplot for a range of years")
        print("2. Generate a line plot for a specific year and month")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            try:
                start_year = int(input("Enter the start year (e.g., 2020): "))
                end_year = int(input("Enter the end year (e.g., 2023): "))
                plotter.plot_boxplot(start_year, end_year)
            except ValueError:
                print("Invalid input. Please enter valid years.")
        elif choice == "2":
            try:
                year = int(input("Enter the year (e.g., 2023): "))
                month = int(input("Enter the month (1-12): "))
                if 1 <= month <= 12:
                    plotter.plot_lineplot(year, month)
                else:
                    print("Invalid month. Please enter a value between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter a valid year and month.")
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
