import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# load model + data
model = joblib.load("models/salary_predictor.pkl")
df = pd.read_csv("data/enhanced/salary_clean_enhanced.csv")

# sample for speed
df_sample = df.sample(min(200, len(df)), random_state=42)

# isolate features (same used during training)
features = ["job_title", "company", "location"]
if "experience" in df_sample.columns:
    features.append("experience")

X = df_sample[features]

# build SHAP explainer
explainer = shap.Explainer(model.named_steps["regressor"], 
                           model.named_steps["preprocess"].transform(X))
shap_values = explainer(model.named_steps["preprocess"].transform(X))

# summary plot
plt.title("Feature Importance (SHAP values)")
shap.summary_plot(shap_values, show=False)
plt.savefig("models/feature_importance_shap.png", bbox_inches="tight")
print("✅ Saved models/feature_importance_shap.png")
