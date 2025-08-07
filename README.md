# Vendor-Performance-Analysis-python-powerbi

This project performs a detailed **Vendor Performance Analysis** by consolidating multiple SQL data sources, analyzing performance metrics, and visualizing key business insights in Power BI. The objective is to help decision-makers identify underperforming vendors, optimize procurement strategies, and enhance vendor management.


## 📌 Objective

To automate and streamline the process of analyzing vendor data by:
- Extracting and merging data from multiple relational tables
- Performing exploratory data analysis (EDA)
- Classifying vendors based on defined business logic
- Creating a visual Power BI dashboard for quick decision-making

  ## 🛠️ Tools & Technologies

- **Python 3.x** – Data wrangling & transformation  
- **Pandas** – Data manipulation  
- **SQLite3** – Querying relational data  
- **Power BI** – Interactive data visualization  
- **Matplotlib / Seaborn** – Optional EDA plotting (if used)  
- **Logging** – For debugging and traceability

  ## 🧩 Project Workflow

### 1. 🧠 Data Ingestion & Transformation (Script: `get_vendor_summary.py`)

### 2. 📊 Exploratory Data Analysis (EDA)

Performed initial EDA using Python:
- Checked for null values, outliers, and duplicates
- Grouped vendors by category and calculated metrics
- Used summary statistics to understand data distribution
- Optional visualizations: Bar charts, box plots, etc.

### 3. 📈 Vendor Performance Analysis
It answers following business questions:
- Identifying Brands that needs Promotional or Pricing Adjustments which exhibit lower sales performance but higher profit margins.
- Which vendors and brands demonstrate the highest sales performance?
- Which vendors contribute the most to toal purchase dollars?
- How much of total procurement is dependent on the top vendors?
- Does purchasing in bulk reduce the unit price, and what is the optimal purchase volume for cost savings?
- How much capital is locked in unsold inventory per vendor and which vendors contribute the most to it?

  ### 4. 📉 Power BI Dashboard

![image](https://github.com/user-attachments/assets/07a32b68-783a-4a5a-abd8-19811b13974a)

![image](https://github.com/user-attachments/assets/ed666aa2-e286-442e-93f3-b567e1f03bf8)
