import sys
import argparse
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Argument parser
parser = argparse.ArgumentParser(description='Load data for dashboard application.')

# Add arguments
parser.add_argument('--order_data_path', type=str, help='Path to the order data CSV file', default='jewelry_order_form.csv')
parser.add_argument('--item_cost_path', type=str, help='Path to the item cost CSV file', default='jewelry_prices.csv')
parser.add_argument('--date_column_name', type=str, help='Name of column that contains date data', default='Pickup Date')
parser.add_argument('--email_column_name', type=str, help='Name of column that contains email data', default='Email Address')

# Parse arguments
args = parser.parse_args()

# Import data
order_data_path = args.order_data_path
item_cost_path = args.item_cost_path
order_data = pd.read_csv(order_data_path)
item_cost_data = pd.read_csv(item_cost_path)

date_column_name = args.date_column_name
email_column_name = args.email_column_name

# Data Cleaning

# Convert Pickup Date to datetime
order_data[date_column_name] = pd.to_datetime(order_data[date_column_name])

# Extract Year-Month from Pickup Date for grouping
order_data['Year-Month'] = order_data[date_column_name].dt.to_period('M')
order_data['Year'] = order_data[date_column_name].dt.to_period('Y')

# Create a mapping of items to their prices
item_price_map = dict(zip(item_cost_data['Item'], item_cost_data['Price']))
item_cost_map = dict(zip(item_cost_data['Item'], item_cost_data['Cost']))

# Financial KPIs Overview:
# This section focuses on visualizing key financial metrics to assess the bakery's financial health and growth over time.
# The metrics include Month-over-Month (MoM) and Year-over-Year (YoY) changes in revenue and costs,
# providing valuable insights for strategic planning and performance evaluation.

# Figure 1: Cost and Price Comparison for Each Item
# This figure illustrates the cost versus selling price for each bakery item,
# offering insight into profit margins and pricing strategies.
fig1 = px.bar(item_cost_data, x='Item', y=['Cost', 'Price'], title='Cost and Price for Each Item')

# Figure 2: Annual Sum of Total Order Profits
# Visualizes the total profit earned each year, highlighting annual financial performance and growth.
# This helps in understanding the overall profitability trend over the years.

# Calculate total order value
order_items_columns = item_cost_data['Item']
total_order_value = []
for index, row in order_data.iterrows():
    total_value = 0
    for item in order_items_columns:
        if item in order_data.columns and pd.notnull(row[item]):
            total_value += row[item] * item_price_map.get(item, 0)
    total_order_value.append(total_value)

order_data['Total Order Value'] = total_order_value

# Calculate Total Order Cost
order_items_columns = item_cost_data['Item']
total_order_cost = []
for index, row in order_data.iterrows():
    total_cost = 0
    for item in order_items_columns:
        if item in order_data.columns and pd.notnull(row[item]):
            total_cost += row[item] * item_cost_map.get(item, 1)
    total_order_cost.append(total_cost)

order_data['Total Order Cost'] = total_order_cost

# Calculate total order profit (value - cost)
order_data['Total Order Profit'] = order_data['Total Order Value'] - order_data['Total Order Cost']

# Plot Sum of Total Order Profits by Year
order_data.groupby(order_data['Year'])['Total Order Profit'].sum()
fig2 = px.bar(order_data.groupby(order_data['Year'].astype(str))['Total Order Profit'].sum().reset_index(), x='Year', y='Total Order Profit',
             title='Sum of Total Order Profits by Year',
             labels={'Year': 'Year', 'Total Order Profit': 'Total Order Profit'})

# Figure 3: Annual Comparison of Total Order Profits and Costs
# This figure compares the yearly totals of order profits against costs,
# facilitating a deeper understanding of financial management and cost efficiency.


# Plot Sum of Total Order Profits and Costs by Year
fig3 = px.bar(order_data.groupby(order_data['Year'].astype(str))['Total Order Profit'].sum().reset_index(), x='Year', y='Total Order Profit',
             title='Sum of Total Order Profits and Costs by Year',
             labels={'Year': 'Year', 'Total Order Profit': 'Total Order Profit'})

fig3.add_trace(go.Bar(
    x=order_data.groupby(order_data['Year'].astype(str))['Total Order Cost'].sum().reset_index()['Year'],
    y=order_data.groupby(order_data['Year'].astype(str))['Total Order Cost'].sum().reset_index()['Total Order Cost'],
    name='Total Order Cost',
    marker_color='red'
))

fig3.update_layout(barmode='overlay')


# Figure 4: Monthly Revenue Generation
# Tracks revenue generated each month, showing trends and identifying seasonal patterns.
# Essential for short-term financial planning and performance monitoring.

# Group by Year-Month and calculate sum of Total Order Value for monthly revenue
monthly_revenue = order_data.groupby('Year-Month')['Total Order Value'].sum().reset_index()
monthly_revenue['Year-Month'] = monthly_revenue['Year-Month'].astype(str)

# Plot Monthly Revenue Generation
fig4 = px.line(monthly_revenue, x='Year-Month', y='Total Order Value',
              title='Monthly Revenue Generation',
              labels={'Total Order Value': 'Revenue ($)', 'Year-Month': 'Year-Month'},
              markers=True)

# Set x-axis ticks to display each month
fig4.update_xaxes(tickangle=-45, tickmode='array', tickvals=monthly_revenue['Year-Month'], ticktext=monthly_revenue['Year-Month'])

# Figure 5: Monthly Revenue versus Cost of Goods Sold (COGS)
# Compares monthly revenue against the Cost of Goods Sold (COGS),
# crucial for evaluating the cost-effectiveness and operational efficiency of the bakery.

order_data['Year-Month'] = order_data[date_column_name].dt.to_period('M').astype(str)  # Ensure this is string for plotting
monthly_cogs = order_data.groupby('Year-Month')['Total Order Cost'].sum().reset_index()

# Ensure the 'Year-Month' column in both dataframes is in string format for plotting
monthly_revenue['Year-Month'] = monthly_revenue['Year-Month'].astype(str)
monthly_cogs['Year-Month'] = monthly_cogs['Year-Month'].astype(str)

# Create the figure
fig5 = go.Figure()

# Add revenue line
fig5.add_trace(go.Scatter(x=monthly_revenue['Year-Month'], y=monthly_revenue['Total Order Value'],
                         mode='lines+markers', name='Revenue', line=dict(color='blue')))

# Add COGS line
fig5.add_trace(go.Scatter(x=monthly_cogs['Year-Month'], y=monthly_cogs['Total Order Cost'],
                         mode='lines+markers', name='COGS', line=dict(color='red')))

# Update the layout
fig5.update_layout(title='Monthly Revenue vs. COGS',
                  xaxis=dict(title='Year-Month', tickmode='array',
                             tickvals=monthly_revenue['Year-Month'], tickangle=-45),
                  yaxis=dict(title='Amount ($)'),
                  legend=dict(y=1, x=1))

# Customer Satisfaction KPIs Overview:
# This section delves into metrics that shed light on customer loyalty and acquisition strategies.
# By analyzing repeat customer rates and the influx of new customers, we can gauge customer satisfaction,
# loyalty, and the effectiveness of marketing strategies.

# Figure 6: Monthly Repeat Customer Rate
# This figure calculates and visualizes the percentage of orders each month that come from repeat customers,
# defined as customers who have made more than one purchase over the dataset's time period.
# High repeat customer rates may indicate strong customer satisfaction and loyalty.
# Understanding this metric helps in evaluating the success of retention strategies.

# Count the number of orders per customer (using email as unique identifier)
customer_order_counts = order_data[email_column_name].value_counts()

# Identify repeat customers as those with more than one order
repeat_customers = customer_order_counts[customer_order_counts > 1].index.tolist()

# Mark each order as from a repeat customer or not
order_data['Is Repeat Customer'] = order_data[email_column_name].isin(repeat_customers)

# Group by Year-Month and calculate the total number of orders and the number of repeat orders
monthly_orders_summary = order_data.groupby('Year-Month').agg(
    Total_Orders=('Is Repeat Customer', 'size'),
    Repeat_Orders=('Is Repeat Customer', 'sum')
).reset_index()

# Calculate the monthly repeat customer rate
monthly_orders_summary['Repeat Customer Rate'] = (monthly_orders_summary['Repeat_Orders'] / monthly_orders_summary['Total_Orders']) * 100

# Ensure the 'Year-Month' column is in string format for plotting
monthly_orders_summary['Year-Month'] = monthly_orders_summary['Year-Month'].astype(str)

# Use Plotly Express to create the line plot for Repeat Customer Rate
fig6 = px.line(monthly_orders_summary, x='Year-Month', y='Repeat Customer Rate',
              title='Monthly Repeat Customer Rate',
              labels={'Repeat Customer Rate': 'Rate (%)', 'Year-Month': 'Year-Month'},
              markers=True)

# Update the layout
fig6.update_layout(title='Monthly Repeat Customer Rate',
                  xaxis=dict(title='Year-Month', tickmode='array',
                             tickvals=monthly_revenue['Year-Month'], tickangle=-45),
                  yaxis=dict(title='Repeat Customer Rate (%)'),
                  legend=dict(y=1, x=1))

# Calculate the total number of unique customers
total_unique_customers = order_data[email_column_name].nunique()

# Calculate the total number of orders
total_orders = len(order_data)

# Calculate the repeat customer rate
repeat_customer_rate = (total_orders - total_unique_customers) / total_unique_customers

# Print the repeat customer rate
print(f"Total Unique Customers: {total_unique_customers}")
print(f"Repeat Customer Rate: {repeat_customer_rate:.2%}")
print(f"Unique Customer Rate: {1-repeat_customer_rate:.2%}")

# Figure 7: Monthly New Customer Acquisition
# This figure tracks the number of new customers each month, showcasing the effectiveness of marketing campaigns
# and outreach efforts in attracting first-time buyers. Monitoring new customer acquisition trends
# is crucial for assessing growth opportunities and the appeal of the bakery to new market segments.

# Convert date_column_name to datetime if it isn't already
order_data[date_column_name] = pd.to_datetime(order_data[date_column_name])

# Group by email_column_name to find the first order date for each customer
first_order_date_per_customer = order_data.groupby(email_column_name)[date_column_name].min().reset_index()
first_order_date_per_customer.rename(columns={date_column_name: 'First Order Date'}, inplace=True)

# Merge this information back into the original DataFrame
order_data = order_data.merge(first_order_date_per_customer, on=email_column_name)

# Determine if each order is the customer's first order
order_data['Is First Order'] = order_data[date_column_name] == order_data['First Order Date']

# Group by Year and Month of date_column_name to count new customers each month
order_data['Year-Month'] = order_data[date_column_name].dt.to_period('M')
new_customers_per_month = order_data[order_data['Is First Order']].groupby('Year-Month').size()

# Convert the Series to a DataFrame for plotting
new_customers_per_month_df = new_customers_per_month.reset_index(name='Number of New Customers')
new_customers_per_month_df['Year-Month'] = new_customers_per_month_df['Year-Month'].astype(str)

# Use Plotly Express to create the bar chart
fig7 = px.bar(new_customers_per_month_df, x='Year-Month', y='Number of New Customers',
             title='New Customers Acquired Each Month',
             labels={'Number of New Customers': 'Number of New Customers', 'Year-Month': 'Year-Month'})

# Update layout for better readability
fig7.update_layout(xaxis_tickangle=-45)

# Product Performance KPIs Overview:
# This section focuses on analyzing individual product performances to identify best sellers,
# track sales trends, and evaluate product profitability. Understanding these metrics is key to optimizing
# product mix, pricing strategies, and inventory management.

# Figure 8: Month-over-Month Units Sold Per Item
# This figure provides a detailed view of how many units of each item were sold month-over-month.
# It's essential for identifying trends in product popularity, seasonal demands, or the impact of marketing campaigns.
# Such insights can guide decisions on promotional strategies or product discontinuations.

# Aggregate Units Sold Per Item
total_units_sold = order_data[item_cost_data['Item'].tolist()].sum()

# Prepare Data for Plotting
units_sold_df = total_units_sold.reset_index().rename(columns={'index': 'Item', 0: 'Total Units Sold'})

# Step 3: Plot Using Plotly
fig8 = px.bar(units_sold_df, x='Item', y='Total Units Sold', title='Units Sold Per Item',
             labels={'Total Units Sold': 'Units Sold', 'Item': 'Item'})
fig8.update_layout(xaxis={'categoryorder': 'total descending'})  # Order bars by descending units sold

# Figure 9: Monthly Sales Per Item
# Displays the monthly sales volume for each product, allowing for a direct comparison of product performance over time.
# This analysis helps in pinpointing which products consistently perform well and which may require marketing boosts or phased discontinuation.

# Melt the DataFrame to long format
melted_order_data = pd.melt(order_data, id_vars=['Year-Month'], value_vars=order_items_columns, var_name='Item', value_name='Quantity Sold')
melted_order_data

# Filter out rows where 'Quantity Sold' is NaN or zero
melted_order_data = melted_order_data.dropna(subset=['Quantity Sold'])
melted_order_data = melted_order_data[melted_order_data['Quantity Sold'] > 0]

# Group by 'Year-Month' and 'Item', then sum the 'Quantity Sold'
monthly_sales_per_item = melted_order_data.groupby(['Year-Month', 'Item'])['Quantity Sold'].sum().reset_index()
monthly_sales_per_item
monthly_sales_per_item['Year-Month'] = monthly_sales_per_item['Year-Month'].astype(str)

# Aggregate total sales per 'Year-Month' for the line plot
total_sales_per_month = monthly_sales_per_item.groupby('Year-Month')['Quantity Sold'].sum().reset_index()

fig9 = px.bar(monthly_sales_per_item, x='Year-Month', y='Quantity Sold', color='Item',
             title='Monthly Sales Per Item with Total Sales',
             labels={'Quantity Sold': 'Quantity Sold', 'Item': 'Item'},
             barmode='group')

# Add a line plot for total sales per 'Year-Month'
# We're using Plotly Graph Objects here to add to the figure created by Plotly Express
fig9.add_trace(go.Scatter(x=total_sales_per_month['Year-Month'], y=total_sales_per_month['Quantity Sold'],
                         mode='lines+markers',
                         name='Total Sales',
                         marker=dict(color='black'),  # Customize marker color
                         line=dict(color='black')))  # Customize line color

# Update layout to include both bar and line plots cohesively
fig9.update_layout(xaxis={'categoryorder': 'total descending'},
                  xaxis_title='Year-Month',
                  yaxis_title='Quantity Sold')

# Figure 10: Average Order Metrics
# This figure compiles average values of key order metrics such as average order size, value, and profitability.
# These averages are crucial for understanding the typical customer purchase behavior and the overall profitability
# of orders. Insights gained can inform strategies to increase average order value through up-selling or cross-selling.

average_order_price = order_data['Total Order Value'].mean()
average_order_cost = order_data['Total Order Cost'].mean()
average_order_profit = order_data['Total Order Profit'].mean()

# Data for plotting
categories = ['Average Order Price', 'Average Order Cost', 'Average Order Profit']
values = [average_order_price, average_order_cost, average_order_profit]

# Create the plot
fig10 = go.Figure(go.Bar(x=categories, y=values, marker_color=['blue', 'red', 'green']))

# Customize the layout
fig10.update_layout(title='Average Order Metrics',
                  yaxis_title='Amount ($)',
                  xaxis_title='Metric')


# Dashboard code

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('KPI Dashboard'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Financial KPIs', value='tab-1'),
        dcc.Tab(label='Customer Satisfaction KPIs', value='tab-2'),
        dcc.Tab(label='Product Performance KPIs', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4),
            dcc.Graph(figure=fig5),
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(figure=fig6),
            dcc.Graph(figure=fig7),
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(figure=fig8),
            dcc.Graph(figure=fig9),
            dcc.Graph(figure=fig10),
        ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8022)
