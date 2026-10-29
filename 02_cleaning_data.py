# ==========================================================
# 02_cleaning_data.py
# Job of this file: load the 5 tables from MySQL and clean them
# Used later by: 03, 04, 05 analysis files and the dashboard
# ==========================================================

import os                                          # for working with folders
import importlib                                   # lets us import a file whose name starts with a number
import pandas as pd                                # pandas = our data tool

connect = importlib.import_module("01_connect_sql")  # loads our 01_connect_sql.py file

# Folder (next to this file) where we save a CSV copy of each table
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_FOLDER, "Data_SQL")


# ---------- Function 1: load the tables and save CSV copies ----------
def load_data():
    tables = connect.connect_tables()              # returns 5 DataFrames (or None if it failed)

    if tables is None:                             # connection or loading failed
        return None

    # Names in the SAME order that connect_tables() returns the tables
    tablenames = ["Customers", "Restaurants", "Menu_Items", "Orders", "Delivery"]

    os.makedirs(SAVE_FOLDER, exist_ok=True)        # create the folder if it does not exist

    data = {}                                      # a dictionary: table name -> DataFrame
    for i in range(len(tablenames)):               # i = 0, 1, 2, 3, 4
        name = tablenames[i]
        table = tables[i]
        table.to_csv(os.path.join(SAVE_FOLDER, f"{name}.csv"), index=False)  # save a copy
        data[name] = table                         # store it in the dictionary
    return data


# ---------- Function 2: clean ONE table ----------
def clean_data(df):
    df = df.copy()                                 # work on a copy, the original stays safe

    df = df.dropna()                               # remove rows that have empty (missing) values
    df = df.drop_duplicates()                      # remove rows that are fully repeated

    # Remove extra spaces from every text column
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):  # is this a text column?
            df[col] = df[col].str.strip()

    # Make Gender spelling consistent: "male" / "MALE" -> "Male"
    if "C_Gender" in df.columns:
        df["C_Gender"] = df["C_Gender"].str.title()

    # Make Status spelling consistent: "in transit" -> "In Transit"
    if "Status" in df.columns:
        df["Status"] = df["Status"].str.title()

    # Make sure date columns are real dates (needed for trends and delivery time)
    for col in ["C_Sign_Up_Date", "Order_DateTime", "Del_Time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Food_Availability is stored as 0/1 in MySQL, make it True/False
    if "Food_Availability" in df.columns:
        df["Food_Availability"] = df["Food_Availability"].astype(bool)

    return df


# ---------- Function 3: load + clean all tables ----------
def load_clean_data():
    data = load_data()                             # step 1: load

    if data is None:
        return None

    clean_df = {}                                  # will hold the cleaned tables
    for table_name, table_data in data.items():
        clean_df[table_name] = clean_data(table_data)  # step 2: clean each table
    return clean_df


# ---------- Runs only when you run this file directly ----------
if __name__ == "__main__":
    raw = load_data()

    if raw is not None:
        print("\nRows before and after cleaning:")
        for name, table in raw.items():
            cleaned = clean_data(table)
            print(f"{name:12} before: {len(table):3}   after: {len(cleaned):3}")

        clean = load_clean_data()                  # the full cleaned data (dictionary)
        print("\nDelivery Status counts:")
        print(clean["Delivery"]["Status"].value_counts())
        print("\nOrders data types:")
        print(clean["Orders"].dtypes)