import os
import pandas as pd
import torch
import torch.nn as nn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from langdetect import detect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. NLPtown (Çok Dilli BERT) Modelinin Yüklenmesi ---
model_name_nlptown = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer_nlptown = AutoTokenizer.from_pretrained(model_name_nlptown)
model_nlptown = AutoModelForSequenceClassification.from_pretrained(model_name_nlptown)

sentiment_map_nlptown = {
    0: "Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Positive"
}

# --- 2. RoBERTa Modelinin Yüklenmesi ---
model_name_roberta = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer_roberta = AutoTokenizer.from_pretrained(model_name_roberta)
model_roberta = AutoModelForSequenceClassification.from_pretrained(model_name_roberta)

sentiment_map_roberta = {
    0: "Negative", 1: "Neutral", 2: "Positive"
}

# --- 3. LSTM Modelinin Yüklenmesi ---
class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, text):
        embedded = self.embedding(text)
        output, (hidden, cell) = self.lstm(embedded)
        return self.fc(hidden[-1])

# İşleri kolaylaştırmak adına kelime sözlüğü olarak nlptown tokenizer'ını kullanıyoruz
VOCAB_SIZE = len(tokenizer_nlptown)
lstm_model = SentimentLSTM(vocab_size=VOCAB_SIZE, embedding_dim=128, hidden_dim=256, output_dim=3)

lstm_model_path = "lstm_model.pth"
lstm_ready = False
if os.path.exists(lstm_model_path):
    lstm_model.load_state_dict(torch.load(lstm_model_path, map_location=torch.device('cpu')))
    lstm_model.eval()
    lstm_ready = True

# API ucuna "model_type" adında yeni bir parametre ekledik
@app.get("/analyze-csv")
def analyze_csv(limit: int = 20, model_type: str = "nlptown", product: str = "adidas", time_filter: int = 30):
    product_lower = product.lower().strip()
    
    # Akıllı Arama: Anahtar kelimelere göre dosya eşleştirme
    file_mapping = {
        "samsung_phone.csv": ["samsung", "galaxy", "s23", "android", "mobile phone"],
        "apple_phone.csv": ["apple", "iphone", "ios", "mac", "pro max"],
        "tarte_concealer.csv": ["tarte", "concealer", "makeup", "shape tape", "cosmetics"],
        "oysho_sports.csv": ["oysho", "legging", "sport", "yoga", "compression", "clothes"],
        "amazon_shoes.csv": ["amazon", "shoe", "sneaker", "adidas", "new balance", "puma", "asics"]
    }
    
    file_path = "samsung_phone.csv" # Default file
    
    for filename, keywords in file_mapping.items():
        if any(kw in product_lower for kw in keywords):
            file_path = filename
            break
    
    if not os.path.exists(file_path):
        return {"error": f"No product found matching '{product}'. Please enter a valid keyword (e.g., galaxy, leggings)."}
        
    df = pd.read_csv(file_path, encoding="utf-8")

    # Eğer amazon_shoes.csv kullanılıyorsa, aranılan spesifik markayı filtrele
    if file_path == "amazon_shoes.csv":
        for brand in ["adidas", "new balance", "puma", "asics"]:
            if brand in product_lower:
                df = df[df['product_name'].str.contains(brand, case=False, na=False)]
                break
                
    df_selected = df.dropna(subset=['review_text', 'review_date']).copy()
    
    # Parse date string to actual datetime
    df_selected['parsed_date'] = pd.to_datetime(df_selected['review_date'].str.split(' on ').str[-1], errors='coerce')
    
    from datetime import datetime, timedelta
    current_date = datetime(2026, 5, 9)
    cutoff_date = current_date - timedelta(days=time_filter)
    
    df_filtered = df_selected[df_selected['parsed_date'] >= cutoff_date]
    
    # If no reviews found in the selected date range, fallback to all available data
    if len(df_filtered) == 0:
        df_filtered = df_selected
        
    df_filtered = df_filtered.sort_values(by='parsed_date', ascending=False)
    
    # Sadece İngilizce olan yorumları filtrele (langdetect kullanarak)
    all_reviews = df_filtered['review_text'].dropna().tolist()
    reviews = []
    for text in all_reviews:
        try:
            if detect(str(text)) == 'en':
                reviews.append(text)
        except:
            continue
        if len(reviews) >= limit:
            break
    
    results = []
    for text in reviews:
        if model_type == "roberta":
            # RoBERTa modelini kullan
            inputs = tokenizer_roberta(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model_roberta(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
            sentiment = sentiment_map_roberta.get(predicted_class, "Unknown")
            
        elif model_type == "lstm":
            if lstm_ready:
                # LSTM modelimiz hazırsa gerçek çıkarım yapıyoruz
                inputs = tokenizer_nlptown(text, return_tensors="pt", truncation=True, max_length=128)
                with torch.no_grad():
                    outputs = lstm_model(inputs['input_ids'])
                predicted_class = torch.argmax(outputs, dim=1).item()
                sentiment = {0: "Negative", 1: "Neutral", 2: "Positive"}.get(predicted_class, "Unknown")
            else:
                import random
                sentiment = random.choice(["Positive", "Negative", "Neutral"]) + " (Mock - No Model)"
            
        else:
            # NLPtown modelini kullan (Varsayılan)
            inputs = tokenizer_nlptown(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model_nlptown(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
            sentiment = sentiment_map_nlptown.get(predicted_class, "Unknown")
            
        results.append({
            "text": text,
            "sentiment": sentiment
        })
        
    return {"results": results}

@app.get("/price-data")
def get_price_data():
    file_path = "price_manipulation_data.csv"
    if not os.path.exists(file_path):
        return {"error": "Price data not found. Please run generate_price_data.py first."}
    df = pd.read_csv(file_path, encoding="utf-8")
    return df.to_dict(orient="records")

@app.get("/analyze-price")
def analyze_price(product: str = "all", model_type: str = "isolation_forest"):
    file_path = "price_manipulation_data.csv"
    if not os.path.exists(file_path):
        return {"error": "Price data not found. Please run generate_price_data.py first."}
        
    df = pd.read_csv(file_path, encoding="utf-8")
    if product != "all":
        df = df[df["product_name"] == product]
        
    if len(df) == 0:
        return {"anomalies": []}

    results = []
    # Group by product to analyze time series for each separately
    for prod, group in df.groupby("product_name"):
        group = group.sort_values("date").copy()
        
        # Feature Engineering for ML Model (Unsupervised)
        group['discount_claim'] = group['claimed_original_price'] - group['actual_price']
        group['rolling_avg'] = group['actual_price'].rolling(window=7, min_periods=1).mean()
        group['price_diff_from_avg'] = group['actual_price'] - group['rolling_avg']
        
        X = group[['discount_claim', 'price_diff_from_avg']].fillna(0)
        
        if model_type == "svm":
            # One-Class Support Vector Machine for Anomaly Detection
            model = OneClassSVM(nu=0.15, kernel="rbf", gamma="scale")
            group['anomaly'] = model.fit_predict(X)
            # SVM decision function gives distance to separating hyperplane
            group['anomaly_score'] = model.decision_function(X) * 10 
        else:
            # Isolation Forest Anomaly Detection Model (Default)
            model = IsolationForest(contamination=0.15, random_state=42)
            group['anomaly'] = model.fit_predict(X)
            group['anomaly_score'] = model.decision_function(X)
        
        # Filter true anomalies detected by AI
        anomalies = group[(group['anomaly'] == -1) & (group['discount_claim'] > 0) & (group['actual_price'] >= group['rolling_avg'] * 0.9)]
        
        for _, row in anomalies.iterrows():
            confidence = min(99.9, abs(row['anomaly_score']) * 200 + 60)
            results.append({
                "date": row["date"],
                "product": prod,
                "seller": row["seller"],
                "claimed_price": round(row["claimed_original_price"], 2),
                "actual_price": round(row["actual_price"], 2),
                "confidence": round(confidence, 1)
            })
            
    results = sorted(results, key=lambda x: x["date"], reverse=True)
    return {"anomalies": results}
