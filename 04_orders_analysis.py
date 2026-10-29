# ==========================================================
# 04_orders_analysis.py
# Job of this file: analyse ORDERS (revenue, restaurants, food, trends)
# Style: many small functions, each one answers ONE question
# ==========================================================

import importlib                                          # lets us import a file whose name starts with a number

cleaning = importlib.import_module("02_cleaning_data")    # loads our cleaning file (02)
load_clean_data = cleaning.load_clean_data                # we will use this function to get the cleaned data


# ---------- Function 1: key numbers (revenue, orders, average) ----------
def analyze_order(Orders):
    revenue = Orders['Total_Price'].sum()                 # add up all the order money
    total_orders = Orders['Order_ID'].nunique()           # count the different orders
    average_order_value = Orders['Total_Price'].mean()    # average money per order
    average_discount = Orders['Discount'].mean() * 100    # average discount in percent (0.10 -> 10%)

    return {
        'Total_Revenue': float(revenue),
        'Total_Orders': int(total_orders),
        'Average_Order_Value': round(float(average_order_value), 2),
        'Average_Discount_Percent': round(float(average_discount), 2)
    }


# ---------- Function 2: orders in each month ----------
def monthly_orders(Orders):
    Orders = Orders.copy()                                # copy, so the original table is not changed
    Orders['months'] = Orders['Order_DateTime'].dt.to_period('M').astype(str)   # e.g. 2025-07

    return Orders.groupby('months')['Order_ID'].nunique() # count orders in each month


# ---------- Function 3: revenue in each month ----------
def monthly_revenue(Orders):
    Orders = Orders.copy()
    Orders['months'] = Orders['Order_DateTime'].dt.to_period('M').astype(str)

    return Orders.groupby('months')['Total_Price'].sum()  # add up the money in each month


# ---------- Function 4: orders on each date ----------
# (our data covers only about one month, so a daily trend looks better than a monthly one)
def daily_orders(Orders):
    Orders = Orders.copy()
    Orders['date'] = Orders['Order_DateTime'].dt.date     # keep only the date part, e.g. 2025-07-20

    return Orders.groupby('date')['Order_ID'].nunique()


# ---------- Function 5: busiest hours of the day ----------
def orders_by_hour(Orders):
    hours = Orders['Order_DateTime'].dt.hour              # take the hour (0 to 23) of every order

    return hours.value_counts().sort_index()              # count orders in each hour, in hour order


# ---------- Function 6: revenue by restaurant (top 10) ----------
def revenue_by_restaurant(Orders, Restaurants):
    # Join Orders with Restaurants so every order knows its restaurant name
    # (we pick only the columns we need, so the tables do not clash)
    merged = Orders.merge(Restaurants[['Res_ID', 'Res_Name']], on='Res_ID', how='left')

    result = merged.groupby('Res_Name')['Total_Price'].sum()   # add up money for each restaurant
    return result.sort_values(ascending=False).head(10)        # biggest first, keep top 10


# ---------- Function 7: revenue by cuisine ----------
def revenue_by_cuisine(Orders, Restaurants):
    merged = Orders.merge(Restaurants[['Res_ID', 'Res_Cuisine']], on='Res_ID', how='left')

    result = merged.groupby('Res_Cuisine')['Total_Price'].sum()
    return result.sort_values(ascending=False)


# ---------- Function 8: top selling food items (by quantity) ----------
def top_food_items(Orders, Menu_Items):
    # Join Orders with Menu_Items so every order knows the food name
    merged = Orders.merge(Menu_Items[['Item_ID', 'Food_Item']], on='Item_ID', how='left')

    result = merged.groupby('Food_Item')['Quantity'].sum()     # total quantity sold of each item
    return result.sort_values(ascending=False).head(10)


# ---------- Runs only when you run this file directly ----------
# (When the dashboard imports this file later, this part is skipped)
if __name__ == "__main__":
    data = load_clean_data()                  # load and clean all tables ONCE

    if data is not None:
        Orders = data['Orders']               # the cleaned Orders table
        Restaurants = data['Restaurants']     # the cleaned Restaurants table
        Menu_Items = data['Menu_Items']       # the cleaned Menu_Items table

        print("\nMissing values in Orders:")
        print(Orders.isnull().sum())          # quick data check (should be all 0)

        print("\nKey numbers:")
        print(analyze_order(Orders))

        print("\nOrders per month:")
        print(monthly_orders(Orders))

        print("\nRevenue per month:")
        print(monthly_revenue(Orders))

        print("\nOrders per date:")
        print(daily_orders(Orders))

        print("\nOrders by hour:")
        print(orders_by_hour(Orders))

        print("\nRevenue by restaurant (top 10):")
        print(revenue_by_restaurant(Orders, Restaurants))

        print("\nRevenue by cuisine:")
        print(revenue_by_cuisine(Orders, Restaurants))

        print("\nTop selling food items:")
        print(top_food_items(Orders, Menu_Items))