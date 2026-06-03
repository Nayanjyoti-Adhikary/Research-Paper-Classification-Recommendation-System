import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_papers.csv")

print("Dataset loaded successfully!")

# Remove missing values
df = df.dropna()

# Combine title and abstract
df["text"] = df["title"] + " " + df["abstract"]

# Features and labels
X = df["text"]
y = df["category"]

print("Preparing TF-IDF vectors...")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_vectors = vectorizer.fit_transform(X)

print("Splitting dataset...")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectors,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Decision Tree model...")

# Decision Tree model
model = DecisionTreeClassifier(
    max_depth=20,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# Save model
pickle.dump(model, open("model.pkl", "wb"))

# Save vectorizer
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\nModel and vectorizer saved successfully!")