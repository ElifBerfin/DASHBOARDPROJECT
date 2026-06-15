import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split

# 1. VERİ HAZIRLIĞI
print("Veri yükleniyor...")
df = pd.read_csv("amazon_shoes.csv")
df = df.dropna(subset=['review_text', 'review_rating'])
df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce").dropna()

def map_sentiment(rating):
    if rating <= 2: return 0
    elif rating == 3: return 1
    else: return 2

df['label'] = df['review_rating'].apply(map_sentiment)

# Daha hızlı deneme için 1000 veri kullanabilirsiniz, arttırmak modeli iyileştirecektir
df = df.sample(n=min(1000, len(df)), random_state=42) 

# 2. TOKENIZER
# app.py ile aynı input yapısını kullanmak için hazır tokenizer kullanıyoruz
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

class ReviewsDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts.iloc[idx])
        label = self.labels.iloc[idx]
        
        encoding = tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

X_train, X_test, y_train, y_test = train_test_split(df['review_text'], df['label'], test_size=0.2, random_state=42)
train_dataset = ReviewsDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# 3. LSTM MODELİ (app.py ile birebir aynı olmalı)
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

VOCAB_SIZE = len(tokenizer)
model = SentimentLSTM(vocab_size=VOCAB_SIZE, embedding_dim=128, hidden_dim=256, output_dim=3)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. SADECE 1 EPOCH'LUK HIZLI EĞİTİM (Ağırlıkları Kaydetmek İçin)
print(f"Eğitim başlıyor... Cihaz: {device}")
model.train()
for batch in train_loader:
    optimizer.zero_grad()
    loss = criterion(model(batch['input_ids'].to(device)), batch['label'].to(device))
    loss.backward()
    optimizer.step()

# 5. MODELİ KAYDET
torch.save(model.state_dict(), "lstm_model.pth")
print("Model basariyla egitildi ve 'lstm_model.pth' olarak kaydedildi!")