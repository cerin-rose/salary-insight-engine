import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

csv_path = "data/enhanced/salary_clean_enhanced.csv"
df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),   # e.g. bocalgx-il32543 or il32543.us-east-1
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    # authenticator="externalbrowser",  # uncomment if using SSO
)

cur = conn.cursor()
cur.execute("""
CREATE OR REPLACE TABLE SALARY_DATA (
  JOB_TITLE STRING,
  COMPANY STRING,
  LOCATION STRING,
  MIN_SALARY FLOAT,
  MAX_SALARY FLOAT,
  MEDIAN_SALARY FLOAT,
  MIN_BASE_SALARY FLOAT,
  MAX_BASE_SALARY FLOAT,
  MEDIAN_BASE_SALARY FLOAT,
  SALARY_PERIOD STRING,
  SALARY_CURRENCY STRING,
  SALARY_COUNT FLOAT,
  CONFIDENCE STRING
)
""")

success, nchunks, nrows, _ = write_pandas(conn, df, "SALARY_DATA")
print(f"✅ Uploaded {nrows} rows to SALARY_DATA")

cur.close()
conn.close()
