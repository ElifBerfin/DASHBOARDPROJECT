import sqlite3
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load the local models
bert_model_path = "./fine_tuned_bert"
roberta_model_path = "./fine_tuned_roberta"

print("Checking if fine-tuned models exist...")
if not os.path.exists(bert_model_path):
    print(f"Error: {bert_model_path} not found. Please download your trained BERT model from Colab first.")
    exit(1)

if not os.path.exists(roberta_model_path):
    print(f"Error: {roberta_model_path} not found.")
    exit(1)

print("Loading models...")
tokenizer_bert = AutoTokenizer.from_pretrained(bert_model_path)
model_bert = AutoModelForSequenceClassification.from_pretrained(bert_model_path)

tokenizer_roberta = AutoTokenizer.from_pretrained(roberta_model_path)
model_roberta = AutoModelForSequenceClassification.from_pretrained(roberta_model_path)

sentiment_map_bert = {0: "Negative", 1: "Neutral", 2: "Positive"}
sentiment_map_roberta = {0: "Negative", 1: "Neutral", 2: "Positive"} # Correct mapping

def predict_bert(text):
    inputs = tokenizer_bert(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model_bert(**inputs)
    cls_id = torch.argmax(outputs.logits, dim=1).item()
    return sentiment_map_bert.get(cls_id, "Positive")

def predict_roberta(text):
    inputs = tokenizer_roberta(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model_roberta(**inputs)
    cls_id = torch.argmax(outputs.logits, dim=1).item()
    return sentiment_map_roberta.get(cls_id, "Positive")

def update_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("Fetching reviews from database...")
    cursor.execute("SELECT id, review_text FROM reviews;")
    rows = cursor.fetchall()
    print(f"Total reviews to update: {len(rows)}")
    
    count = 0
    for rid, text in rows:
        sent_bert = predict_bert(text)
        sent_roberta = predict_roberta(text)
        
        cursor.execute("""
            UPDATE reviews 
            SET sentiment_bert = ?, sentiment_roberta = ? 
            WHERE id = ?;
        """, (sent_bert, sent_roberta, rid))
        
        count += 1
        if count % 100 == 0:
            print(f"Updated {count}/{len(rows)} reviews...")
            conn.commit()
            
    conn.commit()
    conn.close()
    print("Database successfully updated with new model predictions! 🎉")

if __name__ == "__main__":
    update_database()
