import pandas as pd
from functools import reduce
import re
from income_housing import df_median_income as income_and_housing

# Function to preprocess state names using regex matching
def match_states(state_name, states_list):
    clean_state = re.sub(r'\s+', ' ', state_name.strip()).lower()
    return next((state for state in states_list if re.fullmatch(clean_state, re.sub(r'\s+', ' ', state.strip()).lower())), None)

# Function to convert string values to numeric, handling '%' and ','
def convert_to_numeric(value):
    if isinstance(value, str):
        value = value.replace('%', '').replace(',', '')
    return float(value) if value else value  # Convert to float or return original value

# Function to load and preprocess dataset
def load_and_preprocess_dataset(filepath, state_column, value_columns):
    df = pd.read_csv(filepath)[[state_column] + value_columns]
    return df

# Function to merge all datasets
def merge_datasets(dfs):
    return reduce(lambda left, right: pd.merge(left, right, on='State', how='outer'), dfs)

# Main processing function
def process_data():
    # Load datasets and initialize states_list from the first dataset
    datasets = {
        'income_and_housing': income_and_housing[['State', 'Median Household Income $', 'Median Annual Housing Costs']],  # Only keep specified columns
        'medical': load_and_preprocess_dataset('med_ins_exp_forbes.csv', 'State', ['Total Score Out of 100']),
        'cpi': load_and_preprocess_dataset('cpi.csv', 'State', ['CPI']),
        'gas': load_and_preprocess_dataset('gas 2024 oct.csv', 'State', ['Mid Price Gas']),
        'tax': load_and_preprocess_dataset('tax 2024.csv', 'State', ['Combined Average Tax Burden']),
    }

    # Derive the state list from the income and housing dataset
    states_list = datasets['income_and_housing']['State'].unique().tolist()  # Get unique state names from the income and housing dataset

    # Match states in all datasets and convert relevant columns to numeric
    for key, df in datasets.items():
        df['State'] = df['State'].apply(lambda x: match_states(x, states_list))
        # Convert all relevant columns to numeric, excluding 'State'
        df.iloc[:, 1:] = df.iloc[:, 1:].applymap(convert_to_numeric)

    # Merge all DataFrames
    all_dfs = list(datasets.values())
    merged_df = merge_datasets(all_dfs)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('newdf.csv', index=False)

    # Optional: Check the final merged DataFrame
    print(merged_df.tail())

# Run the main processing function
if __name__ == "__main__":
    process_data()
