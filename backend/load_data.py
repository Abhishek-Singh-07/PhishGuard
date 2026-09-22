print("load_data.py started")

from scipy.io import arff

# Load the ARFF dataset
data, meta = arff.loadarff("../dataset/Training Dataset.arff")

print("Dataset loaded successfully!")

print("Number of rows:", len(data))
print("Number of columns:", len(meta.names()))

print("\nColumn names:")
print(meta.names())

print("\nFirst row:")
print(data[0])

print("\nDataset inspection completed.")