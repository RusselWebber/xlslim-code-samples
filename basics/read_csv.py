# Load a csv file for use in Excel
import os
import csv


def read_csv(filepath, dialect="excel"):
    """Reads the csv file at filepath.
    
    Uses the Python csv module as described at https://docs.python.org/3/library/csv.html
    """
    rows = []
    if not os.path.exists(filepath):
        raise ValueError(f"{filepath} does not exist.")
    with open(filepath) as csvfile:
        rows.extend(csv.reader(csvfile, dialect))
    return rows


if __name__ == "__main__":
    # Data from https://eforexcel.com/wp/downloads-18-sample-csv-files-data-sets-for-testing-sales/
    print(read_csv(r"D:\github\xlslim-code-samples\data\10000SalesRecords.csv"))
