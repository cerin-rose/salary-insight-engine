import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

DATA_PATH = "data/processed/clean_salary_data.csv"
MODEL_PATH = "models/salary_predictor.pkl"

# 1️⃣ Load dataset
df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")

# 2️⃣ Basic feature setup
features = [c for c in ["job_title", "company", "location", "experience"] if c in df.columns]
target = "median_salary"

X = df[features]
y = df[target]

# 3️⃣ Build preprocessing
cat_cols = [c for c in ["job_title", "company", "location"] if c in X.columns]
num_cols = [c for c in ["experience"] if c in X.columns]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", StandardScaler(), num_cols),
    ],
    remainder="drop"
)

# 4️⃣ Build & train model (no split)
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

model.fit(X, y)
print("✅ Model trained successfully on all data (no split).")

# 5️⃣ Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"✅ Model saved → {MODEL_PATH}")
