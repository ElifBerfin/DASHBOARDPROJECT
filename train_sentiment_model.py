import os
import sys
import argparse
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
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Original shape: {df.shape}")
    
    # Drop rows without text or rating
    df = df.dropna(subset=["review_text", "review_rating"])
    df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")
    df = df.dropna(subset=["review_rating"])
    
    # Filter for Adidas and New Balance
    print("Filtering for Adidas and New Balance...")
    df_filtered = df[df["product_name"].str.contains("adidas|new balance", case=False, na=False)].copy()
    print(f"Filtered shape after brand selection: {df_filtered.shape}")
    
    # Filter for English reviews
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
    
    # Map ratings: 1-2 -> 0 (Negative), 3 -> 1 (Neutral), 4-5 -> 2 (Positive)
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

def train_model(model_type, output_dir, sample_size=1000):
    # Set model name
    if model_type == "bert":
        model_name = "bert-base-uncased"
    elif model_type == "roberta":
        model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    else:
        raise ValueError(f"Unknown model_type: {model_type}")
        
    print(f"Fine-tuning model: {model_name} (Saving to: {output_dir})")
    
    # Load and sample data
    df = clean_and_filter_data()
    df = df.sample(n=min(sample_size, len(df)), random_state=42)
    print(f"Training sample size: {len(df)}")
    
    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    
    # Load Tokenizer & Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3, ignore_mismatched_sizes=True)
    
    has_gpu = torch.cuda.is_available()
    print(f"GPU Available: {'YES' if has_gpu else 'NO (Using CPU - training will take longer)'}")
    
    # If no GPU, freeze the base model parameters to make training extremely fast on CPU
    if not has_gpu:
        print("Freezing lower layers of the base model for CPU training (leaving top 2 layers unfrozen)...")
        for param in model.base_model.parameters():
            param.requires_grad = False
        if hasattr(model.base_model, "encoder") and hasattr(model.base_model.encoder, "layer"):
            for layer in model.base_model.encoder.layer[10:]:
                for param in layer.parameters():
                    param.requires_grad = True
            
    # Tokenize dataset
    def tokenize_fn(batch):
        return tokenizer(
            batch["text"],
            padding="max_length",
            truncation=True,
            max_length=64 # Keep length small for speed
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
    
    # Set Training Arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=2,
        weight_decay=0.01,
        logging_steps=10,
        fp16=has_gpu,
        use_cpu=not has_gpu
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        compute_metrics=compute_metrics
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save Model & Tokenizer
    print(f"Saving model and tokenizer to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Fine-tuning completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune BERT or RoBERTa for Sentiment Analysis.")
    parser.add_argument("--model_type", type=str, required=True, choices=["bert", "roberta"], help="Type of model to train (bert or roberta)")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the fine-tuned model")
    parser.add_argument("--sample_size", type=int, default=1000, help="Number of reviews to sample for training")
    
    args = parser.parse_args()
    train_model(args.model_type, args.output_dir, args.sample_size)
