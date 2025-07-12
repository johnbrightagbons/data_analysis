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

# Import all necessary libraries
import pandas as pd # For tables and data manipulation
import matplotlib.pyplot as plt # For plotting graphs
import os # For file path operations
from datetime import datetime # For date handling

# Define the file path for the dataset
input_file_path = 'sale_data.csv'  # Path to the file
output_file_path = 'sale_analysis_result.csv' # Path for file output
analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Show current time

# Check if file exist before making attempt to read from it
if not os.path.exists(input_file_path): 
    print(f"Error finding {input_file_path}.")
    print("Creating file for analysis...")

    # Create a data sample if file does not exist
    data_sample =  {
        'Month': [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        'Revenue': [1500, 1800, 2400, 2000, 2300, 1900, 2100, 2200, 2500, 2700, 2600, 2800],
        'Expenses': [500, 600, 800, 700, 900, 750, 850, 950, 1000, 1100, 1050, 1200]
    }
    df = pd.DataFrame(data_sample)

    # Save the data sample as an Excel CSV file
    df.to_csv(input_file_path, index=False) 
    print(f"File Created at: {input_file_path}")

else:
    try:
        # Read data from the Excel CSV file
        df = pd.read_csv(input_file_path)
        print(f"File Successfully Loaded From: {input_file_path}")
    except Exception as e:
        print(f"Error Reading the Excel File: {e}")
        exit()

# Data Validation to check if required columns exist
required_columns = ['Month', 'Revenue', 'Expenses']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Error: Missing required columns: {missing_columns}")
    exit()

# Data Cleaning 
# Check for missing values in the dataset
if df.isnull().values.any():
    print("Warning: Missing values found in the dataset. Filling with 0.")
    df.fillna(0, inplace=True)

# Convert revenue and expenses to numeric values
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce') 
df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')

# Data Analysis
# Calculate the profit (Revenue - Expenses) 
# and add it as a new column called 'Profit'
df['Profit'] = df['Revenue'] - df['Expenses'] 

# Calculate the Profit Margin Percentage
df['Profit_Margin_Percentage'] = (df['Profit'] / df['Revenue']) * 100

# Calculate total and average revenue needed for analysis
total_revenue = df['Revenue'].sum() # Total revenue
average_revenue = df['Revenue'].mean() # Average revenue
total_profit = df['Profit'].sum() # Total profit
average_profit = df['Profit'].mean() # Average profit

 # Print the analysis results
print("\n================== Analysis Results ==================")
print(f"Analysis Time: {analysis_time}") # Current time of analysis
print(f"Number of Months Analyzed: {len(df)}") # Total months analyzed
print(f"Total Revenue: ${total_revenue:.2f}") # Total revenue
print(f"Average Monthly Revenue: ${average_revenue:.2f}") # Average monthly revenue
print(f"Total Profit: ${total_profit:.2f}") # Total profit
print(f"Average Monthly Profit: ${average_profit:.2f}") # Average monthly profit
print("\nMonthly Breakdown:") # Monthly breakdown of revenue, expenses, and profit
print(df[['Month', 'Revenue', 'Expenses', 'Profit', 'Profit_Margin_Percentage']].to_string(index=False))

# Find the best-performing month based on revenue
highest_revenue_month = df.loc[df['Revenue'].idxmax()]['Month']
highest_revenue_value = df['Revenue'].max() # Best performing month revenue
print(f"\nThe Best Performing Month: {highest_revenue_month} with a Revenue of: ${highest_revenue_value:.2f}")

# Find the month with above average revenue
above_average_revenue_months = df[df['Revenue'] > average_revenue]['Month'].tolist()
print(f"\n The Months with Above Average Revenue: {', '.join(above_average_revenue_months)}")

# Preparing Data for Visualization
visualization_df = df.copy()  # Create a copy of the DataFrame for visualization

# Visualize monthly revenue using a bar chart
plt.figure(figsize=(12, 6))  # Set the figure size for the bar chart
bars = plt.bar(visualization_df['Month'], visualization_df['Revenue'], color='Green')  # Create a bar chart with green bars
plt.title('Monthly Revenue Analysis', fontsize=16)  # Set the title of the chart to 16 font size
plt.xlabel('Month', fontsize=14)  # Set the x-axis label to 14 font size
plt.ylabel('Revenue ($)', fontsize=14)  # Set the y-axis label to
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add a grid to the y-axis with dashed lines

# Adding data labels on top of each bar
for bar in bars: # Iterate through each bar in the chart
    height = bar.get_height() # Get the height of the bar
    # Add a text label on top of the bar with the height value
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{height:,.0f}',
        ha='center',
        va='bottom'
    )
plt.tight_layout()  # Adjust the layout to prevent overlap
plt.show()  # Display the bar chart 

# Show the Profit Margin Percentage Trend
plt.figure(figsize=(12, 6))  # Set the figure size for profit margin trend
bars = plt.bar(visualization_df['Month'], 
               visualization_df['Profit_Margin_Percentage'], color='Blue', alpha=0.7)  # Create a bar chart for profit margin with blue bars
plt.title('Monthly Profit Margin Percentage', fontsize=16)  # Set the title of the chart to 16 font size
plt.xlabel('Month', fontsize=14)  # Set the x-axis label to 14 font size
plt.ylabel('Profit Margin Percentage (%)', fontsize=14)  # Set the y-axis label
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add a grid to the y-axis with dashed lines

# Adding data labels on top of each bar for profit margin
for bar in bars:  # Iterate through each bar in the chart
    height = bar.get_height()  # Get the height of the bar
    # Add a text label on top of the bar with the height value
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{height:.2f}%',
        ha='center',
        va='bottom')
plt.tight_layout()  # Adjust the layout to prevent overlap
plt.show()  # Display the profit margin bar chart

# Export the analysis results to a new CSV file
analysis_results = df.copy()  # Create a copy of the DataFrame for export
analysis_results['Analysis_Time'] = analysis_time  # Add the analysis time to the DataFrame
try: 
    analysis_results.to_csv(output_file_path, index=False)  # Export the DataFrame to a new CSV file
    print(f"\nAnalysis results exported successfully to {output_file_path}.") # Print success message
except Exception as e:
    print(f"Error exporting analysis results: {e}")  # Print error message if export is not successful

# End of the data analysis project
print("\n=============== Analysis Completed ===============")
print("The analysis has been performed and visualizations have been displayed.")
print("Check the output file for detailed results.")