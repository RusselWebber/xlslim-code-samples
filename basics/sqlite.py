# Read a csv file into SQLite and analyse
import os
import csv
import sqlite3


def calculate_revenue_by_region(filepath):
    """Calculates revenue by region.
    
    Loads the csv file into SQLite and groups by region.
    """
    if not os.path.exists(filepath):
        raise ValueError(f"{filepath} does not exist.")

    # Create an in-memory sqlite db
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    # Create the table
    cur.execute(
        'CREATE TABLE SaleSummary ("Region","Country","Item Type","Sales Channel","Order Priority","Order Date","Order ID","Ship Date","Units Sold","Unit Price","Unit Cost","Total Revenue","Total Cost","Total Profit");'
    )

    # Load the data from csv
    with open(filepath) as csvfile:
        dr = csv.DictReader(csvfile)
        to_db = [
            (
                i["Region"],
                i["Country"],
                i["Item Type"],
                i["Sales Channel"],
                i["Order Priority"],
                i["Order Date"],
                i["Order ID"],
                i["Ship Date"],
                i["Units Sold"],
                i["Unit Price"],
                i["Unit Cost"],
                i["Total Revenue"],
                i["Total Cost"],
                i["Total Profit"],
            )
            for i in dr
        ]

    cur.executemany(
        'INSERT INTO SaleSummary ("Region","Country","Item Type","Sales Channel","Order Priority","Order Date","Order ID","Ship Date","Units Sold","Unit Price","Unit Cost","Total Revenue","Total Cost","Total Profit") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
        to_db,
    )
    con.commit()

    # Select with a group by
    cur.execute('SELECT Region,SUM("Total Revenue") FROM SaleSummary GROUP BY Region;')
    rows = cur.fetchall()

    con.close()
    return rows


if __name__ == "__main__":
    print(
        calculate_revenue_by_region(
            r"D:\github\xlslim-code-samples\data\10000SalesRecords.csv"
        )
    )
