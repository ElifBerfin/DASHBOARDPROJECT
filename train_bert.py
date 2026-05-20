import pandas as pd
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import sys
# ==========================================
# 1. VERİ HAZIRLIĞI
# ==========================================
print("Veri yükleniyor...")

df = pd.read_csv("amazon_shoes.csv")

df = df.dropna(subset=['review_text', 'review_rating'])
df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")
df = df.dropna(subset=['review_rating'])

# Sentiment mapping
def map_sentiment(rating):
    if rating <= 2:
        return 0
    elif rating == 3:
        return 1
    else:
        return 2

df['label'] = df['review_rating'].apply(map_sentiment)

df = df[['review_text', 'label']].rename(columns={'review_text': 'text'})

# Küçük veri (hız için)
df = df.sample(n=min(500, len(df)), random_state=42)

# Dataset
dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2)

# ==========================================
# 2. MODEL & TOKENIZER
# ==========================================
print("Model ve Tokenizer indiriliyor...")

model_name = sys.argv[1] if len(sys.argv) > 1 else "distilbert-base-uncased"
output_dir = f"./model_{model_name.replace('-', '_')}"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# ==========================================
# 3. TOKENIZE
# ==========================================
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

print("Veriler tokenize ediliyor...")
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# ==========================================
# 4. TRAINING
# ==========================================
has_gpu = torch.cuda.is_available()
print(f"GPU Kullanımı: {'EVET 🚀' if has_gpu else 'HAYIR 🐢'}")
training_args = TrainingArguments(
    output_dir=output_dir,
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=2,
    weight_decay=0.01,
    fp16=has_gpu,
    use_cpu=not has_gpu
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"]
)

# ==========================================
# 5. TRAIN
# ==========================================
print("Eğitim başlıyor...")
trainer.train()

# ==========================================
# 6. SAVE MODEL
# ==========================================
# ==========================================
# 6. SAVE MODEL
# ==========================================
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Model kaydedildi: {output_dir}")

print("Model kaydedildi: bert_ayakkabi_modeli")