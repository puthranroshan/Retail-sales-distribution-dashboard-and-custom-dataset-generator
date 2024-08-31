import pandas as pd
import numpy as np
sales=pd.read_csv('C:/Users/proshan/OneDrive - SymphonyAI RETAIL CPG/Desktop/Projects/custom dataset generator/980sales.csv',sep=';')
promo=pd.read_csv('C:/Users/proshan/OneDrive - SymphonyAI RETAIL CPG/Desktop/Projects/custom dataset generator/980promo.csv',sep=';')
print(sales.head())
# merged=pd.merge(sales,promo,how='left',on=['ART_CINV'])
# print("The merged dataframe is ")
# print(merged.head())
print(sales.shape)
# print(merged.shape)
# Convert 'MVT_DATE' to datetime
sales['MVT_DATE'] = pd.to_datetime(sales['MVT_DATE'])

# Calculate duration
date_min = sales['MVT_DATE'].min()
date_max = sales['MVT_DATE'].max()
duration = date_max - date_min

# Determine the exact time period
if duration.days < 31:
    time_period = f"{duration.days} days"
elif 31 <= duration.days < 61:
    time_period = f"{duration.days // 7} weeks"
elif 61 <= duration.days < 366:
    time_period = f"{duration.days // 30} months"
elif 366 <= duration.days < 731:
    time_period = "more than one year but less than two years"
elif 731 <= duration.days < 1096:
    time_period = "more than two years but less than three years"
else:
    time_period = "three years or more"

print(f"The data covers a period of: {time_period}")


import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# Define a function to generate past dates
def generate_past_dates(current_date, years):
    start_date = current_date - timedelta(days=365 * years)
    date_range = pd.date_range(start=start_date, end=current_date, freq='D')
    return date_range

# Load the dataset (assuming it's in a CSV file for this example)
# Replace 'your_dataset.csv' with your actual dataset file
df = sales

# Convert MVT_DATE column to datetime
df['MVT_DATE'] = pd.to_datetime(df['MVT_DATE'])

# Generate past dates for 3 years
current_date = df['MVT_DATE'].max()
date_range = generate_past_dates(current_date, 3)

# Create an empty dataframe to hold the historical data
historical_data = pd.DataFrame()

# Generate historical sales data
for i, row in df.iterrows():
    article_code = row['ART_CINV']
    store_code = row['STORE_CODE']
    dc_code = row['DC_CODE']
    mvt_type = row['MVT_TYPE']
    sales_sp = row['SALES_SP']
    
    # Generate sales pattern based on existing SALES_QTY
    sales_qty_pattern = row['SALES_QTY'] + np.random.randint(-3, 3, size=len(date_range))
    sales_qty_pattern[sales_qty_pattern < 0] = 0  # Ensure sales quantity is non-negative
    
    # Create a new dataframe for this article and store
    historical_df = pd.DataFrame({
        'SALES_QTY': sales_qty_pattern,
        'ART_CINV': article_code,
        'STORE_CODE': store_code,
        'DC_CODE': dc_code,
        'MVT_DATE': date_range,
        'MVT_TIME': row['MVT_TIME'],
        'MVT_TYPE': mvt_type,
        'SALES_SP': sales_sp,
        'STK_QTY': row['STK_QTY']
    })
    
    # Append to historical data
    historical_data = pd.concat([historical_data, historical_df], ignore_index=True)

# Concatenate original and historical data
combined_df = pd.concat([df, historical_data], ignore_index=True)
combined_df
