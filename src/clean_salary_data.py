# src/clean_salary_data.py
import os, time, ast
import pandas as pd
import numpy as np

RAW = "data/raw/api_salary_data.csv"
PROCESSED_TMP = "data/processed/_tmp_clean_salary_data.csv"
PROCESSED_OUT = "data/processed/clean_salary_data.csv"

os.makedirs("data/processed", exist_ok=True)

# --- load raw ---
df_raw = pd.read_csv(RAW)
print("🔎 raw columns:", list(df_raw.columns))

# --- two input shapes supported ---
# A) Old shape: one column 'data' containing a stringified list of dicts
# B) New shape: already flattened rows (your new fetcher)
records = []
if "data" in df_raw.columns:
    # OLD: parse stringified list
    for i, row in df_raw.iterrows():
        try:
            for item in ast.literal_eval(str(row["data"])):
                records.append(item)
        except Exception as e:
            print("⚠️ parse error on row", i, e)
    flat = pd.DataFrame(records)
else:
    # NEW: already flat
    flat = df_raw.copy()

# --- normalize column names (case-insensitive) ---
flat.columns = [c.strip().lower() for c in flat.columns]

# map possible vendor variants -> our standard names
variants = {
    "job_title": ["job_title", "title", "job", "role"],
    "company": ["company", "company_name", "employer"],
    "location": ["location", "country", "region", "city"],
    "min_salary": ["min_salary", "minsalary", "salary_min"],
    "max_salary": ["max_salary", "maxsalary", "salary_max"],
    "median_salary": ["median_salary", "mediansalary", "salary", "base_salary"],
    "min_base_salary": ["min_base_salary", "minbasesalary"],
    "max_base_salary": ["max_base_salary", "maxbasesalary"],
    "median_base_salary": ["median_base_salary", "medianbasesalary"],
    "salary_period": ["salary_period", "period"],
    "salary_currency": ["salary_currency", "currency"],
    "salary_count": ["salary_count", "samples", "count"],
    "confidence": ["confidence", "confidence_level"],
}

def pick(colgroup):
    for name in colgroup:
        if name in flat.columns:
            return name
    return None

# build standardized frame
data = {}
for std, cand in variants.items():
    src = pick(cand)
    if src is not None:
        data[std] = flat[src]
    else:
        # create missing columns so downstream code is stable
        data[std] = np.nan

flat_df = pd.DataFrame(data)

# light type cleanup
num_cols = [
    "min_salary","max_salary","median_salary",
    "min_base_salary","max_base_salary","median_base_salary","salary_count"
]
for c in num_cols:
    flat_df[c] = pd.to_numeric(flat_df[c], errors="coerce")

# final minimal filter (keep only cols we standardized)
keep_cols = list(variants.keys())
flat_df = flat_df[keep_cols]

# --- safe save with retry (handles Windows file locks) ---
flat_df.to_csv(PROCESSED_TMP, index=False)
for _ in range(3):
    try:
        os.replace(PROCESSED_TMP, PROCESSED_OUT)
        break
    except PermissionError:
        print("🔄 file locked; retrying…")
        time.sleep(2)

print(f"✅ cleaned → {PROCESSED_OUT}  rows={len(flat_df)} cols={len(flat_df.columns)}")
print(flat_df.head())

