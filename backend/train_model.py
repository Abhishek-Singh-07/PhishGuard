from scipy.io import arff
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# 1. Load the ARFF dataset
# ============================================================

data, meta = arff.loadarff("../dataset/Training Dataset.arff")

# Get the feature names
columns = meta.names()

print("Total columns:", len(columns))
print("Total records:", len(data))


# ============================================================
# 2. Convert ARFF byte values into numbers
# ============================================================

rows = []

for row in data:
    values = []

    for value in row:
        values.append(float(value.decode("utf-8")))

    rows.append(values)


# Convert the data into a NumPy array
data_array = np.array(rows)


# ============================================================
# 3. Separate features and target
# ============================================================

# First 30 columns = input features
# Last column = target (Result)

X = data_array[:, :-1]
y = data_array[:, -1]


# ============================================================
# 4. Split dataset into training and testing data
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining features:", X_train.shape)
print("Testing features:", X_test.shape)

print("Training targets:", y_train.shape)
print("Testing targets:", y_test.shape)


# ============================================================
# 5. Create Random Forest model
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# ============================================================
# 6. Train the model
# ============================================================

model.fit(X_train, y_train)

print("\nRandom Forest model trained successfully!")


# ============================================================
# 7. Make predictions on test data
# ============================================================

y_pred = model.predict(X_test)

print("\nPredictions generated successfully!")

print("First 10 actual values:")
print(y_test[:10])

print("\nFirst 10 predicted values:")
print(y_pred[:10])


# ============================================================
# 8. Calculate Accuracy
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("Model Accuracy Percentage:", accuracy * 100, "%")


# ============================================================
# 9. Calculate Precision
# ============================================================

precision = precision_score(
    y_test,
    y_pred,
    pos_label=1
)

print("\nPrecision:", precision)
print("Precision Percentage:", precision * 100, "%")


# ============================================================
# 10. Calculate Recall
# ============================================================

recall = recall_score(
    y_test,
    y_pred,
    pos_label=1
)

print("\nRecall:", recall)
print("Recall Percentage:", recall * 100, "%")


# ============================================================
# 11. Calculate F1 Score
# ============================================================

f1 = f1_score(
    y_test,
    y_pred,
    pos_label=1
)

print("\nF1 Score:", f1)
print("F1 Score Percentage:", f1 * 100, "%")


# ============================================================
# 12. Calculate Confusion Matrix
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# 13. Save the trained model
# ============================================================

model_path = "../model/phishguard_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Model path:", model_path)


# ============================================================
# 14. Display dataset information
# ============================================================

print("\nFeature matrix shape:", X.shape)
print("Target shape:", y.shape)

print("\nNumber of features:", X.shape[1])

print("\nFirst feature row:")
print(X[0])

print("\nFirst target value:")
print(y[0])