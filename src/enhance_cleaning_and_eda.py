import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, time, numpy as np

# Step 1. Load cleaned data
df = pd.read_csv("data/processed/clean_salary_data.csv")

# Step 2. Clean / fill / enhance
num_cols = df.select_dtypes(include=[np.number]).columns
cat_cols = df.select_dtypes(exclude=[np.number]).columns
df[num_cols] = df[num_cols].apply(lambda s: s.fillna(s.median()))
df[cat_cols] = df[cat_cols].fillna("Unknown")

# Step 3. Simple visualization examples
sns.histplot(df["median_salary"], kde=True)
plt.title("Salary Distribution")
plt.savefig("data/enhanced/salary_distribution.png")
plt.close()

# Step 4. Save enhanced CSV safely
os.makedirs("data/enhanced", exist_ok=True)
temp_path = "data/enhanced/_tmp_salary_clean_enhanced.csv"
output_path = "data/enhanced/salary_clean_enhanced.csv"

df.to_csv(temp_path, index=False)
for _ in range(3):
    try:
        os.replace(temp_path, output_path)
        break
    except PermissionError:
        print("⚠️ File locked; retrying...")
        time.sleep(2)

print(f"✅ Enhanced file saved: {output_path}")
print(f"🔹 Rows: {len(df)}, Columns: {len(df.columns)}")
