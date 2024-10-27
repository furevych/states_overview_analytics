import pandas as pd
import matplotlib.pyplot as plt

# Load the processed DataFrame
df = pd.read_csv('newdf.csv')

# Function to plot stacked bar chart for one state
def plot_data(state_name):
    # Select data for the specified state
    state_data = df[df['State'] == state_name]

    if state_data.empty:
        print(f"State '{state_name}' not found in the data.")
        return

    # Define expense categories and income (removing 'Normalized' from names)
    expense_categories = {
        'Medical Costs': 'Normalized Medical Expenses',
        'Housing Costs': 'Normalized Median Annual Housing Costs',
        'CPI (Cost of Living Index)': 'Normalized CPI',
        'Gas Prices': 'Normalized Mid Price Gas',
        'Tax Burden': 'Normalized Combined Average Tax Burden'
    }
    income_category = 'Normalized Median Household Income $'

    # Get values for expenses and income
    expenses = [state_data[category].values[0] for category in expense_categories.values()]
    income = state_data[income_category].values[0]

    # Plot stacked bar for expenses
    plt.figure(figsize=(10, 6))

    # Create the bar chart for expenses (stacked)
    plt.bar("Expenses", sum(expenses), color='gray', label='Total Expenses')

    # Add individual expense categories (stacked) with shades of red
    bottom_val = 0
    red_shades = ['#FF9999', '#FF6666', '#FF3333', '#CC0000', '#990000']
    for i, (label, category) in enumerate(expense_categories.items()):
        plt.bar("Expenses", state_data[category].values[0], bottom=bottom_val, color=red_shades[i], label=label)
        bottom_val += state_data[category].values[0]

    # Add income bar next to the stacked expenses
    plt.bar('Income', income, color='#3399FF', label='Median Household Income')
    
    # Set x-ticks with appropriate labels under each bar
    plt.xticks([0, 1], ['Expenses', 'Income'], rotation=0, ha='center', fontsize=12)

    # Add titles and labels
    plt.title(f'Expenses vs Income for {state_name}', fontsize=16)

    # Remove tick marks and labels from the y-axis
    plt.gca().tick_params(axis='y', which='both', left=False, labelleft=False)

    # Add legend
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Show the plot
    plt.tight_layout()
    plt.show()

# List of states to visualize
states_to_plot = ['Massachusetts', 'Florida', 'Texas', 'New York']

# Plot for each state in the list
for state in states_to_plot:
    plot_data(state)
