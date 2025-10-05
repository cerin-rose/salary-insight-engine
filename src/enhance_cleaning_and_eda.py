import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 1️⃣ Load cleaned data
df = pd.read_csv("data/processed/clean_salary_data.csv")

# 2️⃣ Check & handle missing values
print("\nMissing values before cleaning:\n", df.isna().sum())

# Example: fill numeric nulls with median, categorical with 'Unknown'
num_cols = df.select_dtypes(include=[np.number]).columns
cat_cols = df.select_dtypes(exclude=[np.number]).columns

for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)
for col in cat_cols:
    df[col].fillna("Unknown", inplace=True)

# 3️⃣ Remove duplicates
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)
print(f"\nRemoved {before - after} duplicate rows")

# 4️⃣ Clean text columns (standardize)
text_cols = ['job_title', 'company', 'location', 'confidence']
for col in text_cols:
    df[col] = (
        df[col]
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-zA-Z0-9\s]", "", regex=True)
        .str.title()
    )

# 5️⃣ Convert experience columns (if you have them)
if "experience" in df.columns:
    df["experience"] = df["experience"].str.extract("(\d+)").astype(float)

# 6️⃣ Feature relationships
corr = df.select_dtypes(include=[np.number]).corr()
print("\nCorrelation Matrix:\n", corr)

# 7️⃣ Save enhanced dataset
os.makedirs("data/enhanced", exist_ok=True)
df.to_csv("data/enhanced/salary_clean_enhanced.csv", index=False)
print("✅ Saved enhanced dataset to data/enhanced/salary_clean_enhanced.csv")

# 8️⃣ 📊 EDA Visuals
sns.set(style="whitegrid")

# Salary distribution
plt.figure(figsize=(6,4))
sns.histplot(df['median_salary'], bins=10, kde=True)
plt.title("Salary Distribution")
plt.show()

# Job title vs salary
plt.figure(figsize=(8,4))
sns.barplot(data=df, x='job_title', y='median_salary')
plt.title("Average Salary per Job Title")
plt.xticks(rotation=30)
plt.show()

# Company vs salary spread
plt.figure(figsize=(8,4))
sns.boxplot(data=df, x='company', y='median_salary')
plt.title("Salary Spread by Company")
plt.xticks(rotation=30)
plt.show()

# Correlation heatmap
plt.figure(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Feature Correlations")
plt.show()
