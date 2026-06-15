import sqlite3
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM prices WHERE product_id=1 AND seller='Amazon' ORDER BY date ASC;", conn)
conn.close()

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained('./fine_tuned_price_bert')
model = AutoModelForSequenceClassification.from_pretrained('./fine_tuned_price_bert')

df['rolling_avg'] = df['actual_price'].rolling(7, min_periods=1).mean()
df['rolling_avg'] = df['rolling_avg'].fillna(df['actual_price'])

texts = []
for idx, row in df.iterrows():
    text = f"Product: Adidas Running Shoes. Seller: Amazon. Historical average price: ${row['rolling_avg']:.2f}. Today's actual selling price: ${row['actual_price']:.2f}. Claimed original discount price: ${row['claimed_original_price']:.2f}."
    texts.append(text)

inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=128)
with torch.no_grad():
    outputs = model(**inputs)

probs = torch.softmax(outputs.logits, dim=1)
preds = torch.argmax(outputs.logits, dim=1)

count = 0
for i in range(len(df)):
    if preds[i].item() == 1:
        print(f"Row {i}: Manipulation FOUND! {texts[i]} Conf: {probs[i][1].item():.4f}")
        count += 1
print(f'Total Manipulations: {count}')
