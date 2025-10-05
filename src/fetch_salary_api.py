import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

url = "https://job-salary-data.p.rapidapi.com/company-job-salary"

querystring = {
    "company": "Amazon",
    "job_title": "software developer",
    "location_type": "ANY",
    "years_of_experience": "ALL"
}

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()
print("Raw JSON:\n", data)

# Convert to DataFrame if possible
if isinstance(data, dict):
    df = pd.json_normalize(data)
else:
    df = pd.DataFrame(data)

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/api_salary_data.csv", index=False)
print("Saved to data/raw/api_salary_data.csv")
