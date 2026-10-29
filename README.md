# 🍔 Food Delivery Customer Analysis

An end-to-end data analytics project that transforms food delivery data into meaningful business insights using **MySQL, Python, Pandas, and Streamlit**.

The project follows a structured data journey, from retrieving records from a relational database to cleaning, analyzing, and visualizing the data through an interactive dashboard.

## 📌 Project Overview

Food delivery businesses generate valuable data about customers, orders, restaurants, food preferences, and delivery performance. Analyzing this data helps businesses understand customer behavior, monitor sales, identify popular food categories, and evaluate operational efficiency.

This project connects MySQL with Python to perform data analysis and presents the results through a Streamlit dashboard. The goal is to make important business insights accessible through interactive visualizations without requiring users to read SQL queries or Python code.

## 🎯 Project Objectives

- Analyze customer behavior and ordering patterns.
- Evaluate order performance and revenue trends.
- Identify high-performing restaurants and popular food items.
- Examine delivery duration and delivery status.
- Track key performance indicators (KPIs).
- Build an interactive dashboard for exploring business insights.
- Practice an end-to-end data analytics workflow using real-world tools.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| MySQL | Relational database and data retrieval |
| Python | Data processing and analysis |
| Pandas | Data manipulation and cleaning |
| Streamlit | Interactive dashboard development |
| Data Visualization Libraries | Charts and visual representation of insights |
| VS Code | Development environment |
| Git & GitHub | Version control and project hosting |

## 🔄 Project Workflow

The project follows a simple, step-by-step data analytics pipeline:

**MySQL → Python → Data Cleaning → Analysis → Streamlit Dashboard**

1. **Database:** Store and retrieve structured food delivery data from MySQL.
2. **Data Connection:** Connect Python to the database to access the required records.
3. **Data Cleaning:** Prepare the data for analysis by checking its quality and consistency.
4. **Customer Analysis:** Explore customer-related patterns and behavior.
5. **Order Analysis:** Analyze order volumes, revenue, monthly trends, and restaurant performance.
6. **Delivery Analysis:** Evaluate delivery statuses, delivery durations, and executive performance.
7. **Dashboard:** Present key metrics and analytical results through an interactive Streamlit application.

## 📊 Dashboard Features

### 1. Business Overview
- Overview of key business metrics.
- Summary of order and revenue performance.
- Quick access to important analytical results.

### 2. Customer Analysis
- Customer-related analysis and behavioral patterns.
- Exploration of customer data to understand ordering activity.

### 3. Order Analysis
- Monthly order trends.
- Monthly revenue analysis.
- Daily order patterns.
- Order distribution by hour.
- Revenue by restaurant.
- Revenue by cuisine.
- Top-performing food items.

### 4. Delivery Analysis
- Delivery status distribution.
- Delivery performance KPIs.
- Delivery duration analysis.
- Delivery executive performance.
- Identification of negative or invalid delivery-time values.

### 5. Interactive Streamlit Interface
- User-friendly dashboard layout.
- Sidebar navigation between analytical sections.
- Visual representation of business metrics.
- Database connection feedback.

## 📁 Project Structure

The project is organized into separate modules to make the code easier to understand, maintain, and extend.

```text
Project_Food_Delivery_Analysis/
│__food_delivery_csv_import_pack
|__My_sql_Analysis as name Food_Delivery
├── Python/
│_ 01_connect_sql.py 
  _02_cleaning_data.py
  _03_customer_analysis.py
  _04_orders_analysis.py
  _05_delivery_analysis.py
├── requirements.txt

```

*Note: Adjust the folder and file names in this tree to match the final structure of your repository.*

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python
- MySQL Server
- A MySQL client such as MySQL Workbench
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/aviragthesoul/Project_Food_Delivery_Analysis.git
```

Navigate to the project directory:

```bash
cd Project_Food_Delivery_Analysis
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

If a `requirements.txt` file is available, install the required libraries:

```bash
pip install -r requirements.txt
```

### Step 4: Configure the MySQL Database

1. Start your MySQL server.
2. Create or import the required database and tables.
3. Update the database connection settings in the Python configuration used by the project.
4. Ensure that the database credentials and table names match your local setup.

**Security note:** Keep database passwords and other sensitive credentials outside the repository. Use environment variables or a local `.env` file, and exclude that file from Git using `.gitignore`.

### Step 5: Run the Streamlit Dashboard

Navigate to the directory containing `06_app.py` and run:

```bash
streamlit run 06_app.py
```

Streamlit will start the application and provide a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your browser to explore the dashboard.

## 📈 Business Value

This project demonstrates how data analytics can help food delivery businesses:

- Understand customer activity and ordering patterns.
- Monitor revenue and order performance over time.
- Discover popular cuisines, restaurants, and food items.
- Evaluate delivery operations and executive performance.
- Identify data quality issues that may affect business reporting.
- Make more informed, data-driven decisions.

## 🚀 Learning Outcomes

Through this project, I am developing practical skills in:

- Connecting Python applications to MySQL.
- Retrieving and processing relational data.
- Organizing Python code into reusable analytical modules.
- Performing data cleaning and exploratory data analysis.
- Analyzing customer, order, and delivery performance.
- Building interactive dashboards using Streamlit.
- Structuring and documenting an end-to-end data analytics project.
- Publishing project code using GitHub.

## 🔮 Future Enhancements

Potential improvements include:

- Adding interactive filters for dates, restaurants, and cuisines.
- Implementing more advanced customer segmentation.
- Adding additional KPIs and business performance comparisons.
- Improving dashboard design and responsiveness.
- Adding automated data validation and error handling.
- Deploying the dashboard so it can be accessed online.

## 👨‍💻 Author

**Avirag**

Aspiring Data Analyst | Python | SQL | Data Analysis | Streamlit

GitHub: [@aviragthesoul](https://github.com/aviragthesoul)

---

⭐ If you find this project useful, consider giving the repository a star.

