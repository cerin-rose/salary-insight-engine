# src/fetch_salary_api.py
import os, time, requests, pandas as pd
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://job-salary-data.p.rapidapi.com/company-job-salary"
HEADERS = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY", "PASTE_KEY_HERE"),
    "x-rapidapi-host": "job-salary-data.p.rapidapi.com",
}

primary = [
    ("Amazon", "Software Engineer"),
    ("Google", "Data Scientist"),
    ("Apple", "Machine Learning Engineer"),
    ("Microsoft", "Data Analyst"),
    ("Netflix", "Backend Developer"),
]
fallback = [
    ("Meta", "Software Engineer"),
    ("Amazon", "Data Scientist"),
    ("Google", "ML Engineer"),
    ("Apple", "Data Analyst"),
    ("Microsoft", "Backend Developer"),
]

def fetch(queries):
    rows = []
    for company, role in queries:
        params = {"company": company, "job_title": role, "location": "United States"}
        print(f"→ {company} · {role}")
        try:
            r = requests.get(API_URL, headers=HEADERS, params=params, timeout=20)
            r.raise_for_status()
            payload = r.json()
            rows.extend(payload.get("data", []))
        except Exception as e:
            print("   ⚠️  skipped:", e)
        time.sleep(1)
    return rows

rows = fetch(primary)
if len(rows) < 5:
    print("…less than 5 rows, trying fallback queries")
    rows += fetch(fallback)

df = pd.DataFrame(rows).drop_duplicates(
    subset=["company","job_title","location","median_salary"], keep="first"
).head(5)

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/api_salary_data.csv", index=False)
print(f"✅ saved {len(df)} rows → data/raw/api_salary_data.csv")
