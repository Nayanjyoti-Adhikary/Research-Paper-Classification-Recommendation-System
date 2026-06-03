import pandas as pd

df = pd.read_csv("dataset/cleaned_papers.csv")

print(df["category"].value_counts())