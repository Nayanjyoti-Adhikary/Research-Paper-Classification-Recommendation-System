import pandas as pd

# Load dataset
df = pd.read_csv("dataset/papers.csv")

print("Original dataset size:", len(df))

# Keep needed columns
df = df[["titles", "summaries", "terms"]]

# Category mapping
category_map = {
    "cs.AI": "AI",
    "cs.LG": "Machine Learning",
    "cs.CV": "Computer Vision",
   
}
cleaned_data = []

# Process rows
for _, row in df.iterrows():

    terms = str(row["terms"])

    assigned_category = None

    for key in category_map:

        if key in terms:
            assigned_category = category_map[key]
            break

    if assigned_category:

        cleaned_data.append({
            "title": row["titles"],
            "abstract": row["summaries"],
            "category": assigned_category
        })

# Create dataframe
clean_df = pd.DataFrame(cleaned_data)

print("\nBefore balancing:")
print(clean_df["category"].value_counts())

# Balance dataset
samples_per_category = 1000

balanced_df = clean_df.groupby("category").apply(
    lambda x: x.sample(
        min(len(x), samples_per_category),
        random_state=42
    )
).reset_index(drop=True)

print("\nAfter balancing:")
print(balanced_df["category"].value_counts())

# Save cleaned dataset
balanced_df.to_csv("dataset/cleaned_papers.csv", index=False)

print("\nBalanced dataset saved successfully!")