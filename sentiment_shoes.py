import pandas as pd

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("amazon_shoes.csv")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)
print("\nFirst rows:")
print(df.head())

# =========================
# CLEAN RATING
# =========================
df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")

# =========================
# SENTIMENT MAPPING
# =========================
def map_sentiment(r):
    if r <= 2:
        return "Negative"
    elif r == 3:
        return "Neutral"
    else:
        return "Positive"

df["sentiment"] = df["review_rating"].apply(map_sentiment)

# =========================
# TOP PRODUCTS (MODELS)
# =========================
top_products = (
    df.groupby("product_name")
      .size()
      .reset_index(name="review_count")
      .sort_values("review_count", ascending=False)
)

print("\n🏆 TOP PRODUCTS:")
print(top_products.head(10))

# =========================
# BRAND-SPECIFIC TOP MODELS
# =========================
def top_models_by_brand(keyword, label):
    models = (
        df[df["product_name"].str.contains(keyword, case=False, na=False)]
        .groupby("product_name")
        .size()
        .reset_index(name="review_count")
        .sort_values("review_count", ascending=False)
        .head(5)
    )
    print(f"\n🔹 {label} TOP MODELS:")
    print(models)

top_models_by_brand("adidas", "Adidas")
top_models_by_brand("new balance", "New Balance")
top_models_by_brand("nike", "Nike")
top_models_by_brand("puma", "Puma")

# ⚠️ On için daha güvenli filtre
top_models_by_brand(" on ", "On Running")

# =========================
# MODEL x SENTIMENT
# =========================
model_sentiment = (
    df.groupby(["product_name", "sentiment"])
      .size()
      .reset_index(name="count")
)

print("\n📊 MODEL SENTIMENT SAMPLE:")
print(model_sentiment.head())

# =========================
# MOST POSITIVE MODELS
# =========================
positive_models = (
    df[df["sentiment"] == "Positive"]
    .groupby("product_name")
    .size()
    .sort_values(ascending=False)
)

print("\n🙂 MOST POSITIVE MODELS:")
print(positive_models.head())
