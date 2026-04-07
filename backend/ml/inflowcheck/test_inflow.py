import joblib
import pandas as pd

# Load model
model = joblib.load("inflow_model.pkl")

print("✅ Model Loaded Successfully\n")

# ---------- SINGLE DATE TEST ----------
date = input("Enter date (YYYY-MM-DD): ")

date_obj = pd.to_datetime(date)
day = date_obj.toordinal()

prediction = model.predict(pd.DataFrame([[day]], columns=['Day']))

print(f"\n📅 Date: {date}")
print(f"👥 Predicted Patients: {int(prediction[0])}")

# ---------- MULTIPLE DAYS TEST ----------
print("\n🔮 Predict next N days")
n = int(input("Enter number of days: "))

print("\nPredictions:\n")

for i in range(n):
    future_date = date_obj + pd.Timedelta(days=i)
    day = future_date.toordinal()

    pred = model.predict(pd.DataFrame([[day]], columns=['Day']))

    print(f"{future_date.date()} → {int(pred[0])} patients")