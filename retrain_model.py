import os
import torch
import random
import warnings
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

warnings.filterwarnings("ignore")

def generate_synthetic_data():
    texts = []
    labels = []
    
    products = ["Adidas Running Shoes", "iPhone 14", "Samsung Galaxy", "Coffee Maker", "Desk Lamp"]
    sellers = ["Amazon", "Trendyol", "Hepsiburada", "MediaMarkt", "Apple"]
    
    # 1. Generate Fake Discounts (Label 1)
    # Claimed price is high, but actual price is same as historical
    for _ in range(80):
        p = random.choice(products)
        s = random.choice(sellers)
        base = round(random.uniform(50, 1000), 2)
        claimed = round(base * random.uniform(1.3, 2.0), 2)
        text = f"Product: {p}. Seller: {s}. Historical average price: ${base:.2f}. Today's actual selling price: ${base:.2f}. Claimed original discount price: ${claimed:.2f}."
        texts.append(text)
        labels.append(1)
        
    # 2. Generate Real Discounts (Label 0)
    # Actual price is much lower than historical
    for _ in range(80):
        p = random.choice(products)
        s = random.choice(sellers)
        base = round(random.uniform(50, 1000), 2)
        actual = round(base * random.uniform(0.5, 0.8), 2)
        text = f"Product: {p}. Seller: {s}. Historical average price: ${base:.2f}. Today's actual selling price: ${actual:.2f}. Claimed original discount price: ${base:.2f}."
        texts.append(text)
        labels.append(0)
        
    # 3. Generate Stable Prices (Label 0)
    # Claimed = Actual = Historical
    for _ in range(40):
        p = random.choice(products)
        s = random.choice(sellers)
        base = round(random.uniform(50, 1000), 2)
        text = f"Product: {p}. Seller: {s}. Historical average price: ${base:.2f}. Today's actual selling price: ${base:.2f}. Claimed original discount price: ${base:.2f}."
        texts.append(text)
        labels.append(0)
        
    # Shuffle
    combined = list(zip(texts, labels))
    random.shuffle(combined)
    texts, labels = zip(*combined)
    return list(texts), list(labels)

def main():
    model_path = "./fine_tuned_price_bert"
    print("Loading existing model...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
    
    texts, labels = generate_synthetic_data()
    
    # Tokenize
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)
    
    # Format as HuggingFace Dataset
    class CustomDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)
            
    dataset = CustomDataset(encodings, labels)
    
    # Training Arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        logging_steps=10,
        save_strategy="no",
        use_cpu=True # Force CPU since CUDA is not available
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    
    print("Starting rapid fine-tuning on synthetic data...")
    trainer.train()
    
    print("Saving highly trained model back to directory...")
    model.save_pretrained(model_path + "_v2")
    tokenizer.save_pretrained(model_path + "_v2")
    print("Done! The AI is now a math genius.")

if __name__ == "__main__":
    main()
