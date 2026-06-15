"""
Instructions for Google Colab:
1. Open Google Colab and create a New Notebook.
2. Go to Runtime > Change runtime type > Select T4 GPU.
3. Upload this file and your 'amazon_shoes.csv' to Colab.
4. Run: !pip install transformers torch pandas scikit-learn
5. Run this script! Once finished, download 'lstm_finetuned_model.pth' and put it in your Dashboard project.
"""

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModel
from sklearn.model_selection import train_test_split

print("1. Loading dataset...")
df = pd.read_csv("amazon_shoes.csv").dropna(subset=['review_text', 'review_rating'])
df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce").dropna()

def map_sentiment(rating):
    if rating <= 2: return 0
    elif rating == 3: return 1
    else: return 2

df['label'] = df['review_rating'].apply(map_sentiment)
df = df.sample(n=min(5000, len(df)), random_state=42) # Using 5000 for a solid Fine-Tune

print("2. Downloading Pre-Trained Tokenizer and BERT Embeddings...")
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
pretrained_bert = AutoModel.from_pretrained(model_name)

# EXTRACT PRE-TRAINED WEIGHTS
pretrained_embeddings = pretrained_bert.embeddings.word_embeddings.weight.data.clone()
embedding_dim = pretrained_embeddings.shape[1] # This will be 768 for BERT
vocab_size = pretrained_embeddings.shape[0]

class ReviewsDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts.iloc[idx])
        label = self.labels.iloc[idx]
        encoding = tokenizer(text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
        return {'input_ids': encoding['input_ids'].flatten(), 'label': torch.tensor(label, dtype=torch.long)}

X_train, X_test, y_train, y_test = train_test_split(df['review_text'], df['label'], test_size=0.2, random_state=42)
train_loader = DataLoader(ReviewsDataset(X_train, y_train), batch_size=32, shuffle=True)

print("3. Building LSTM with Pre-Trained BERT Weights (Transfer Learning)...")
class FineTunedSentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super().__init__()
        # Initialize embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        # INJECT PRE-TRAINED WEIGHTS HERE! This makes it a Fine-Tuning process.
        self.embedding.weight.data.copy_(pretrained_embeddings)
        
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, text):
        embedded = self.embedding(text)
        output, (hidden, cell) = self.lstm(embedded)
        return self.fc(hidden[-1])

model = FineTunedSentimentLSTM(vocab_size=vocab_size, embedding_dim=embedding_dim, hidden_dim=256, output_dim=3)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print(f"4. Starting Fine-Tuning on {device}...")
model.train()
epochs = 3
for epoch in range(epochs):
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch['input_ids'].to(device)), batch['label'].to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss/len(train_loader):.4f}")

print("5. Saving the Fine-Tuned LSTM Model...")
torch.save(model.state_dict(), "lstm_finetuned_model.pth")
print("DONE! Download 'lstm_finetuned_model.pth' from Colab and put it in your Dashboard folder.")
