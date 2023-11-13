from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd
import os


csvFiles = os.listdir("data")

data = []
for file in csvFiles:
    df = pd.read_csv('data/' + file)

    # Selecting necessary columns
    selected_data = df[['Date', 'Symbol', 'Close']]

    # Pivot the table
    pivoted_data = selected_data.pivot(index='Date', columns='Symbol', values='Close')

    # Rename the columns
    pivoted_data.columns.name = pivoted_data.columns.name if pivoted_data.columns.name is not None else ''
    pivoted_data = pivoted_data.reset_index().rename_axis(None, axis=1)

    data.append(pivoted_data)


df = pd.concat([df.set_index('Date') for df in data], axis=1).reset_index()

# Sort by the 'Date' column in descending order
df = df.sort_values('Date', ascending=False)

# Visualise Data
#styler = df.style.highlight_max(axis='index')
#breakpoint()
