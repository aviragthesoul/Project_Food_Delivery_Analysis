# ==========================================================
# 01_connect_sql.py
# Job of this file: connect Python to MySQL and load the tables
# ==========================================================

import pandas as pd                        # pandas stores table data in DataFrames
from sqlalchemy import create_engine, URL  # tools to build the connection to MySQL


# ---------- Function 1: connect to the database ----------
def connect_database():
    try:
        # Build the connection address (URL) step by step
        url = URL.create(
            drivername="mysql+mysqlconnector",  # the MySQL driver we installed
            username="root",                    # your MySQL username
            password="MyNewPassword123",        # your MySQL password
            host="localhost",                   # MySQL runs on your own computer
            port=3306,                          # default MySQL port
            database="Food_Delivery"            # the database we created in MySQL
        )

        engine = create_engine(url)             # the engine is the "bridge" to MySQL

        # Open a connection just to test that it really works
        with engine.connect() as connection:
            print("Database Connected Successfully!")

        return engine                           # give the engine to whoever called this function

    except Exception as e:                      # if anything goes wrong, we land here
        print("Connection Failed:", e)          # show the reason
        return None                             # None means "connection failed"


# ---------- Function 2: load all 5 tables into DataFrames ----------
def connect_tables():
    engine = connect_database()                 # first, connect using Function 1

    if engine is None:                          # if the connection failed
        return None                             # stop here

    try:
        with engine.connect() as connection:
            # Each line runs a SQL query and stores the result in a DataFrame
            Customers = pd.read_sql_query("SELECT * FROM Customer;", connection)
            Restaurants = pd.read_sql_query("SELECT * FROM Restaurent;", connection)
            Menu_Items = pd.read_sql_query("SELECT * FROM Menu_Items;", connection)
            Orders = pd.read_sql_query("SELECT * FROM ORDERS;", connection)
            Delivery = pd.read_sql_query("SELECT * FROM DELIVERY;", connection)

        # Send all 5 DataFrames back together
        return Customers, Restaurants, Menu_Items, Orders, Delivery

    except Exception as e:                      # if any table fails to load
        print("Table could not be connected:", e)
        return None


# ---------- This part runs ONLY when you run this file directly ----------
# When another file (like 02_cleaning_data.py) imports this file,
# this part is skipped, so nothing gets printed twice.
if __name__ == "__main__":
    tables = connect_tables()                   # load the tables

    if tables is not None:                      # continue only if loading worked
        Customers, Restaurants, Menu_Items, Orders, Delivery = tables

        print("All tables loaded successfully!")

        # shape = (number of rows, number of columns)
        print("Customers  :", Customers.shape)
        print("Restaurants:", Restaurants.shape)
        print("Menu_Items :", Menu_Items.shape)
        print("Orders     :", Orders.shape)
        print("Delivery   :", Delivery.shape)

        # Remove the # in front of a line to see the first 5 rows of that table
        # print(Customers.head())
        # print(Restaurants.head())
        # print(Menu_Items.head())
        # print(Orders.head())
        # print(Delivery.head())