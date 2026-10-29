# ==========================================================
# 06_app.py
# Job of this file: the Streamlit DASHBOARD
# It only SHOWS results. All the maths lives in files 02 to 05.
# Run it with:  streamlit run 06_app.py
# ==========================================================

import importlib                                              # lets us import files whose names start with a number
import streamlit as st                                        # streamlit builds the web dashboard

# ---------- Import our own files and pick the functions we need ----------
cleaning = importlib.import_module("02_cleaning_data")
customer_file = importlib.import_module("03_customer_analysis")
orders_file = importlib.import_module("04_orders_analysis")
delivery_file = importlib.import_module("05_delivery_analysis")

load_clean_data = cleaning.load_clean_data

customer_analysis = customer_file.customer_analysis

analyze_order = orders_file.analyze_order
monthly_orders = orders_file.monthly_orders
daily_orders = orders_file.daily_orders
orders_by_hour = orders_file.orders_by_hour
revenue_by_restaurant = orders_file.revenue_by_restaurant
revenue_by_cuisine = orders_file.revenue_by_cuisine
top_food_items = orders_file.top_food_items

delivery_status = delivery_file.delivery_status
delivery_kpis = delivery_file.delivery_kpis
delivery_time_list = delivery_file.delivery_time_list
executive_performance = delivery_file.executive_performance


# ---------- Page configuration ----------
st.set_page_config(
    page_title="Food Delivery Analysis",
    page_icon="🚚",
    layout="wide"
)


# ---------- Minimal styling ----------
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


# ---------- App title ----------
st.title("🚚 Food Delivery Analysis")
st.caption("Customer insights, order performance and delivery overview")

st.divider()


# ---------- Load data (only once, then remembered) ----------
# Streamlit re-runs this whole file after every click.
# @st.cache_data remembers the result, so MySQL is not read again and again.
@st.cache_data
def get_data():
    data = load_clean_data()                                  # connect to MySQL, load and clean the tables
    if data is None:                                          # load_clean_data returns None when something fails
        raise Exception("Could not load data. Check that MySQL is running and the settings in 01_connect_sql.py.")
    return data


# ---------- Load data and check database status ----------
try:
    data = get_data()

    customer = data['Customers']
    menu = data['Menu_Items']
    restaurant = data['Restaurants']
    order = data['Orders']
    delivery = data['Delivery']

    db_connected = True

except Exception as e:
    db_connected = False
    error_message = str(e)


# ---------- Sidebar ----------
with st.sidebar:
    st.title("Food Delivery")
    st.caption("Analytics Dashboard")

    st.divider()

    st.subheader("Database Status")

    if db_connected:
        st.success("Connected")
    else:
        st.error("Not connected")
        st.caption(error_message)

    # Button to read the latest data from MySQL again
    if st.button("Refresh data"):
        st.cache_data.clear()                                 # forget the remembered data
        st.rerun()                                            # run the page again

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Customer Analysis",
            "Order Analysis",
            "Delivery Analysis"
        ]
    )

    st.divider()
    st.caption("Food Delivery Customer Analysis")


# ---------- Stop if data could not be loaded ----------
if not db_connected:
    st.error(
        "Unable to load project data. "
        "Check your database connection and table names."
    )
    st.stop()


# ==========================================================
# PAGE 1: Overview
# ==========================================================
if page == "Overview":

    st.subheader("Dashboard Overview")
    st.caption("A quick summary of your food delivery data.")

    total_customers = customer['C_ID'].nunique()
    total_orders = order['Order_ID'].nunique()
    total_restaurants = restaurant['Res_ID'].nunique()
    total_revenue = order['Total_Price'].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Restaurants", f"{total_restaurants:,}")
    col4.metric("Total Revenue", f"{total_revenue:,.2f}")

    st.divider()

    # Our data covers about one month, so a daily chart is clearer than a monthly one
    st.subheader("Daily Orders")
    st.line_chart(daily_orders(order))

    st.subheader("Recent Orders")
    st.dataframe(order.tail(10))


# ==========================================================
# PAGE 2: Customer Analysis
# ==========================================================
elif page == "Customer Analysis":

    st.subheader("Customer Analysis")
    customer_data = customer_analysis(customer, order)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", customer_data['Total_Customers'])
    col2.metric("Repeated Customers", customer_data['Repeated_Customers'])
    col3.metric("One-time Customers", customer_data['One_Time_Customers'])
    col4.metric("Never Ordered", customer_data['Never_Ordered_Customers'])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customers by Gender")
        st.bar_chart(customer_data['Gender_Count'])

    with col2:
        st.subheader("Customers by City")
        st.bar_chart(customer_data['City_Count'])


# ==========================================================
# PAGE 3: Order Analysis
# ==========================================================
elif page == "Order Analysis":

    st.subheader("Order Analysis")
    order_data = analyze_order(order)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"{order_data['Total_Revenue']:,.2f}")
    col2.metric("Total Orders", f"{order_data['Total_Orders']:,}")
    col3.metric("Average Order Value", f"{order_data['Average_Order_Value']:,.2f}")
    col4.metric("Average Discount", f"{order_data['Average_Discount_Percent']:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Orders")
        st.bar_chart(monthly_orders(order))

    with col2:
        st.subheader("Daily Orders")
        st.line_chart(daily_orders(order))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Restaurants by Revenue")
        st.bar_chart(revenue_by_restaurant(order, restaurant))

    with col2:
        st.subheader("Revenue by Cuisine")
        st.bar_chart(revenue_by_cuisine(order, restaurant))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Selling Food Items")
        st.bar_chart(top_food_items(order, menu))

    with col2:
        st.subheader("Orders by Hour of the Day")
        st.bar_chart(orders_by_hour(order))

    st.subheader("Order Records")
    st.dataframe(order)


# ==========================================================
# PAGE 4: Delivery Analysis
# ==========================================================
elif page == "Delivery Analysis":

    st.subheader("Delivery Analysis")
    delivery_data = delivery_kpis(order, delivery)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Deliveries", f"{delivery_data['Total_Deliveries']:,}")
    col2.metric("Success Rate", f"{delivery_data['Success_Rate_Percent']:.1f}%")
    col3.metric("Failure Rate", f"{delivery_data['Failure_Rate_Percent']:.1f}%")
    col4.metric("Average Delivery Time", f"{delivery_data['Average_Delivery_Minutes']:.1f} min")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Delivery Status")
        st.bar_chart(delivery_status(delivery))

    with col2:
        st.subheader("Delivery Time (minutes) vs Number of Orders")
        times = delivery_time_list(order, delivery).round(0)  # round to whole minutes
        st.bar_chart(times.value_counts().sort_index())       # how many orders took each time

    st.subheader("Delivery Executive Performance")
    st.dataframe(executive_performance(order, delivery))

    st.subheader("Delivery Records")
    st.dataframe(delivery)