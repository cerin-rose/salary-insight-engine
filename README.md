# Salary Insight Engine

An intelligent salary prediction dashboard
that uses real-time salary data from APIs and machine learning to estimate
salaries by job title, company, location, and experience.

## Overview

Salary Insight Engine is a mini end-to-end
ML project built with public API data collection, automated data cleaning,
exploratory data analysis, and a linear regression model served through an
interactive Streamlit dashboard.

## Architecture

 salary-insight-engine

├── data/

│   ├── raw/               → Fetched API data

│   ├── processed/         → Cleaned CSVs

│   └── enhanced/          → EDA-ready data

├── models/

│   └── salary_predictor.pkl  → Trained ML model

├── dashboard/

│   └── app.py             → Streamlit app UI

├── src/

│   ├── fetch_salary_api.py       → Fetch data from API

│   ├── clean_salary_data.py      → Clean & process raw data

│   ├── enhance_cleaning_and_eda.py →
Handle missing data + EDA

│   ├── train_baseline.py         → Train regression model

│   └── explain_model.py          → Interpret model predictions

├── requirements.txt

└── README.md

## ⚙️ Installation & Setup

1️⃣ Clone this repository

git clone https://github.com/cerin-rose/salary-insight-engine.git

2️⃣ Create & activate a virtual
environment

python -m venv .venv

.\.venv\Scripts\activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Add your RapidAPI key

Edit src/fetch_salary_api.py and add your key under 'x-rapidapi-key'

## 🧩 Run the Pipeline

1️⃣ Fetch & Clean Data:

python src/fetch_salary_api.py

python src/clean_salary_data.py

python src/enhance_cleaning_and_eda.py

2️⃣ Train the Model:

python src/train_baseline.py

3️⃣ Launch the Dashboard:

streamlit run dashboard/app.py

## 📊 Example Output

| Job Title | Company | Location |
Predicted Salary |

|------------|----------|-----------|------------------|

| Software Developer | Amazon | United States | 💰 $225,724.70 |

## Machine Learning Stages

| Stage               | Task                       | Tools                 |
| ------------------- | -------------------------- | --------------------- |
| Data Collection     | Public API / Scraping      | requests, pandas      |
| Data Cleaning       | Handle missing, duplicates | pandas, numpy         |
| EDA                 | Visualize patterns         | matplotlib, seaborn   |
| Feature Engineering | Encode + scale             | sklearn.preprocessing |
| Model Training      | Linear Regression          | scikit-learn          |
| Deployment          | Interactive app            | Streamlit             |

## Future Enhancements

- Add SHAP explainability
- Integrate Snowflake / BigQuery
- Enable live API fetching
- Add CI/CD pipeline
- Build salary trend visualizations



