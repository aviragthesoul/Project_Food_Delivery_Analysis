# ==========================================================
# 03_customer_analysis.py
# Job of this file: analyse CUSTOMERS
# Input : cleaned Customers table + cleaned Orders table
# Output: a dictionary of results (the dashboard will use it later)
# ==========================================================

import importlib                                          # lets us import a file whose name starts with a number

cleaning = importlib.import_module("02_cleaning_data")    # loads our cleaning file (02)
load_clean_data = cleaning.load_clean_data                # we will use this function to get the cleaned data


def customer_analysis(customer_df, order_df):

    # ---------- 1. Total customers ----------
    # nunique() counts how many DIFFERENT customer IDs there are
    total_customer = customer_df['C_ID'].nunique()

    # ---------- 2. Gender count ----------
    # value_counts() counts how many times each value appears (Male / Female)
    gender_count = customer_df['C_Gender'].value_counts()

    # ---------- 3. City count ----------
    # Make a copy so we do not change the original table
    customer_df = customer_df.copy()

    # An address can look like "Sector 18, Noida", so we keep only the last part (the city).
    # If the address is just "Delhi", split(',') gives ["Delhi"] and [-1] still returns "Delhi".
    city = []                                             # empty list to store the cities
    for address in customer_df['C_Address']:              # go through every address one by one
        city.append(address.split(',')[-1].strip())       # split at comma, take last part, remove spaces

    customer_df['C_City'] = city                          # add the cities as a new column
    city_count = customer_df['C_City'].value_counts()     # count customers in each city

    # ---------- 4. Repeated, one-time and never-ordered customers ----------
    # Count how many orders each customer has placed
    orders_per_customer = order_df['C_ID'].value_counts()

    # Customers with MORE than 1 order = repeated customers
    total_repeated_customers = len(orders_per_customer[orders_per_customer > 1])

    # Customers with exactly 1 order = one-time customers
    one_time_customers = len(orders_per_customer[orders_per_customer == 1])

    # Customers who are in the Customers table but never placed an order
    never_ordered_customers = total_customer - len(orders_per_customer)

    # ---------- 5. Send all results back together ----------
    return {
        'Total_Customers': total_customer,
        'Gender_Count': gender_count,
        'City_Count': city_count,
        'Repeated_Customers': total_repeated_customers,
        'One_Time_Customers': one_time_customers,
        'Never_Ordered_Customers': never_ordered_customers
    }


# ---------- Runs only when you run this file directly ----------
# (When the dashboard imports this file later, this part is skipped)
if __name__ == "__main__":
    data = load_clean_data()                  # load and clean all tables ONCE

    if data is not None:
        customer_df = data['Customers']       # the cleaned Customers table
        order_df = data['Orders']             # the cleaned Orders table

        result = customer_analysis(customer_df, order_df)

        # Print each result on its own line so it is easy to read
        for name, value in result.items():
            print("\n" + name + ":")
            print(value)