import numpy as np
import joblib

from feature_extractor import extract_features


# ============================================================
# 1. Load the trained Random Forest model
# ============================================================

model_path = "../model/phishguard_model.pkl"

model = joblib.load(model_path)

print("Trained model loaded successfully!")


# ============================================================
# 2. Test URL
# ============================================================

url = "https://example.com/login"

print("\nTesting URL:")
print(url)


# ============================================================
# 3. Extract features from the URL
# ============================================================

features = extract_features(url)

print("\nExtracted features:")
print(features)

print("\nNumber of features:", len(features))


# ============================================================
# 4. Convert features into NumPy array
# ============================================================

features_array = np.array(features).reshape(1, -1)

print("\nFeature array shape:")
print(features_array.shape)


# ============================================================
# 5. Make prediction
# ============================================================

prediction = model.predict(features_array)[0]

print("\nRaw model prediction:")
print(prediction)


# ============================================================
# 6. Convert prediction into readable result
# ============================================================

if prediction == 1:
    result = "Phishing"
else:
    result = "Safe"


print("\nFinal Prediction:", result)