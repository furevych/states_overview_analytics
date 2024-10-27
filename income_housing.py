#complex dataset with sub-columns, dwnld from U.S Census Bureau, y 2024, in csv, original name "Financial Characteristics for Housing Units With a Mortgage"  

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('housing.csv')
#States names repr. as col names in alph. order, each col contains subcolumn nm 'Estimate' with needed values
state_columns = [col for col in df.columns if 'Estimate' in col]

# Prepare a list to hold results
results = []

# Loop through the relevant columns for each state
for column in state_columns:
    # Fetch the value for by row index
    median_income_value = df[column].iloc[26]  # This corresponds to "Median household income (dollars) in the df"
    median_housing_cost = df[column].iloc[9]  # Med. housing unit cost with mortgage
    med_month_housing_cost = df[column].iloc[44] #med. monthly housing cost
    
    # Extract the state name from the column header
    state_name = column.split('!!')[0]  # State name ends before '!!' in th csv 
    
    # Appending results
    results.append({
        'State': state_name, 
        'Median Household Income $': median_income_value, 
        'Median Cost of Housing Unit with Mortgage': median_housing_cost,
        "Median Monthly Housing Costs": med_month_housing_cost
    })

# Create a new DataFrame from the results
df_median_income = pd.DataFrame(results)

# Remove duplicates based on 'State' and keep the first occurrence
df_median_income = df_median_income.drop_duplicates(subset=['State'], keep='first')
# Reset the index after dropping duplicates
df_median_income.reset_index(drop=True, inplace=True)

# Convertion to numeric, removing commas
df_median_income['Median Household Income $'] = pd.to_numeric(
    df_median_income['Median Household Income $'].str.replace(',', ''), 
    errors='coerce')
df_median_income['Median Cost of Housing Unit with Mortgage'] = pd.to_numeric(
    df_median_income['Median Cost of Housing Unit with Mortgage'].str.replace(',', ''), 
    errors='coerce')
df_median_income['Median Monthly Housing Costs'] = pd.to_numeric(
    df_median_income['Median Monthly Housing Costs'].str.replace(',', ''), 
    errors='coerce')


##calc-s:
# Calculate the ratios for visualization
df_median_income['Housing to Income Ratio'] = df_median_income['Median Cost of Housing Unit with Mortgage'] / df_median_income['Median Household Income $']
#calc. annual housing costs
df_median_income['Median Annual Housing Costs'] = df_median_income['Median Monthly Housing Costs'] *12


# Sort, create, manipulate df to display
sorted_df = df_median_income.sort_values(by='Housing to Income Ratio')
viz1 = sorted_df.head(10)  # Best (least) ratio
viz2 = df_median_income.sort_values(by='Median Household Income $').head(10) #sorted by the lowest income
viz3 = df_median_income.sort_values(by='Median Household Income $').tail(10) #sorted by the highest income

#function to viz. df as barchart: pass pre-aggregated df to 'viz_data, its 'title', columns names to compare values
def visualize(viz_data, title, col_name1, col_name2):
 
    # Creating the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the bars for the first column (e.g., median household income)
    ax.barh(viz_data['State'], viz_data[col_name1], color='darkblue', label=col_name1, alpha=0.7)
    
    # Plot the bars for the second column (e.g., median housing cost)
    ax.barh(viz_data['State'], viz_data[col_name2], color='lightblue', label=col_name2, alpha=0.5)

    # Set the x-axis limit for better visualization
    ax.set_xlim(0, max(viz_data[col_name1].max(), viz_data[col_name2].max()) * 1.1)

    # Adding actual values on bars
    for index, value in enumerate(viz_data[col_name1]):
        ax.text(value, index, f'{value:,.0f}', color='black', ha='right', va='center')

    for index, value in enumerate(viz_data[col_name2]):
        ax.text(value, index, f'{value:,.0f}', color='black', ha='right', va='center')

    # Add labels and title
    ax.set_xlabel('Dollars')
    ax.set_title(title)
    ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()

#viz the dfs
#visualize(viz3, 'Highest Annual Household Income vs. Annual Housing Costs by State', 'Median Household Income $', 'Median Annual Housing Costs')

#visualize(viz2, 'Lowest Annual Household Income vs. Annual Housing Costs by State', 'Median Household Income $', 'Median Annual Housing Costs')

#visualize(viz1, 'Top 10 states with the best Housing Price to Income ratio', 'Median Household Income $', 'Median Cost of Housing Unit with Mortgage' )
#visualize(viz3, 'Top 10 states with the Highest Household Income compared to Housing Unit Price', 'Median Household Income $', 'Median Cost of Housing Unit with Mortgage' )