"""
Instructions for Google Colab:
1. Open Google Colab (https://colab.research.google.com) and create a New Notebook.
2. Go to Runtime > Change runtime type > Select T4 GPU (to train with GPU speed).
3. Upload this file ('train_bert_colab.py') and your 'amazon_shoes.csv' to Colab.
4. Create a code cell and run:
   !pip install transformers[torch] datasets pandas scikit-learn accelerate langdetect
5. Run the script:
   !python train_bert_colab.py
6. Once finished, download the 'fine_tuned_bert.zip' file, extract it, and place the 'fine_tuned_bert' folder in your local Dashboard project directory.
"""

import os
import zipfile
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
from langdetect import detect

def clean_and_filter_data(csv_path="amazon_shoes.csv"):
    print("Loading dataset...")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}. Please upload it to Colab.")
    
    df = pd.read_csv(csv_path)
    print(f"Original shape: {df.shape}")
    
    df = df.dropna(subset=["review_text", "review_rating"])
    df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")
    df = df.dropna(subset=["review_rating"])
    
    print("Filtering for Adidas and New Balance...")
    df_filtered = df[df["product_name"].str.contains("adidas|new balance", case=False, na=False)].copy()
    print(f"Filtered shape after brand selection: {df_filtered.shape}")
    
    print("Filtering for English reviews...")
    english_reviews = []
    for _, row in df_filtered.iterrows():
        try:
            if detect(str(row["review_text"])) == 'en':
                english_reviews.append(row)
        except:
            continue
            
    if not english_reviews:
        print("Warning: No English reviews detected. Using raw filtered dataset.")
        df_final = df_filtered
    else:
        df_final = pd.DataFrame(english_reviews)
    
    print(f"Final shape of English reviews: {df_final.shape}")
    
    def map_sentiment(r):
        if r <= 2:
            return 0
        elif r == 3:
            return 1
        else:
            return 2
            
    df_final["label"] = df_final["review_rating"].apply(map_sentiment)
    df_final = df_final[["review_text", "label"]].rename(columns={"review_text": "text"})
    
    return df_final

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=1)
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="weighted")
    return {"accuracy": acc, "f1": f1}

def train_model():
    model_name = "bert-base-uncased"
    output_dir = "./fine_tuned_bert"
    
    print(f"Fine-tuning model: {model_name} (Saving to: {output_dir})")
    
    df = clean_and_filter_data()
    # Sample 1000 reviews for a solid fine-tuning
    sample_size = min(1000, len(df))
    df = df.sample(n=sample_size, random_state=42)
    print(f"Training sample size: {len(df)}")
    
    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3, ignore_mismatched_sizes=True)
    
    has_gpu = torch.cuda.is_available()
    print(f"GPU Available: {'YES (All BERT parameters will be fine-tuned 🚀)' if has_gpu else 'NO'}")
    
    # Do NOT freeze any parameters if GPU is available (Colab will use T4 GPU)
    if not has_gpu:
        print("Freezing lower layers of the base model for CPU training fallback...")
        for param in model.base_model.parameters():
            param.requires_grad = False
        if hasattr(model.base_model, "encoder") and hasattr(model.base_model.encoder, "layer"):
            for layer in model.base_model.encoder.layer[10:]:
                for param in layer.parameters():
                    param.requires_grad = True
            
    def tokenize_fn(batch):
        return tokenizer(
            batch["text"],
            padding="max_length",
            truncation=True,
            max_length=64
        )
        
    tokenized_dataset = dataset.map(tokenize_fn, batched=True)
    tokenized_dataset = tokenized_dataset.remove_columns(["text"])
    
    class TorchDataset(torch.utils.data.Dataset):
        def __init__(self, hf_dataset):
            self.hf_dataset = hf_dataset
        def __len__(self):
            return len(self.hf_dataset)
        def __getitem__(self, idx):
            item = self.hf_dataset[idx]
            return {
                "input_ids": torch.tensor(item["input_ids"]),
                "attention_mask": torch.tensor(item["attention_mask"]),
                "label": torch.tensor(item["label"])
            }
            
    train_dataset = TorchDataset(tokenized_dataset["train"])
    eval_dataset = TorchDataset(tokenized_dataset["test"])
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16 if has_gpu else 8,
        per_device_eval_batch_size=16 if has_gpu else 8,
        num_train_epochs=3 if has_gpu else 2,
        weight_decay=0.01,
        logging_steps=10,
        fp16=has_gpu,
        use_cpu=not has_gpu
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        compute_metrics=compute_metrics
    )
    
    print("Starting training...")
    trainer.train()
    
    print(f"Saving model and tokenizer to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Fine-tuning completed successfully!")
    
    # Zip the fine_tuned_bert folder for easy download from Colab
    print("Zipping the fine_tuned_bert directory...")
    zip_path = "fine_tuned_bert.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(output_dir))
                zipf.write(file_path, arcname)
    print(f"DONE! Download '{zip_path}' from Colab, extract it, and place it in your local Dashboard folder.")

if __name__ == "__main__":
    train_model()
