# Surfs Up!

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

-----

# Step 1 

 To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
-----

## Climate Analysis and Exploration

* To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

-----

# Set up jupyter notebook

```python
# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = 'Resources/purchase_data.csv'

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

# Display a sample purchasing data
purchase_data.sample(10)
```

-----

# Player Count

* Display total number of players

```Python
# Calculate unique total players by 'SN'
total_SN = total_SN=len(purchase_df['SN'].unique())
total_SN

# Create a dataframe to display total players
player_count=pd.DataFrame({'Total Players':[total_SN]})
player_count
```

-----

# Purchasing Analysis (Total)

* Run basic calculations to obtain number of unique items, average price, etc.
* Create a summary data frame to hold the results
* Optional: give the displayed data cleaner formatting
* Display the summary data frame

```Python
# Calculate number of unique items
unique_items=len(purchase_df['Item Name'].unique())
unique_items

# Calculate average price
average_price=purchase_df['Price'].mean()
average_price

# Calculate number of purchases
purchase_count=len(purchase_df['Purchase ID'].unique())
purchase_count

# Calculate total revenue
total_revenue=purchase_df['Price'].sum()
total_revenue

# Create a dataframe of purchasing analysis
purchasing_analysis=pd.DataFrame({'Number of Unique Items':[unique_items],
                                    'Average Price':[average_price],
                                    'Number of Purchases':[purchase_count],
                                     'Total Revenue':[total_revenue]
                                    })
purchasing_analysis

# Create a purchasing analysis dataframe with cleaner formatting
purchasing_analysis['Average Price'] = purchasing_analysis['Average Price'].map('${:,.2f}'.format)
purchasing_analysis['Total Revenue'] = purchasing_analysis['Total Revenue'].map('${:,.2f}'.format)
purchasing_analysis
```
-----