import pytest
import sys
from io import StringIO
from monthly_finance_app import MonthlyFinanceTracker

@pytest.fixture
def tracker():
    # Mocking the stdin input for 12 months
    input_data = "n\n" + "1000\n200\n50\n5000\n100\n" * 12
    sys.stdin = StringIO(input_data)
    tr = MonthlyFinanceTracker()
    tr.collect_monthly_data()
    return tr

def test_save_data(tracker):
    # This should test the method that saves data (if there's one)
    # Assuming there's a method called save_data() in the MonthlyFinanceTracker class
    tracker.save_data("test_save.csv")
    # Check if "test_save.csv" exists, and if its contents match what's expected

def test_manual_input():
    sys.stdin = StringIO("n\n" + "1000\n200\n50\n5000\n100\n" * 12)
    finance_data = MonthlyFinanceTracker()
    finance_data.collect_monthly_data()

    # Add asserts based on what you expect from the collected data
    # For example:
    assert finance_data.budgets_data[0] == 1000
    assert finance_data.expenses_data[0]["Extras"] == 200
    assert finance_data.expenses_data[0]["Utilities"] == 50
    assert finance_data.incomes_data[0]["Salary"] == 5000

def test_csv_input(tracker):
    # Creating a dummy csv file for testing
    with open("test_data.csv", "w") as f:
        f.write("Month,Budget,Extras,Utilities,Salary,Investments\n")
        f.write("1/2023,1000,200,50,5000,100\n")

    tracker.collect_monthly_data("test_data.csv")
    
    assert tracker.budgets_data[0] == 1000
    assert tracker.expenses_data[0]["Extras"] == 200
    assert tracker.expenses_data[0]["Utilities"] == 50
    assert tracker.incomes_data[0]["Salary"] == 5000

# Add more test functions as required
