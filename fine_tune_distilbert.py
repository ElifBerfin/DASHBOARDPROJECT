import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

from sklearn.metrics import accuracy_score, f1_score


# =========================
# 2. LOAD DATA
# =========================
df = pd.read_csv("amazon_shoes.csv") # Dosya yolu aynı klasördeki ile eşitlendi

# Sayısal olmayan veya boş rating değerlerini temizleyelim (hata önleyici)
df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")

# Rating -> Sentiment Label
# 0 = Negative, 1 = Neutral, 2 = Positive
def map_sentiment(r):
    if r <= 2:
        return 0
    elif r == 3:
        return 1
    else:
        return 2

df["label"] = df["review_rating"].apply(map_sentiment)

# Sadece gerekli kolonlar
df = df[["review_text", "label"]].dropna()

# 1. HIZLANDIRMA: Veri setin 500'den azsa çökmemesi için dinamik hale getirdik
df = df.sample(n=min(500, len(df)), random_state=42)

print("Dataset size:", df.shape)
print("GPU Kullanımı Aktif mi?:", "EVET 🚀" if torch.cuda.is_available() else "HAYIR (CPU kullanılıyor, bu yüzden çok yavaş!) 🐢")


# =========================
# 3. HUGGINGFACE DATASET
# =========================
dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2, seed=42)


# =========================
# 4. TOKENIZER & MODEL
# =========================
# İhtiyacınıza göre burayı "roberta-base", "xlm-roberta-base" veya "albert-base-v2" yapabilirsiniz
model_name = "xlm-roberta-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3
)

# =========================
# 4.1 FREEZE BASE MODEL LAYERS
# =========================
# Sadece sınıflandırma (classifier) katmanını eğitmek için temel modelin ağırlıklarını donduralım:
for param in model.base_model.parameters():
    param.requires_grad = False

# =========================
# 5. TOKENIZATION
# =========================
def tokenize(batch):
    return tokenizer(
        batch["review_text"],
        padding="max_length",
        truncation=True,
        # 2. HIZLANDIRMA: Token uzunluğunu 128'den 64'e düşürelim
        max_length=64
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.remove_columns(["review_text"])
dataset.set_format("torch")


# =========================
# 6. METRICS
# =========================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=1)

    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="weighted")

    return {
        "accuracy": acc,
        "f1": f1
    }


# =========================
# 7. TRAINING ARGUMENTS
# =========================
training_args = TrainingArguments(
    output_dir=f"./results_{model_name.replace('/', '_')}",
    evaluation_strategy="epoch", # Eski sürümlerle de uyumlu olması için düzeltildi
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,  # Süreyi kısaltmak için 2'den 1'e düşürdük
    weight_decay=0.01,
    logging_steps=50,
    fp16=torch.cuda.is_available(),  # HATA BURADAYDI: CPU varsa FP16 kapatılmalı, GPU varsa açılmalı
    use_cpu=not torch.cuda.is_available() # Sadece CPU kullanılıyorsa Trainer'a belirtiyoruz
)


# =========================
# 8. TRAINER
# =========================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer, # processing_class yerine eski sürümlerle de uyumlu tokenizer kullanıldı
    compute_metrics=compute_metrics
)


# =========================
# 9. TRAIN
# =========================
trainer.train()


# =========================
# 10. FINAL EVALUATION
# =========================
results = trainer.evaluate()
print("\nFinal evaluation results:")
print(results)

# =========================
# 11. MODELİ TEST ETME
# =========================
test_text = "This shoe is terrible!"
inputs = tokenizer(test_text, return_tensors="pt", truncation=True, padding=True, max_length=128)

# Tensorleri modelin bulunduğu cihaza (GPU/CPU) taşıyalım
inputs = {k: v.to(model.device) for k, v in inputs.items()}

with torch.no_grad(): # Sadece tahmin yapacağımız için gradient hesaplamasını kapatalım
    outputs = model(**inputs)

predicted_class_id = torch.argmax(outputs.logits, dim=1).item()
sentiment_map = {0: "Negatif", 1: "Nötr", 2: "Pozitif"}

print(f"\nTest Edilen Yorum: '{test_text}'")
print(f"Modelin Tahmini: {sentiment_map[predicted_class_id]}")
