import pandas as pd
import ast
import os

# Load the raw file
raw_path = "data/raw/api_salary_data.csv"
df = pd.read_csv(raw_path)

# Step 1: Extract the JSON-like string from the 'data' column
# The API returns a list (as a string), so we convert it to Python objects
records = []
for i, row in df.iterrows():
    try:
        # safely evaluate the string into a list of dicts
        data_list = ast.literal_eval(row['data'])
        for item in data_list:
            records.append(item)
    except Exception as e:
        print("Error on row", i, e)

# Step 2: Flatten into a clean DataFrame
flat_df = pd.DataFrame(records)

# Step 3: Keep only the main columns you care about
keep_cols = [
    'location', 'job_title', 'company',
    'min_salary', 'max_salary', 'median_salary',
    'min_base_salary', 'max_base_salary', 'median_base_salary',
    'salary_period', 'salary_currency', 'salary_count', 'confidence'
]
flat_df = flat_df[keep_cols]

# Step 4: Save cleaned data
os.makedirs("data/processed", exist_ok=True)
flat_df.to_csv("data/processed/clean_salary_data.csv", index=False)
print("Cleaned file saved to data/processed/clean_salary_data.csv")
print(flat_df.head())
