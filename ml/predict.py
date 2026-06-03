import pickle
import pandas as pd
import json
import sys
import os

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct paths
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")
dataset_path = os.path.join(BASE_DIR, "dataset", "cleaned_papers.csv")

# Load model
model = pickle.load(open(model_path, "rb"))

# Load vectorizer
vectorizer = pickle.load(open(vectorizer_path, "rb"))

# Load dataset
df = pd.read_csv(dataset_path)

# Read JSON input from Node.js
data = json.load(sys.stdin)

text = data["text"]

# Convert text to vector
text_vector = vectorizer.transform([text])

# Predict category
prediction = model.predict(text_vector)[0]

# Get recommendations
recommended = df[df["category"] == prediction]

# Top 5 recommendations
recommendations = recommended["title"].head(5).tolist()

# Final result
result = {
    "prediction": prediction,
    "recommendations": recommendations
}

# Return JSON
print(json.dumps(result))