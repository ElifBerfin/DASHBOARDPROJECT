
import os
import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)

# 1. Load the tabular data
print("Loading data...")
df = pd.read_csv("price_manipulation_data.csv")

# 2. Transform Tabular Data to Text (Tabular-as-Text Approach)
# We calculate a simple 7-day rolling average to give the model context
df['rolling_avg'] = df.groupby(['product_name', 'seller'])['actual_price'].transform(lambda x: x.rolling(7, min_periods=1).mean())

def create_text_sequence(row):
    # This sentence format is what BERT will learn to classify!
    return f"Product: {row['product_name']}. Seller: {row['seller']}. Historical average price: ${row['rolling_avg']:.2f}. Today's actual selling price: ${row['actual_price']:.2f}. Claimed original discount price: ${row['claimed_original_price']:.2f}."

print("Converting numerical tables to text sentences for BERT...")
df['text'] = df.apply(create_text_sequence, axis=1)

# Map labels: False -> 0 (Normal), True -> 1 (Manipulation/Fake Discount)
df['label'] = df['is_manipulation'].astype(int)

# Keep only the columns we need for BERT
bert_df = df[['text', 'label']]

# Split into Train and Eval sets
train_df, eval_df = train_test_split(bert_df, test_size=0.15, random_state=42)

# Convert Pandas DataFrames to Hugging Face Datasets
train_dataset = Dataset.from_pandas(train_df, preserve_index=False)
eval_dataset = Dataset.from_pandas(eval_df, preserve_index=False)

# 3. Load Pre-Trained BERT Model & Tokenizer
model_name = "bert-base-uncased"
print(f"Downloading pre-trained {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
# We have 2 classes: 0 (Normal), 1 (Manipulation)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 4. Tokenization function
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

print("Tokenizing datasets...")
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_eval = eval_dataset.map(tokenize_function, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# 5. Define Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,           # 5 epochs for deep learning on tabular text
    weight_decay=0.01,
    eval_strategy="epoch",        # Changed from evaluation_strategy for newer transformers versions
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# 6. Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,
    processing_class=tokenizer,   # Changed from tokenizer=tokenizer for newest transformers
    data_collator=data_collator,
)

# 7. Start Fine-Tuning
print("Starting Fine-Tuning Process on GPU...")
trainer.train()

# 8. Save the explicitly fine-tuned model
save_path = "./fine_tuned_price_bert"
print(f"Training complete! Saving fine-tuned model to {save_path}...")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print("DONE! You can now download the 'fine_tuned_price_bert' folder and put it in your Dashboard project.")
