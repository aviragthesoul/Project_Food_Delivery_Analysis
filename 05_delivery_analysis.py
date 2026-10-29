# ==========================================================
# 05_delivery_analysis.py
# Job of this file: analyse DELIVERY (time taken, status, executives)
# Style: many small functions, each one answers ONE question
# ==========================================================

import importlib                                          # lets us import a file whose name starts with a number

cleaning = importlib.import_module("02_cleaning_data")    # loads our cleaning file (02)
load_clean_data = cleaning.load_clean_data                # we will use this function to get the cleaned data


# ---------- Function 1: join Orders + Delivery and add "delivery_minutes" ----------
# Orders table has the order time, Delivery table has the delivery time.
# So we join them, then: minutes taken = delivery time - order time
def analyze_delivery(orders, delivery):
    # Bring the needed Delivery columns into the Orders table (matching rows using Order_ID)
    df = orders.merge(
        delivery[['Order_ID', 'Del_Time', 'Status', 'Assigned_Executive']],
        on='Order_ID',
        how='left'                                        # keep every order
    )

    # Subtract the two dates, then convert the difference into minutes
    # (total_seconds() gives seconds, dividing by 60 gives minutes)
    df['delivery_minutes'] = (df['Del_Time'] - df['Order_DateTime']).dt.total_seconds() / 60

    return df


# ---------- Function 2: how many deliveries in each status? ----------
def delivery_status(delivery):
    return delivery['Status'].value_counts()              # Delivered / Failed / In Transit


# ---------- Function 3: key numbers ----------
def delivery_kpis(orders, delivery):
    df = analyze_delivery(orders, delivery)               # table with delivery_minutes

    total = len(df)                                       # all deliveries
    delivered = int((df['Status'] == 'Delivered').sum())  # successful deliveries
    failed = int((df['Status'] == 'Failed').sum())        # failed deliveries
    in_transit = int((df['Status'] == 'In Transit').sum())  # still on the way

    # Time taken makes sense only for DELIVERED orders, so we keep only those rows
    delivered_df = df[df['Status'] == 'Delivered']

    return {
        'Total_Deliveries': total,
        'Delivered': delivered,
        'Failed': failed,
        'In_Transit': in_transit,
        'Success_Rate_Percent': round(delivered / total * 100, 2),
        'Failure_Rate_Percent': round(failed / total * 100, 2),
        'Average_Delivery_Minutes': round(float(delivered_df['delivery_minutes'].mean()), 1),
        'Fastest_Delivery_Minutes': round(float(delivered_df['delivery_minutes'].min()), 1),
        'Slowest_Delivery_Minutes': round(float(delivered_df['delivery_minutes'].max()), 1)
    }


# ---------- Function 4: delivery times of all delivered orders ----------
# (the dashboard will draw a histogram from these numbers)
def delivery_time_list(orders, delivery):
    df = analyze_delivery(orders, delivery)
    delivered_df = df[df['Status'] == 'Delivered']

    return delivered_df['delivery_minutes'].round(1)


# ---------- Function 5: performance of each delivery executive ----------
def executive_performance(orders, delivery):
    df = analyze_delivery(orders, delivery)

    # Make two True/False columns, so we can add them up per executive
    df['Is_Delivered'] = df['Status'] == 'Delivered'
    df['Is_Failed'] = df['Status'] == 'Failed'

    # Group by executive: count total deliveries, delivered and failed
    summary = df.groupby('Assigned_Executive').agg(
        Total_Deliveries=('Order_ID', 'count'),
        Delivered=('Is_Delivered', 'sum'),
        Failed=('Is_Failed', 'sum')
    )

    # Average minutes, using DELIVERED rows only
    delivered_df = df[df['Status'] == 'Delivered']
    summary['Average_Minutes'] = delivered_df.groupby('Assigned_Executive')['delivery_minutes'].mean().round(1)

    return summary.sort_values('Total_Deliveries', ascending=False)   # busiest executive first


# ---------- Function 6: data check - any delivery before the order time? ----------
def check_negative_time(orders, delivery):
    df = analyze_delivery(orders, delivery)

    return int((df['delivery_minutes'] < 0).sum())        # should be 0


# ---------- Runs only when you run this file directly ----------
# (When the dashboard imports this file later, this part is skipped)
if __name__ == "__main__":
    data = load_clean_data()                  # load and clean all tables ONCE

    if data is not None:
        orders = data['Orders']               # the cleaned Orders table
        delivery = data['Delivery']           # the cleaned Delivery table

        print("\nDeliveries with negative time (should be 0):")
        print(check_negative_time(orders, delivery))

        print("\nStatus count:")
        print(delivery_status(delivery))

        print("\nOrders joined with delivery (first 5 rows):")
        print(analyze_delivery(orders, delivery).head())

        print("\nKey numbers:")
        print(delivery_kpis(orders, delivery))

        print("\nDelivery time summary (minutes):")
        print(delivery_time_list(orders, delivery).describe())

        print("\nExecutive performance:")
        print(executive_performance(orders, delivery))