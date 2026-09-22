from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib

from feature_extractor import extract_features


app = Flask(__name__)

# Allow frontend requests
CORS(app)


# Load trained model
model_path = "../model/phishguard_model.pkl"
model = joblib.load(model_path)

print("PhishGuard model loaded successfully!")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "PhishGuard API is running",
        "status": "success"
    })


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    url = data.get("url")

    if not url:
        return jsonify({
            "error": "URL is required"
        }), 400

    # -----------------------------------
    # Step 1: Extract 30 features
    # -----------------------------------

    features = extract_features(url)

    # -----------------------------------
    # Step 2: Convert features into
    #         model input
    # -----------------------------------

    features_array = np.array(features).reshape(1, -1)

    # -----------------------------------
    # Step 3: Generate prediction
    # -----------------------------------

    prediction = model.predict(features_array)[0]

    # -----------------------------------
    # Step 4: Get model probabilities
    # -----------------------------------

    probabilities = model.predict_proba(features_array)[0]

    classes = model.classes_

    safe_probability = 0.0
    phishing_probability = 0.0

    for class_value, probability in zip(classes, probabilities):

        if class_value == -1:
            safe_probability = float(probability)

        elif class_value == 1:
            phishing_probability = float(probability)

    # -----------------------------------
    # Step 5: Convert prediction
    #         into readable result
    # -----------------------------------

    if prediction == 1:
        result = "Phishing"
    else:
        result = "Safe"

    # -----------------------------------
    # Step 6: Send JSON response
    # -----------------------------------

    return jsonify({
        "url": url,
        "prediction": result,
        "result": int(prediction),
        "probabilities": {
            "safe": round(safe_probability * 100, 2),
            "phishing": round(phishing_probability * 100, 2)
        }
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )