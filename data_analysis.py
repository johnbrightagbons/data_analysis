# Python Data Analysis Project
# Project Title: Monthly Sales Data Analysis
# Project Goal:
# Analyze a small sales dataset to find out:
# - Total and average revenue
# - Best-performing month
# - Visualize monthly revenue using a bar chart
# - Analyze profit trends
# - Calculate profit margin percentage
# - Identify months with above-average revenue
# - Export analysis results to a new CSV file
# - Analyze month-over-month profit growth 
# - Visualize profit trend with a line chart 

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Define the file path for the dataset
input_file_path = 'sale_data.csv'
output_file_path = 'sale_analysis_result.csv'
analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Check if file exists before attempting to read from it
if not os.path.exists(input_file_path):
    print(f"Error finding {input_file_path}.")
    print("Creating file for analysis...")
    # Create a data sample if file does not exist
    data_sample = {
        'Month': [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        'Revenue': [1500, 1800, 2400, 2000, 2300, 1900, 2100, 2200, 2500, 2700, 2600, 2800],
        'Expenses': [500, 600, 800, 700, 900, 750, 850, 950, 1000, 1100, 1050, 1200]
    }
    df = pd.DataFrame(data_sample)
    df.to_csv(input_file_path, index=False)
    print(f"File Created at: {input_file_path}")
else:
    try:
        df = pd.read_csv(input_file_path)
        print(f"File Successfully Loaded From: {input_file_path}")
    except Exception as e:
        print(f"Error Reading the Excel File: {e}")
        exit()

# Data Validation
required_columns = ['Month', 'Revenue', 'Expenses']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing required columns: {missing_columns}")
    exit()

# Data Cleaning
if df.isnull().values.any():
    print("Warning: Missing values found in the dataset. Filling with 0.")
    df.fillna(0, inplace=True)

# Convert revenue and expenses to numeric values
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')

# Sort months chronologically
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
df = df.sort_values('Month')

# Data Analysis
df['Profit'] = df['Revenue'] - df['Expenses']
df['Profit_Margin_Percentage'] = (df['Profit'] / df['Revenue']) * 100
df['Profit_MoM_Change'] = df['Profit'].pct_change() * 100  # Month-over-month change

# Calculate key metrics
total_revenue = df['Revenue'].sum()
average_revenue = df['Revenue'].mean()
total_profit = df['Profit'].sum()
average_profit = df['Profit'].mean()
average_profit_margin = df['Profit_Margin_Percentage'].mean()

# Print analysis results
print("\n================== Analysis Results ==================")
print(f"Analysis Time: {analysis_time}")
print(f"Number of Months Analyzed: {len(df)}")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Average Monthly Revenue: ${average_revenue:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Average Monthly Profit: ${average_profit:,.2f}")
print(f"Average Profit Margin: {average_profit_margin:.2f}%")
print("\nMonthly Breakdown:")
print(df[['Month', 'Revenue', 'Expenses', 'Profit', 'Profit_Margin_Percentage']].to_string(index=False))

# Find the best-performing month based on revenue
highest_revenue_month = df.loc[df['Revenue'].idxmax()]['Month']
highest_revenue_value = df['Revenue'].max()
print(f"\nBest Performing Month: {highest_revenue_month} with Revenue: ${highest_revenue_value:,.2f}")

# Find months with above-average revenue
above_average_revenue_months = df[df['Revenue'] > average_revenue]['Month'].tolist()
print(f"\nMonths with Above Average Revenue: {', '.join(above_average_revenue_months)}")

# Find months with above-average profit margin
above_average_margin_months = df[df['Profit_Margin_Percentage'] > average_profit_margin]['Month'].tolist()
print(f"\nMonths with Above Average Profit Margin: {', '.join(above_average_margin_months)}")

# Find the month with highest profit growth
if df['Profit_MoM_Change'].notna().any():
    highest_growth_month = df.loc[df['Profit_MoM_Change'].idxmax()]['Month']
    highest_growth_value = df['Profit_MoM_Change'].max()
    print(f"\nHighest Month-over-Month Profit Growth: {highest_growth_month} ({highest_growth_value:.2f}%)")
else:
    print("\nInsufficient data for month-over-month profit growth analysis")

# Visualization 1: Monthly Revenue Bar Chart
plt.figure(figsize=(12, 6))
bars = plt.bar(df['Month'], df['Revenue'], color='Green')
plt.title('Monthly Revenue Analysis', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Revenue ($)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)

# Add data labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'${height:,.0f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Visualization 2: Profit Margin Percentage Bar Chart
plt.figure(figsize=(12, 6))
bars = plt.bar(df['Month'], df['Profit_Margin_Percentage'], color='Blue', alpha=0.7)
plt.title('Monthly Profit Margin Percentage', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Profit Margin (%)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)

# Add data labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%',
             ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Visualization 3: Profit Trend Line Chart
plt.figure(figsize=(12, 6))
plt.plot(df['Month'], df['Profit'], marker='o', linestyle='-', color='Red', linewidth=2, markersize=8)
plt.title('Monthly Profit Trend', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Profit ($)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)

# Add data labels
for i, profit in enumerate(df['Profit']):
    plt.text(i, profit + 50, f'${profit:,.0f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Export results
analysis_results = df.copy()
analysis_results['Analysis_Time'] = analysis_time
try:
    analysis_results.to_csv(output_file_path, index=False)
    print(f"\nAnalysis results exported successfully to {output_file_path}")
except Exception as e:
    print(f"\nError exporting analysis results: {e}")

print("\n=============== Analysis Completed ===============")
print("The analysis has been Completed and visualizations have been displayed.")
print("Check the output file for detailed results.")