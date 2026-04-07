import joblib
import numpy as np

# Load model files
model = joblib.load("disease_model.pkl")
encoder = joblib.load("label_encoder.pkl")
columns = joblib.load("symptom_columns.pkl")

print("✅ Disease Model Loaded Successfully\n")

# Show some symptoms
print("Available symptoms (sample):")
print(columns[:20])  # show first 20

# Take input
user_input = input("\nEnter symptoms (comma separated): ")

# Convert to list
symptoms = [s.strip() for s in user_input.split(",")]

# Create input vector
input_data = np.zeros(len(columns))

# Set symptoms = 1
for s in symptoms:
    if s in columns:
        input_data[columns.index(s)] = 1
    else:
        print(f"⚠️ Warning: '{s}' not found in dataset")

# Predict
prediction = model.predict([input_data])
disease = encoder.inverse_transform(prediction)[0]

print("\n🦠 Predicted Disease:", disease)