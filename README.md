# Democratizing Data-Driven Decisions: An Open-Source Modular KPI Dashboard Kit for Small Business Entrepreneurs

## Abstract
The digital age presents significant opportunities and challenges for small businesses, especially in utilizing data analytics for informed decision-making. High costs and technical complexities often preclude small entrepreneurs from accessing sophisticated data tools, especially in budding/early ventures. This project introduces a no-cost, modular Key Performance Indicator (KPI) dashboard utilizing open-source technologies like Plotly and Dash, aimed at empowering small business owners by simplifying data analysis. This dashboard allows users to upload CSV files to track and visualize KPIs relevant to financial health, customer satisfaction, and product performance. The current version allows enhanced accessibility to data analytics, fostering more informed business decisions among entrepreneurs.

## Introduction:
In 2020, the United States witnessed an unprecedented surge in entrepreneurship, marking a 24% increase in business applications from the previous year. Despite this growth, small businesses, which constitute 99.9% of U.S. enterprises, face high failure rates due to inadequate planning and insufficient data insights. The necessity for accessible and intuitive data analytics tools is evident [1]. This project aims to address these challenges by developing an open-source, modular KPI dashboard to aid small business owners in data-driven decision-making without the burden of high costs or complexity.

Currently retail commerce sights include built-in analytics tools like [Square](https://squareup.com/us/en/point-of-sale/features/dashboard/analytics) and [Shopify](https://www.shopify.com/analytics), where entrepreneurs can post their products and track analytics; however, these sites come with hefty price tags and subscription fees - which can be unfeasible for a new entrepreneur who is still establishing their business viability.

Thus, in this project, we envision a free, open-source solution for retail commerce/product sales analytics by simply uploading a few CSV files.

## Project Overview
This project is a Dash-based [2] web application designed to visualize key performance indicators (KPIs) for a micro business, like a private handmade jewelry seller. It features a comprehensive dashboard that displays financial metrics, customer satisfaction indices, and product performance insights, allowing for effective business strategy planning and performance evaluation.

Read more via my blog post here: https://leannmendoza.squarespace.com/work/democratizing-data-driven-decisions-developing-no-cost-modular-kpi-dashboard-kit-for-small-business-entrepreneurs

## Features

- **Financial KPIs Overview**: Visualizes monthly and annual revenue, costs, and profits to assess the financial health and growth of the business.
- **Customer Satisfaction KPIs**: Analyzes repeat customer rates and new customer acquisition trends to gauge customer satisfaction and loyalty.
- **Product Performance KPIs**: Offers insights into product popularity, sales trends, and inventory management through detailed item-specific sales data.
![Example Image](financialkpis.png "This is an example image")
![Example Image](customersatisfactionkpis.png "This is an example image")
![Example Image](productkpis.png "This is an example image")

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- pip

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/leannmendoza/Modular_KPI_Dashboard.git
cd Modular_KPI_Dashboard
```
2. **Set up a virtual environment (Optional but recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the requirements**
   
```bash
pip install -r requirements.txt
```
### Running the Application

1. **Prepare your data**

Ensure you have the jewelry_order_form.csv and jewelry_prices.csv files in the root directory or specify their paths via command-line arguments.

2. **Start the Dash app**

```bash
python dashboard.py --order_data_path your_order_data.csv --item_cost_path your_item_cost_data.csv --date_column_name OrderDate --email_column_name Email
```
Replace your_order_data.csv and your_item_cost_data.csv with the paths to your CSV files if they are different from the defaults.
Replace OrderDate and Email with the column name that contains the date data and customer email data

your_order_data.csv.csv
This CSV file can be downloaded directly if your business takes orders from Google forms. A few columns are required for modularity to work: 
* Column that contains date data
* Column that contains email data
* Columns that match Item names in your_item_cost_data.csv

your_item_cost_data.csv
This CSV file should list all the items or services offered by your business, along with their costs and prices. The structure is as follows: [Item, Cost, Price]

3. **Access the Dashboard**

Open a web browser and navigate to http://127.0.0.1:8022/ (or the port you specified). See Line 369.

### Built With

* Dash - The main framework used for creating the web application.
* Plotly - Used for creating interactive charts.

### Statement of Contributions:
Leann Mendoza: Conceptualization, design, and implementation of the dashboard, as well as drafting the manuscript.

## References:
[1] U.S. Small Business Administration. (2020). "Small Business GDP: Update 2002-2020." U.S. Small Business Administration Office of Advocacy. This source provides statistics on the importance and economic impact of small businesses in the U.S.
[2] Plotly Technologies Inc. (2022). "Plotly and Dash Documentation." https://plotly.com/. This documentation helped in using Plotly and Dash frameworks for building interactive web applications.


