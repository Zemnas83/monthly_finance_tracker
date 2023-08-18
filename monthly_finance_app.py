import argparse
import csv
import matplotlib.pyplot as plt
import pandas as pd


class FinanceData:
    """
    A base class for handling financial data collection and storage.

    Attributes:
    - months: List of months for which data is collected.
    - budgets_data: List of monthly budget amounts.
    - expenses_data: List of dictionaries, each representing expense categories and their values for a given month.
    - incomes_data: List of dictionaries, each representing income sources and their values for a given month.
    """
    
    def __init__(self):
        self.months = []
        self.budgets_data = []
        self.expenses_data = []
        self.incomes_data = []

    def collect_monthly_data(self, input_csv=None):
        """
        A method to collect user's monthly financial data.
        Allows for manual input of data or reading from a provided CSV file. 
        If manually entering, prompts user for budgets, incomes, and expenses for each month.
        """
        if input_csv:
            try:
                with open(input_csv, mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        self.months.append(row['Month'])
                        self.budgets_data.append(float(row['Budget']))
                        
                        expenses = {category: float(row[category]) for category in row.keys() if category != 'Month' and category != 'Budget'}
                        incomes = {source: float(row[source]) for source in row.keys() if 'Income' in source}
                        
                        self.expenses_data.append(expenses)
                        self.incomes_data.append(incomes)
            except FileNotFoundError:
                print(f"Error: File {input_csv} not found.")
            except csv.Error:
                print("Error reading CSV. Please check the file format.")
        else:
            for month in range(1, 13):
                self.months.append(f"{month}/2023")
                
                budget = self._get_input(f"Enter budget for month {month}: ")
                self.budgets_data.append(budget)
                
                expenses = {
                    "Extras": self._get_input(f"Enter expenses for extras in month {month}: "),
                    "Utilities": self._get_input(f"Enter expenses for Utilities in month {month}: ")
                }
                incomes = {
                    "Salary": self._get_input(f"Enter income from Salary in month {month}: "),
                    "Investments": self._get_input(f"Enter income from Investments in month {month}: ")
                }

                self.expenses_data.append(expenses)
                self.incomes_data.append(incomes)

    def _get_input(self, prompt):
        """
        Helper method to validate manual input.
        """
        while True:
            try:
                value = float(input(prompt))
                if value >= 0:
                    return value
                else:
                    print("Please enter a non-negative value.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class MonthlyFinanceTracker(FinanceData):
    """
    A class for tracking monthly personal finances, including budgets, expenses, and incomes.
    """
    def display_monthly_summaries(self):
        """Display monthly summaries including expenses, budgets, and budget progress.""" 
        for month in range(len(self.months)):
            print(f"Month: {self.months[month]}")
            print("Expenses:")
            total_expenses = sum(self.expenses_data[month].values())
            for category, amount in self.expenses_data[month].items():
                print(f"{category}: ${amount:.2f}")
            print(f"Total Expenses: ${total_expenses:.2f}")
            print(f"Budget: ${self.budgets_data[month]:.2f}")
            budget_remaining = self.budgets_data[month] - total_expenses
            print(f"Budget Remaining: ${budget_remaining:.2f}")
            print()

    def visualize_finances(self):
        """
        Creates a line graph to visualize monthly budgets, expenses, and incomes over the course of a year.

        This method uses matplotlib to produce a graph showing trends in budgets, total expenses, and total incomes.
        Each data type is represented as a separate line in the graph.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.months, self.budgets_data, marker='o', label='Budgets')
        plt.plot(self.months, [sum(expenses.values()) for expenses in self.expenses_data], marker='o', label='Expenses')
        if self.incomes_data:
            plt.plot(self.months, [sum(incomes.values()) for incomes in self.incomes_data], marker='o', label='Incomes')
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.title('Personal Finances Over a Year')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid()
        plt.show()

    def save_data(self, filename):
        """
        Save user inputted financial data into a CSV file.

        Writes the monthly data for budgets, expenses by category, and incomes by source to the specified CSV file.
        
        Args:
        - filename (str): Name of the CSV file to save data to.
        """
        data = {
            "Month": self.months,
            "Budget": self.budgets_data
        }

        for category in self.expenses_data[0].keys():
            data[category] = [expenses[category] for expenses in self.expenses_data]

        for source in self.incomes_data[0].keys():
            data[source] = [incomes[source] for incomes in self.incomes_data]

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            writer.writerows(zip(*data.values()))

        print(f"Data saved to {filename}")
        
    def to_dataframe(self):
        """
        Convert the stored data into a Pandas DataFrame for easier analysis.

        Returns:
        DataFrame: A Pandas DataFrame containing the monthly budgets, incomes, and expenses data.
        """
        data = {
            "Month": self.months,
            "Budget": self.budgets_data
        }

        for category in self.expenses_data[0].keys():
            data[category] = [expenses[category] for expenses in self.expenses_data]

        for source in self.incomes_data[0].keys():
            data[source] = [incomes[source] for incomes in self.incomes_data]

        return pd.DataFrame(data)

    def analysis(self):
        """Perform statistical analysis on the data and display the results."""
        df = self.to_dataframe()

        # Calculating and displaying mean, median, and mode for Budgets, Incomes, and Expenses
        for column in df.columns:
            if column != 'Month':  # Exclude 'Month' from analysis
                print(f"Analysis for {column}:\n")
                print(f"Mean: {df[column].mean()}")
                print(f"Median: {df[column].median()}")
                mode = df[column].mode()
                print(f"Mode: {mode[0] if not mode.empty else 'No mode'}\n")
                
        
def parse_args():
    """
    Parses command line arguments for the script.
    
    Args:
    - -m or --manual: Flag to indicate manual data entry. If set, the user will be prompted to enter data manually.
    - -i or --input: The input CSV filename, if data is to be read from a CSV file.
    - -o or --output: The output CSV filename to save data to. Defaults to 'finance_data.csv'.

    Returns:
    argparse.Namespace: Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(description="Track and visualize monthly personal finances.")
    parser.add_argument("-m", "--manual", action="store_true", help="Enter data manually")
    parser.add_argument("-i", "--input", help="Input CSV filename")
    parser.add_argument("-o", "--output", default="finance_data.csv", help="Output CSV filename")
    return parser.parse_args()


def main():
    """
    Main execution function for the script.

    Initializes the MonthlyFinanceTracker class, collects data (either manually or from CSV), 
    displays monthly summaries, visualizes the data with a graph, and saves the data to a CSV file.
    """
    args = parse_args()
    tracker = MonthlyFinanceTracker()

    if args.manual:
        tracker.collect_monthly_data()
    else:
        tracker.collect_monthly_data(args.input)

    tracker.display_monthly_summaries()
    tracker.analysis()
    tracker.visualize_finances()
    tracker.save_data(args.output)


if __name__ == "__main__":
    main()
